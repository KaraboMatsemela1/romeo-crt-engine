from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256

from romeo_crt_engine.alpha_lab.models import CostModel, Direction, Metrics, Trade


@dataclass(frozen=True, slots=True)
class V3Config:
    lookback_hours: int
    breakout_buffer_bps: float
    use_ema200_regime: bool
    volatility_ratio_min: float
    close_location_min: float
    atr_period: int
    volatility_lookback: int
    stop_atr: float
    target_r: float
    max_hold_bars: int
    risk_fraction: float = 0.01

    def __post_init__(self) -> None:
        if self.lookback_hours < 2:
            raise ValueError("lookback_hours must be >= 2")
        if self.breakout_buffer_bps < 0:
            raise ValueError("breakout_buffer_bps must be non-negative")
        if self.volatility_ratio_min <= 0:
            raise ValueError("volatility_ratio_min must be positive")
        if not 0 <= self.close_location_min <= 1:
            raise ValueError("close_location_min must be in [0, 1]")
        if self.atr_period < 2:
            raise ValueError("atr_period must be >= 2")
        if self.volatility_lookback < 2:
            raise ValueError("volatility_lookback must be >= 2")
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
        return "v3-" + sha256(payload.encode("utf-8")).hexdigest()[:20]


@dataclass(frozen=True, slots=True)
class V3Signal:
    signal_index: int
    direction: Direction
    atr: float
    reference_level: float
    observed_volatility_ratio: float
    close_location: float


@dataclass(frozen=True, slots=True)
class V3BacktestResult:
    config: V3Config
    costs: CostModel
    metrics: Metrics
    trades: tuple[Trade, ...]


@dataclass(frozen=True, slots=True)
class V3SearchResult:
    result: V3BacktestResult
    score: float
    searched_configs: int
    gate_pass: bool
