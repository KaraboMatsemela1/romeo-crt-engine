from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256

from romeo_crt_engine.market_data.history_qualification_v2 import MissingInterval
from romeo_crt_engine.market_data.session_policy_v2 import MarketGapV2, validate_gap_policy


@dataclass(frozen=True, slots=True)
class GapReconciliationSummaryV2:
    provider: str
    venue: str
    instrument: str
    policy_version: str
    missing_interval_count: int
    approved_gap_count: int
    missing_minutes: int
    approved_minutes: int
    reconciliation_sha256: str
    status: str = "FULLY_RECONCILED"

    def __post_init__(self) -> None:
        if not self.provider or not self.venue or not self.instrument or not self.policy_version:
            raise ValueError("reconciliation identity fields must not be empty")
        if self.missing_interval_count < 0 or self.approved_gap_count < 0:
            raise ValueError("reconciliation counts must be non-negative")
        if self.missing_minutes < 0 or self.approved_minutes < 0:
            raise ValueError("reconciliation minute totals must be non-negative")
        if self.missing_minutes != self.approved_minutes:
            raise ValueError("fully reconciled minute totals must match")
        if len(self.reconciliation_sha256) != 64:
            raise ValueError("reconciliation_sha256 must be a SHA-256 value")
        if self.status != "FULLY_RECONCILED":
            raise ValueError("successful reconciliation status must be FULLY_RECONCILED")


def _validate_missing_intervals(missing: tuple[MissingInterval, ...]) -> None:
    previous_end = None
    for interval in missing:
        if previous_end is not None and interval.start < previous_end:
            raise ValueError("raw missing intervals must be ordered and non-overlapping")
        previous_end = interval.end


def _gap_minutes(gap: MarketGapV2) -> int:
    seconds = (gap.end_time - gap.start_time).total_seconds()
    if seconds % 60 != 0:
        raise ValueError("approved gap boundaries must be minute-aligned")
    return int(seconds // 60)


def reconcile_missing_intervals_exactly(
    missing: tuple[MissingInterval, ...],
    approved_gaps: tuple[MarketGapV2, ...],
    *,
    provider: str,
    venue: str,
    instrument: str,
    policy_version: str,
) -> GapReconciliationSummaryV2:
    """Require approved evidence to cover raw missing intervals exactly and only."""

    _validate_missing_intervals(missing)
    validate_gap_policy(
        approved_gaps,
        provider=provider,
        venue=venue,
        instrument=instrument,
        policy_version=policy_version,
    )

    sorted_gaps = tuple(sorted(approved_gaps, key=lambda item: item.start_time))
    gap_index = 0

    for interval in missing:
        cursor = interval.start
        while gap_index < len(sorted_gaps):
            gap = sorted_gaps[gap_index]
            if gap.end_time <= interval.start:
                raise ValueError("approved gap lies outside raw missing intervals")
            if gap.start_time >= interval.end:
                break
            if gap.start_time != cursor:
                raise ValueError("raw missing interval contains uncovered minutes")
            if gap.end_time > interval.end:
                raise ValueError("approved gap covers provider observations outside raw gap")
            cursor = gap.end_time
            gap_index += 1
        if cursor != interval.end:
            raise ValueError("raw missing interval is not fully reconciled")

    if gap_index != len(sorted_gaps):
        raise ValueError("approved gap lies outside raw missing intervals")

    missing_minutes = sum(interval.missing_minutes for interval in missing)
    approved_minutes = sum(_gap_minutes(gap) for gap in sorted_gaps)
    if missing_minutes != approved_minutes:
        raise ValueError("approved gap minutes do not equal raw missing minutes")

    digest = sha256()
    digest.update(b"P6B_GAP_RECONCILIATION_V2\n")
    for interval in missing:
        digest.update(interval.start.isoformat().encode())
        digest.update(b"|")
        digest.update(interval.end.isoformat().encode())
        digest.update(b"\n")
    digest.update(b"--APPROVED--\n")
    for gap in sorted_gaps:
        digest.update(gap.start_time.isoformat().encode())
        digest.update(b"|")
        digest.update(gap.end_time.isoformat().encode())
        digest.update(b"|")
        digest.update(gap.category.value.encode())
        digest.update(b"|")
        digest.update(gap.evidence_id.encode())
        digest.update(b"|")
        digest.update(gap.evidence_source.encode())
        digest.update(b"\n")

    return GapReconciliationSummaryV2(
        provider=provider,
        venue=venue,
        instrument=instrument,
        policy_version=policy_version,
        missing_interval_count=len(missing),
        approved_gap_count=len(sorted_gaps),
        missing_minutes=missing_minutes,
        approved_minutes=approved_minutes,
        reconciliation_sha256=digest.hexdigest(),
    )
