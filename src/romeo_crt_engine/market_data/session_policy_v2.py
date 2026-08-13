from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum


class GapCategory(StrEnum):
    MARKET_CLOSED = "MARKET_CLOSED"
    SESSION_BREAK = "SESSION_BREAK"
    HOLIDAY_OR_EARLY_CLOSE = "HOLIDAY_OR_EARLY_CLOSE"
    PROVIDER_MISSING = "PROVIDER_MISSING"
    UNKNOWN_GAP = "UNKNOWN_GAP"


APPROVED_EXPECTED_GAP_CATEGORIES = frozenset(
    {
        GapCategory.MARKET_CLOSED,
        GapCategory.SESSION_BREAK,
        GapCategory.HOLIDAY_OR_EARLY_CLOSE,
    }
)


@dataclass(frozen=True, slots=True)
class MarketGapV2:
    provider: str
    venue: str
    instrument: str
    start_time: datetime
    end_time: datetime
    category: GapCategory
    policy_version: str
    evidence_id: str
    evidence_source: str

    def __post_init__(self) -> None:
        if not self.provider or not self.venue or not self.instrument:
            raise ValueError("gap identity fields must not be empty")
        if not self.policy_version or not self.evidence_id or not self.evidence_source:
            raise ValueError("gap policy/evidence fields must not be empty")
        if self.start_time.utcoffset() != timedelta(0) or self.end_time.utcoffset() != timedelta(0):
            raise ValueError("gap timestamps must be UTC")
        if self.end_time <= self.start_time:
            raise ValueError("gap end_time must be after start_time")

    @property
    def is_approved_expected_gap(self) -> bool:
        return self.category in APPROVED_EXPECTED_GAP_CATEGORIES

    def contains_minute_open(self, timestamp: datetime) -> bool:
        if timestamp.utcoffset() != timedelta(0):
            raise ValueError("timestamp must be UTC")
        return self.start_time <= timestamp < self.end_time

    def overlaps(self, start: datetime, end: datetime) -> bool:
        if start.utcoffset() != timedelta(0) or end.utcoffset() != timedelta(0):
            raise ValueError("window timestamps must be UTC")
        return self.start_time < end and self.end_time > start


def validate_gap_policy(
    gaps: tuple[MarketGapV2, ...],
    *,
    provider: str,
    venue: str,
    instrument: str,
    policy_version: str,
) -> None:
    previous_end: datetime | None = None
    for gap in sorted(gaps, key=lambda item: item.start_time):
        if (gap.provider, gap.venue, gap.instrument, gap.policy_version) != (
            provider,
            venue,
            instrument,
            policy_version,
        ):
            raise ValueError("gap does not match requested provider/instrument policy")
        if not gap.is_approved_expected_gap:
            raise ValueError(
                f"unapproved gap category cannot remove expected observations: {gap.category.value}"
            )
        if previous_end is not None and gap.start_time < previous_end:
            raise ValueError("approved gaps must not overlap")
        previous_end = gap.end_time


def minute_is_expected(
    timestamp: datetime,
    gaps: tuple[MarketGapV2, ...],
) -> bool:
    """Return False only when a minute is covered by an approved expected gap."""

    if timestamp.utcoffset() != timedelta(0):
        raise ValueError("timestamp must be UTC")
    for gap in gaps:
        if gap.contains_minute_open(timestamp):
            if not gap.is_approved_expected_gap:
                raise ValueError(
                    f"unapproved gap category cannot remove expected observations: {gap.category.value}"
                )
            return False
    return True
