from __future__ import annotations

from dataclasses import replace

from pytest import MonkeyPatch

from romeo_crt_engine.alpha_lab import optimize
from romeo_crt_engine.alpha_lab.models import (
    BacktestResult,
    CostModel,
    Metrics,
    StrategyConfig,
)


def _config(*, target_r: float) -> StrategyConfig:
    return StrategyConfig(
        lookback_hours=12,
        min_sweep_bps=0.0,
        reclaim_fraction=0.0,
        ema_fast=0,
        ema_slow=0,
        direction_mode="both",
        atr_period=14,
        stop_buffer_atr=0.0,
        target_r=target_r,
        max_hold_bars=12,
    )


def _result(config: StrategyConfig, metrics: Metrics) -> BacktestResult:
    return BacktestResult(config=config, costs=CostModel(), metrics=metrics, trades=())


def test_search_prefers_gate_passing_candidate(monkeypatch: MonkeyPatch) -> None:
    failing = _config(target_r=1.0)
    passing = _config(target_r=2.0)
    base_metrics = Metrics(
        closed_trades=120,
        wins=70,
        losses=50,
        win_rate=70 / 120,
        expectancy_r=0.10,
        profit_factor=1.40,
        net_pnl=1000.0,
        return_pct=1.0,
        max_drawdown_pct=10.0,
        final_equity=101_000.0,
    )
    results = {
        failing.config_id: _result(
            failing,
            replace(base_metrics, profit_factor=1.20, expectancy_r=0.50),
        ),
        passing.config_id: _result(passing, base_metrics),
    }

    def fake_backtest(*args: object, **kwargs: object) -> BacktestResult:
        config = args[1]
        assert isinstance(config, StrategyConfig)
        return results[config.config_id]

    monkeypatch.setattr(optimize, "run_backtest", fake_backtest)
    search = optimize.search_dev([], configs=(failing, passing))

    assert search.gate_pass is True
    assert search.result.config == passing
