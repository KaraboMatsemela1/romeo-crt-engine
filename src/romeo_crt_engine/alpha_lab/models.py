from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from hashlib import sha256
from typing import Literal

Direction = Literal["long", "short"]
DirectionMode = Literal["both", "long_only", "short_only"]
ExitReason = Literal["target", "stop", "stop_same_bar", "max_hold"]


@dataclass(frozen=True, slots=True)
class Bar:
    open_time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

    def __post_init__(self) -> None:
        if self.open_time.tzinfo is None:
            raise ValueError("bar timestamps must be timezone-aware")
        if self.low > min(self.open, self.close, self.high):
            raise ValueError("low must not exceed OHLC values")
        if self.high < max(self.open, self.close, self.low):
            raise ValueError("high must not be below OHLC values")
        if self.low <= 0 or self.open <= 0 or self.high <= 0 or self.close <= 0:
            raise ValueError("prices must be positive")
        if self.volume < 0:
            raise ValueError("volume must be non-negative")


@dataclass(frozen=True, slots=True)
class CostModel:
    fee_bps_per_side: float = 4.0
    slippage_bps_per_side: float = 2.0
    max_leverage: float = 3.0

    def __post_init__(self) -> None:
        if self.fee_bps_per_side < 0 or self.slippage_bps_per_side < 0:
            raise ValueError("costs must be non-negative")
        if self.max_leverage <= 0:
            raise ValueError("max_leverage must be positive")


@dataclass(frozen=True, slots=True)
class StrategyConfig:
    lookback_hours: int
    min_sweep_bps: float
    reclaim_fraction: float
    ema_fast: int
    ema_slow: int
    direction_mode: DirectionMode
    atr_period: int
    stop_buffer_atr: float
    target_r: float
    max_hold_bars: int
    risk_fraction: float = 0.01

    def __post_init__(self) -> None:
        if self.lookback_hours < 2:
            raise ValueError("lookback_hours must be >= 2")
        if self.min_sweep_bps < 0:
            raise ValueError("min_sweep_bps must be non-negative")
        if not 0 <= self.reclaim_fraction <= 1:
            raise ValueError("reclaim_fraction must be between 0 and 1")
        if (self.ema_fast == 0) != (self.ema_slow == 0):
            raise ValueError("EMA periods must both be zero or both be positive")
        if self.ema_fast < 0 or self.ema_slow < 0:
            raise ValueError("EMA periods must be non-negative")
        if self.ema_fast and self.ema_fast >= self.ema_slow:
            raise ValueError("ema_fast must be less than ema_slow")
        if self.atr_period < 2:
            raise ValueError("atr_period must be >= 2")
        if self.stop_buffer_atr < 0:
            raise ValueError("stop_buffer_atr must be non-negative")
        if self.target_r <= 0:
            raise ValueError("target_r must be positive")
        if self.max_hold_bars < 1:
            raise ValueError("max_hold_bars must be >= 1")
        if not 0 < self.risk_fraction <= 0.05:
            raise ValueError("risk_fraction must be in (0, 0.05]")

    @property
    def config_id(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))
        return sha256(payload.encode("utf-8")).hexdigest()[:20]


@dataclass(frozen=True, slots=True)
class Signal:
    signal_index: int
    direction: Direction
    reference_level: float
    signal_low: float
    signal_high: float
    atr: float


@dataclass(frozen=True, slots=True)
class Trade:
    direction: Direction
    signal_time: datetime
    entry_time: datetime
    exit_time: datetime
    entry_price: float
    exit_price: float
    stop_price: float
    target_price: float
    quantity: float
    risk_budget: float
    gross_pnl: float
    fees: float
    net_pnl: float
    r_multiple: float
    exit_reason: ExitReason


@dataclass(frozen=True, slots=True)
class Metrics:
    closed_trades: int
    wins: int
    losses: int
    win_rate: float
    expectancy_r: float
    profit_factor: float | None
    net_pnl: float
    return_pct: float
    max_drawdown_pct: float
    final_equity: float


@dataclass(frozen=True, slots=True)
class BacktestResult:
    config: StrategyConfig
    costs: CostModel
    metrics: Metrics
    trades: tuple[Trade, ...]


@dataclass(frozen=True, slots=True)
class Dataset:
    symbol: str
    start: datetime
    end: datetime
    bars: tuple[Bar, ...]
    dataset_sha256: str
    source_hashes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SearchResult:
    result: BacktestResult
    score: float
    searched_configs: int
    gate_pass: bool
