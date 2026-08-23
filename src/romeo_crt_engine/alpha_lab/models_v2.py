from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256

from romeo_crt_engine.alpha_lab.models import (
    CostModel,
    Direction,
    DirectionMode,
    Metrics,
    Trade,
)


@dataclass(frozen=True, slots=True)
class V2Config:
    lookback_hours: int
    breakout_buffer_bps: float
    ema_fast: int
    ema_slow: int
    direction_mode: DirectionMode
    atr_period: int
    stop_atr: float
    target_r: float
    max_hold_bars: int
    risk_fraction: float = 0.01

    def __post_init__(self) -> None:
        if self.lookback_hours < 2:
            raise ValueError("lookback_hours must be >= 2")
        if self.breakout_buffer_bps < 0:
            raise ValueError("breakout_buffer_bps must be non-negative")
        if (self.ema_fast == 0) != (self.ema_slow == 0):
            raise ValueError("EMA periods must both be zero or both be positive")
        if self.ema_fast < 0 or self.ema_slow < 0:
            raise ValueError("EMA periods must be non-negative")
        if self.ema_fast and self.ema_fast >= self.ema_slow:
            raise ValueError("ema_fast must be less than ema_slow")
        if self.atr_period < 2:
            raise ValueError("atr_period must be >= 2")
        if self.stop_atr <= 0:
            raise ValueError("stop_atr must be positive")
        if self.target_r <= 0:
            raise ValueError("target_r must be positive")
        if self.max_hold_bars < 1:
            raise ValueError("max_hold_bars must be >= 1")
        if not 0 < self.risk_fraction <= 0.05:
            raise ValueError("risk_fraction must be in (0, 0.05]")

    @property
    def config_id(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))
        return "v2-" + sha256(payload.encode("utf-8")).hexdigest()[:20]


@dataclass(frozen=True, slots=True)
class V2Signal:
    signal_index: int
    direction: Direction
    atr: float
    reference_level: float


@dataclass(frozen=True, slots=True)
class V2BacktestResult:
    config: V2Config
    costs: CostModel
    metrics: Metrics
    trades: tuple[Trade, ...]


@dataclass(frozen=True, slots=True)
class V2SearchResult:
    result: V2BacktestResult
    score: float
    searched_configs: int
    gate_pass: bool
