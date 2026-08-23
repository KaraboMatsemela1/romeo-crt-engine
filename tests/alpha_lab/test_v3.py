from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from romeo_crt_engine.alpha_lab import optimize_v3
from romeo_crt_engine.alpha_lab.backtest_v3 import run_v3_backtest
from romeo_crt_engine.alpha_lab.models import Bar, CostModel, Metrics
from romeo_crt_engine.alpha_lab.models_v3 import V3BacktestResult, V3Config
from romeo_crt_engine.alpha_lab.optimize_v3 import v3_search_space
from romeo_crt_engine.alpha_lab.strategy_v3 import generate_v3_signals


def _bar(index: int, *, open_: float, high: float, low: float, close: float) -> Bar:
    return Bar(
        open_time=datetime(2020, 1, 1, tzinfo=UTC) + timedelta(hours=index),
        open=open_,
        high=high,
        low=low,
        close=close,
        volume=100.0,
    )


def _config(**overrides: object) -> V3Config:
    values: dict[str, object] = {
        "lookback_hours": 2,
        "breakout_buffer_bps": 0.0,
        "use_ema200_regime": False,
        "volatility_ratio_min": 0.1,
        "close_location_min": 0.5,
        "atr_period": 2,
        "volatility_lookback": 2,
        "stop_atr": 1.5,
        "target_r": 2.0,
        "max_hold_bars": 2,
    }
    values.update(overrides)
    return V3Config(**values)  # type: ignore[arg-type]


def _signal_bars(*, weak_close: bool = False) -> tuple[Bar, ...]:
    bars = [
        _bar(0, open_=100.0, high=101.0, low=99.0, close=100.0),
        _bar(1, open_=100.0, high=101.0, low=99.5, close=100.5),
        _bar(2, open_=100.5, high=101.0, low=100.0, close=100.5),
        _bar(3, open_=100.5, high=101.0, low=100.0, close=100.5),
        _bar(4, open_=100.5, high=101.0, low=100.0, close=100.5),
    ]
    signal_close = 101.2 if weak_close else 103.0
    bars.append(_bar(5, open_=100.5, high=104.0, low=100.0, close=signal_close))
    bars.extend(
        [
            _bar(6, open_=103.5, high=104.0, low=102.0, close=103.0),
            _bar(7, open_=103.0, high=107.0, low=102.5, close=106.0),
            _bar(8, open_=106.0, high=107.0, low=105.0, close=106.0),
        ]
    )
    return tuple(bars)


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


def test_v3_search_space_is_preregistered_576_configs() -> None:
    configs = tuple(v3_search_space())
    assert len(configs) == 576
    assert len({config.config_id for config in configs}) == 576


def test_v3_signal_uses_strong_close_filter() -> None:
    strong = generate_v3_signals(_signal_bars(), _config(close_location_min=0.75))
    weak = generate_v3_signals(_signal_bars(weak_close=True), _config(close_location_min=0.75))
    assert 5 in {signal.signal_index for signal in strong}
    assert 5 not in {signal.signal_index for signal in weak}


def test_v3_enters_on_next_bar_open() -> None:
    bars = _signal_bars()
    result = run_v3_backtest(bars, _config(), costs=CostModel())
    assert result.trades
    trade = result.trades[0]
    assert trade.signal_time == bars[5].open_time
    assert trade.entry_time == bars[6].open_time
    assert trade.entry_time > trade.signal_time


def test_v3_search_prefers_hard_gate_passing_candidate(monkeypatch: pytest.MonkeyPatch) -> None:
    failing = _config(target_r=2.0)
    passing = _config(target_r=3.0)
    results = {
        failing.config_id: V3BacktestResult(
            config=failing,
            costs=CostModel(),
            metrics=_metrics(expectancy_r=0.50, profit_factor=1.20),
            trades=(),
        ),
        passing.config_id: V3BacktestResult(
            config=passing,
            costs=CostModel(),
            metrics=_metrics(expectancy_r=0.10, profit_factor=1.40),
            trades=(),
        ),
    }

    def fake_backtest(*args: object, **kwargs: object) -> V3BacktestResult:
        config = args[1]
        assert isinstance(config, V3Config)
        return results[config.config_id]

    monkeypatch.setattr(optimize_v3, "run_v3_backtest", fake_backtest)
    search = optimize_v3.search_v3_dev([], configs=(failing, passing))
    assert search.gate_pass is True
    assert search.result.config == passing
