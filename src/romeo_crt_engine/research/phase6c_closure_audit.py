from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from pathlib import Path
from typing import Any

from romeo_crt_engine.research.corpus_index_v1 import CorpusEntryV1, CorpusIndexV1
from romeo_crt_engine.research.predicate_ledger_v2 import EvidenceCoverage, PredicateField
from romeo_crt_engine.research.source_acquisition_v1 import (
    AcquisitionStatus,
    CaptureKind,
    SourceAcquisitionManifestV1,
    SourceArtifactV1,
    SourceIdentityV1,
    SourceKind,
)


class ClosureAuditError(ValueError):
    """Raised when a closure audit cannot establish an unbroken evidence chain."""


@dataclass(frozen=True, slots=True)
class ClosureAuditPaths:
    registry: Path
    acquisitions: Path
    corpus_index: Path
    ledger: Path
    payloads: Path


def canonical_json_digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return sha256(encoded.encode("utf-8")).hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ClosureAuditError(f"cannot load JSON: {path}") from error
    if not isinstance(value, dict):
        raise ClosureAuditError(f"JSON root must be an object: {path}")
    return value


def _load_registry(path: Path) -> dict[str, str]:
    try:
        with path.open(encoding="utf-8", newline="") as handle:
            rows = tuple(csv.DictReader(handle))
    except OSError as error:
        raise ClosureAuditError(f"cannot load source registry: {path}") from error
    registry: dict[str, str] = {}
    for row in rows:
        source_id = row.get("source_id", "")
        url = row.get("url", "")
        if not source_id or not url or source_id in registry:
            raise ClosureAuditError("source registry has missing or duplicate source identity")
        registry[source_id] = url
    return registry


