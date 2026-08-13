from __future__ import annotations

from datetime import date
from hashlib import sha256

import pytest

from romeo_crt_engine.market_data.models import ProviderVerificationEvidence
from romeo_crt_engine.market_data.providers.binance_public import (
    ARCHIVE_BASE_URL,
    MARKET_DATA_API_BASE_URL,
    PROVIDER,
    REST_VERIFICATION_METHOD,
    VENUE,
    RawArchive,
)
from romeo_crt_engine.market_data.verification import (
    CHECKSUM_VERIFICATION_METHOD,
    VerificationPolicy,
    build_provider_verification_evidence,
    checksum_verification_evidence,
    monthly_rest_sample_hashes,
)


def _archive(day: date) -> RawArchive:
    digest = sha256(day.isoformat().encode("utf-8")).hexdigest()
    filename = f"BTCUSDT-1m-{day.isoformat()}.zip"
    return RawArchive(
        archive_date=day,
        filename=filename,
        source_url=f"{ARCHIVE_BASE_URL}/{filename}",
        checksum_url=f"{ARCHIVE_BASE_URL}/{filename}.CHECKSUM",
        sha256=digest,
        content=b"not-used-by-verification-policy-tests",
    )


def test_monthly_rest_sampling_selects_first_available_archive_per_month() -> None:
    archives = (
        _archive(date(2020, 1, 2)),
        _archive(date(2020, 1, 4)),
        _archive(date(2020, 2, 5)),
        _archive(date(2020, 2, 6)),
    )

    selected = monthly_rest_sample_hashes(archives)

    assert selected == frozenset({archives[0].sha256, archives[2].sha256})


def test_checksum_evidence_records_provider_checksum_contract() -> None:
    archive = _archive(date(2020, 1, 2))

    evidence = checksum_verification_evidence(archive, symbol="btcusdt")

    assert evidence.provider == PROVIDER
    assert evidence.venue == VENUE
    assert evidence.symbol == "BTCUSDT"
    assert evidence.source_sha256 == archive.sha256
    assert evidence.sample_refs == (archive.checksum_url,)
    assert evidence.endpoint_base == ARCHIVE_BASE_URL
    assert evidence.verification_method == CHECKSUM_VERIFICATION_METHOD


def test_monthly_policy_keeps_one_evidence_record_per_archive_and_sparse_rest(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from romeo_crt_engine.market_data import verification

    archives = (
        _archive(date(2020, 1, 2)),
        _archive(date(2020, 1, 4)),
        _archive(date(2020, 2, 5)),
        _archive(date(2020, 2, 6)),
    )
    archive_by_date = {archive.archive_date: archive for archive in archives}
    parsed_dates: list[date] = []

    def fake_parse(archive: RawArchive, *, symbol: str) -> tuple[object, ...]:
        assert symbol == "BTCUSDT"
        parsed_dates.append(archive.archive_date)
        return (archive.archive_date,)

    def fake_rest_check(bars: tuple[object, ...]) -> ProviderVerificationEvidence:
        day = bars[0]
        assert isinstance(day, date)
        archive = archive_by_date[day]
        return ProviderVerificationEvidence(
            provider=PROVIDER,
            venue=VENUE,
            symbol="BTCUSDT",
            source_sha256=archive.sha256,
            sample_refs=(day.isoformat(),),
            endpoint_base=MARKET_DATA_API_BASE_URL,
            verification_method=REST_VERIFICATION_METHOD,
        )

    monkeypatch.setattr(verification, "parse_1m_archive", fake_parse)
    monkeypatch.setattr(verification, "crosscheck_bars_with_rest", fake_rest_check)

    evidence = build_provider_verification_evidence(
        archives,
        symbol="BTCUSDT",
        policy=VerificationPolicy.CHECKSUM_ALL_REST_MONTHLY,
    )

    assert len(evidence) == len(archives)
    assert {item.source_sha256 for item in evidence} == {archive.sha256 for archive in archives}
    assert parsed_dates == [date(2020, 1, 2), date(2020, 2, 5)]
    assert [item.verification_method for item in evidence] == [
        REST_VERIFICATION_METHOD,
        CHECKSUM_VERIFICATION_METHOD,
        REST_VERIFICATION_METHOD,
        CHECKSUM_VERIFICATION_METHOD,
    ]


def test_rest_every_archive_policy_preserves_phase3_behavior(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from romeo_crt_engine.market_data import verification

    archives = (_archive(date(2020, 1, 2)), _archive(date(2020, 1, 3)))
    archive_by_date = {archive.archive_date: archive for archive in archives}
    parsed_dates: list[date] = []

    def fake_parse(archive: RawArchive, *, symbol: str) -> tuple[object, ...]:
        assert symbol == "BTCUSDT"
        parsed_dates.append(archive.archive_date)
        return (archive.archive_date,)

    def fake_rest_check(bars: tuple[object, ...]) -> ProviderVerificationEvidence:
        day = bars[0]
        assert isinstance(day, date)
        archive = archive_by_date[day]
        return ProviderVerificationEvidence(
            provider=PROVIDER,
            venue=VENUE,
            symbol="BTCUSDT",
            source_sha256=archive.sha256,
            sample_refs=(day.isoformat(),),
            endpoint_base=MARKET_DATA_API_BASE_URL,
            verification_method=REST_VERIFICATION_METHOD,
        )

    monkeypatch.setattr(verification, "parse_1m_archive", fake_parse)
    monkeypatch.setattr(verification, "crosscheck_bars_with_rest", fake_rest_check)

    evidence = build_provider_verification_evidence(
        archives,
        symbol="BTCUSDT",
        policy=VerificationPolicy.REST_EVERY_ARCHIVE,
    )

    assert parsed_dates == [archive.archive_date for archive in archives]
    assert all(item.verification_method == REST_VERIFICATION_METHOD for item in evidence)
