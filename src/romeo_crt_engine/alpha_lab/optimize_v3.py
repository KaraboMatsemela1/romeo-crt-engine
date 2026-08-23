from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from itertools import product

from romeo_crt_engine.alpha_lab.backtest_v3 import run_v3_backtest
from romeo_crt_engine.alpha_lab.models import Bar, CostModel
from romeo_crt_engine.alpha_lab.models_v3 import V3BacktestResult, V3Config, V3SearchResult

DEV_MIN_TRADES = 100
DEV_MIN_PROFIT_FACTOR = 1.30
DEV_MAX_DRAWDOWN_PCT = 20.0
OOS_MIN_TRADES = 50
OOS_MIN_PROFIT_FACTOR = 1.15


def v3_dev_gate(result: V3BacktestResult) -> bool:
    metrics = result.metrics
    return (
        metrics.closed_trades >= DEV_MIN_TRADES
        and metrics.profit_factor is not None
        and metrics.profit_factor >= DEV_MIN_PROFIT_FACTOR
        and metrics.expectancy_r > 0
        and metrics.max_drawdown_pct <= DEV_MAX_DRAWDOWN_PCT
    )


def v3_oos_gate(result: V3BacktestResult) -> bool:
    metrics = result.metrics
    return (
        metrics.closed_trades >= OOS_MIN_TRADES
        and metrics.profit_factor is not None
        and metrics.profit_factor >= OOS_MIN_PROFIT_FACTOR
        and metrics.expectancy_r > 0
    )


def _score(result: V3BacktestResult) -> float:
    metrics = result.metrics
    if metrics.closed_trades < DEV_MIN_TRADES:
        return -1_000_000.0 + metrics.closed_trades
    profit_factor = metrics.profit_factor or 0.0
    return (
        metrics.expectancy_r * math.sqrt(metrics.closed_trades)
        + (0.10 * min(profit_factor, 3.0))
        - (0.02 * metrics.max_drawdown_pct)
    )


def v3_search_space() -> Iterable[V3Config]:
    lookbacks = (24, 48)
    buffers = (0.0, 5.0, 10.0)
    regimes = (False, True)
    volatility_ratios = (0.8, 1.0, 1.2)
    close_locations = (0.50, 0.75)
    stops = (1.5, 2.0)
    targets = (2.0, 3.0)
    holds = (24, 48)
    for (
        lookback,
        buffer_bps,
        use_regime,
        volatility_ratio,
        close_location,
        stop_atr,
        target_r,
        hold,
    ) in product(
        lookbacks,
        buffers,
        regimes,
        volatility_ratios,
        close_locations,
        stops,
        targets,
        holds,
    ):
        yield V3Config(
            lookback_hours=lookback,
            breakout_buffer_bps=buffer_bps,
            use_ema200_regime=use_regime,
            volatility_ratio_min=volatility_ratio,
            close_location_min=close_location,
            atr_period=14,
            volatility_lookback=48,
            stop_atr=stop_atr,
            target_r=target_r,
            max_hold_bars=hold,
        )


def search_v3_dev(
    bars: Sequence[Bar],
    *,
    costs: CostModel | None = None,
    configs: Iterable[V3Config] | None = None,
) -> V3SearchResult:
    if costs is None:
        costs = CostModel()
    if configs is None:
        configs = v3_search_space()
    best_overall: V3BacktestResult | None = None
    best_overall_score = -math.inf
    best_passing: V3BacktestResult | None = None
    best_passing_score = -math.inf
    searched = 0
    for config in configs:
        result = run_v3_backtest(bars, config, costs=costs)
        score = _score(result)
        searched += 1
        if best_overall is None or score > best_overall_score or (
            score == best_overall_score and config.config_id < best_overall.config.config_id
        ):
            best_overall = result
            best_overall_score = score
        if v3_dev_gate(result) and (
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
    return V3SearchResult(
        result=selected,
        score=selected_score,
        searched_configs=searched,
        gate_pass=best_passing is not None,
    )
