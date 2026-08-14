from __future__ import annotations

import json
from pathlib import Path

from romeo_crt_engine.research.predicate_ledger_v1 import (
    PredicateEvidenceV1,
    PredicateField,
    PredicateLedgerRowV1,
    PredicateLedgerV1,
)
from romeo_crt_engine.research.registry_v1 import load_source_registry_v1

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "research/romeo/SOURCE_REGISTRY.csv"
LEDGER_PATH = ROOT / "research/romeo/phase6d/PREDICATE_LEDGER_V1.json"


def _load_ledger() -> PredicateLedgerV1:
    raw = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    rows: list[PredicateLedgerRowV1] = []
    for item in raw["rows"]:
        evidence = tuple(
            PredicateEvidenceV1(
                field=PredicateField(entry["field"]),
                source_id=entry["source_id"],
                locator=entry["locator"],
                artifact_sha256=entry["artifact_sha256"],
                statement=entry["statement"],
                first_party_verified=entry["first_party_verified"],
            )
            for entry in item["evidence"]
        )
        rows.append(
            PredicateLedgerRowV1(
                predicate_id=item["predicate_id"],
                description=item["description"],
                required_fields=tuple(PredicateField(value) for value in item["required_fields"]),
                evidence=evidence,
                schema_version=raw["schema_version"],
            )
        )
    return PredicateLedgerV1(rows=tuple(rows), schema_version=raw["schema_version"])


def main() -> None:
    registry = load_source_registry_v1(REGISTRY_PATH)
    source_ids = {row.source_id for row in registry}
    ledger = _load_ledger()
    unknown_sources = sorted(
        {
            evidence.source_id
            for row in ledger.rows
            for evidence in row.evidence
            if evidence.source_id not in source_ids
        }
    )
    if unknown_sources:
        raise ValueError(f"predicate ledger references unknown sources: {unknown_sources}")

    summary = {
        "source_registry_rows": len(registry),
        "predicate_rows": len(ledger.rows),
        "candidate_ready_rows": len(ledger.candidate_ready_rows),
        "closed_predicate_ids": [row.predicate_id for row in ledger.candidate_ready_rows],
        "outcome_access_authorized": False,
        "detector_activity_authorized": False,
        "candidate_creation_authorized": False,
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
