from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal
from hashlib import sha256

from romeo_crt_engine.backtest.engine import run_backtest
from romeo_crt_engine.backtest.models import (
    BASE_COSTS,
    IDEAL_COSTS,
    SIMULATOR_VERSION,
    BacktestConfig,
    ExitReason,
)
from romeo_crt_engine.crt.detector import (
    DETECTOR_VERSION,
    DetectorDataset,
    DetectorDatasetIdentity,
    detect_dataset,
)
from romeo_crt_engine.crt.v0_1 import STRATEGY_VERSION
from romeo_crt_engine.market_data.dataset import normalized_digest
from romeo_crt_engine.market_data.models import BarTimeframe, CanonicalBar

PROVIDER = "TEST_PROVIDER"
VENUE = "TEST_VENUE"
SYMBOL = "TESTUSD"


def _digest(label: str) -> str:
    return sha256(label.encode("utf-8")).hexdigest()


def _bar(
    *,
    timeframe: BarTimeframe,
    open_time: datetime,
    open_: str,
    high: str,
    low: str,
    close: str,
    label: str,
) -> CanonicalBar:
    duration = timedelta(hours=1) if timeframe is BarTimeframe.H1 else timedelta(days=1)
    return CanonicalBar(
        provider=PROVIDER,
        venue=VENUE,
        symbol=SYMBOL,
        timeframe=timeframe,
        open_time=open_time,
        close_time=open_time + duration,
        open=Decimal(open_),
        high=Decimal(high),
        low=Decimal(low),
        close=Decimal(close),
        volume=Decimal(1),
        quote_volume=Decimal(1),
        trade_count=1,
        source_count=60 if timeframe is BarTimeframe.H1 else 24,
        source_digest=_digest(label),
    )


def _scenario_dataset(
    post_entry: tuple[str, str, str, str] | None,
) -> DetectorDataset:
    c1_open = datetime(2025, 9, 15, 4, 0, tzinfo=UTC)
    c2_open = datetime(2025, 9, 16, 4, 0, tzinfo=UTC)
    c3_open = datetime(2025, 9, 17, 4, 0, tzinfo=UTC)

    c1 = _bar(
        timeframe=BarTimeframe.D1,
        open_time=c1_open,
        open_="100",
        high="110",
        low="90",
        close="105",
        label="c1",
    )
    c2 = _bar(
        timeframe=BarTimeframe.D1,
        open_time=c2_open,
        open_="105",
        high="112",
        low="103",
        close="108",
        label="c2",
    )

    h1 = [
        _bar(
            timeframe=BarTimeframe.H1,
            open_time=c3_open,
            open_="108",
            high="109",
            low="106",
            close="108.5",
            label="h1-0",
        ),
        _bar(
            timeframe=BarTimeframe.H1,
            open_time=c3_open + timedelta(hours=1),
            open_="108.5",
            high="113",
            low="107",
            close="112",
            label="h1-1-model1",
        ),
        _bar(
            timeframe=BarTimeframe.H1,
            open_time=c3_open + timedelta(hours=2),
            open_="112",
            high="112.5",
            low="105",
            close="106",
            label="h1-2-confirm",
        ),
    ]
    if post_entry is not None:
        open_, high, low, close = post_entry
        h1.append(
            _bar(
                timeframe=BarTimeframe.H1,
                open_time=c3_open + timedelta(hours=3),
                open_=open_,
                high=high,
                low=low,
                close=close,
                label="h1-3-post-entry",
            )
        )

    c3_high = max(bar.high for bar in h1)
    c3_low = min(bar.low for bar in h1)
    c3_close = h1[-1].close
    c3 = _bar(
        timeframe=BarTimeframe.D1,
        open_time=c3_open,
        open_="108",
        high=str(c3_high),
        low=str(c3_low),
        close=str(c3_close),
        label="c3",
    )

    h1_tuple = tuple(h1)
    d1 = (c1, c2, c3)
    normalized_sha = normalized_digest(h1_tuple, d1)
    identity = DetectorDatasetIdentity(
        dataset_version="phase5-synthetic-fixture",
        manifest_sha256=_digest("phase5-synthetic-manifest"),
        normalized_sha256=normalized_sha,
        provider=PROVIDER,
        venue=VENUE,
        symbol=SYMBOL,
        tick_size=Decimal("0.25"),
        h1_rows=len(h1_tuple),
        d1_rows=3,
        quality_status="TRUSTED",
        schema_version="PHASE3_DATASET_MANIFEST_V1",
    )
    return DetectorDataset(identity=identity, h1=h1_tuple, d1=d1)


