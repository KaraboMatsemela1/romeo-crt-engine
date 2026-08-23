from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime, timedelta

from pytest import MonkeyPatch

from romeo_crt_engine.alpha_lab import optimize_v2
from romeo_crt_engine.alpha_lab.backtest_v2 import run_v2_backtest
from romeo_crt_engine.alpha_lab.models import Bar, CostModel, Metrics
from romeo_crt_engine.alpha_lab.models_v2 import V2BacktestResult, V2Config
from romeo_crt_engine.alpha_lab.strategy_v2 import generate_v2_signals


def _bar(hour: int, *, o: float, h: float, l: float, c: float) -> Bar:
    return Bar(
        open_time=datetime(2024, 3, 1, tzinfo=UTC) + timedelta(hours=hour),
        open=o,
        high=h,
        low=l,
        close=c,
        volume=100.0,
    )


def _config(**changes: object) -> V2Config:
    base = V2Config(
        lookback_hours=3,
        breakout_buffer_bps=0.0,
        ema_fast=0,
        ema_slow=0,
        direction_mode="long_only",
        atr_period=2,
        stop_atr=1.0,
        target_r=1.5,
        max_hold_bars=3,
    )
    return replace(base, **changes)


def test_v2_breakout_is_close_confirmed_and_enters_next_open() -> None:
    bars = [
        _bar(0, o=100, h=101, l=99, c=100),
        _bar(1, o=100, h=102, l=99, c=101),
        _bar(2, o=101, h=102, l=100, c=101),
        _bar(3, o=101, h=104, l=101, c=103),
        _bar(4, o=103, h=107, l=102.5, c=106),
        _bar(5, o=106, h=107, l=105, c=106),
        _bar(6, o=106, h=107, l=105, c=106),
    ]
    signals = generate_v2_signals(bars, _config())
    assert signals
    assert signals[0].signal_index == 3
    result = run_v2_backtest(bars, _config(), costs=CostModel(0.0, 0.0, 3.0))
    assert result.metrics.closed_trades == 1
    assert result.trades[0].signal_time == bars[3].open_time
    assert result.trades[0].entry_time == bars[4].open_time


def test_v2_breakout_buffer_blocks_shallow_close() -> None:
    bars = [
        _bar(0, o=100, h=101, l=99, c=100),
        _bar(1, o=100, h=102, l=99, c=101),
        _bar(2, o=101, h=102, l=100, c=101),
        _bar(3, o=101, h=102.03, l=101, c=102.02),
        _bar(4, o=102, h=103, l=101, c=102),
        _bar(5, o=102, h=103, l=101, c=102),
    ]
    assert generate_v2_signals(bars, _config(breakout_buffer_bps=5.0)) == ()


def test_v2_search_prefers_hard_gate_pass(monkeypatch: MonkeyPatch) -> None:
    failing = _config(target_r=1.5)
    passing = _config(target_r=2.0)
    base = Metrics(
        closed_trades=120,
        wins=60,
        losses=60,
        win_rate=0.5,
        expectancy_r=0.10,
        profit_factor=1.40,
        net_pnl=1000.0,
        return_pct=1.0,
        max_drawdown_pct=10.0,
        final_equity=101_000.0,
    )
    mapping = {
        failing.config_id: V2BacktestResult(
            config=failing,
            costs=CostModel(),
            metrics=replace(base, profit_factor=1.20, expectancy_r=0.50),
            trades=(),
        ),
        passing.config_id: V2BacktestResult(
            config=passing,
            costs=CostModel(),
            metrics=base,
            trades=(),
        ),
    }

    def fake_run(*args: object, **kwargs: object) -> V2BacktestResult:
        config = args[1]
        assert isinstance(config, V2Config)
        return mapping[config.config_id]

    monkeypatch.setattr(optimize_v2, "run_v2_backtest", fake_run)
    search = optimize_v2.search_v2_dev([], configs=(failing, passing))
    assert search.gate_pass is True
    assert search.result.config == passing


def test_v2_grid_is_preregistered_size() -> None:
    assert sum(1 for _ in optimize_v2.v2_search_space()) == 1296
