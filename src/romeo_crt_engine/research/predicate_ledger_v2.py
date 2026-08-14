from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

PREDICATE_LEDGER_SCHEMA_VERSION = "P6D_PREDICATE_LEDGER_V2"


class PredicateField(StrEnum):
    EXACT_PREDICATE = "EXACT_PREDICATE"
    INFORMATION_AVAILABILITY_TIME = "INFORMATION_AVAILABILITY_TIME"
    DIRECTION_TIMEFRAME_OWNERSHIP = "DIRECTION_TIMEFRAME_OWNERSHIP"
    CONFIRMATION = "CONFIRMATION"
    INVALIDATION = "INVALIDATION"
    EXPIRY = "EXPIRY"
    DATA_REQUIREMENTS = "DATA_REQUIREMENTS"


class EvidenceCoverage(StrEnum):
    PARTIAL = "PARTIAL"
    CLOSING = "CLOSING"


class PredicateStatus(StrEnum):
    UNRESOLVED = "UNRESOLVED"
    PARTIAL = "PARTIAL"
    CLOSED = "CLOSED"


def _is_sha256(value: str) -> bool:
    return len(value) == 64 and all(char in "0123456789abcdef" for char in value)


@dataclass(frozen=True, slots=True)
class PredicateEvidenceV2:
    field: PredicateField
    source_id: str
    locator: str
    artifact_sha256: str
    statement: str
    coverage: EvidenceCoverage
    first_party_verified: bool

    def __post_init__(self) -> None:
        if not self.source_id.strip() or not self.locator.strip() or not self.statement.strip():
            raise ValueError("predicate evidence fields must not be empty")
        if not _is_sha256(self.artifact_sha256):
            raise ValueError("artifact_sha256 must be a lowercase SHA-256 digest")
        if not self.first_party_verified:
            raise ValueError("predicate evidence must be directly first-party verified")


@dataclass(frozen=True, slots=True)
class PredicateLedgerRowV2:
    predicate_id: str
    description: str
    required_fields: tuple[PredicateField, ...]
    evidence: tuple[PredicateEvidenceV2, ...] = ()
    schema_version: str = PREDICATE_LEDGER_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != PREDICATE_LEDGER_SCHEMA_VERSION:
            raise ValueError("unsupported predicate-ledger schema")
        if not self.predicate_id.strip() or not self.description.strip():
            raise ValueError("predicate identity fields must not be empty")
        if not self.required_fields:
            raise ValueError("predicate must declare at least one required field")
        if len(set(self.required_fields)) != len(self.required_fields):
            raise ValueError("required_fields must be unique")
        required = set(self.required_fields)
        if any(item.field not in required for item in self.evidence):
            raise ValueError("predicate evidence field must be declared in required_fields")
        keys = [
            (item.field, item.source_id, item.locator, item.artifact_sha256, item.coverage)
            for item in self.evidence
        ]
        if len(keys) != len(set(keys)):
            raise ValueError("predicate evidence entries must be unique")

    @property
    def observed_fields(self) -> frozenset[PredicateField]:
        return frozenset(item.field for item in self.evidence)

    @property
    def satisfied_fields(self) -> frozenset[PredicateField]:
        return frozenset(
            item.field for item in self.evidence if item.coverage is EvidenceCoverage.CLOSING
        )

    @property
    def missing_fields(self) -> tuple[PredicateField, ...]:
        satisfied = self.satisfied_fields
        return tuple(field for field in self.required_fields if field not in satisfied)

    @property
    def status(self) -> PredicateStatus:
        if not self.evidence:
            return PredicateStatus.UNRESOLVED
        if self.missing_fields:
            return PredicateStatus.PARTIAL
        return PredicateStatus.CLOSED

    @property
    def candidate_ready(self) -> bool:
        return self.status is PredicateStatus.CLOSED


@dataclass(frozen=True, slots=True)
class PredicateLedgerV2:
    rows: tuple[PredicateLedgerRowV2, ...]
    schema_version: str = PREDICATE_LEDGER_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != PREDICATE_LEDGER_SCHEMA_VERSION:
            raise ValueError("unsupported predicate-ledger schema")
        identifiers = [row.predicate_id for row in self.rows]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("predicate IDs must be unique")

    @property
    def candidate_ready_rows(self) -> tuple[PredicateLedgerRowV2, ...]:
        return tuple(row for row in self.rows if row.candidate_ready)
