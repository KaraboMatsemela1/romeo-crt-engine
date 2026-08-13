from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from romeo_crt_engine.market_data.models import BarTimeframe
from romeo_crt_engine.market_data.oanda_qualification import canonicalize_oanda_m1
from romeo_crt_engine.market_data.price_data_v2 import (
    ActivityMeasure,
    ActivitySemantic,
    CanonicalPriceBarV2,
    PriceComponent,
    PriceDatasetIdentityV2,
    PriceQuantumSource,
    canonical_price_bar_record,
    normalized_price_digest_v2,
)
from romeo_crt_engine.market_data.providers.oanda_v20 import OandaPriceCandle

SOURCE_SHA = "b" * 64
SESSION_POLICY = "P6B_OANDA_SESSION_POLICY_PENDING_V1"


def _bar(
    *,
    timeframe: BarTimeframe,
    open_time: datetime,
    price_component: PriceComponent = PriceComponent.MID,
    activity: tuple[ActivityMeasure, ...] = (),
) -> CanonicalPriceBarV2:
    duration = timedelta(hours=1) if timeframe is BarTimeframe.H1 else timedelta(days=1)
    return CanonicalPriceBarV2(
        provider="OANDA_V20",
        venue="OANDA_FXTRADE",
        instrument="EUR_USD",
        price_component=price_component,
        timeframe=timeframe,
        open_time=open_time,
        close_time=open_time + duration,
        open=Decimal("1.1000"),
        high=Decimal("1.1100"),
        low=Decimal("1.0900"),
        close=Decimal("1.1050"),
        source_count=60 if timeframe is BarTimeframe.H1 else 24,
        source_digest=SOURCE_SHA,
        session_policy_version=SESSION_POLICY,
        activity=activity,
    )


def test_oanda_m1_canonicalization_preserves_price_count_semantics_only() -> None:
    candle = OandaPriceCandle(
        instrument="EUR_USD",
        price_component="M",
        open_time=datetime(2026, 8, 13, 8, 0, tzinfo=UTC),
        close_time=datetime(2026, 8, 13, 8, 1, tzinfo=UTC),
        open=Decimal("1.1000"),
        high=Decimal("1.1004"),
        low=Decimal("1.0999"),
        close=Decimal("1.1002"),
        price_count=17,
        complete=True,
        source_sha256=SOURCE_SHA,
    )

    canonical = canonicalize_oanda_m1((candle,), session_policy_version=SESSION_POLICY)

    assert len(canonical) == 1
    bar = canonical[0]
    assert bar.timeframe is BarTimeframe.M1
    assert bar.price_component is PriceComponent.MID
    assert bar.activity == (
        ActivityMeasure(semantic=ActivitySemantic.PRICE_COUNT, value=Decimal(17)),
    )
    record = canonical_price_bar_record(bar)
    assert "volume" not in record
    assert "quote_volume" not in record
    assert "trade_count" not in record
    assert record["activity"] == [{"semantic": "PRICE_COUNT", "value": "17"}]


def test_canonical_price_activity_is_semantically_unique() -> None:
    with pytest.raises(ValueError, match="activity semantic"):
        CanonicalPriceBarV2(
            provider="OANDA_V20",
            venue="OANDA_FXTRADE",
            instrument="EUR_USD",
            price_component=PriceComponent.MID,
            timeframe=BarTimeframe.M1,
            open_time=datetime(2026, 8, 13, 8, 0, tzinfo=UTC),
            close_time=datetime(2026, 8, 13, 8, 1, tzinfo=UTC),
            open=Decimal(1),
            high=Decimal(2),
            low=Decimal(1),
            close=Decimal("1.5"),
            source_count=1,
            source_digest=SOURCE_SHA,
            session_policy_version=SESSION_POLICY,
            activity=(
                ActivityMeasure(ActivitySemantic.PRICE_COUNT, Decimal(2)),
                ActivityMeasure(ActivitySemantic.PRICE_COUNT, Decimal(3)),
            ),
        )


def test_normalized_price_digest_changes_with_price_component() -> None:
    open_time = datetime(2026, 8, 13, 8, 0, tzinfo=UTC)
    h1_mid = (_bar(timeframe=BarTimeframe.H1, open_time=open_time),)
    d1_mid = (_bar(timeframe=BarTimeframe.D1, open_time=open_time),)
    h1_bid = (
        _bar(
            timeframe=BarTimeframe.H1,
            open_time=open_time,
            price_component=PriceComponent.BID,
        ),
    )
    d1_bid = (
        _bar(
            timeframe=BarTimeframe.D1,
            open_time=open_time,
            price_component=PriceComponent.BID,
        ),
    )

    assert normalized_price_digest_v2(h1_mid, d1_mid) != normalized_price_digest_v2(
        h1_bid, d1_bid
    )


def test_dataset_identity_requires_explicit_positive_price_quantum() -> None:
    identity = PriceDatasetIdentityV2(
        dataset_version="abc123",
        provider="OANDA_V20",
        venue="OANDA_FXTRADE",
        instrument="EUR_USD",
        price_component=PriceComponent.MID,
        price_quantum=Decimal("0.00001"),
        price_quantum_source=PriceQuantumSource.PROJECT_EXECUTION_PARAMETER,
        price_quantum_observed_at=datetime(2026, 8, 13, 10, 0, tzinfo=UTC),
        instrument_metadata_sha256="c" * 64,
        session_policy_version=SESSION_POLICY,
        normalized_sha256="d" * 64,
        h1_rows=10,
        d1_rows=2,
        quality_status="TRUSTED",
    )

    assert identity.price_quantum == Decimal("0.00001")

    with pytest.raises(ValueError, match="price_quantum"):
        PriceDatasetIdentityV2(
            dataset_version="abc123",
            provider="OANDA_V20",
            venue="OANDA_FXTRADE",
            instrument="EUR_USD",
            price_component=PriceComponent.MID,
            price_quantum=Decimal(0),
            price_quantum_source=PriceQuantumSource.PROJECT_EXECUTION_PARAMETER,
            price_quantum_observed_at=datetime(2026, 8, 13, 10, 0, tzinfo=UTC),
            instrument_metadata_sha256="c" * 64,
            session_policy_version=SESSION_POLICY,
            normalized_sha256="d" * 64,
            h1_rows=10,
            d1_rows=2,
            quality_status="TRUSTED",
        )
