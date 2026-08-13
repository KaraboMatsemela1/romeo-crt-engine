from __future__ import annotations

import csv
from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from hashlib import sha256
from io import BytesIO, StringIO
from zipfile import ZIP_DEFLATED, ZipFile

from romeo_crt_engine.market_data.closures import archive_exclusion, gap_is_approved
from romeo_crt_engine.market_data.models import AssetClass, InstrumentMetadata
from romeo_crt_engine.market_data.pipeline import build_trusted_binance_dataset
from romeo_crt_engine.market_data.providers.binance_public import PROVIDER, VENUE, RawArchive
from romeo_crt_engine.market_data.verification import (
    CHECKSUM_VERIFICATION_METHOD,
    VerificationPolicy,
    build_provider_verification_evidence,
    checksum_verification_evidence,
    monthly_rest_sample_hashes,
)

SYMBOL = "BTCUSDT"


def _full_day_archive(day: date) -> RawArchive:
    csv_buffer = StringIO(newline="")
    writer = csv.writer(csv_buffer)
    start = datetime.combine(day, datetime.min.time(), tzinfo=UTC)
    for minute in range(1_440):
        open_time = start + timedelta(minutes=minute)
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
    filename = f"BTCUSDT-1m-{day.isoformat()}.zip"
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as zipped:
        zipped.writestr(filename.removesuffix(".zip") + ".csv", payload)
    content = output.getvalue()
    digest = sha256(content).hexdigest()
    return RawArchive(
        archive_date=day,
        filename=filename,
        source_url=f"https://example.invalid/{filename}",
        checksum_url=f"https://example.invalid/{filename}.CHECKSUM",
        sha256=digest,
        content=content,
    )


def _malformed_archive(day: date) -> RawArchive:
    content = b"provider-authenticated-malformed-archive"
    digest = sha256(content).hexdigest()
    filename = f"BTCUSDT-1m-{day.isoformat()}.zip"
    return RawArchive(
        archive_date=day,
        filename=filename,
        source_url=f"https://example.invalid/{filename}",
        checksum_url=f"https://example.invalid/{filename}.CHECKSUM",
        sha256=digest,
        content=content,
    )


def _metadata() -> InstrumentMetadata:
    return InstrumentMetadata(
        provider=PROVIDER,
        venue=VENUE,
        symbol=SYMBOL,
        asset_class=AssetClass.CRYPTO_SPOT,
        price_tick_size=Decimal("0.01"),
        quantity_step=Decimal("0.00001"),
        observed_at=datetime(2026, 8, 13, tzinfo=UTC),
        metadata_version="phase6-exclusion-fixture",
    )


def test_adjacent_archive_exclusions_cover_one_continuous_observed_gap() -> None:
    first = archive_exclusion(
        provider=PROVIDER,
        venue=VENUE,
        symbol=SYMBOL,
        archive_date=date(2021, 1, 2),
        source_sha256="a" * 64,
    )
    second = archive_exclusion(
        provider=PROVIDER,
        venue=VENUE,
        symbol=SYMBOL,
        archive_date=date(2021, 1, 3),
        source_sha256="b" * 64,
    )

    assert gap_is_approved(first.start_utc, second.end_utc, (first, second))


def test_monthly_rest_selection_skips_excluded_first_archive() -> None:
    archives = (
        _full_day_archive(date(2021, 1, 1)),
        _full_day_archive(date(2021, 1, 2)),
        _full_day_archive(date(2021, 2, 1)),
    )

    selected = monthly_rest_sample_hashes(
        archives,
        excluded_source_hashes=frozenset({archives[0].sha256}),
    )

    assert selected == frozenset({archives[1].sha256, archives[2].sha256})


def test_excluded_archive_receives_checksum_evidence_without_parser_or_rest() -> None:
    archive = _malformed_archive(date(2021, 1, 1))

    evidence = build_provider_verification_evidence(
        (archive,),
        symbol=SYMBOL,
        policy=VerificationPolicy.REST_EVERY_ARCHIVE,
        excluded_source_hashes=frozenset({archive.sha256}),
    )

    assert len(evidence) == 1
    assert evidence[0].source_sha256 == archive.sha256
    assert evidence[0].verification_method == CHECKSUM_VERIFICATION_METHOD


def test_pipeline_preserves_excluded_raw_archive_but_never_normalizes_its_minutes() -> None:
    archives = (
        _full_day_archive(date(2022, 1, 1)),
        _malformed_archive(date(2022, 1, 2)),
        _full_day_archive(date(2022, 1, 3)),
        _full_day_archive(date(2022, 1, 4)),
    )
    excluded = frozenset({archives[1].sha256})
    evidence = tuple(checksum_verification_evidence(item, symbol=SYMBOL) for item in archives)

    dataset = build_trusted_binance_dataset(
        archives=archives,
        provider_crosschecks=evidence,
        metadata=_metadata(),
        market_data_code_sha256="c" * 64,
        dependency_lock_sha256="d" * 64,
        git_revision="phase6-fixture",
        created_at=datetime(2026, 8, 13, tzinfo=UTC),
        excluded_source_hashes=excluded,
    )

    assert len(dataset.raw_artifacts) == 4
    assert {item.sha256 for item in dataset.raw_artifacts} == {item.sha256 for item in archives}
    assert len(dataset.minute_bars) == 3 * 1_440
    assert all(item.source_sha256 != archives[1].sha256 for item in dataset.minute_bars)
    assert len(dataset.h1_bars) == 72
    assert len(dataset.d1_bars) == 1
    assert dataset.d1_bars[0].open_time == datetime(2022, 1, 3, 5, 0, tzinfo=UTC)
