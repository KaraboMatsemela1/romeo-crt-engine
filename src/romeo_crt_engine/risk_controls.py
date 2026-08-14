"""Fail-closed synthetic risk and order safety controls."""

from dataclasses import dataclass
from enum import StrEnum
from math import floor


class RiskDecision(StrEnum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"


@dataclass(frozen=True)
class RiskConfig:
    risk_per_trade: float = 0.01
    max_concurrent_positions: int = 1
    max_session_loss: float = 0.02
    max_stale_seconds: int = 60
    max_spread: float = 0.0005
    unit_precision: int = 0
    kill_switch_engaged: bool = True


@dataclass(frozen=True)
class OrderSafetyInput:
    equity: float
    requested_risk: float
    concurrent_positions: int
    session_loss: float
    market_age_seconds: int
    spread: float
    session_eligible: bool
    stop_distance: float
    value_per_unit: float


@dataclass(frozen=True)
class RiskResult:
    decision: RiskDecision
    reasons: tuple[str, ...]
    units: int = 0


def rounded_units(
    equity: float,
    risk: float,
    stop_distance: float,
    value_per_unit: float,
    precision: int,
) -> int:
    if equity <= 0 or risk <= 0 or stop_distance <= 0 or value_per_unit <= 0:
        raise ValueError("position sizing inputs must be positive")
    raw = equity * risk / (stop_distance * value_per_unit)
    factor = 10**precision
    return int(floor(raw * factor) // factor)


def check_order(config: RiskConfig, request: OrderSafetyInput) -> RiskResult:
    failures: list[str] = []
    if config.kill_switch_engaged:
        failures.append("kill switch is engaged")
    if request.requested_risk > config.risk_per_trade:
        failures.append("requested risk exceeds per-trade limit")
    if request.concurrent_positions >= config.max_concurrent_positions:
        failures.append("maximum concurrent positions reached")
    if request.session_loss >= config.max_session_loss:
        failures.append("session loss limit reached")
    if request.market_age_seconds > config.max_stale_seconds:
        failures.append("market data is stale")
    if request.spread > config.max_spread:
        failures.append("spread exceeds limit")
    if not request.session_eligible:
        failures.append("session is not eligible")
    try:
        units = rounded_units(
            request.equity,
            request.requested_risk,
            request.stop_distance,
            request.value_per_unit,
            config.unit_precision,
        )
    except ValueError as error:
        failures.append(str(error))
        units = 0
    if units <= 0:
        failures.append("calculated position size is zero")
    if failures:
        return RiskResult(RiskDecision.REJECT, tuple(failures), units)
    return RiskResult(RiskDecision.ACCEPT, (), units)
