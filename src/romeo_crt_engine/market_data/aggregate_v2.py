from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from hashlib import sha256
from zoneinfo import ZoneInfo

from romeo_crt_engine.market_data.models import BarTimeframe
from romeo_crt_engine.market_data.price_data_v2 import (
    ActivityMeasure,
    ActivitySemantic,
    CanonicalPriceBarV2,
)
from romeo_crt_engine.market_data.session_policy_v2 import (
    MarketGapV2,
    minute_is_expected,
    validate_gap_policy,
)

NEW_YORK = ZoneInfo("America/New_York")


def _validate_m1_identity(bars: tuple[CanonicalPriceBarV2, ...]) -> None:
    if not bars:
        raise ValueError("price aggregation requires M1 observations")
    first = bars[0]
    if first.timeframe is not BarTimeframe.M1:
        raise ValueError("price aggregation input must be M1")
    identity = (
        first.provider,
        first.venue,
        first.instrument,
        first.price_component,
        first.session_policy_version,
    )
    previous_open: datetime | None = None
    for bar in bars:
        if bar.timeframe is not BarTimeframe.M1:
            raise ValueError("price aggregation input must contain only M1 bars")
        if (
            bar.provider,
            bar.venue,
            bar.instrument,
            bar.price_component,
            bar.session_policy_version,
        ) != identity:
            raise ValueError("M1 observations must share one provider/instrument/component/policy")
        if previous_open is not None and bar.open_time <= previous_open:
            raise ValueError("M1 observations must be strictly ordered and unique")
        previous_open = bar.open_time


def _expected_minute_opens(
    start: datetime,
    end: datetime,
    gaps: tuple[MarketGapV2, ...],
) -> tuple[datetime, ...]:
    if start.utcoffset() != timedelta(0) or end.utcoffset() != timedelta(0):
        raise ValueError("aggregation windows must be UTC")
    if end <= start:
        raise ValueError("aggregation end must be after start")
    current = start
    expected: list[datetime] = []
    while current < end:
        if minute_is_expected(current, gaps):
            expected.append(current)
        current += timedelta(minutes=1)
    return tuple(expected)


def _window_bars(
    by_open: dict[datetime, CanonicalPriceBarV2],
    *,
    start: datetime,
    end: datetime,
    expected_opens: tuple[datetime, ...],
) -> tuple[CanonicalPriceBarV2, ...]:
    expected = set(expected_opens)
    actual = {timestamp for timestamp in by_open if start <= timestamp < end}
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    if missing or unexpected:
        missing_preview = ",".join(value.isoformat() for value in missing[:3])
        unexpected_preview = ",".join(value.isoformat() for value in unexpected[:3])
        raise ValueError(
            "price window does not match expected tradable observations: "
            f"missing={len(missing)}[{missing_preview}] "
            f"unexpected={len(unexpected)}[{unexpected_preview}]"
        )
    return tuple(by_open[timestamp] for timestamp in expected_opens)


def _activity_map(bar: CanonicalPriceBarV2) -> dict[ActivitySemantic, Decimal]:
    return {measure.semantic: measure.value for measure in bar.activity}


def _aggregate_activity(
    bars: tuple[CanonicalPriceBarV2, ...],
) -> tuple[ActivityMeasure, ...]:
    if not bars:
        return ()
    maps = [_activity_map(bar) for bar in bars]
    common = set(maps[0])
    for values in maps[1:]:
        common.intersection_update(values)
    return tuple(
        ActivityMeasure(
            semantic=semantic,
            value=sum((values[semantic] for values in maps), Decimal(0)),
        )
        for semantic in sorted(common, key=lambda item: item.value)
    )


def _source_digest(
    bars: tuple[CanonicalPriceBarV2, ...],
    *,
    timeframe: BarTimeframe,
    start: datetime,
    end: datetime,
) -> str:
    digest = sha256()
    digest.update(timeframe.value.encode())
    digest.update(b"\0")
    digest.update(start.isoformat().encode())
    digest.update(b"\0")
    digest.update(end.isoformat().encode())
    digest.update(b"\0")
    for bar in bars:
        digest.update(bar.open_time.isoformat().encode())
        digest.update(b"|")
        digest.update(bar.source_digest.encode())
        digest.update(b"\n")
    return digest.hexdigest()


