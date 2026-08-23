from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from romeo_crt_engine.alpha_lab import optimize_v4
from romeo_crt_engine.alpha_lab.backtest_v4 import run_v4_backtest
from romeo_crt_engine.alpha_lab.models import Bar, CostModel, Metrics
from romeo_crt_engine.alpha_lab.models_v4 import V4BacktestResult, V4Config
from romeo_crt_engine.alpha_lab.optimize_v4 import v4_search_space
from romeo_crt_engine.alpha_lab.strategy_v4 import generate_v4_signals


def _bar(index: int, *, open_: float, high: float, low: float, close: float) -> Bar:
    return Bar(
        open_time=datetime(2020, 1, 1, tzinfo=UTC) + timedelta(hours=index),
        open=open_,
        high=high,
        low=low,
        close=close,
        volume=100.0,
    )


def _config(**overrides: object) -> V4Config:
    values: dict[str, object] = {
        "entry_lookback": 2,
        "breakout_buffer_bps": 0.0,
        "use_rising_ema200_regime": False,
        "atr_period": 2,
        "initial_stop_atr": 2.5,
        "trail_atr": 2.0,
        "max_hold_bars": 4,
    }
    values.update(overrides)
    return V4Config(**values)  # type: ignore[arg-type]


def _trend_bars() -> tuple[Bar, ...]:
    return (
        _bar(0, open_=100.0, high=101.0, low=99.0, close=100.0),
        _bar(1, open_=100.0, high=101.0, low=99.5, close=100.0),
        _bar(2, open_=100.0, high=101.0, low=99.5, close=100.0),
        _bar(3, open_=100.0, high=103.0, low=99.8, close=102.5),
        _bar(4, open_=103.0, high=110.0, low=101.0, close=109.0),
        _bar(5, open_=108.0, high=109.0, low=99.0, close=100.0),
        _bar(6, open_=100.0, high=101.0, low=98.0, close=99.0),
        _bar(7, open_=99.0, high=100.0, low=97.0, close=98.0),
    )


def _metrics(*, expectancy_r: float, profit_factor: float) -> Metrics:
    return Metrics(
        closed_trades=120,
        wins=60,
        losses=60,
        win_rate=0.5,
        expectancy_r=expectancy_r,
        profit_factor=profit_factor,
        net_pnl=1000.0,
        return_pct=1.0,
        max_drawdown_pct=10.0,
        final_equity=101_000.0,
    )


def test_v4_search_space_is_exactly_144_configs() -> None:
    configs = tuple(v4_search_space())
    assert len(configs) == 144
    assert len({config.config_id for config in configs}) == 144


def test_v4_signal_is_known_before_next_open_entry() -> None:
    bars = _trend_bars()
    signals = generate_v4_signals(bars, _config())
    assert signals
    assert signals[0].signal_index == 3
    result = run_v4_backtest(bars, _config(), costs=CostModel())
    assert result.trades
    assert result.trades[0].signal_time == bars[3].open_time
    assert result.trades[0].entry_time == bars[4].open_time


def test_v4_trailing_stop_from_completed_bar_is_not_retroactive() -> None:
    bars = _trend_bars()
    result = run_v4_backtest(bars, _config(), costs=CostModel())
    assert result.trades
    trade = result.trades[0]
    assert trade.exit_reason == "stop"
    assert trade.exit_time >= bars[5].open_time
    assert trade.exit_time > bars[4].open_time
    assert trade.target_price == 0.0


def test_v4_search_prefers_gate_passing_candidate(monkeypatch: pytest.MonkeyPatch) -> None:
    failing = _config(trail_atr=2.0)
    passing = _config(trail_atr=3.0)
    results = {
        failing.config_id: V4BacktestResult(
            config=failing,
            costs=CostModel(),
            metrics=_metrics(expectancy_r=0.50, profit_factor=1.20),
            trades=(),
        ),
        passing.config_id: V4BacktestResult(
            config=passing,
            costs=CostModel(),
            metrics=_metrics(expectancy_r=0.10, profit_factor=1.40),
            trades=(),
        ),
    }

    def fake_backtest(*args: object, **kwargs: object) -> V4BacktestResult:
        config = args[1]
        assert isinstance(config, V4Config)
        return results[config.config_id]

    monkeypatch.setattr(optimize_v4, "run_v4_backtest", fake_backtest)
    search = optimize_v4.search_v4_dev([], configs=(failing, passing))
    assert search.gate_pass is True
    assert search.result.config == passing
