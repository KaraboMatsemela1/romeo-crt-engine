from __future__ import annotations

import json
from pathlib import Path

from audit_phase6d_corpus_migration import _load_manifest

from romeo_crt_engine.research.registry_v1 import load_source_registry_v1
from romeo_crt_engine.research.source_acquisition_v1 import AcquisitionStatus

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "research/romeo/SOURCE_REGISTRY.csv"
ACQUISITION_DIR = ROOT / "research/romeo/phase6d/acquisitions"
INVENTORY_PATH = ROOT / "research/romeo/phase6d/RECOVERY_003_ROUTE_INVENTORY.json"
SCHEMA_VERSION = "P6D_RECOVERY_003_ROUTE_INVENTORY_V1"
NO_SOURCE_OBSERVATION = "NETWORK_DNS_UNAVAILABLE_NO_SOURCE_OBSERVATION"


def main() -> None:
    raw = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    if raw.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported Recovery 003 route-inventory schema")

    routes = raw.get("routes")
    if not isinstance(routes, list) or len(routes) != 6:
        raise ValueError("Recovery 003 must preserve exactly six bounded routes")

    registry = {row.source_id: row for row in load_source_registry_v1(REGISTRY_PATH)}
    source_ids = [route.get("source_id") for route in routes]
    if len(source_ids) != len(set(source_ids)):
        raise ValueError("Recovery 003 route source IDs must be unique")

    source_observations = 0
    for route in routes:
        source_id = route.get("source_id")
        if not isinstance(source_id, str) or source_id not in registry:
            raise ValueError(f"Recovery 003 route source is not registered: {source_id}")
        if route.get("route") != registry[source_id].url:
            raise ValueError(f"Recovery 003 route URL differs from registry: {source_id}")

        manifest_name = route.get("acquisition_manifest")
        if not isinstance(manifest_name, str):
            raise TypeError(f"Recovery 003 manifest name is missing: {source_id}")
        manifest, digest = _load_manifest(ACQUISITION_DIR / manifest_name)
        if manifest.source.source_id != source_id:
            raise ValueError(f"Recovery 003 manifest source mismatch: {source_id}")
        # The route inventory is an immutable Recovery-003 snapshot.  A later
        # admission may legitimately evolve the live manifest, but cannot alter
        # this pass's recorded zero-artifact conclusion.
        historical_digest = route.get("manifest_sha256")
        if not isinstance(historical_digest, str) or len(historical_digest) != 64:
            raise ValueError(f"Recovery 003 historical manifest digest is invalid: {source_id}")
        if manifest.source.url != route["route"]:
            raise ValueError(f"Recovery 003 manifest URL mismatch: {source_id}")
        if manifest.source.source_kind.value != route.get("source_kind"):
            raise ValueError(f"Recovery 003 source kind mismatch: {source_id}")
        if not route.get("predicate_ids"):
            raise ValueError(f"Recovery 003 predicate binding is missing: {source_id}")
        if not isinstance(route.get("tool"), str) or not route["tool"].strip():
            raise ValueError(f"Recovery 003 retrieval tool is missing: {source_id}")
        if route.get("result") != NO_SOURCE_OBSERVATION:
            source_observations += 1

        # Existing captured Telegram evidence remains in its prior manifest; this
        # pass did not obtain a new artifact through any of the bounded routes.
        is_existing_telegram_capture = source_id == "ROMEO-2026-TG-TIME-TS-6361"
        if (
            not is_existing_telegram_capture
            and digest == historical_digest
            and (manifest.status is not AcquisitionStatus.PARTIAL or manifest.artifacts)
        ):
            raise ValueError(f"Recovery 003 snapshot manifest is inconsistent: {source_id}")

    summary = {
        "bounded_routes": len(routes),
        "new_artifacts": 0,
        "new_payload_sha256s": 0,
        "source_availability_observed": source_observations,
        "candidate_creation_authorized": False,
        "detector_activity_authorized": False,
        "outcome_access_authorized": False,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
