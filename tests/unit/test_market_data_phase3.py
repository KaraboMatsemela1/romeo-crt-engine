from __future__ import annotations

import csv
import json
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from hashlib import sha256
from io import BytesIO, StringIO
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import pytest

from romeo_crt_engine.market_data.aggregate import build_complete_new_york_d1, build_h1
from romeo_crt_engine.market_data.dataset import write_dataset
from romeo_crt_engine.market_data.models import (
    AssetClass,
    InstrumentMetadata,
    MinuteBar,
    ProviderVerificationEvidence,
)
from romeo_crt_engine.market_data.pipeline import TrustedDataset, build_trusted_binance_dataset
from romeo_crt_engine.market_data.providers.binance_public import (
    MARKET_DATA_API_BASE_URL,
    PROVIDER,
    REST_VERIFICATION_METHOD,
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
CODE_SHA = "c" * 64
GIT_REVISION = "deadbeef"


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
    member = ZipInfo(
        filename=f"BTCUSDT-1m-{day.isoformat()}.csv",
        date_time=(2020, 1, 1, 0, 0, 0),
    )
    member.compress_type = ZIP_DEFLATED
    with ZipFile(zip_buffer, "w") as zipped:
        zipped.writestr(member, buffer.getvalue())
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


def _crosschecks(
    archives: tuple[RawArchive, ...],
) -> tuple[ProviderVerificationEvidence, ...]:
    return tuple(
        ProviderVerificationEvidence(
            provider=PROVIDER,
            venue=VENUE,
            symbol="BTCUSDT",
            source_sha256=archive.sha256,
            sample_refs=(
                f"{archive.archive_date.isoformat()}T00:00:00+00:00",
                f"{archive.archive_date.isoformat()}T12:00:00+00:00",
                f"{archive.archive_date.isoformat()}T23:59:00+00:00",
            ),
            endpoint_base=MARKET_DATA_API_BASE_URL,
            verification_method=REST_VERIFICATION_METHOD,
        )
        for archive in archives
    )


def _dataset(created_at: datetime, metadata_time: datetime | None = None) -> TrustedDataset:
    archives = (
        _archive(date(2025, 9, 17), microseconds=True),
        _archive(date(2025, 9, 18), microseconds=True),
    )
    return build_trusted_binance_dataset(
        archives=archives,
        provider_crosschecks=_crosschecks(archives),
        metadata=_metadata(metadata_time or created_at),
        market_data_code_sha256=CODE_SHA,
        dependency_lock_sha256=LOCK_SHA,
        git_revision=GIT_REVISION,
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


def test_minute_quality_gate_rejects_gap_duplicate_order_and_future() -> None:
    bars = _minute_bars(datetime(2026, 1, 1, tzinfo=UTC), 120)

    with pytest.raises(DataQualityError) as gap:
        validate_minute_series(bars[:30] + bars[31:])
    assert gap.value.code is DataQualityCode.GAP

    with pytest.raises(DataQualityError) as duplicate:
        validate_minute_series(bars[:30] + (bars[29],) + bars[30:])
    assert duplicate.value.code is DataQualityCode.DUPLICATE_TIMESTAMP

    with pytest.raises(DataQualityError) as order:
        validate_minute_series((bars[0], bars[1], bars[0]))
    assert order.value.code is DataQualityCode.OUT_OF_ORDER

    with pytest.raises(DataQualityError) as future:
        validate_minute_series(bars, as_of=bars[-1].open_time)
    assert future.value.code is DataQualityCode.FUTURE_TIMESTAMP


def test_minute_bar_rejects_impossible_ohlc() -> None:
    with pytest.raises(ValueError, match="high must contain"):
        MinuteBar(
            provider=PROVIDER,
            venue=VENUE,
            symbol="BTCUSDT",
            open_time=datetime(2026, 1, 1, tzinfo=UTC),
            close_time=datetime(2026, 1, 1, 0, 1, tzinfo=UTC),
            open=Decimal(100),
            high=Decimal(99),
            low=Decimal(90),
            close=Decimal(95),
            volume=Decimal(1),
            quote_volume=Decimal(100),
            trade_count=1,
            source_sha256=SOURCE_SHA,
        )


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


def test_trusted_promotion_rejects_missing_provider_crosscheck() -> None:
    created_at = datetime(2025, 9, 20, tzinfo=UTC)
    archives = (
        _archive(date(2025, 9, 17), microseconds=True),
        _archive(date(2025, 9, 18), microseconds=True),
    )
    with pytest.raises(ValueError, match="provider cross-check"):
        build_trusted_binance_dataset(
            archives=archives,
            provider_crosschecks=(),
            metadata=_metadata(created_at),
            market_data_code_sha256=CODE_SHA,
            dependency_lock_sha256=LOCK_SHA,
            git_revision=GIT_REVISION,
            created_at=created_at,
        )


def test_two_utc_daily_archives_reproduce_one_complete_new_york_day() -> None:
    dataset = _dataset(datetime(2025, 9, 20, tzinfo=UTC))

    assert len(dataset.minute_bars) == 2880
    assert len(dataset.h1_bars) == 48
    assert len(dataset.d1_bars) == 1
    assert dataset.d1_bars[0].open_time == datetime(2025, 9, 17, 4, 0, tzinfo=UTC)
    assert dataset.d1_bars[0].close_time == datetime(2025, 9, 18, 4, 0, tzinfo=UTC)
    assert dataset.manifest.quality_status == "TRUSTED"
    assert dataset.manifest.m1_rows == 2880
    assert len(dataset.manifest.provider_crosschecks) == 2
    assert len(dataset.manifest.dataset_version) == 24
    assert dataset.receipt.to_dataset_ref().version == dataset.manifest.dataset_version


def test_dataset_manifest_is_stable_across_ingestion_timestamp_only() -> None:
    metadata_time = datetime(2025, 9, 19, tzinfo=UTC)
    archives = (
        _archive(date(2025, 9, 17), microseconds=True),
        _archive(date(2025, 9, 18), microseconds=True),
    )
    crosschecks = _crosschecks(archives)
    first = build_trusted_binance_dataset(
        archives=archives,
        provider_crosschecks=crosschecks,
        metadata=_metadata(metadata_time),
        market_data_code_sha256=CODE_SHA,
        dependency_lock_sha256=LOCK_SHA,
        git_revision=GIT_REVISION,
        created_at=datetime(2025, 9, 20, tzinfo=UTC),
    )
    second = build_trusted_binance_dataset(
        archives=archives,
        provider_crosschecks=crosschecks,
        metadata=_metadata(metadata_time),
        market_data_code_sha256=CODE_SHA,
        dependency_lock_sha256=LOCK_SHA,
        git_revision=GIT_REVISION,
        created_at=datetime(2025, 9, 21, tzinfo=UTC),
    )

    assert first.manifest.dataset_version == second.manifest.dataset_version
    assert first.manifest.normalized_sha256 == second.manifest.normalized_sha256
    assert first.manifest.manifest_sha256 == second.manifest.manifest_sha256
    assert first.receipt.receipt_sha256 != second.receipt.receipt_sha256


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


def test_market_data_code_change_changes_dataset_identity() -> None:
    created_at = datetime(2025, 9, 20, tzinfo=UTC)
    archives = (
        _archive(date(2025, 9, 17), microseconds=True),
        _archive(date(2025, 9, 18), microseconds=True),
    )
    kwargs = {
        "archives": archives,
        "provider_crosschecks": _crosschecks(archives),
        "metadata": _metadata(created_at),
        "dependency_lock_sha256": LOCK_SHA,
        "git_revision": GIT_REVISION,
        "created_at": created_at,
    }
    first = build_trusted_binance_dataset(
        market_data_code_sha256=CODE_SHA,
        **kwargs,
    )
    second = build_trusted_binance_dataset(
        market_data_code_sha256="d" * 64,
        **kwargs,
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
        receipt=dataset.receipt,
    )
    second = write_dataset(
        root=tmp_path,
        raw_artifacts=dataset.raw_artifacts,
        h1=dataset.h1_bars,
        d1=dataset.d1_bars,
        manifest=dataset.manifest,
        receipt=dataset.receipt,
    )

    assert first == second
    assert (first / "manifest.json").read_text(encoding="utf-8") == dataset.manifest.to_json()
    receipt_path = (
        tmp_path
        / "receipts"
        / dataset.manifest.dataset_version
        / f"{dataset.receipt.receipt_sha256}.json"
    )
    assert receipt_path.exists()
