from datetime import UTC, datetime, timedelta

import pytest

from romeo_crt_engine.market_data.gap_reconciliation_v2 import (
    reconcile_missing_intervals_partially,
)
from romeo_crt_engine.market_data.history_qualification_v2 import MissingInterval
from romeo_crt_engine.market_data.session_policy_v2 import GapCategory, MarketGapV2


def _gap(start: datetime, end: datetime, category: GapCategory) -> MarketGapV2:
    return MarketGapV2(
        provider="OANDA_V20",
        venue="OANDA_FXTRADE",
        instrument="EUR_USD",
        start_time=start,
        end_time=end,
        category=category,
        policy_version="P6B_OANDA_OBSERVATION_POLICY_V2",
        evidence_id="TEST-EVIDENCE",
        evidence_source="test-fixture",
    )


def test_partial_reconciliation_preserves_unresolved_minutes() -> None:
    start = datetime(2022, 2, 1, 3, 0, tzinfo=UTC)
    missing = (MissingInterval(start=start, end=start + timedelta(minutes=3)),)
    approved = (_gap(start, start + timedelta(minutes=1), GapCategory.NO_PRICE_OBSERVATION),)

    summary = reconcile_missing_intervals_partially(
        missing,
        approved,
        provider="OANDA_V20",
        venue="OANDA_FXTRADE",
        instrument="EUR_USD",
        policy_version="P6B_OANDA_OBSERVATION_POLICY_V2",
    )

    assert summary.status == "PARTIALLY_RECONCILED"
    assert summary.approved_minutes == 1
    assert summary.unresolved_minutes == 2
    assert summary.unresolved_intervals == (
        MissingInterval(start=start + timedelta(minutes=1), end=start + timedelta(minutes=3)),
    )


def test_partial_reconciliation_rejects_provider_missing_as_approved() -> None:
    start = datetime(2022, 2, 1, 3, 0, tzinfo=UTC)
    missing = (MissingInterval(start=start, end=start + timedelta(minutes=1)),)
    approved = (_gap(start, start + timedelta(minutes=1), GapCategory.PROVIDER_MISSING),)

    with pytest.raises(ValueError, match="unapproved gap category"):
        reconcile_missing_intervals_partially(
            missing,
            approved,
            provider="OANDA_V20",
            venue="OANDA_FXTRADE",
            instrument="EUR_USD",
            policy_version="P6B_OANDA_OBSERVATION_POLICY_V2",
        )
