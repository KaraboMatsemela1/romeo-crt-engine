from __future__ import annotations

import csv
import json
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from hashlib import sha256
from io import BytesIO, StringIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import pytest

from romeo_crt_engine.market_data.aggregate import build_complete_new_york_d1, build_h1
from romeo_crt_engine.market_data.dataset import write_dataset
from romeo_crt_engine.market_data.models import AssetClass, InstrumentMetadata, MinuteBar
from romeo_crt_engine.market_data.pipeline import build_trusted_binance_dataset
from romeo_crt_engine.market_data.providers.binance_public import (
    PROVIDER,
    VENUE,
    RawArchive,
    daily_checksum_url,
    daily_kline_filename,
    daily_kline_url,
    parse_1m_archive,
    parse_exchange_info,
)
from romeo_crt_engine.market_data.quality import (
    DataQualityCode,
    DataQualityError,
    validate_minute_series,
)

SOURCE_SHA = "a" * 64
LOCK_SHA = "b" * 64


def _metadata(observed_at: datetime) -> InstrumentMetadata:
    return InstrumentMetadata(
        provider=PROVIDER,
        venue=VENUE,
        symbol="BTCUSDT",
        asset_class=AssetClass.CRYPTO_SPOT,
        price_tick_size=Decimal("0.01"),
        quantity_step=Decimal("0.00001"),
        observed_at=observed_at,
        metadata_version="btc-spot-v1",
    )


def _minute_bars(start: datetime, count: int) -> tuple[MinuteBar, ...]:
    output: list[MinuteBar] = []
    for offset in range(count):
        open_time = start + timedelta(minutes=offset)
        price = Decimal(50000) + Decimal(offset) / Decimal(100)
        output.append(
            MinuteBar(
                provider=PROVIDER,
                venue=VENUE,
                symbol="BTCUSDT",
                open_time=open_time,
                close_time=open_time + timedelta(minutes=1),
                open=price,
                high=price + Decimal(1),
                low=price - Decimal(1),
                close=price + Decimal("0.25"),
                volume=Decimal(1),
                quote_volume=Decimal(50000),
                trade_count=10,
                source_sha256=SOURCE_SHA,
            )
        )
    return tuple(output)


def _archive(day: date, *, microseconds: bool) -> RawArchive:
    start = datetime.combine(day, datetime.min.time(), tzinfo=UTC)
    scale = 1_000_000 if microseconds else 1_000
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    for minute in range(1440):
        open_time = start + timedelta(minutes=minute)
        raw_open = int(open_time.timestamp()) * scale
        raw_close = raw_open + (60 * scale) - 1
        price = Decimal(50000) + Decimal(minute) / Decimal(100)
        writer.writerow(
            [
                raw_open,
                format(price, "f"),
                format(price + Decimal(1), "f"),
                format(price - Decimal(1), "f"),
                format(price + Decimal("0.25"), "f"),
                "1.0",
                raw_close,
                "50000.0",
                10,
                "0.5",
                "25000.0",
                0,
            ]
        )

    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, "w", compression=ZIP_DEFLATED) as zipped:
        zipped.writestr(f"BTCUSDT-1m-{day.isoformat()}.csv", buffer.getvalue())
    content = zip_buffer.getvalue()
    digest = sha256(content).hexdigest()
    return RawArchive(
        archive_date=day,
        filename=daily_kline_filename("BTCUSDT", day),
        source_url=daily_kline_url("BTCUSDT", day),
        checksum_url=daily_checksum_url("BTCUSDT", day),
        sha256=digest,
        content=content,
    )


def _dataset(created_at: datetime, metadata_time: datetime | None = None):
    return build_trusted_binance_dataset(
        archives=(
            _archive(date(2025, 9, 17), microseconds=True),
            _archive(date(2025, 9, 18), microseconds=True),
        ),
        metadata=_metadata(metadata_time or created_at),
        code_version="deadbeef",
        dependency_lock_sha256=LOCK_SHA,
        created_at=created_at,
    )


def test_binance_archive_parser_supports_millisecond_and_microsecond_eras() -> None:
    old = parse_1m_archive(_archive(date(2024, 1, 2), microseconds=False), symbol="BTCUSDT")
    new = parse_1m_archive(_archive(date(2025, 1, 2), microseconds=True), symbol="BTCUSDT")

    assert len(old) == 1440
    assert len(new) == 1440
    assert old[0].open_time == datetime(2024, 1, 2, tzinfo=UTC)
    assert new[0].open_time == datetime(2025, 1, 2, tzinfo=UTC)


def test_archive_checksum_mismatch_fails_closed() -> None:
    archive = _archive(date(2025, 1, 2), microseconds=True)
    damaged = RawArchive(
        archive_date=archive.archive_date,
        filename=archive.filename,
        source_url=archive.source_url,
        checksum_url=archive.checksum_url,
        sha256="0" * 64,
        content=archive.content,
    )
    with pytest.raises(DataQualityError) as error:
        parse_1m_archive(damaged, symbol="BTCUSDT")
    assert error.value.code is DataQualityCode.CHECKSUM_MISMATCH


