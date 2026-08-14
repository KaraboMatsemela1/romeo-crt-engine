from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from romeo_crt_engine.market_data.gap_reconciliation_v2 import (
    reconcile_missing_intervals_exactly,
)
from romeo_crt_engine.market_data.history_qualification_v2 import (
    REFETCH_WINDOWS_UTC,
    MissingInterval,
    assert_refetch_equal,
    enumerate_missing_intervals,
    gap_digest,
    normalized_m1_sha256,
)
from romeo_crt_engine.market_data.providers.oanda_history import _parse_history_page_candles
from romeo_crt_engine.market_data.providers.oanda_v20 import OandaPriceCandle
from romeo_crt_engine.market_data.session_policy_v2 import GapCategory, MarketGapV2


def _candle(minute: int, close: str = "1.1001") -> OandaPriceCandle:
    open_time = datetime(2020, 1, 2, 12, minute, tzinfo=UTC)
    return OandaPriceCandle(
        instrument="EUR_USD",
        price_component="M",
        open_time=open_time,
        close_time=open_time + timedelta(minutes=1),
        open=Decimal("1.1000"),
        high=Decimal("1.1002"),
        low=Decimal("1.0999"),
        close=Decimal(close),
        price_count=10,
        complete=True,
        source_sha256="a" * 64,
    )


def test_provider_confirmed_empty_history_page_is_allowed() -> None:
    payload = json.dumps(
        {"instrument": "EUR_USD", "granularity": "M1", "candles": []}
    ).encode()

    assert _parse_history_page_candles(
        payload,
        instrument="EUR_USD",
        price_component="M",
    ) == ()


def test_empty_wrong_identity_still_fails_closed() -> None:
    payload = json.dumps(
        {"instrument": "GBP_USD", "granularity": "M1", "candles": []}
    ).encode()

    with pytest.raises(ValueError):
        _parse_history_page_candles(
            payload,
            instrument="EUR_USD",
            price_component="M",
        )


def test_missing_interval_enumeration_includes_internal_and_boundary_gaps() -> None:
    candles = (_candle(1), _candle(2), _candle(5))
    start = datetime(2020, 1, 2, 12, 0, tzinfo=UTC)
    end = datetime(2020, 1, 2, 12, 7, tzinfo=UTC)

    gaps = enumerate_missing_intervals(candles, requested_start=start, requested_end=end)

    assert [(gap.start.minute, gap.end.minute, gap.missing_minutes) for gap in gaps] == [
        (0, 1, 1),
        (3, 5, 2),
        (6, 7, 1),
    ]
    assert len(gap_digest(gaps)) == 64


def test_normalized_m1_digest_ignores_page_source_digest() -> None:
    first = _candle(0)
    second = OandaPriceCandle(
        instrument=first.instrument,
        price_component=first.price_component,
        open_time=first.open_time,
        close_time=first.close_time,
        open=first.open,
        high=first.high,
        low=first.low,
        close=first.close,
        price_count=first.price_count,
        complete=first.complete,
        source_sha256="b" * 64,
    )

    assert normalized_m1_sha256((first,)) == normalized_m1_sha256((second,))


def test_independent_refetch_compares_provider_values_not_page_hashes() -> None:
    primary = (_candle(0), _candle(1))
    refetched = tuple(
        OandaPriceCandle(
            instrument=item.instrument,
            price_component=item.price_component,
            open_time=item.open_time,
            close_time=item.close_time,
            open=item.open,
            high=item.high,
            low=item.low,
            close=item.close,
            price_count=item.price_count,
            complete=item.complete,
            source_sha256="c" * 64,
        )
        for item in primary
    )

    digest = assert_refetch_equal(
        primary,
        refetched,
        start=primary[0].open_time,
        end=primary[-1].close_time,
    )
    assert len(digest) == 64


def test_refetch_windows_are_frozen_inside_dev_and_one_hour_each() -> None:
    for start, end in REFETCH_WINDOWS_UTC:
        assert datetime(2019, 1, 1, tzinfo=UTC) <= start < datetime(2023, 1, 1, tzinfo=UTC)
        assert end - start == timedelta(hours=1)


def test_gap_reconciliation_requires_exact_coverage() -> None:
    start = datetime(2021, 6, 28, 16, 0, tzinfo=UTC)
    end = datetime(2021, 6, 28, 17, 0, tzinfo=UTC)
    missing = (MissingInterval(start=start, end=end),)
    approved = (
        MarketGapV2(
            provider="OANDA_V20",
            venue="OANDA_FXTRADE",
            instrument="NAS100_USD",
            start_time=start,
            end_time=end,
            category=GapCategory.SESSION_BREAK,
            policy_version="P6B-HISTORICAL-SESSION-POLICY-V1",
            evidence_id="TEST-E1",
            evidence_source="first-party-test-fixture",
        ),
    )

    summary = reconcile_missing_intervals_exactly(
        missing,
        approved,
        provider="OANDA_V20",
        venue="OANDA_FXTRADE",
        instrument="NAS100_USD",
        policy_version="P6B-HISTORICAL-SESSION-POLICY-V1",
    )

    assert summary.status == "FULLY_RECONCILED"
    assert summary.missing_minutes == 60
    assert summary.approved_minutes == 60
    assert len(summary.reconciliation_sha256) == 64


def test_gap_reconciliation_rejects_evidence_that_hides_observed_minutes() -> None:
    start = datetime(2021, 6, 28, 16, 0, tzinfo=UTC)
    end = datetime(2021, 6, 28, 17, 0, tzinfo=UTC)
    missing = (MissingInterval(start=start, end=end),)
    approved = (
        MarketGapV2(
            provider="OANDA_V20",
            venue="OANDA_FXTRADE",
            instrument="NAS100_USD",
            start_time=start,
            end_time=end + timedelta(minutes=1),
            category=GapCategory.SESSION_BREAK,
            policy_version="P6B-HISTORICAL-SESSION-POLICY-V1",
            evidence_id="TEST-E2",
            evidence_source="first-party-test-fixture",
        ),
    )

    with pytest.raises(ValueError, match="outside raw gap"):
        reconcile_missing_intervals_exactly(
            missing,
            approved,
            provider="OANDA_V20",
            venue="OANDA_FXTRADE",
            instrument="NAS100_USD",
            policy_version="P6B-HISTORICAL-SESSION-POLICY-V1",
        )
