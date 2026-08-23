from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256

from romeo_crt_engine.alpha_lab.models import CostModel, Metrics, Trade


@dataclass(frozen=True, slots=True)
class V4Config:
    entry_lookback: int
    breakout_buffer_bps: float
    use_rising_ema200_regime: bool
    atr_period: int
    initial_stop_atr: float
    trail_atr: float
    max_hold_bars: int
    risk_fraction: float = 0.01

    def __post_init__(self) -> None:
        if self.entry_lookback < 2:
            raise ValueError("entry_lookback must be >= 2")
        if self.breakout_buffer_bps < 0:
            raise ValueError("breakout_buffer_bps must be non-negative")
        if self.atr_period < 2:
            raise ValueError("atr_period must be >= 2")
        if self.initial_stop_atr <= 0 or self.trail_atr <= 0:
            raise ValueError("ATR stop multiples must be positive")
        if self.max_hold_bars < 2:
            raise ValueError("max_hold_bars must be >= 2")
        if not 0 < self.risk_fraction <= 0.05:
            raise ValueError("risk_fraction must be in (0, 0.05]")

    @property
    def config_id(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))
        return "v4-" + sha256(payload.encode("utf-8")).hexdigest()[:20]


@dataclass(frozen=True, slots=True)
class V4Signal:
    signal_index: int
    atr: float
    reference_high: float


@dataclass(frozen=True, slots=True)
class V4BacktestResult:
    config: V4Config
    costs: CostModel
    metrics: Metrics
    trades: tuple[Trade, ...]


@dataclass(frozen=True, slots=True)
class V4SearchResult:
    result: V4BacktestResult
    score: float
    searched_configs: int
    gate_pass: bool