def test_minute_quality_gate_rejects_gap() -> None:
    bars = _minute_bars(datetime(2026, 1, 1, tzinfo=UTC), 120)
    damaged = bars[:30] + bars[31:]
    with pytest.raises(DataQualityError) as error:
        validate_minute_series(damaged)
    assert error.value.code is DataQualityCode.GAP


def test_spring_dst_new_york_day_contains_23_elapsed_h1_bars() -> None:
    bars = _minute_bars(datetime(2026, 3, 8, 5, 0, tzinfo=UTC), 23 * 60)
    h1 = build_h1(bars)
    d1 = build_complete_new_york_d1(h1)

    assert len(h1) == 23
    assert len(d1) == 1
    assert d1[0].close_time.timestamp() - d1[0].open_time.timestamp() == 23 * 3600
    assert d1[0].source_count == 23


def test_fall_dst_new_york_day_contains_25_elapsed_h1_bars() -> None:
    bars = _minute_bars(datetime(2026, 11, 1, 4, 0, tzinfo=UTC), 25 * 60)
    h1 = build_h1(bars)
    d1 = build_complete_new_york_d1(h1)

    assert len(h1) == 25
    assert len(d1) == 1
    assert d1[0].close_time.timestamp() - d1[0].open_time.timestamp() == 25 * 3600
    assert d1[0].source_count == 25


def test_exchange_info_captures_tick_and_quantity_step_snapshot() -> None:
    observed_at = datetime(2026, 8, 12, tzinfo=UTC)
    payload = json.dumps(
        {
            "symbols": [
                {
                    "symbol": "BTCUSDT",
                    "filters": [
                        {"filterType": "PRICE_FILTER", "tickSize": "0.01000000"},
                        {"filterType": "LOT_SIZE", "stepSize": "0.00001000"},
                    ],
                }
            ]
        }
    ).encode()
    metadata = parse_exchange_info(payload, symbol="BTCUSDT", observed_at=observed_at)

    assert metadata.price_tick_size == Decimal("0.01000000")
    assert metadata.quantity_step == Decimal("0.00001000")
    assert metadata.temporal_semantics == "SNAPSHOT_AT_INGESTION"


def test_two_utc_daily_archives_reproduce_one_complete_new_york_day() -> None:
    dataset = _dataset(datetime(2025, 9, 20, tzinfo=UTC))

    assert len(dataset.minute_bars) == 2880
    assert len(dataset.h1_bars) == 48
    assert len(dataset.d1_bars) == 1
    assert dataset.d1_bars[0].open_time == datetime(2025, 9, 17, 4, 0, tzinfo=UTC)
    assert dataset.d1_bars[0].close_time == datetime(2025, 9, 18, 4, 0, tzinfo=UTC)
    assert dataset.manifest.quality_status == "TRUSTED"
    assert dataset.manifest.m1_rows == 2880
    assert len(dataset.manifest.dataset_version) == 24


def test_dataset_manifest_is_stable_across_ingestion_timestamp_only() -> None:
    metadata_time = datetime(2025, 9, 19, tzinfo=UTC)
    archives = (
        _archive(date(2025, 9, 17), microseconds=True),
        _archive(date(2025, 9, 18), microseconds=True),
    )
    first = build_trusted_binance_dataset(
        archives=archives,
        metadata=_metadata(metadata_time),
        code_version="deadbeef",
        dependency_lock_sha256=LOCK_SHA,
        created_at=datetime(2025, 9, 20, tzinfo=UTC),
    )
    second = build_trusted_binance_dataset(
        archives=archives,
        metadata=_metadata(metadata_time),
        code_version="deadbeef",
        dependency_lock_sha256=LOCK_SHA,
        created_at=datetime(2025, 9, 21, tzinfo=UTC),
    )

    assert first.manifest.dataset_version == second.manifest.dataset_version
    assert first.manifest.normalized_sha256 == second.manifest.normalized_sha256
    assert first.manifest.manifest_sha256 == second.manifest.manifest_sha256


def test_metadata_snapshot_time_changes_dataset_identity() -> None:
    first = _dataset(
        datetime(2025, 9, 20, tzinfo=UTC),
        metadata_time=datetime(2025, 9, 19, tzinfo=UTC),
    )
    second = _dataset(
        datetime(2025, 9, 20, tzinfo=UTC),
        metadata_time=datetime(2025, 9, 20, tzinfo=UTC),
    )
    assert first.manifest.dataset_version != second.manifest.dataset_version


def test_dataset_writer_is_idempotent_for_identical_version(tmp_path: Path) -> None:
    dataset = _dataset(datetime(2025, 9, 20, tzinfo=UTC))
    first = write_dataset(
        root=tmp_path,
        raw_artifacts=dataset.raw_artifacts,
        h1=dataset.h1_bars,
        d1=dataset.d1_bars,
        manifest=dataset.manifest,
    )
    second = write_dataset(
        root=tmp_path,
        raw_artifacts=dataset.raw_artifacts,
        h1=dataset.h1_bars,
        d1=dataset.d1_bars,
        manifest=dataset.manifest,
    )

    assert first == second
    assert (first / "manifest.json").read_text(encoding="utf-8") == dataset.manifest.to_json()