def _aggregate_price_window(
    bars: tuple[CanonicalPriceBarV2, ...],
    *,
    timeframe: BarTimeframe,
    start: datetime,
    end: datetime,
) -> CanonicalPriceBarV2:
    if not bars:
        raise ValueError("cannot aggregate an empty tradable price window")
    first = bars[0]
    return CanonicalPriceBarV2(
        provider=first.provider,
        venue=first.venue,
        instrument=first.instrument,
        price_component=first.price_component,
        timeframe=timeframe,
        open_time=start,
        close_time=end,
        open=bars[0].open,
        high=max(bar.high for bar in bars),
        low=min(bar.low for bar in bars),
        close=bars[-1].close,
        source_count=sum(bar.source_count for bar in bars),
        source_digest=_source_digest(bars, timeframe=timeframe, start=start, end=end),
        session_policy_version=first.session_policy_version,
        activity=_aggregate_activity(bars),
    )


def _validate_gaps_for_bars(
    bars: tuple[CanonicalPriceBarV2, ...],
    gaps: tuple[MarketGapV2, ...],
) -> None:
    first = bars[0]
    validate_gap_policy(
        gaps,
        provider=first.provider,
        venue=first.venue,
        instrument=first.instrument,
        policy_version=first.session_policy_version,
    )


def build_h1_price_bars_v2(
    m1: tuple[CanonicalPriceBarV2, ...],
    *,
    coverage_start: datetime,
    coverage_end: datetime,
    gaps: tuple[MarketGapV2, ...] = (),
) -> tuple[CanonicalPriceBarV2, ...]:
    """Build H1 bars against an explicit expected-trading-minute policy.

    A known partial-hour closure may produce an H1 bar from fewer than 60 M1
    observations, but only when every absent minute is covered by the frozen
    approved gap policy. Fully closed hours produce no H1 bar.
    """

    _validate_m1_identity(m1)
    _validate_gaps_for_bars(m1, gaps)
    if coverage_start.utcoffset() != timedelta(0) or coverage_end.utcoffset() != timedelta(0):
        raise ValueError("H1 coverage boundaries must be UTC")
    if coverage_start.minute or coverage_start.second or coverage_start.microsecond:
        raise ValueError("H1 coverage_start must be hour-aligned")
    if coverage_end.minute or coverage_end.second or coverage_end.microsecond:
        raise ValueError("H1 coverage_end must be hour-aligned")
    if coverage_end <= coverage_start:
        raise ValueError("H1 coverage_end must be after coverage_start")
    if any(bar.open_time < coverage_start or bar.close_time > coverage_end for bar in m1):
        raise ValueError("M1 observation lies outside declared H1 coverage")

    by_open = {bar.open_time: bar for bar in m1}
    output: list[CanonicalPriceBarV2] = []
    start = coverage_start
    while start < coverage_end:
        end = start + timedelta(hours=1)
        expected = _expected_minute_opens(start, end, gaps)
        bars = _window_bars(by_open, start=start, end=end, expected_opens=expected)
        if bars:
            output.append(
                _aggregate_price_window(
                    bars,
                    timeframe=BarTimeframe.H1,
                    start=start,
                    end=end,
                )
            )
        start = end
    return tuple(output)


def build_new_york_d1_price_bars_v2(
    m1: tuple[CanonicalPriceBarV2, ...],
    *,
    eligible_local_dates: Iterable[date],
    gaps: tuple[MarketGapV2, ...] = (),
) -> tuple[CanonicalPriceBarV2, ...]:
    """Build strategy-calendar D1 bars for explicitly eligible New-York dates.

    Date eligibility is intentionally supplied by the versioned session policy;
    this function does not guess whether weekends/holidays should create a CRT
    Daily candle. Within each eligible date, every absent minute must be covered
    by an approved expected gap.
    """

    _validate_m1_identity(m1)
    _validate_gaps_for_bars(m1, gaps)
    by_open = {bar.open_time: bar for bar in m1}
    output: list[CanonicalPriceBarV2] = []
    previous_date: date | None = None

    for local_date in eligible_local_dates:
        if previous_date is not None and local_date <= previous_date:
            raise ValueError("eligible_local_dates must be strictly increasing and unique")
        previous_date = local_date
        local_start = datetime.combine(local_date, time.min, tzinfo=NEW_YORK)
        local_end = datetime.combine(local_date + timedelta(days=1), time.min, tzinfo=NEW_YORK)
        start = local_start.astimezone(UTC)
        end = local_end.astimezone(UTC)
        expected = _expected_minute_opens(start, end, gaps)
        bars = _window_bars(by_open, start=start, end=end, expected_opens=expected)
        if not bars:
            raise ValueError(f"eligible D1 date has no expected tradable observations: {local_date}")
        output.append(
            _aggregate_price_window(
                bars,
                timeframe=BarTimeframe.D1,
                start=start,
                end=end,
            )
        )
    return tuple(output)
