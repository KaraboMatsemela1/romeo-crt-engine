from __future__ import annotations

import json
from pathlib import Path

from audit_phase6d_corpus_migration import _load_manifest

from romeo_crt_engine.research.registry_v1 import load_source_registry_v1

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "research/romeo/SOURCE_REGISTRY.csv"
ACQUISITION_DIR = ROOT / "research/romeo/phase6d/acquisitions"
INVENTORY_PATH = ROOT / "research/romeo/phase6d/RECOVERY_004_ROUTE_INVENTORY.json"
SCHEMA_VERSION = "P6D_RECOVERY_004_ROUTE_INVENTORY_V1"
SOURCE_UNAVAILABLE = "SOURCE_UNAVAILABLE"


def main() -> None:
    raw = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    if raw.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported Recovery 004 route-inventory schema")
    routes = raw.get("routes")
    if not isinstance(routes, list) or len(routes) != 6:
        raise ValueError("Recovery 004 must preserve exactly six bounded routes")

    registry = {row.source_id: row for row in load_source_registry_v1(REGISTRY_PATH)}
    source_ids = [route.get("source_id") for route in routes]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("Recovery 004 route source IDs must be unique")

    for route in routes:
        source_id = route.get("source_id")
        if not isinstance(source_id, str) or source_id not in registry:
            raise ValueError(f"Recovery 004 route source is not registered: {source_id}")
        if route.get("route") != registry[source_id].url:
            raise ValueError(f"Recovery 004 route URL differs from registry: {source_id}")
        manifest_name = route.get("acquisition_manifest")
        if not isinstance(manifest_name, str):
            raise TypeError(f"Recovery 004 manifest name is missing: {source_id}")
        manifest, _ = _load_manifest(ACQUISITION_DIR / manifest_name)
        historical_digest = route.get("manifest_sha256")
        if manifest.source.source_id != source_id:
            raise ValueError(f"Recovery 004 manifest binding mismatch: {source_id}")
        if not isinstance(historical_digest, str) or len(historical_digest) != 64:
            raise ValueError(f"Recovery 004 historical manifest digest is invalid: {source_id}")
        if manifest.source.url != route["route"] or manifest.source.source_kind.value != route.get("source_kind"):
            raise ValueError(f"Recovery 004 source binding mismatch: {source_id}")
        if not route.get("predicate_ids"):
            raise ValueError(f"Recovery 004 predicate binding is missing: {source_id}")
        for attempt_name in ("availability_check", "channel_index_search"):
            attempt = route.get(attempt_name)
            if not isinstance(attempt, dict):
                raise TypeError(f"Recovery 004 {attempt_name} is missing: {source_id}")
            if attempt.get("result") != SOURCE_UNAVAILABLE or attempt.get("source_contact_observed") is not False:
                raise ValueError(f"Recovery 004 must fail closed before source contact: {source_id}")
            if not isinstance(attempt.get("method"), str) or not isinstance(attempt.get("retrieved_at_utc"), str):
                raise TypeError(f"Recovery 004 attempt provenance is incomplete: {source_id}")
        search = route["channel_index_search"]
        if not isinstance(search.get("route"), str) or not search["route"].startswith("https://t.me/s/officialRomeotpt?q="):
            raise ValueError(f"Recovery 004 index route is not official Romeo Telegram: {source_id}")

    print(json.dumps({
        "bounded_routes": len(routes),
        "availability_checks": len(routes),
        "official_channel_index_searches": len(routes),
        "source_unavailable_routes": len(routes),
        "new_artifacts": 0,
        "new_payload_sha256s": 0,
        "closing_field_evidence": 0,
        "candidate_ready_rows": 0,
        "candidate_creation_authorized": False,
        "detector_activity_authorized": False,
        "outcome_access_authorized": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
