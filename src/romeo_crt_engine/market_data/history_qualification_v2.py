from __future__ import annotations

import gzip
import json
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from pathlib import Path
from typing import Final

from romeo_crt_engine.market_data.providers.oanda_v20 import OandaPriceCandle

HISTORY_QUALIFICATION_SCHEMA_VERSION: Final = "P6B_OANDA_HISTORY_QUALIFICATION_V1"
DEV_START_UTC: Final = datetime(2019, 1, 1, tzinfo=UTC)
DEV_END_UTC: Final = datetime(2023, 1, 1, tzinfo=UTC)

# Frozen before provider-backed DEV activity access. All windows are ordinary
# weekdays and are used only to compare provider values from an independent
# second request against the primary retrieval.
REFETCH_WINDOWS_UTC: Final = (
    (datetime(2019, 3, 12, 14, 0, tzinfo=UTC), datetime(2019, 3, 12, 15, 0, tzinfo=UTC)),
    (datetime(2020, 9, 15, 14, 0, tzinfo=UTC), datetime(2020, 9, 15, 15, 0, tzinfo=UTC)),
    (datetime(2021, 4, 13, 14, 0, tzinfo=UTC), datetime(2021, 4, 13, 15, 0, tzinfo=UTC)),
    (datetime(2022, 10, 18, 14, 0, tzinfo=UTC), datetime(2022, 10, 18, 15, 0, tzinfo=UTC)),
)


@dataclass(frozen=True, slots=True)
class MissingInterval:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.start.utcoffset() != timedelta(0) or self.end.utcoffset() != timedelta(0):
            raise ValueError("missing interval timestamps must be UTC")
        if self.end <= self.start:
            raise ValueError("missing interval end must be after start")
        if self.start.second or self.start.microsecond or self.end.second or self.end.microsecond:
            raise ValueError("missing intervals must be minute-aligned")

    @property
    def missing_minutes(self) -> int:
        return int((self.end - self.start).total_seconds() // 60)


def candle_value_record(candle: OandaPriceCandle) -> dict[str, object]:
    """Canonical provider-value record, deliberately excluding page-response hashes."""

    return {
        "instrument": candle.instrument,
        "price_component": candle.price_component,
        "open_time_utc": candle.open_time.astimezone(UTC).isoformat(),
        "close_time_utc": candle.close_time.astimezone(UTC).isoformat(),
        "open": format(candle.open, "f"),
        "high": format(candle.high, "f"),
        "low": format(candle.low, "f"),
        "close": format(candle.close, "f"),
        "price_count": candle.price_count,
        "complete": candle.complete,
    }


def normalized_m1_sha256(candles: Sequence[OandaPriceCandle]) -> str:
    digest = sha256()
    digest.update(b"P6B_OANDA_M1_VALUE_STREAM_V1\n")
    for candle in candles:
        record = json.dumps(
            candle_value_record(candle),
            sort_keys=True,
            separators=(",", ":"),
        )
        digest.update(record.encode())
        digest.update(b"\n")
    return digest.hexdigest()


def enumerate_missing_intervals(
    candles: Sequence[OandaPriceCandle],
    *,
    requested_start: datetime,
    requested_end: datetime,
) -> tuple[MissingInterval, ...]:
    if requested_start.utcoffset() is None or requested_end.utcoffset() is None:
        raise ValueError("requested history boundaries must be timezone-aware")
    start = requested_start.astimezone(UTC)
    end = requested_end.astimezone(UTC)
    if end <= start:
        raise ValueError("requested history end must be after start")
    if not candles:
        return (MissingInterval(start=start, end=end),)

    missing: list[MissingInterval] = []
    cursor = start
    previous_open: datetime | None = None

    for candle in candles:
        if candle.open_time < start or candle.close_time > end:
            raise ValueError("candle lies outside requested history interval")
        if previous_open is not None and candle.open_time <= previous_open:
            raise ValueError("history candles must be strictly ordered and unique")
        if candle.open_time < cursor:
            raise ValueError("history candles overlap")
        if candle.open_time > cursor:
            missing.append(MissingInterval(start=cursor, end=candle.open_time))
        cursor = candle.close_time
        previous_open = candle.open_time

    if cursor < end:
        missing.append(MissingInterval(start=cursor, end=end))
    return tuple(missing)


def gap_digest(intervals: Sequence[MissingInterval]) -> str:
    digest = sha256()
    digest.update(b"P6B_OANDA_MISSING_INTERVALS_V1\n")
    for interval in intervals:
        digest.update(interval.start.isoformat().encode())
        digest.update(b"|")
        digest.update(interval.end.isoformat().encode())
        digest.update(b"|")
        digest.update(str(interval.missing_minutes).encode())
        digest.update(b"\n")
    return digest.hexdigest()


def values_for_window(
    candles: Sequence[OandaPriceCandle],
    *,
    start: datetime,
    end: datetime,
) -> tuple[dict[str, object], ...]:
    start_utc = start.astimezone(UTC)
    end_utc = end.astimezone(UTC)
    return tuple(
        candle_value_record(candle)
        for candle in candles
        if start_utc <= candle.open_time < end_utc
    )


def assert_refetch_equal(
    primary: Sequence[OandaPriceCandle],
    refetched: Sequence[OandaPriceCandle],
    *,
    start: datetime,
    end: datetime,
) -> str:
    primary_values = values_for_window(primary, start=start, end=end)
    refetch_values = values_for_window(refetched, start=start, end=end)
    if not primary_values:
        raise ValueError("frozen re-fetch window contains no primary provider observations")
    if primary_values != refetch_values:
        raise ValueError("independent OANDA re-fetch does not match the primary retrieval")
    payload = json.dumps(primary_values, sort_keys=True, separators=(",", ":")).encode()
    return sha256(payload).hexdigest()


def write_m1_jsonl_gz(path: Path, candles: Sequence[OandaPriceCandle]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    digest = sha256()
    with gzip.open(path, "wt", encoding="utf-8", newline="\n") as handle:
        for candle in candles:
            line = json.dumps(
                candle_value_record(candle),
                sort_keys=True,
                separators=(",", ":"),
            )
            handle.write(line)
            handle.write("\n")
            digest.update(line.encode())
            digest.update(b"\n")
    return digest.hexdigest()


def missing_interval_record(interval: MissingInterval) -> dict[str, object]:
    return {
        "start_utc": interval.start.isoformat(),
        "end_utc": interval.end.isoformat(),
        "missing_minutes": interval.missing_minutes,
        "classification": "UNRECONCILED",
    }
