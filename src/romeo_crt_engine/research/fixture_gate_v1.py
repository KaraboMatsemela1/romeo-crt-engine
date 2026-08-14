from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from romeo_crt_engine.research.predicate_ledger_v1 import PredicateLedgerRowV1


class FixtureKind(StrEnum):
    POSITIVE = "POSITIVE"
    NEGATIVE = "NEGATIVE"


@dataclass(frozen=True, slots=True)
class PredicateFixtureV1:
    fixture_id: str
    predicate_id: str
    kind: FixtureKind
    source_ids: tuple[str, ...]
    information_available_at: str
    observed_inputs: str
    expected_label: str

    def __post_init__(self) -> None:
        values = (
            self.fixture_id,
            self.predicate_id,
            self.information_available_at,
            self.observed_inputs,
            self.expected_label,
        )
        if any(not value.strip() for value in values):
            raise ValueError("fixture fields must not be empty")
        if not self.source_ids or any(not source_id.strip() for source_id in self.source_ids):
            raise ValueError("fixture must cite at least one source")


def assert_fixture_gate(
    predicate: PredicateLedgerRowV1,
    fixtures: tuple[PredicateFixtureV1, ...],
) -> None:
    if not predicate.candidate_ready:
        raise ValueError("predicate must be CLOSED before fixture gate can pass")
    relevant = tuple(item for item in fixtures if item.predicate_id == predicate.predicate_id)
    if len({item.fixture_id for item in relevant}) != len(relevant):
        raise ValueError("fixture IDs must be unique per predicate")
    kinds = {item.kind for item in relevant}
    if FixtureKind.POSITIVE not in kinds or FixtureKind.NEGATIVE not in kinds:
        raise ValueError("fixture gate requires at least one positive and one negative fixture")
