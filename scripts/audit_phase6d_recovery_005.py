from __future__ import annotations

import json
from pathlib import Path

from romeo_crt_engine.research.registry_v1 import load_source_registry_v1

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "research/romeo/SOURCE_REGISTRY.csv"
INVENTORY_PATH = ROOT / "research/romeo/phase6d/RECOVERY_005_ROUTE_INVENTORY.json"


def main() -> None:
    raw = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    if raw.get("schema_version") != "P6D_RECOVERY_005_ROUTE_INVENTORY_V1":
        raise ValueError("unsupported Recovery 005 route-inventory schema")
    if raw.get("decision") != "RECOVERY_COMPLETE_NO_PREDICATE_CLOSURE":
        raise ValueError("Recovery 005 decision changed")
    routes = raw.get("routes")
    if not isinstance(routes, list) or len(routes) != 6:
        raise ValueError("Recovery 005 must preserve exactly six bounded routes")
    registry = {row.source_id: row for row in load_source_registry_v1(REGISTRY_PATH)}
    if len({route.get("source_id") for route in routes}) != 6:
        raise ValueError("Recovery 005 route source IDs must be unique")
    for route in routes:
        source_id = route.get("source_id")
        if source_id not in registry or route.get("registered_route") != registry[source_id].url:
            raise ValueError(f"Recovery 005 registry binding mismatch: {source_id}")
        if route.get("outcome") not in {
            "CONTACTED_NO_RELEVANT_PAYLOAD",
            "ENVIRONMENT_ACCESS_FAILURE",
        } or route.get("payload_admitted") is not False:
            raise ValueError(f"Recovery 005 historical route conclusion changed: {source_id}")
    if raw.get("new_replayable_artifacts") != 0 or raw.get("new_closing_field_evidence") != 0 or raw.get("candidate_ready_rows") != 0 or raw.get("issue_16_recommendation") != "KEEP_BLOCKED":
        raise ValueError("Recovery 005 must remain a zero-admission historical pass")
    print(json.dumps({"bounded_routes": 6, "new_artifacts": 0, "closing_field_evidence": 0, "candidate_ready_rows": 0, "candidate_creation_authorized": False, "detector_activity_authorized": False, "outcome_access_authorized": False}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
