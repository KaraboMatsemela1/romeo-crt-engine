from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class DoctrineDeltaClassification(StrEnum):
    CLARIFICATION = "CLARIFICATION"
    REFINEMENT = "REFINEMENT"
    NEW_OPTIONAL_BRANCH = "NEW_OPTIONAL_BRANCH"
    SUPERSEDING_RULE = "SUPERSEDING_RULE"
    NON_ALPHA_CONTEXT = "NON_ALPHA_CONTEXT"
    UNRESOLVED = "UNRESOLVED"


@dataclass(frozen=True, slots=True)
class DoctrineStatementV1:
    statement_id: str
    text: str
    source_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.statement_id.strip() or not self.text.strip():
            raise ValueError("doctrine statement identity/text must not be empty")
        if not self.source_ids or any(not source_id.strip() for source_id in self.source_ids):
            raise ValueError("doctrine statement must cite at least one source")
        if len(set(self.source_ids)) != len(self.source_ids):
            raise ValueError("doctrine source_ids must be unique")


@dataclass(frozen=True, slots=True)
class DoctrineDeltaV1:
    baseline: DoctrineStatementV1
    incoming: DoctrineStatementV1
    classification: DoctrineDeltaClassification
    deterministic_effect: bool
    rationale: str

    def __post_init__(self) -> None:
        if self.baseline.statement_id == self.incoming.statement_id:
            raise ValueError("baseline and incoming statements must be distinct")
        if not self.rationale.strip():
            raise ValueError("doctrine delta rationale must not be empty")
        if self.classification in {
            DoctrineDeltaClassification.UNRESOLVED,
            DoctrineDeltaClassification.NON_ALPHA_CONTEXT,
        } and self.deterministic_effect:
            raise ValueError("unresolved/non-alpha doctrine cannot have deterministic alpha effect")


def record_doctrine_delta(
    *,
    baseline: DoctrineStatementV1,
    incoming: DoctrineStatementV1,
    classification: DoctrineDeltaClassification,
    deterministic_effect: bool,
    rationale: str,
) -> DoctrineDeltaV1:
    """Validate an explicit research classification; never infer strategy semantics automatically."""
    return DoctrineDeltaV1(
        baseline=baseline,
        incoming=incoming,
        classification=classification,
        deterministic_effect=deterministic_effect,
        rationale=rationale,
    )