def _backtest(
    post_entry: tuple[str, str, str, str] | None,
    *,
    costs=IDEAL_COSTS,
):
    dataset = _scenario_dataset(post_entry)
    detector_run = detect_dataset(dataset)
    assert detector_run.trade_plan_count == 1
    config = BacktestConfig(
        initial_equity=Decimal(100_000),
        risk_fraction=Decimal("0.01"),
        cost_model=costs,
    )
    result = run_backtest(
        detector_run,
        dataset,
        quantity_step=Decimal("0.01"),
        config=config,
    )
    return dataset, detector_run, result


def test_target_exit_occurs_only_after_confirmation_bar_closes() -> None:
    _, detector_run, result = _backtest(("106", "107", "99", "100"))

    assert result.simulator_version == SIMULATOR_VERSION
    assert result.strategy_version == STRATEGY_VERSION
    assert result.detector_version == DETECTOR_VERSION
    assert len(result.completed_trades) == 1
    trade = result.completed_trades[0]
    plan = detector_run.candidates[0].trade_plan
    assert plan is not None
    assert trade.entry_fill.timestamp == plan.entry_time
    assert trade.exit_fill.timestamp > trade.entry_fill.timestamp
    assert trade.exit_reason is ExitReason.TARGET
    assert trade.entry_fill.reference_price == Decimal(106)
    assert trade.exit_fill.reference_price == Decimal(100)
    assert trade.net_pnl > 0
    assert trade.r_multiple > 0


def test_stop_exit_uses_structural_stop_reference() -> None:
    _, _, result = _backtest(("106", "114", "104", "113"))

    trade = result.completed_trades[0]
    assert trade.exit_reason is ExitReason.STOP
    assert trade.exit_fill.reference_price == Decimal("113.25")
    assert trade.net_pnl < 0
    assert trade.r_multiple < 0


def test_same_bar_stop_and_target_uses_conservative_stop_first_policy() -> None:
    _, _, result = _backtest(("106", "114", "99", "105"))

    trade = result.completed_trades[0]
    assert trade.exit_reason is ExitReason.STOP_SAME_BAR_AMBIGUITY
    assert trade.exit_fill.reference_price == Decimal("113.25")
    assert trade.net_pnl < 0


def test_stop_gap_uses_worse_bar_open() -> None:
    _, _, result = _backtest(("115", "116", "114", "115"))

    trade = result.completed_trades[0]
    assert trade.exit_reason is ExitReason.STOP_GAP
    assert trade.exit_fill.reference_price == Decimal(115)
    assert trade.net_pnl < 0
    assert trade.r_multiple < Decimal(-1)


def test_target_gap_does_not_grant_favorable_price_improvement() -> None:
    _, _, result = _backtest(("98", "99", "97", "98"))

    trade = result.completed_trades[0]
    assert trade.exit_reason is ExitReason.TARGET_GAP
    assert trade.exit_fill.reference_price == Decimal(100)
    assert trade.exit_fill.fill_price == Decimal(100)


def test_open_position_at_dataset_end_is_not_force_closed() -> None:
    _, detector_run, result = _backtest(None)

    assert result.completed_trades == ()
    assert len(result.open_at_end) == 1
    assert result.final_realized_equity == Decimal(100_000)
    open_position = result.open_at_end[0]
    plan = detector_run.candidates[0].trade_plan
    assert plan is not None
    assert open_position.entry_fill.timestamp == plan.entry_time
    assert open_position.final_mark_time == plan.entry_time
    assert result.metrics.closed_trades == 0
    assert result.metrics.expectancy_r is None


def test_base_costs_are_adverse_and_stop_sizing_respects_risk_budget() -> None:
    _, _, result = _backtest(("106", "114", "104", "113"), costs=BASE_COSTS)

    trade = result.completed_trades[0]
    assert trade.entry_fill.fill_price < trade.entry_fill.reference_price
    assert trade.exit_fill.fill_price > trade.exit_fill.reference_price
    assert trade.total_fees > 0
    assert -trade.net_pnl <= trade.risk_budget
    assert trade.entry_fill.quantity % Decimal("0.01") == 0


def test_backtest_run_hash_is_deterministic_for_identical_inputs() -> None:
    dataset = _scenario_dataset(("106", "107", "99", "100"))
    detector_run = detect_dataset(dataset)
    config = BacktestConfig(
        initial_equity=Decimal(100_000),
        risk_fraction=Decimal("0.01"),
        cost_model=BASE_COSTS,
    )

    first = run_backtest(
        detector_run,
        dataset,
        quantity_step=Decimal("0.01"),
        config=config,
    )
    second = run_backtest(
        detector_run,
        dataset,
        quantity_step=Decimal("0.01"),
        config=config,
    )
    assert first.run_sha256 == second.run_sha256
    assert first.completed_trades == second.completed_trades
    assert first.metrics == second.metrics
