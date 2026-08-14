from datetime import UTC, datetime
from decimal import Decimal

import pytest

from romeo_crt_engine.market_data.canonical_coverage_v2 import (
    CANONICAL_COVERAGE_END_UTC,
    CANONICAL_COVERAGE_START_UTC,
    CANONICAL_TAIL_END_UTC,
    CANONICAL_TAIL_START_UTC,
    eligible_new_york_dates_from_m1,
)
from romeo_crt_engine.market_data.models import BarTimeframe
from romeo_crt_engine.market_data.price_data_v2 import CanonicalPriceBarV2, PriceComponent


def _bar(open_time: datetime) -> CanonicalPriceBarV2:
    from datetime import timedelta

    return CanonicalPriceBarV2(
        provider="OANDA_V20",
        venue="OANDA_FXTRADE",
        instrument="EUR_USD",
        price_component=PriceComponent.MID,
        timeframe=BarTimeframe.M1,
        open_time=open_time,
        close_time=open_time + timedelta(minutes=1),
        open=Decimal("1.1"),
        high=Decimal("1.1"),
        low=Decimal("1.1"),
        close=Decimal("1.1"),
        source_count=1,
        source_digest="a" * 64,
        session_policy_version="P6B_OANDA_OBSERVATION_POLICY_V2",
    )


def test_frozen_new_york_window_has_exact_utc_bounds() -> None:
    assert CANONICAL_COVERAGE_START_UTC == datetime(2019, 1, 1, 5, 0, tzinfo=UTC)
    assert CANONICAL_COVERAGE_END_UTC == datetime(2023, 1, 1, 5, 0, tzinfo=UTC)
    assert CANONICAL_TAIL_START_UTC == datetime(2023, 1, 1, 0, 0, tzinfo=UTC)
    assert CANONICAL_TAIL_END_UTC == datetime(2023, 1, 1, 5, 0, tzinfo=UTC)


def test_eligible_dates_are_derived_from_provider_observations() -> None:
    bars = (
        _bar(datetime(2019, 1, 1, 5, 0, tzinfo=UTC)),
        _bar(datetime(2019, 1, 2, 4, 59, tzinfo=UTC)),
        _bar(datetime(2019, 1, 2, 5, 0, tzinfo=UTC)),
    )
    assert eligible_new_york_dates_from_m1(bars) == (
        datetime(2019, 1, 1).date(),
        datetime(2019, 1, 2).date(),
    )


def test_date_derivation_rejects_observations_outside_frozen_window() -> None:
    with pytest.raises(ValueError, match="outside the frozen Phase-6B canonical coverage"):
        eligible_new_york_dates_from_m1(
            (_bar(datetime(2023, 1, 1, 5, 0, tzinfo=UTC)),)
        )
