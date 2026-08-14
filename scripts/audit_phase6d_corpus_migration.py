from __future__ import annotations

import json
from datetime import datetime
from hashlib import sha256
from pathlib import Path

from romeo_crt_engine.research.corpus_index_v1 import CorpusEntryV1, CorpusIndexV1
from romeo_crt_engine.research.predicate_ledger_v2 import (
    EvidenceCoverage,
    PredicateEvidenceV2,
    PredicateField,
    PredicateLedgerRowV2,
    PredicateLedgerV2,
)
from romeo_crt_engine.research.registry_v1 import load_source_registry_v1
from romeo_crt_engine.research.source_acquisition_v1 import (
    AcquisitionStatus,
    CaptureKind,
    SourceAcquisitionManifestV1,
    SourceArtifactV1,
    SourceIdentityV1,
    SourceKind,
)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "research/romeo/SOURCE_REGISTRY.csv"
ACQUISITION_DIR = ROOT / "research/romeo/phase6d/acquisitions"
CORPUS_INDEX_PATH = ROOT / "research/romeo/phase6d/CORPUS_INDEX_V1.json"
LEDGER_PATH = ROOT / "research/romeo/phase6d/PREDICATE_LEDGER_V2.json"
PAYLOAD_DIR = ROOT / "research/romeo/phase6d/payloads"


def _load_manifest(path: Path) -> tuple[SourceAcquisitionManifestV1, str]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    expected_digest = raw.pop("manifest_sha256")
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
    if manifest.digest() != expected_digest:
        raise ValueError(f"manifest digest mismatch: {path.name}")
    return manifest, expected_digest


def _load_corpus_index() -> tuple[CorpusIndexV1, str]:
    raw = json.loads(CORPUS_INDEX_PATH.read_text(encoding="utf-8"))
    expected_digest = raw["corpus_index_sha256"]
    index = CorpusIndexV1(
        entries=tuple(
            CorpusEntryV1(
                source_id=item["source_id"],
                manifest_sha256=item["manifest_sha256"],
                artifact_sha256s=tuple(item["artifact_sha256s"]),
            )
            for item in raw["entries"]
        )
    )
    if index.digest() != expected_digest:
        raise ValueError("corpus index digest mismatch")
    return index, expected_digest


def _load_ledger() -> PredicateLedgerV2:
    raw = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows: list[PredicateLedgerRowV2] = []
    for item in raw["rows"]:
        evidence = tuple(
            PredicateEvidenceV2(
                field=PredicateField(entry["field"]),
                source_id=entry["source_id"],
                locator=entry["locator"],
                artifact_sha256=entry["artifact_sha256"],
                statement=entry["statement"],
                coverage=EvidenceCoverage(entry["coverage"]),
                first_party_verified=entry["first_party_verified"],
            )
            for entry in item["evidence"]
        )
        rows.append(
            PredicateLedgerRowV2(
                predicate_id=item["predicate_id"],
                description=item["description"],
                required_fields=tuple(PredicateField(value) for value in item["required_fields"]),
                evidence=evidence,
                schema_version=raw["schema_version"],
            )
        )
    return PredicateLedgerV2(rows=tuple(rows), schema_version=raw["schema_version"])


def main() -> None:
    registry = load_source_registry_v1(REGISTRY_PATH)
    registry_by_id = {row.source_id: row for row in registry}

    loaded = tuple(_load_manifest(path) for path in sorted(ACQUISITION_DIR.glob("*.json")))
    manifests = tuple(item[0] for item in loaded)
    manifest_digest_by_source = {manifest.source.source_id: digest for manifest, digest in loaded}
    if len(manifest_digest_by_source) != len(manifests):
        raise ValueError("acquisition source IDs must be unique")

    for manifest in manifests:
        registered = registry_by_id.get(manifest.source.source_id)
        if registered is None:
            raise ValueError(f"acquisition source is not registered: {manifest.source.source_id}")
        if registered.url != manifest.source.url:
            raise ValueError(f"acquisition URL differs from registry: {manifest.source.source_id}")

    artifact_by_sha: dict[str, SourceArtifactV1] = {}
    for manifest in manifests:
        for artifact in manifest.artifacts:
            if artifact.payload_sha256 in artifact_by_sha:
                raise ValueError(f"artifact SHA appears in multiple manifests: {artifact.payload_sha256}")
            artifact_by_sha[artifact.payload_sha256] = artifact

    corpus, corpus_digest = _load_corpus_index()
    indexed_artifacts: set[str] = set()
    for entry in corpus.entries:
        manifest_digest = manifest_digest_by_source.get(entry.source_id)
        if manifest_digest != entry.manifest_sha256:
            raise ValueError(f"corpus entry manifest mismatch: {entry.source_id}")
        for artifact_sha in entry.artifact_sha256s:
            artifact = artifact_by_sha.get(artifact_sha)
            if artifact is None or artifact.source_id != entry.source_id:
                raise ValueError(f"corpus artifact is not provenance-bound: {artifact_sha}")
            payload_path = PAYLOAD_DIR / f"{artifact_sha}.txt"
            if not payload_path.is_file():
                raise ValueError(f"corpus artifact payload file is missing: {artifact_sha}")
            payload = payload_path.read_bytes()
            if sha256(payload).hexdigest() != artifact_sha:
                raise ValueError(f"payload SHA does not match artifact: {artifact_sha}")
            if len(payload) != artifact.byte_length:
                raise ValueError(f"payload byte length does not match manifest: {artifact_sha}")
            indexed_artifacts.add(artifact_sha)

    ledger = _load_ledger()
    for row in ledger.rows:
        for evidence in row.evidence:
            if evidence.source_id not in registry_by_id:
                raise ValueError(f"ledger references unknown source: {evidence.source_id}")
            artifact = artifact_by_sha.get(evidence.artifact_sha256)
            if artifact is None:
                raise ValueError(f"ledger evidence lacks acquisition artifact: {evidence.artifact_sha256}")
            if artifact.source_id != evidence.source_id:
                raise ValueError("ledger evidence source does not own artifact SHA")
            if evidence.artifact_sha256 not in indexed_artifacts:
                raise ValueError("ledger evidence artifact is not admitted to corpus index")

    observed_evidence = tuple(item for row in ledger.rows for item in row.evidence)
    closing_evidence = tuple(
        item for item in observed_evidence if item.coverage is EvidenceCoverage.CLOSING
    )
    rows_with_evidence = tuple(row for row in ledger.rows if row.evidence)

    summary = {
        "acquisition_manifests": len(manifests),
        "captured_manifests": sum(
            manifest.status is AcquisitionStatus.CAPTURED for manifest in manifests
        ),
        "partial_manifests": sum(
            manifest.status is AcquisitionStatus.PARTIAL for manifest in manifests
        ),
        "corpus_index_sha256": corpus_digest,
        "corpus_sources": len(corpus.entries),
        "corpus_artifacts": len(indexed_artifacts),
        "payload_files_verified": len(indexed_artifacts),
        "predicate_rows": len(ledger.rows),
        "predicate_rows_with_artifact_evidence": len(rows_with_evidence),
        "observed_field_evidence": len(observed_evidence),
        "closing_field_evidence": len(closing_evidence),
        "candidate_ready_rows": len(ledger.candidate_ready_rows),
        "closed_predicate_ids": [row.predicate_id for row in ledger.candidate_ready_rows],
        "candidate_creation_authorized": False,
        "detector_activity_authorized": False,
        "outcome_access_authorized": False,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
