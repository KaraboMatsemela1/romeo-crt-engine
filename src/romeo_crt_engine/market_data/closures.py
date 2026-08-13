from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from typing import TypeAlias


@dataclass(frozen=True, slots=True)
class VenueClosure:
    provider: str
    venue: str
    symbol: str
    start_utc: datetime
    end_utc: datetime
    evidence_id: str
    reason: str

    def __post_init__(self) -> None:
        _validate_gap_fields(
            provider=self.provider,
            venue=self.venue,
            symbol=self.symbol,
            start_utc=self.start_utc,
            end_utc=self.end_utc,
            evidence_id=self.evidence_id,
            label="venue closure",
        )


@dataclass(frozen=True, slots=True)
class ArchiveExclusion:
    """A provider-authenticated UTC archive excluded whole from canonical normalization."""

    provider: str
    venue: str
    symbol: str
    archive_date: date
    source_sha256: str
    evidence_id: str
    reason: str

    def __post_init__(self) -> None:
        if not self.provider or not self.venue or not self.symbol or not self.evidence_id:
            raise ValueError("archive exclusion identity/evidence fields must not be empty")
        if len(self.source_sha256) != 64:
            raise ValueError("archive exclusion source_sha256 must be a SHA-256 digest")
        try:
            int(self.source_sha256, 16)
        except ValueError as error:
            raise ValueError("archive exclusion source_sha256 must be hexadecimal") from error
        if not self.reason:
            raise ValueError("archive exclusion reason must not be empty")

    @property
    def start_utc(self) -> datetime:
        return datetime.combine(self.archive_date, time.min, tzinfo=UTC)

    @property
    def end_utc(self) -> datetime:
        return self.start_utc + timedelta(days=1)


ApprovedGap: TypeAlias = VenueClosure | ArchiveExclusion


def _validate_gap_fields(
    *,
    provider: str,
    venue: str,
    symbol: str,
    start_utc: datetime,
    end_utc: datetime,
    evidence_id: str,
    label: str,
) -> None:
    if start_utc.tzinfo is None or end_utc.tzinfo is None:
        raise ValueError(f"{label} timestamps must be timezone-aware")
    if start_utc.tzinfo != UTC or end_utc.tzinfo != UTC:
        raise ValueError(f"{label} timestamps must use UTC")
    if end_utc <= start_utc:
        raise ValueError(f"{label} end must be after start")
    if not provider or not venue or not symbol or not evidence_id:
        raise ValueError(f"{label} identity/evidence fields must not be empty")


BINANCE_BTCUSDT_2019_03_12 = VenueClosure(
    provider="BINANCE_PUBLIC_DATA",
    venue="BINANCE_SPOT",
    symbol="BTCUSDT",
    start_utc=datetime(2019, 3, 12, 2, 0, tzinfo=UTC),
    end_utc=datetime(2019, 3, 12, 8, 0, tzinfo=UTC),
    evidence_id="P6-DATA-QUALITY-AMENDMENT-001",
    reason="BINANCE_SCHEDULED_SYSTEM_UPGRADE_TRADING_SUSPENDED",
)

KNOWN_VENUE_CLOSURES: tuple[VenueClosure, ...] = (BINANCE_BTCUSDT_2019_03_12,)


def closures_for(
    *,
    provider: str,
    venue: str,
    symbol: str,
) -> tuple[VenueClosure, ...]:
    identity = (provider, venue, symbol.upper())
    return tuple(
        closure
        for closure in KNOWN_VENUE_CLOSURES
        if (closure.provider, closure.venue, closure.symbol) == identity
    )


def archive_exclusion(
    *,
    provider: str,
    venue: str,
    symbol: str,
    archive_date: date,
    source_sha256: str,
    evidence_id: str = "P6-DATA-QUALITY-AMENDMENT-002",
) -> ArchiveExclusion:
    return ArchiveExclusion(
        provider=provider,
        venue=venue,
        symbol=symbol.upper(),
        archive_date=archive_date,
        source_sha256=source_sha256,
        evidence_id=evidence_id,
        reason="PROVIDER_AUTHENTICATED_INCOMPLETE_OR_MALFORMED_DAILY_ARCHIVE_EXCLUDED",
    )


def exact_gap_is_approved(
    start_utc: datetime,
    end_utc: datetime,
    gaps: tuple[ApprovedGap, ...],
) -> bool:
    return any(start_utc == gap.start_utc and end_utc == gap.end_utc for gap in gaps)


def gap_is_approved(
    start_utc: datetime,
    end_utc: datetime,
    gaps: tuple[ApprovedGap, ...],
) -> bool:
    """Return true when approved gap intervals continuously cover the entire observed gap."""
    if end_utc <= start_utc:
        return False
    cursor = start_utc
    for gap in sorted(gaps, key=lambda item: item.start_utc):
        if gap.end_utc <= cursor:
            continue
        if gap.start_utc > cursor:
            return False
        cursor = max(cursor, gap.end_utc)
        if cursor >= end_utc:
            return True
    return False


def window_overlaps_gap(
    start_utc: datetime,
    end_utc: datetime,
    gaps: tuple[ApprovedGap, ...],
) -> bool:
    return any(start_utc < gap.end_utc and end_utc > gap.start_utc for gap in gaps)


def window_overlaps_closure(
    start_utc: datetime,
    end_utc: datetime,
    closures: tuple[ApprovedGap, ...],
) -> bool:
    """Backward-compatible alias; callers may now pass any approved trusted-data gap."""
    return window_overlaps_gap(start_utc, end_utc, closures)


def expected_minute_opens(
    day_start_utc: datetime,
    day_end_utc: datetime,
    gaps: tuple[ApprovedGap, ...],
) -> tuple[datetime, ...]:
    if day_start_utc.tzinfo != UTC or day_end_utc.tzinfo != UTC:
        raise ValueError("expected minute chronology requires UTC")
    if day_end_utc <= day_start_utc:
        raise ValueError("day end must be after day start")

    output: list[datetime] = []
    cursor = day_start_utc
    while cursor < day_end_utc:
        if not any(gap.start_utc <= cursor < gap.end_utc for gap in gaps):
            output.append(cursor)
        cursor += timedelta(minutes=1)
    return tuple(output)
