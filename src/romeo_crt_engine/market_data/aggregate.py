from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal
from hashlib import sha256
from zoneinfo import ZoneInfo

from romeo_crt_engine.market_data.models import BarTimeframe, CanonicalBar, MinuteBar
from romeo_crt_engine.market_data.quality import DataQualityCode, DataQualityError, validate_minute_series

NY = ZoneInfo("America/New_York")


def _minute_digest(bars: Sequence[MinuteBar]) -> str:
    digest = sha256()
    for bar in bars:
        digest.update(bar.source_sha256.encode("ascii"))
        digest.update(str(int(bar.open_time.timestamp())).encode("ascii"))
    return digest.hexdigest()


def _canonical_digest(bars: Sequence[CanonicalBar]) -> str:
    digest = sha256()
    for bar in bars:
        digest.update(bar.source_digest.encode("ascii"))
        digest.update(str(int(bar.open_time.timestamp())).encode("ascii"))
    return digest.hexdigest()


def _sum_decimal(values: Sequence[Decimal]) -> Decimal:
    return sum(values, start=Decimal("0"))


def build_h1(minute_bars: Sequence[MinuteBar]) -> tuple[CanonicalBar, ...]:
    """Aggregate gapless UTC M1 observations into exact elapsed-hour H1 bars."""
    validate_minute_series(minute_bars)

    buckets: dict[int, list[MinuteBar]] = defaultdict(list)
    for bar in minute_bars:
        bucket_epoch = (int(bar.open_time.timestamp()) // 3600) * 3600
        buckets[bucket_epoch].append(bar)

    output: list[CanonicalBar] = []
    for bucket_epoch in sorted(buckets):
        members = buckets[bucket_epoch]
        if len(members) != 60:
            raise DataQualityError(
                DataQualityCode.INCOMPLETE_BUCKET,
                f"H1 bucket {bucket_epoch} contains {len(members)} minutes, expected 60",
            )
        if int(members[0].open_time.timestamp()) != bucket_epoch:
            raise DataQualityError(
                DataQualityCode.INCOMPLETE_BUCKET,
                f"H1 bucket {bucket_epoch} does not begin on its hour boundary",
            )
        if int(members[-1].close_time.timestamp()) != bucket_epoch + 3600:
            raise DataQualityError(
                DataQualityCode.INCOMPLETE_BUCKET,
                f"H1 bucket {bucket_epoch} does not end on its hour boundary",
            )

        output.append(
            CanonicalBar(
                provider=members[0].provider,
                venue=members[0].venue,
                symbol=members[0].symbol,
                timeframe=BarTimeframe.H1,
                open_time=datetime.fromtimestamp(bucket_epoch, UTC),
                close_time=datetime.fromtimestamp(bucket_epoch + 3600, UTC),
                open=members[0].open,
                high=max(member.high for member in members),
                low=min(member.low for member in members),
                close=members[-1].close,
                volume=_sum_decimal([member.volume for member in members]),
                quote_volume=_sum_decimal([member.quote_volume for member in members]),
                trade_count=sum(member.trade_count for member in members),
                source_count=len(members),
                source_digest=_minute_digest(members),
            )
        )

    return tuple(output)


def _ny_midnight(day: date) -> datetime:
    return datetime.combine(day, time.min, tzinfo=NY)


def _validate_h1_series(bars: Sequence[CanonicalBar]) -> None:
    if not bars:
        raise DataQualityError(DataQualityCode.EMPTY, "H1 series must not be empty")
    identity = (bars[0].provider, bars[0].venue, bars[0].symbol)
    prior_close: float | None = None
    for bar in bars:
        if bar.timeframe is not BarTimeframe.H1:
            raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "expected only H1 bars")
        if (bar.provider, bar.venue, bar.symbol) != identity:
            raise DataQualityError(DataQualityCode.IDENTITY_MISMATCH, "H1 identity mismatch")
        open_ts = bar.open_time.timestamp()
        close_ts = bar.close_time.timestamp()
        if close_ts - open_ts != 3600.0:
            raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "H1 must span 3600 seconds")
        if prior_close is not None and open_ts != prior_close:
            raise DataQualityError(DataQualityCode.GAP, "H1 series is not contiguous")
        prior_close = close_ts


def build_complete_new_york_d1(
    h1_bars: Sequence[CanonicalBar],
) -> tuple[CanonicalBar, ...]:
    """Build only complete New-York wall-clock days; partial edge days are discarded."""
    _validate_h1_series(h1_bars)

    by_day: dict[date, list[CanonicalBar]] = defaultdict(list)
    for bar in h1_bars:
        by_day[bar.open_time.astimezone(NY).date()].append(bar)

    ordered_days = sorted(by_day)
    output: list[CanonicalBar] = []

    for index, day in enumerate(ordered_days):
        members = by_day[day]
        local_open = _ny_midnight(day)
        local_close = _ny_midnight(day + timedelta(days=1))
        expected_open = local_open.timestamp()
        expected_close = local_close.timestamp()
        expected_hours = int((expected_close - expected_open) / 3600)

        is_complete = (
            len(members) == expected_hours
            and members[0].open_time.timestamp() == expected_open
            and members[-1].close_time.timestamp() == expected_close
        )

        if not is_complete:
            if index in (0, len(ordered_days) - 1):
                continue
            raise DataQualityError(
                DataQualityCode.INCOMPLETE_BUCKET,
                f"interior New-York day {day.isoformat()} is incomplete",
            )

        output.append(
            CanonicalBar(
                provider=members[0].provider,
                venue=members[0].venue,
                symbol=members[0].symbol,
                timeframe=BarTimeframe.D1,
                open_time=datetime.fromtimestamp(int(expected_open), UTC),
                close_time=datetime.fromtimestamp(int(expected_close), UTC),
                open=members[0].open,
                high=max(member.high for member in members),
                low=min(member.low for member in members),
                close=members[-1].close,
                volume=_sum_decimal([member.volume for member in members]),
                quote_volume=_sum_decimal([member.quote_volume for member in members]),
                trade_count=sum(member.trade_count for member in members),
                source_count=len(members),
                source_digest=_canonical_digest(members),
            )
        )

    if not output:
        raise DataQualityError(
            DataQualityCode.INCOMPLETE_BUCKET,
            "input coverage contains no complete New-York Daily candle",
        )
    return tuple(output)
