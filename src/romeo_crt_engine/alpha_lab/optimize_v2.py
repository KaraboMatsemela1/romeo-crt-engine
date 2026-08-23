from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from itertools import product

from romeo_crt_engine.alpha_lab.backtest_v2 import run_v2_backtest
from romeo_crt_engine.alpha_lab.models import Bar, CostModel, DirectionMode
from romeo_crt_engine.alpha_lab.models_v2 import V2BacktestResult, V2Config, V2SearchResult

DEV_MIN_TRADES = 100
DEV_MIN_PROFIT_FACTOR = 1.30
DEV_MAX_DRAWDOWN_PCT = 20.0
OOS_MIN_TRADES = 50
OOS_MIN_PROFIT_FACTOR = 1.15


def v2_dev_gate(result: V2BacktestResult) -> bool:
    metrics = result.metrics
    return (
        metrics.closed_trades >= DEV_MIN_TRADES
        and metrics.profit_factor is not None
        and metrics.profit_factor >= DEV_MIN_PROFIT_FACTOR
        and metrics.expectancy_r > 0
        and metrics.max_drawdown_pct <= DEV_MAX_DRAWDOWN_PCT
    )


def v2_oos_gate(result: V2BacktestResult) -> bool:
    metrics = result.metrics
    return (
        metrics.closed_trades >= OOS_MIN_TRADES
        and metrics.profit_factor is not None
        and metrics.profit_factor >= OOS_MIN_PROFIT_FACTOR
        and metrics.expectancy_r > 0
    )


def _score(result: V2BacktestResult) -> float:
    metrics = result.metrics
    if metrics.closed_trades < DEV_MIN_TRADES:
        return -1_000_000.0 + metrics.closed_trades
    profit_factor = metrics.profit_factor or 0.0
    return (
        metrics.expectancy_r * math.sqrt(metrics.closed_trades)
        + (0.10 * min(profit_factor, 3.0))
        - (0.02 * metrics.max_drawdown_pct)
    )


def v2_search_space() -> Iterable[V2Config]:
    lookbacks = (6, 12, 24, 48)
    buffers = (0.0, 5.0)
    ema_pairs = ((0, 0), (24, 72), (48, 200))
    directions: tuple[DirectionMode, ...] = ("both", "long_only", "short_only")
    stops = (1.0, 1.5, 2.0)
    targets = (1.5, 2.0, 3.0)
    holds = (24, 48)
    for lookback, buffer_bps, ema_pair, direction, stop_atr, target_r, hold in product(
        lookbacks,
        buffers,
        ema_pairs,
        directions,
        stops,
        targets,
        holds,
    ):
        ema_fast, ema_slow = ema_pair
        yield V2Config(
            lookback_hours=lookback,
            breakout_buffer_bps=buffer_bps,
            ema_fast=ema_fast,
            ema_slow=ema_slow,
            direction_mode=direction,
            atr_period=14,
            stop_atr=stop_atr,
            target_r=target_r,
            max_hold_bars=hold,
        )


def search_v2_dev(
    bars: Sequence[Bar],
    *,
    costs: CostModel | None = None,
    configs: Iterable[V2Config] | None = None,
) -> V2SearchResult:
    if costs is None:
        costs = CostModel()
    if configs is None:
        configs = v2_search_space()
    best_overall: V2BacktestResult | None = None
    best_overall_score = -math.inf
    best_passing: V2BacktestResult | None = None
    best_passing_score = -math.inf
    searched = 0
    for config in configs:
        result = run_v2_backtest(bars, config, costs=costs)
        score = _score(result)
        searched += 1
        if best_overall is None or score > best_overall_score or (
            score == best_overall_score and config.config_id < best_overall.config.config_id
        ):
            best_overall = result
            best_overall_score = score
        if v2_dev_gate(result) and (
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
    return V2SearchResult(
        result=selected,
        score=selected_score,
        searched_configs=searched,
        gate_pass=best_passing is not None,
    )
