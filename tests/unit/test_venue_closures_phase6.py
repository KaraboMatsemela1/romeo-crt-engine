from __future__ import annotations

import csv
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from hashlib import sha256
from io import BytesIO, StringIO
from zipfile import ZIP_DEFLATED, ZipFile

import pytest

from romeo_crt_engine.backtest.engine import _validate_h1
from romeo_crt_engine.backtest.models import SIMULATOR_VERSION
from romeo_crt_engine.crt.detector import (
    DETECTOR_VERSION,
    DetectorDatasetIdentity,
    DetectorRun,
    DetectorRunStatus,
)
from romeo_crt_engine.crt.v0_1 import STRATEGY_VERSION
from romeo_crt_engine.market_data.aggregate import build_complete_new_york_d1
from romeo_crt_engine.market_data.closures import (
    BINANCE_BTCUSDT_2019_03_12,
    expected_minute_opens,
)
from romeo_crt_engine.market_data.models import BarTimeframe, CanonicalBar
from romeo_crt_engine.market_data.providers.binance_public import (
    PROVIDER,
    VENUE,
    RawArchive,
    parse_1m_archive,
)
from romeo_crt_engine.market_data.quality import DataQualityCode, DataQualityError

SYMBOL = "BTCUSDT"


def _archive_content(opens: tuple[datetime, ...]) -> bytes:
    csv_buffer = StringIO(newline="")
    writer = csv.writer(csv_buffer)
    for open_time in opens:
        open_ms = int(open_time.timestamp() * 1000)
        writer.writerow(
            [
                open_ms,
                "100",
                "101",
                "99",
                "100.5",
                "1",
                open_ms + 59_999,
                "100.5",
                1,
                "0",
                "0",
                "0",
            ]
        )
    payload = csv_buffer.getvalue().encode("utf-8")
    output = BytesIO()
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as zipped:
        zipped.writestr("BTCUSDT-1m-2019-03-12.csv", payload)
    return output.getvalue()


def _raw_archive(opens: tuple[datetime, ...]) -> RawArchive:
    content = _archive_content(opens)
    digest = sha256(content).hexdigest()
    return RawArchive(
        archive_date=BINANCE_BTCUSDT_2019_03_12.start_utc.date(),
        filename="BTCUSDT-1m-2019-03-12.zip",
        source_url="https://example.invalid/BTCUSDT-1m-2019-03-12.zip",
        checksum_url="https://example.invalid/BTCUSDT-1m-2019-03-12.zip.CHECKSUM",
        sha256=digest,
        content=content,
    )


def _h1(open_time: datetime, *, label: str) -> CanonicalBar:
    return CanonicalBar(
        provider=PROVIDER,
        venue=VENUE,
        symbol=SYMBOL,
        timeframe=BarTimeframe.H1,
        open_time=open_time,
        close_time=open_time + timedelta(hours=1),
        open=Decimal("100"),
        high=Decimal("101"),
        low=Decimal("99"),
        close=Decimal("100"),
        volume=Decimal(1),
        quote_volume=Decimal(100),
        trade_count=1,
        source_count=60,
        source_digest=sha256(label.encode("utf-8")).hexdigest(),
    )


def _detector_run() -> DetectorRun:
    identity = DetectorDatasetIdentity(
        dataset_version="phase6-trusted-gap-fixture",
        manifest_sha256="a" * 64,
        normalized_sha256="b" * 64,
        provider=PROVIDER,
        venue=VENUE,
        symbol=SYMBOL,
        tick_size=Decimal("0.01"),
        h1_rows=2,
        d1_rows=0,
        quality_status="TRUSTED",
        schema_version="PHASE3_DATASET_MANIFEST_V1",
    )
    return DetectorRun(
        strategy_version=STRATEGY_VERSION,
        detector_version=DETECTOR_VERSION,
        dataset=identity,
        status=DetectorRunStatus.INSUFFICIENT_D1_HISTORY,
        candidates=(),
        run_sha256="c" * 64,
    )


def test_phase6_simulator_patch_version_is_explicit() -> None:
    assert SIMULATOR_VERSION == "CRT-BACKTEST-v0.1.1"


def test_provider_archive_accepts_only_exact_evidenced_six_hour_closure() -> None:
    day_start = datetime(2019, 3, 12, tzinfo=UTC)
    day_end = day_start + timedelta(days=1)
    expected = expected_minute_opens(
        day_start,
        day_end,
        (BINANCE_BTCUSDT_2019_03_12,),
    )

    bars = parse_1m_archive(_raw_archive(expected), symbol=SYMBOL)

    assert len(bars) == 1_080
    assert bars[119].open_time == datetime(2019, 3, 12, 1, 59, tzinfo=UTC)
    assert bars[120].open_time == datetime(2019, 3, 12, 8, 0, tzinfo=UTC)


def test_same_row_count_with_wrong_missing_interval_fails_closed() -> None:
    day_start = datetime(2019, 3, 12, tzinfo=UTC)
    all_opens = tuple(day_start + timedelta(minutes=index) for index in range(1_440))
    wrong_gap_start = datetime(2019, 3, 12, 8, 0, tzinfo=UTC)
    wrong_gap_end = datetime(2019, 3, 12, 14, 0, tzinfo=UTC)
    wrong_opens = tuple(
        item for item in all_opens if not wrong_gap_start <= item < wrong_gap_end
    )
    assert len(wrong_opens) == 1_080

    with pytest.raises(DataQualityError) as error:
        parse_1m_archive(_raw_archive(wrong_opens), symbol=SYMBOL)

    assert error.value.code is DataQualityCode.INCOMPLETE_BUCKET


def test_closure_affected_new_york_parent_days_are_excluded_not_filled() -> None:
    start = datetime(2019, 3, 10, 5, 0, tzinfo=UTC)
    end = datetime(2019, 3, 14, 4, 0, tzinfo=UTC)
    cursor = start
    bars: list[CanonicalBar] = []
    while cursor < end:
        if not BINANCE_BTCUSDT_2019_03_12.start_utc <= cursor < BINANCE_BTCUSDT_2019_03_12.end_utc:
            bars.append(_h1(cursor, label=cursor.isoformat()))
        cursor += timedelta(hours=1)

    d1 = build_complete_new_york_d1(
        bars,
        allowed_closures=(BINANCE_BTCUSDT_2019_03_12,),
    )

    local_dates = {bar.open_time.astimezone().date() for bar in d1}
    assert len(d1) == 2
    assert d1[0].source_count == 23  # DST-start day, still a complete NY wall-clock day.
    assert d1[1].source_count == 24
    assert d1[0].open_time == datetime(2019, 3, 10, 5, 0, tzinfo=UTC)
    assert d1[1].open_time == datetime(2019, 3, 13, 4, 0, tzinfo=UTC)
    assert local_dates  # keep test explicit that real complete parents remain.


def test_backtester_accepts_forward_gap_after_trusted_data_gate() -> None:
    run = _detector_run()
    bars = (
        _h1(datetime(2019, 3, 12, 1, 0, tzinfo=UTC), label="before"),
        _h1(datetime(2019, 3, 12, 8, 0, tzinfo=UTC), label="after"),
    )

    _validate_h1(bars, run)


def test_backtester_still_rejects_overlapping_h1_events() -> None:
    run = _detector_run()
    bars = (
        _h1(datetime(2019, 3, 12, 1, 0, tzinfo=UTC), label="first"),
        _h1(datetime(2019, 3, 12, 1, 30, tzinfo=UTC), label="overlap"),
    )

    with pytest.raises(ValueError, match="ordered and non-overlapping"):
        _validate_h1(bars, run)
