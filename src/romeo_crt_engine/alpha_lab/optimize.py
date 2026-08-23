from __future__ import annotations

import math
from collections.abc import Iterable, Sequence
from itertools import product

from romeo_crt_engine.alpha_lab.backtest import run_backtest
from romeo_crt_engine.alpha_lab.models import (
    BacktestResult,
    Bar,
    CostModel,
    DirectionMode,
    SearchResult,
    StrategyConfig,
)

DEV_MIN_TRADES = 100
DEV_MIN_PROFIT_FACTOR = 1.30
DEV_MAX_DRAWDOWN_PCT = 20.0
OOS_MIN_TRADES = 50
OOS_MIN_PROFIT_FACTOR = 1.15


def dev_gate(result: BacktestResult) -> bool:
    metrics = result.metrics
    profit_factor = metrics.profit_factor
    return (
        metrics.closed_trades >= DEV_MIN_TRADES
        and profit_factor is not None
        and profit_factor >= DEV_MIN_PROFIT_FACTOR
        and metrics.expectancy_r > 0
        and metrics.max_drawdown_pct <= DEV_MAX_DRAWDOWN_PCT
    )


def oos_gate(result: BacktestResult) -> bool:
    metrics = result.metrics
    profit_factor = metrics.profit_factor
    return (
        metrics.closed_trades >= OOS_MIN_TRADES
        and profit_factor is not None
        and profit_factor >= OOS_MIN_PROFIT_FACTOR
        and metrics.expectancy_r > 0
    )


def _score(result: BacktestResult) -> float:
    metrics = result.metrics
    if metrics.closed_trades < DEV_MIN_TRADES:
        return -1_000_000.0 + metrics.closed_trades
    profit_factor = metrics.profit_factor or 0.0
    return (
        metrics.expectancy_r * math.sqrt(metrics.closed_trades)
        + (0.10 * min(profit_factor, 3.0))
        - (0.02 * metrics.max_drawdown_pct)
    )


def default_search_space() -> Iterable[StrategyConfig]:
    lookbacks = (12, 24, 48)
    sweep_bps = (0.0, 5.0)
    reclaim_fractions = (0.0, 0.5)
    ema_pairs = ((0, 0), (24, 72))
    directions: tuple[DirectionMode, ...] = ("both", "long_only", "short_only")
    stop_buffers = (0.0, 0.25)
    targets = (1.0, 1.5, 2.0)
    holds = (12, 24)

    for (
        lookback,
        sweep,
        reclaim,
        ema_pair,
        direction,
        stop_buffer,
        target,
        hold,
    ) in product(
        lookbacks,
        sweep_bps,
        reclaim_fractions,
        ema_pairs,
        directions,
        stop_buffers,
        targets,
        holds,
    ):
        ema_fast, ema_slow = ema_pair
        yield StrategyConfig(
            lookback_hours=lookback,
            min_sweep_bps=sweep,
            reclaim_fraction=reclaim,
            ema_fast=ema_fast,
            ema_slow=ema_slow,
            direction_mode=direction,
            atr_period=14,
            stop_buffer_atr=stop_buffer,
            target_r=target,
            max_hold_bars=hold,
        )


def search_dev(
    bars: Sequence[Bar],
    *,
    costs: CostModel | None = None,
    configs: Iterable[StrategyConfig] | None = None,
) -> SearchResult:
    if costs is None:
        costs = CostModel()
    if configs is None:
        configs = default_search_space()

    best: BacktestResult | None = None
    best_score = -math.inf
    searched = 0
    for config in configs:
        result = run_backtest(bars, config, costs=costs)
        score = _score(result)
        searched += 1
        if best is None or score > best_score or (
            score == best_score and config.config_id < best.config.config_id
        ):
            best = result
            best_score = score

    if best is None:
        raise ValueError("search space must contain at least one configuration")
    return SearchResult(
        result=best,
        score=best_score,
        searched_configs=searched,
        gate_pass=dev_gate(best),
    )
