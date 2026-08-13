from __future__ import annotations

from datetime import UTC, date, datetime, timedelta
from decimal import Decimal
from zoneinfo import ZoneInfo

import pytest

from romeo_crt_engine.market_data.aggregate_v2 import (
    build_h1_price_bars_v2,
    build_new_york_d1_price_bars_v2,
)
from romeo_crt_engine.market_data.models import BarTimeframe
from romeo_crt_engine.market_data.price_data_v2 import (
    ActivityMeasure,
    ActivitySemantic,
    CanonicalPriceBarV2,
    PriceComponent,
)
from romeo_crt_engine.market_data.session_policy_v2 import GapCategory, MarketGapV2

SESSION_POLICY = "TEST_SESSION_POLICY_V1"
SOURCE_SHA = "e" * 64
NEW_YORK = ZoneInfo("America/New_York")


def _minute(open_time: datetime, value: int) -> CanonicalPriceBarV2:
    price = Decimal(value)
    return CanonicalPriceBarV2(
        provider="OANDA_V20",
        venue="OANDA_FXTRADE",
        instrument="EUR_USD",
        price_component=PriceComponent.MID,
        timeframe=BarTimeframe.M1,
        open_time=open_time,
        close_time=open_time + timedelta(minutes=1),
        open=price,
        high=price + Decimal("0.5"),
        low=price - Decimal("0.5"),
        close=price + Decimal("0.1"),
        source_count=1,
        source_digest=SOURCE_SHA,
        session_policy_version=SESSION_POLICY,
        activity=(ActivityMeasure(ActivitySemantic.PRICE_COUNT, Decimal(1)),),
    )


def _minutes(start: datetime, count: int) -> tuple[CanonicalPriceBarV2, ...]:
    return tuple(_minute(start + timedelta(minutes=index), index + 100) for index in range(count))


def _gap(start: datetime, end: datetime, category: GapCategory) -> MarketGapV2:
    return MarketGapV2(
        provider="OANDA_V20",
        venue="OANDA_FXTRADE",
        instrument="EUR_USD",
        start_time=start,
        end_time=end,
        category=category,
        policy_version=SESSION_POLICY,
        evidence_id="TEST-EVIDENCE",
        evidence_source="unit-test",
    )


def test_h1_aggregates_complete_observations_and_price_count() -> None:
    start = datetime(2026, 8, 13, 8, 0, tzinfo=UTC)
    m1 = _minutes(start, 60)

    h1 = build_h1_price_bars_v2(
        m1,
        coverage_start=start,
        coverage_end=start + timedelta(hours=1),
    )

    assert len(h1) == 1
    assert h1[0].source_count == 60
    assert h1[0].open == m1[0].open
    assert h1[0].close == m1[-1].close
    assert h1[0].activity == (
        ActivityMeasure(ActivitySemantic.PRICE_COUNT, Decimal(60)),
    )


def test_h1_rejects_missing_expected_minute() -> None:
    start = datetime(2026, 8, 13, 8, 0, tzinfo=UTC)
    m1 = _minutes(start, 60)
    missing = m1[:30] + m1[31:]

    with pytest.raises(ValueError, match="missing=1"):
        build_h1_price_bars_v2(
            missing,
            coverage_start=start,
            coverage_end=start + timedelta(hours=1),
        )


def test_h1_allows_evidenced_session_break_without_synthetic_minute() -> None:
    start = datetime(2026, 8, 13, 8, 0, tzinfo=UTC)
    m1 = _minutes(start, 60)
    missing = m1[:30] + m1[31:]
    gap = _gap(
        start + timedelta(minutes=30),
        start + timedelta(minutes=31),
        GapCategory.SESSION_BREAK,
    )

    h1 = build_h1_price_bars_v2(
        missing,
        coverage_start=start,
        coverage_end=start + timedelta(hours=1),
        gaps=(gap,),
    )

    assert len(h1) == 1
    assert h1[0].source_count == 59
    assert h1[0].activity == (
        ActivityMeasure(ActivitySemantic.PRICE_COUNT, Decimal(59)),
    )


def test_provider_missing_gap_can_never_be_used_as_expected_session_time() -> None:
    start = datetime(2026, 8, 13, 8, 0, tzinfo=UTC)
    m1 = _minutes(start, 60)
    missing = m1[:30] + m1[31:]
    gap = _gap(
        start + timedelta(minutes=30),
        start + timedelta(minutes=31),
        GapCategory.PROVIDER_MISSING,
    )

    with pytest.raises(ValueError, match="unapproved gap category"):
        build_h1_price_bars_v2(
            missing,
            coverage_start=start,
            coverage_end=start + timedelta(hours=1),
            gaps=(gap,),
        )


def test_new_york_d1_preserves_spring_forward_wall_clock_envelope() -> None:
    local_date = date(2026, 3, 8)
    start = datetime.combine(local_date, datetime.min.time(), tzinfo=NEW_YORK).astimezone(UTC)
    end = datetime.combine(
        local_date + timedelta(days=1), datetime.min.time(), tzinfo=NEW_YORK
    ).astimezone(UTC)
    assert end - start == timedelta(hours=23)
    m1 = _minutes(start, 23 * 60)

    d1 = build_new_york_d1_price_bars_v2(m1, eligible_local_dates=(local_date,))

    assert len(d1) == 1
    assert d1[0].open_time == start
    assert d1[0].close_time == end
    assert d1[0].source_count == 23 * 60
    assert d1[0].activity == (
        ActivityMeasure(ActivitySemantic.PRICE_COUNT, Decimal(23 * 60)),
    )
