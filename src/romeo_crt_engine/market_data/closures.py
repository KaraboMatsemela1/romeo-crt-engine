from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta


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
        if self.start_utc.tzinfo is None or self.end_utc.tzinfo is None:
            raise ValueError("venue closure timestamps must be timezone-aware")
        if self.start_utc.tzinfo != UTC or self.end_utc.tzinfo != UTC:
            raise ValueError("venue closure timestamps must use UTC")
        if self.end_utc <= self.start_utc:
            raise ValueError("venue closure end must be after start")
        if not self.provider or not self.venue or not self.symbol or not self.evidence_id:
            raise ValueError("venue closure identity/evidence fields must not be empty")


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


def exact_gap_is_approved(
    start_utc: datetime,
    end_utc: datetime,
    closures: tuple[VenueClosure, ...],
) -> bool:
    return any(
        start_utc == closure.start_utc and end_utc == closure.end_utc for closure in closures
    )


def window_overlaps_closure(
    start_utc: datetime,
    end_utc: datetime,
    closures: tuple[VenueClosure, ...],
) -> bool:
    return any(start_utc < closure.end_utc and end_utc > closure.start_utc for closure in closures)


def expected_minute_opens(
    day_start_utc: datetime,
    day_end_utc: datetime,
    closures: tuple[VenueClosure, ...],
) -> tuple[datetime, ...]:
    if day_start_utc.tzinfo != UTC or day_end_utc.tzinfo != UTC:
        raise ValueError("expected minute chronology requires UTC")
    if day_end_utc <= day_start_utc:
        raise ValueError("day end must be after day start")

    output: list[datetime] = []
    cursor = day_start_utc
    while cursor < day_end_utc:
        if not any(closure.start_utc <= cursor < closure.end_utc for closure in closures):
            output.append(cursor)
        cursor += timedelta(minutes=1)
    return tuple(output)
