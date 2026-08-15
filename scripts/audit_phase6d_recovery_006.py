from __future__ import annotations

import json
from pathlib import Path

from audit_phase6d_corpus_migration import _load_manifest

from romeo_crt_engine.research.registry_v1 import load_source_registry_v1

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "research/romeo/SOURCE_REGISTRY.csv"
ACQUISITION_DIR = ROOT / "research/romeo/phase6d/acquisitions"
INVENTORY_PATH = ROOT / "research/romeo/phase6d/RECOVERY_006_ROUTE_INVENTORY.json"
SCHEMA_VERSION = "P6D_RECOVERY_006_ROUTE_INVENTORY_V1"
NO_SOURCE_OBSERVATION = "ENVIRONMENT_DNS_UNAVAILABLE_NO_SOURCE_OBSERVATION"


def main() -> None:
    raw = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    if raw.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported Recovery 006 route-inventory schema")
    if raw.get("decision") != "BLOCKED_NO_VERIFIED_PREDICATE_CLOSURE":
        raise ValueError("Recovery 006 must remain blocked")

    routes = raw.get("routes")
    if not isinstance(routes, list) or len(routes) != 6:
        raise ValueError("Recovery 006 must preserve exactly six bounded routes")

    registry = {row.source_id: row for row in load_source_registry_v1(REGISTRY_PATH)}
    source_ids = [route.get("source_id") for route in routes]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("Recovery 006 route source IDs must be unique")

    for route in routes:
        source_id = route.get("source_id")
        if not isinstance(source_id, str) or source_id not in registry:
            raise ValueError(f"Recovery 006 route source is not registered: {source_id}")
        if route.get("route") != registry[source_id].url:
            raise ValueError(f"Recovery 006 route URL differs from registry: {source_id}")
        if not route.get("predicate_ids"):
            raise ValueError(f"Recovery 006 predicate binding is missing: {source_id}")

        manifest_name = route.get("acquisition_manifest")
        if not isinstance(manifest_name, str):
            raise TypeError(f"Recovery 006 manifest name is missing: {source_id}")
        manifest, digest = _load_manifest(ACQUISITION_DIR / manifest_name)
        if manifest.source.source_id != source_id or digest != route.get("manifest_sha256"):
            raise ValueError(f"Recovery 006 manifest binding mismatch: {source_id}")
        if manifest.source.url != route["route"] or manifest.source.source_kind.value != route.get(
            "source_kind"
        ):
            raise ValueError(f"Recovery 006 source binding mismatch: {source_id}")

        attempt = route.get("attempt")
        if not isinstance(attempt, dict):
            raise TypeError(f"Recovery 006 attempt is missing: {source_id}")
        if attempt.get("result") != NO_SOURCE_OBSERVATION:
            raise ValueError(f"Recovery 006 must fail closed before source contact: {source_id}")
        if attempt.get("source_contact_observed") is not False:
            raise ValueError(f"Recovery 006 cannot claim source contact: {source_id}")
        for field in ("method", "target_payload", "retrieved_at_utc"):
            if not isinstance(attempt.get(field), str) or not attempt[field].strip():
                raise TypeError(f"Recovery 006 attempt {field} is missing: {source_id}")

    expected_zeroes = (
        "new_replayable_artifacts",
        "new_payload_sha256s",
        "new_acquisition_manifests",
        "new_corpus_index_entries",
        "new_closing_field_evidence",
        "candidate_ready_rows",
    )
    if any(raw.get(field) != 0 for field in expected_zeroes):
        raise ValueError("Recovery 006 must not admit artifacts or advance a predicate")
    if raw.get("issue_16_recommendation") != "KEEP_BLOCKED":
        raise ValueError("Recovery 006 must keep Issue #16 blocked")

    print(
        json.dumps(
            {
                "bounded_routes": len(routes),
                "source_contacts_observed": 0,
                "new_artifacts": 0,
                "new_payload_sha256s": 0,
                "closing_field_evidence": 0,
                "candidate_ready_rows": 0,
                "candidate_creation_authorized": False,
                "detector_activity_authorized": False,
                "outcome_access_authorized": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
