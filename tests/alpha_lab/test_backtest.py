from __future__ import annotations

from datetime import UTC, datetime, timedelta

from romeo_crt_engine.alpha_lab.backtest import run_backtest
from romeo_crt_engine.alpha_lab.models import Bar, CostModel, StrategyConfig


def _bar(hour: int, *, o: float, h: float, l: float, c: float) -> Bar:
    return Bar(
        open_time=datetime(2024, 1, 1, tzinfo=UTC) + timedelta(hours=hour),
        open=o,
        high=h,
        low=l,
        close=c,
        volume=100.0,
    )


def _config() -> StrategyConfig:
    return StrategyConfig(
        lookback_hours=3,
        min_sweep_bps=0.0,
        reclaim_fraction=0.0,
        ema_fast=0,
        ema_slow=0,
        direction_mode="long_only",
        atr_period=2,
        stop_buffer_atr=0.0,
        target_r=1.0,
        max_hold_bars=3,
    )


def _prefix() -> list[Bar]:
    return [
        _bar(0, o=105, h=110, l=100, c=106),
        _bar(1, o=106, h=109, l=101, c=105),
        _bar(2, o=105, h=108, l=100, c=104),
        _bar(3, o=104, h=108, l=99, c=105),
    ]


def test_signal_is_entered_on_next_bar_open() -> None:
    bars = _prefix() + [
        _bar(4, o=105, h=112, l=104, c=111),
        _bar(5, o=111, h=112, l=109, c=110),
        _bar(6, o=110, h=111, l=108, c=109),
    ]
    result = run_backtest(bars, _config(), costs=CostModel(0.0, 0.0, 3.0))
    assert result.metrics.closed_trades == 1
    trade = result.trades[0]
    assert trade.signal_time == bars[3].open_time
    assert trade.entry_time == bars[4].open_time
    assert trade.exit_reason == "target"
    assert trade.r_multiple > 0


def test_same_bar_stop_and_target_resolves_to_stop() -> None:
    bars = _prefix() + [
        _bar(4, o=105, h=112, l=98, c=106),
        _bar(5, o=106, h=107, l=104, c=105),
        _bar(6, o=105, h=106, l=103, c=104),
    ]
    result = run_backtest(bars, _config(), costs=CostModel(0.0, 0.0, 3.0))
    assert result.metrics.closed_trades == 1
    assert result.trades[0].exit_reason == "stop_same_bar"
    assert result.trades[0].net_pnl < 0


def test_costs_reduce_trade_result() -> None:
    bars = _prefix() + [
        _bar(4, o=105, h=112, l=104, c=111),
        _bar(5, o=111, h=112, l=109, c=110),
        _bar(6, o=110, h=111, l=108, c=109),
    ]
    zero = run_backtest(bars, _config(), costs=CostModel(0.0, 0.0, 3.0))
    realistic = run_backtest(bars, _config(), costs=CostModel(4.0, 2.0, 3.0))
    assert zero.metrics.closed_trades == realistic.metrics.closed_trades == 1
    assert realistic.trades[0].net_pnl < zero.trades[0].net_pnl
    assert realistic.trades[0].r_multiple < zero.trades[0].r_multiple
