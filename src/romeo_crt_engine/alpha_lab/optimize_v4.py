from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from itertools import product

from romeo_crt_engine.alpha_lab.backtest_v4 import run_v4_backtest
from romeo_crt_engine.alpha_lab.models import Bar, CostModel
from romeo_crt_engine.alpha_lab.models_v4 import V4BacktestResult, V4Config, V4SearchResult

DEV_MIN_TRADES = 100
DEV_MIN_PROFIT_FACTOR = 1.30
HOLDOUT_A_MIN_TRADES = 100
HOLDOUT_A_MIN_PROFIT_FACTOR = 1.15
HOLDOUT_B_MIN_TRADES = 50
HOLDOUT_B_MIN_PROFIT_FACTOR = 1.15
MAX_DRAWDOWN_PCT = 20.0


def _gate(result: V4BacktestResult, *, min_trades: int, min_profit_factor: float) -> bool:
    metrics = result.metrics
    return (
        metrics.closed_trades >= min_trades
        and metrics.profit_factor is not None
        and metrics.profit_factor >= min_profit_factor
        and metrics.expectancy_r > 0
        and metrics.max_drawdown_pct <= MAX_DRAWDOWN_PCT
    )


def v4_dev_gate(result: V4BacktestResult) -> bool:
    return _gate(
        result,
        min_trades=DEV_MIN_TRADES,
        min_profit_factor=DEV_MIN_PROFIT_FACTOR,
    )


def v4_holdout_a_gate(result: V4BacktestResult) -> bool:
    return _gate(
        result,
        min_trades=HOLDOUT_A_MIN_TRADES,
        min_profit_factor=HOLDOUT_A_MIN_PROFIT_FACTOR,
    )


def v4_holdout_b_gate(result: V4BacktestResult) -> bool:
    return _gate(
        result,
        min_trades=HOLDOUT_B_MIN_TRADES,
        min_profit_factor=HOLDOUT_B_MIN_PROFIT_FACTOR,
    )


def _score(result: V4BacktestResult) -> float:
    metrics = result.metrics
    if metrics.closed_trades < DEV_MIN_TRADES:
        return -1_000_000.0 + metrics.closed_trades
    profit_factor = metrics.profit_factor or 0.0
    return (
        metrics.expectancy_r * math.sqrt(metrics.closed_trades)
        + (0.10 * min(profit_factor, 3.0))
        - (0.02 * metrics.max_drawdown_pct)
    )


def v4_search_space() -> Iterable[V4Config]:
    for (
        entry_lookback,
        buffer_bps,
        use_regime,
        initial_stop_atr,
        trail_atr,
        max_hold,
    ) in product(
        (24, 48, 96),
        (0.0, 10.0),
        (False, True),
        (1.5, 2.5),
        (2.0, 3.0, 4.0),
        (72, 168),
    ):
        yield V4Config(
            entry_lookback=entry_lookback,
            breakout_buffer_bps=buffer_bps,
            use_rising_ema200_regime=use_regime,
            atr_period=14,
            initial_stop_atr=initial_stop_atr,
            trail_atr=trail_atr,
            max_hold_bars=max_hold,
        )


def search_v4_dev(
    bars: Sequence[Bar],
    *,
    costs: CostModel | None = None,
    configs: Iterable[V4Config] | None = None,
) -> V4SearchResult:
    if costs is None:
        costs = CostModel()
    if configs is None:
        configs = v4_search_space()

    best_overall: V4BacktestResult | None = None
    best_overall_score = -math.inf
    best_passing: V4BacktestResult | None = None
    best_passing_score = -math.inf
    searched = 0
    for config in configs:
        result = run_v4_backtest(bars, config, costs=costs)
        score = _score(result)
        searched += 1
        if best_overall is None or score > best_overall_score or (
            score == best_overall_score and config.config_id < best_overall.config.config_id
        ):
            best_overall = result
            best_overall_score = score
        if v4_dev_gate(result) and (
            best_passing is None
            or score > best_passing_score
            or (score == best_passing_score and config.config_id < best_passing.config.config_id)
        ):
            best_passing = result
            best_passing_score = score

    if best_overall is None:
        raise ValueError("search space must contain at least one configuration")
    selected = best_passing if best_passing is not None else best_overall
    selected_score = best_passing_score if best_passing is not None else best_overall_score
    return V4SearchResult(
        result=selected,
        score=selected_score,
        searched_configs=searched,
        gate_pass=best_passing is not None,
    )