def _load_manifest(path: Path) -> tuple[SourceAcquisitionManifestV1, str]:
    raw = _load_json(path)
    expected_digest = raw.pop("manifest_sha256", None)
    if not isinstance(expected_digest, str):
        raise ClosureAuditError(f"manifest digest missing: {path.name}")
    try:
        source_raw = raw["source"]
        source = SourceIdentityV1(
            source_id=source_raw["source_id"],
            url=source_raw["url"],
            source_kind=SourceKind(source_raw["source_kind"]),
            provenance_statement=source_raw["provenance_statement"],
            first_party=source_raw["first_party"],
        )
        artifacts = tuple(
            SourceArtifactV1(
                source_id=item["source_id"],
                capture_kind=CaptureKind(item["capture_kind"]),
                retrieved_at=datetime.fromisoformat(item["retrieved_at_utc"]),
                payload_sha256=item["payload_sha256"],
                byte_length=item["byte_length"],
                content_type=item["content_type"],
                locator=item["locator"],
                first_party_verified=item["first_party_verified"],
            )
            for item in raw["artifacts"]
        )
        manifest = SourceAcquisitionManifestV1(
            source=source,
            status=AcquisitionStatus(raw["status"]),
            artifacts=artifacts,
            notes=raw["notes"],
            schema_version=raw["schema_version"],
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ClosureAuditError(f"invalid acquisition manifest: {path.name}") from error
    if manifest.digest() != expected_digest:
        raise ClosureAuditError(f"manifest digest mismatch: {path.name}")
    return manifest, expected_digest


def _load_corpus(path: Path) -> tuple[CorpusIndexV1, str]:
    raw = _load_json(path)
    expected_digest = raw.get("corpus_index_sha256")
    try:
        corpus = CorpusIndexV1(
            tuple(
                CorpusEntryV1(
                    source_id=item["source_id"],
                    manifest_sha256=item["manifest_sha256"],
                    artifact_sha256s=tuple(item["artifact_sha256s"]),
                )
                for item in raw["entries"]
            )
        )
    except (KeyError, TypeError, ValueError) as error:
        raise ClosureAuditError("invalid corpus index") from error
    if not isinstance(expected_digest, str) or corpus.digest() != expected_digest:
        raise ClosureAuditError("corpus index digest mismatch")
    return corpus, expected_digest


def _validate_ledger_shape(raw: dict[str, Any]) -> None:
    if raw.get("schema_version") != "P6D_PREDICATE_LEDGER_V2":
        raise ClosureAuditError("unsupported predicate-ledger schema")
    rows = raw.get("rows")
    if not isinstance(rows, list):
        raise ClosureAuditError("predicate ledger rows must be a list")
    predicate_ids = [item.get("predicate_id") for item in rows if isinstance(item, dict)]
    if len(predicate_ids) != len(rows) or len(set(predicate_ids)) != len(predicate_ids):
        raise ClosureAuditError("predicate ledger IDs must be unique and non-empty")


def build_closure_report(paths: ClosureAuditPaths) -> dict[str, Any]:
    """Build a fail-closed, evidence-chain-validated Phase 6C closure report."""
    registry = _load_registry(paths.registry)
    loaded = tuple(_load_manifest(path) for path in sorted(paths.acquisitions.glob("*.json")))
    manifests = {manifest.source.source_id: (manifest, digest) for manifest, digest in loaded}
    if len(manifests) != len(loaded):
        raise ClosureAuditError("acquisition source IDs must be unique")

    artifacts: dict[str, SourceArtifactV1] = {}
    for manifest, _ in loaded:
        if not manifest.source.first_party:
            raise ClosureAuditError("non-first-party acquisition is outside the closure corpus")
        if registry.get(manifest.source.source_id) != manifest.source.url:
            raise ClosureAuditError(f"acquisition URL differs from registry: {manifest.source.source_id}")
        for artifact in manifest.artifacts:
            if artifact.payload_sha256 in artifacts:
                raise ClosureAuditError(f"artifact SHA appears more than once: {artifact.payload_sha256}")
            artifacts[artifact.payload_sha256] = artifact

    corpus, corpus_digest = _load_corpus(paths.corpus_index)
    indexed_artifacts: set[str] = set()
    source_inventory: list[dict[str, Any]] = []
    for entry in sorted(corpus.entries, key=lambda item: item.source_id):
        manifest_pair = manifests.get(entry.source_id)
        if manifest_pair is None or manifest_pair[1] != entry.manifest_sha256:
            raise ClosureAuditError(f"corpus manifest mismatch: {entry.source_id}")
        manifest = manifest_pair[0]
        artifact_records: list[dict[str, Any]] = []
        for artifact_sha in entry.artifact_sha256s:
            corpus_artifact = artifacts.get(artifact_sha)
            if corpus_artifact is None or corpus_artifact.source_id != entry.source_id:
                raise ClosureAuditError(f"corpus artifact is not provenance-bound: {artifact_sha}")
            payload_path = paths.payloads / f"{artifact_sha}.txt"
            if not payload_path.is_file():
                raise ClosureAuditError(f"corpus payload is missing: {artifact_sha}")
            payload = payload_path.read_bytes()
            if sha256(payload).hexdigest() != artifact_sha or len(payload) != corpus_artifact.byte_length:
                raise ClosureAuditError(f"corpus payload does not match manifest: {artifact_sha}")
            indexed_artifacts.add(artifact_sha)
            artifact_records.append(
                {
                    "artifact_sha256": artifact_sha,
                    "byte_length": corpus_artifact.byte_length,
                    "capture_kind": corpus_artifact.capture_kind.value,
                    "content_type": corpus_artifact.content_type,
                    "first_party_verified": corpus_artifact.first_party_verified,
                    "locator": corpus_artifact.locator,
                    "retrieved_at_utc": corpus_artifact.retrieved_at.isoformat(),
                }
            )
        source_inventory.append(
            {
                "source_id": entry.source_id,
                "source_url": manifest.source.url,
                "manifest_schema_version": manifest.schema_version,
                "manifest_sha256": entry.manifest_sha256,
                "manifest_status": manifest.status.value,
                "artifacts": artifact_records,
            }
        )

    raw_ledger = _load_json(paths.ledger)
    _validate_ledger_shape(raw_ledger)
    valid_fields = {field.value for field in PredicateField}
    valid_coverage = {coverage.value for coverage in EvidenceCoverage}
    predicates: list[dict[str, Any]] = []
    for row in raw_ledger["rows"]:
        required = row.get("required_fields")
        evidence = row.get("evidence")
        if not isinstance(required, list) or not required or set(required) - valid_fields:
            raise ClosureAuditError(f"invalid required fields: {row['predicate_id']}")
        if len(set(required)) != len(required) or not isinstance(evidence, list):
            raise ClosureAuditError(f"duplicate required field or invalid evidence: {row['predicate_id']}")
        evidence_by_field: dict[str, list[dict[str, Any]]] = {field: [] for field in required}
        seen_claims: dict[tuple[str, str, str, str], tuple[str, str]] = {}
        for claim in evidence:
            try:
                field = claim["field"]
                coverage = claim["coverage"]
                source_id = claim["source_id"]
                locator = claim["locator"]
                artifact_sha = claim["artifact_sha256"]
                statement = claim["statement"]
                first_party_verified = claim["first_party_verified"]
            except KeyError as error:
                raise ClosureAuditError(f"incomplete evidence claim: {row['predicate_id']}") from error
            if field not in evidence_by_field or coverage not in valid_coverage:
                raise ClosureAuditError(f"unknown field or coverage status: {row['predicate_id']}")
            if first_party_verified is not True:
                raise ClosureAuditError("non-first-party evidence cannot satisfy a held field")
            evidence_artifact = artifacts.get(artifact_sha)
            if (
                source_id not in registry
                or evidence_artifact is None
                or evidence_artifact.source_id != source_id
                or artifact_sha not in indexed_artifacts
            ):
                raise ClosureAuditError("ledger evidence does not match registry, manifest, and corpus")
            claim_key = (field, source_id, locator, artifact_sha)
            claim_value = (coverage, statement)
            previous = seen_claims.get(claim_key)
            if previous is not None:
                if previous != claim_value:
                    raise ClosureAuditError("duplicate contradictory evidence claim")
                raise ClosureAuditError("duplicate evidence claim")
            seen_claims[claim_key] = claim_value
            evidence_by_field[field].append(
                {
                    "artifact_sha256": artifact_sha,
                    "coverage": coverage.lower(),
                    "first_party_verified": first_party_verified,
                    "locator": locator,
                    "source_id": source_id,
                    "statement": statement,
                }
            )

        field_reports: list[dict[str, Any]] = []
        for field in required:
            claims = evidence_by_field[field]
            has_closing = any(claim["coverage"] == "closing" for claim in claims)
            status = "explicitly_satisfied" if has_closing else "partial" if claims else "missing"
            field_reports.append(
                {
                    "field": field,
                    "status": status,
                    "evidence": claims,
                    "minimal_missing_requirement": (
                        None
                        if has_closing
                        else "direct explicit first-party causal evidence sufficient to close this field"
                    ),
                }
            )
        missing = [item["field"] for item in field_reports if item["status"] != "explicitly_satisfied"]
        predicates.append(
            {
                "predicate_id": row["predicate_id"],
                "description": row["description"],
                "disposition": "CLOSED" if not missing else "OPEN",
                "required_fields": field_reports,
                "minimal_missing_fields": missing,
            }
        )

    report: dict[str, Any] = {
        "schema_version": "P6C_CLOSURE_AUDIT_REPORT_V1",
        "scope": "existing replayable first-party Phase-6D corpus only",
        "input_digests": {
            "corpus_index_sha256": corpus_digest,
            "ledger_sha256": sha256(paths.ledger.read_bytes()).hexdigest(),
            "registry_sha256": sha256(paths.registry.read_bytes()).hexdigest(),
        },
        "corpus_sources": source_inventory,
        "predicates": predicates,
        "summary": {
            "corpus_artifacts": len(indexed_artifacts),
            "corpus_sources": len(source_inventory),
            "held_predicates": len(predicates),
            "closed_predicates": sum(item["disposition"] == "CLOSED" for item in predicates),
            "open_predicates": sum(item["disposition"] == "OPEN" for item in predicates),
            "field_status_counts": {
                status: sum(
                    field["status"] == status
                    for predicate in predicates
                    for field in predicate["required_fields"]
                )
                for status in ("explicitly_satisfied", "partial", "contradictory", "missing")
            },
            "candidate_creation_authorized": False,
            "detector_activity_authorized": False,
            "outcome_access_authorized": False,
            "oos_confirm_authorized": False,
        },
        "closure_review_authorized_predicate_ids": [],
    }
    return report


def report_with_digest(report: dict[str, Any]) -> dict[str, Any]:
    result = dict(report)
    result["report_sha256"] = canonical_json_digest(report)
    return result


def validate_checked_in_report(paths: ClosureAuditPaths, report_path: Path) -> dict[str, Any]:
    expected = report_with_digest(build_closure_report(paths))
    actual = _load_json(report_path)
    if actual != expected:
        raise ClosureAuditError("checked-in closure report differs from recomputed first-party audit")
    closed = {
        item["predicate_id"] for item in actual["predicates"] if item["disposition"] == "CLOSED"
    }
    authorized = set(actual.get("closure_review_authorized_predicate_ids", []))
    if not closed.issubset(authorized):
        raise ClosureAuditError("predicate closure is not authorized for this audit disposition")
    return actual
