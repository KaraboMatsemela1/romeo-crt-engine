"""Deterministic event-driven simulation for frozen CRT detector outputs."""

from romeo_crt_engine.backtest.engine import run_backtest
from romeo_crt_engine.backtest.models import (
    BASE_COSTS,
    IDEAL_COSTS,
    SEVERE_COSTS,
    SIMULATOR_VERSION,
    STRESSED_COSTS,
    BacktestConfig,
    BacktestResult,
    CostModel,
    ExitReason,
    RejectionReason,
)

__all__ = [
    "BASE_COSTS",
    "IDEAL_COSTS",
    "SEVERE_COSTS",
    "SIMULATOR_VERSION",
    "STRESSED_COSTS",
    "BacktestConfig",
    "BacktestResult",
    "CostModel",
    "ExitReason",
    "RejectionReason",
    "run_backtest",
]
