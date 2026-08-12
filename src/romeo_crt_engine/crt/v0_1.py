from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum
from itertools import pairwise
from math import isfinite
from typing import Final
from zoneinfo import ZoneInfo

STRATEGY_VERSION: Final = "CRT-C3-D1-H1-M1-BEAR-v0.1"
DOCTRINE_VERSION: Final = "CRT_SECRETS_2025"
FREEZE_PARAMETER_VERSION: Final = "P2_FREEZE_2026_08_12"
SOURCE_TIMEZONE: Final = "America/New_York"
_NY: Final = ZoneInfo(SOURCE_TIMEZONE)


class Timeframe(StrEnum):
    D1 = "D1"
    H1 = "H1"


class Direction(StrEnum):
    BEARISH = "BEARISH"


class DecisionState(StrEnum):
    NO_SIGNAL = "NO_SIGNAL"
    TRADE_PLAN = "TRADE_PLAN"


class ReasonCode(StrEnum):
    ELIGIBLE = "ELIGIBLE"
    INVALID_CALENDAR = "INVALID_CALENDAR"
    NON_CONSECUTIVE_PARENT = "NON_CONSECUTIVE_PARENT"
    NO_BEARISH_PARENT_SWEEP = "NO_BEARISH_PARENT_SWEEP"
    DOUBLE_OR_OPPOSITE_SWEEP = "DOUBLE_OR_OPPOSITE_SWEEP"
    PARENT_CLOSE_NOT_RECLAIMED = "PARENT_CLOSE_NOT_RECLAIMED"
    TARGET1_CONSUMED_IN_C2 = "TARGET1_CONSUMED_IN_C2"
    EXECUTION_DATA_OUTSIDE_C3 = "EXECUTION_DATA_OUTSIDE_C3"
    TARGET1_CONSUMED_PRE_ENTRY = "TARGET1_CONSUMED_PRE_ENTRY"
    NO_MODEL1_CONFIRMATION = "NO_MODEL1_CONFIRMATION"
    INVALID_TRADE_GEOMETRY = "INVALID_TRADE_GEOMETRY"


@dataclass(frozen=True, slots=True)
class ClosedCandle:
    timeframe: Timeframe
    open_time: datetime
    close_time: datetime
    open: float
    high: float
    low: float
    close: float

    def __post_init__(self) -> None:
        if self.open_time.utcoffset() is None or self.close_time.utcoffset() is None:
            raise ValueError("candle timestamps must be timezone-aware")
        if self.close_time <= self.open_time:
            raise ValueError("close_time must be after open_time")
        values = (self.open, self.high, self.low, self.close)
        if not all(isfinite(value) for value in values):
            raise ValueError("OHLC values must be finite")
        if self.high < self.low:
            raise ValueError("high must be >= low")
        if self.high < max(self.open, self.close):
            raise ValueError("high must contain open and close")
        if self.low > min(self.open, self.close):
            raise ValueError("low must contain open and close")

    @property
    def body_fraction(self) -> float:
        range_size = self.high - self.low
        if range_size == 0.0:
            return 0.0
        return abs(self.close - self.open) / range_size


@dataclass(frozen=True, slots=True)
class CandleWindow:
    timeframe: Timeframe
    open_time: datetime
    close_time: datetime
    open_price: float

    def __post_init__(self) -> None:
        if self.open_time.utcoffset() is None or self.close_time.utcoffset() is None:
            raise ValueError("window timestamps must be timezone-aware")
        if self.close_time <= self.open_time:
            raise ValueError("window close_time must be after open_time")
        if not isfinite(self.open_price):
            raise ValueError("open_price must be finite")


@dataclass(frozen=True, slots=True)
class FreezeParameters:
    model1_min_body_fraction: float = 0.50
    stop_buffer_ticks: int = 1

    def __post_init__(self) -> None:
        if not 0.0 < self.model1_min_body_fraction <= 1.0:
            raise ValueError("model1_min_body_fraction must be in (0, 1]")
        if self.stop_buffer_ticks < 0:
            raise ValueError("stop_buffer_ticks must be >= 0")


DEFAULT_PARAMETERS: Final = FreezeParameters()


@dataclass(frozen=True, slots=True)
class ParentContext:
    direction: Direction
    c1: ClosedCandle
    c2: ClosedCandle
    c3: CandleWindow
    key_level: float
    midpoint_50: float
    parent_structural_high: float


@dataclass(frozen=True, slots=True)
class TradePlan:
    strategy_version: str
    doctrine_version: str
    freeze_parameter_version: str
    direction: Direction
    entry_time: datetime
    entry_price: float
    stop_reference_price: float
    stop_price: float
    target_price: float
    key_level: float
    parent_c1_open_time: datetime
    parent_c2_open_time: datetime
    c3_open_time: datetime
    model1_open_time: datetime
    evidence_ids: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Evaluation:
    state: DecisionState
    reason: ReasonCode
    context: ParentContext | None = None
    trade_plan: TradePlan | None = None


def _is_local_midnight(timestamp: datetime) -> bool:
    local = timestamp.astimezone(_NY)
    return local.hour == 0 and local.minute == 0 and local.second == 0 and local.microsecond == 0


def is_canonical_daily(candle: ClosedCandle) -> bool:
    if candle.timeframe is not Timeframe.D1:
        return False
    if not _is_local_midnight(candle.open_time) or not _is_local_midnight(candle.close_time):
        return False
    local_open = candle.open_time.astimezone(_NY)
    local_close = candle.close_time.astimezone(_NY)
    return local_close.date() == local_open.date() + timedelta(days=1)


def is_canonical_h1(candle: ClosedCandle) -> bool:
    if candle.timeframe is not Timeframe.H1:
        return False
    local_open = candle.open_time.astimezone(_NY)
    local_close = candle.close_time.astimezone(_NY)
    if any((local_open.minute, local_open.second, local_open.microsecond)):
        return False
    if any((local_close.minute, local_close.second, local_close.microsecond)):
        return False
    return candle.close_time - candle.open_time == timedelta(hours=1)


def rolling_parent_pairs(
    daily: Sequence[ClosedCandle],
) -> tuple[tuple[ClosedCandle, ClosedCandle], ...]:
    """Enumerate every consecutive D1 pair without hindsight-based Candle-1 selection."""
    if len(daily) < 2:
        return ()
    pairs: list[tuple[ClosedCandle, ClosedCandle]] = []
    for first, second in pairwise(daily):
        if (
            is_canonical_daily(first)
            and is_canonical_daily(second)
            and first.close_time == second.open_time
        ):
            pairs.append((first, second))
    return tuple(pairs)


def qualify_bearish_parent(
    c1: ClosedCandle,
    c2: ClosedCandle,
    c3: CandleWindow,
) -> Evaluation:
    """Qualify the frozen bearish D1 Candle-1/Candle-2 state at Candle-3 open."""
    if not is_canonical_daily(c1) or not is_canonical_daily(c2):
        return Evaluation(DecisionState.NO_SIGNAL, ReasonCode.INVALID_CALENDAR)
    if (
        c3.timeframe is not Timeframe.D1
        or not _is_local_midnight(c3.open_time)
        or not _is_local_midnight(c3.close_time)
    ):
        return Evaluation(DecisionState.NO_SIGNAL, ReasonCode.INVALID_CALENDAR)
    if c1.close_time != c2.open_time or c2.close_time != c3.open_time:
        return Evaluation(DecisionState.NO_SIGNAL, ReasonCode.NON_CONSECUTIVE_PARENT)

    midpoint = (c1.high + c1.low) / 2.0

    if c2.high <= c1.high:
        return Evaluation(DecisionState.NO_SIGNAL, ReasonCode.NO_BEARISH_PARENT_SWEEP)
    if c2.low < c1.low:
        return Evaluation(DecisionState.NO_SIGNAL, ReasonCode.DOUBLE_OR_OPPOSITE_SWEEP)
    if not c1.low <= c2.close < c1.high:
        return Evaluation(DecisionState.NO_SIGNAL, ReasonCode.PARENT_CLOSE_NOT_RECLAIMED)
    if c2.low <= midpoint:
        return Evaluation(DecisionState.NO_SIGNAL, ReasonCode.TARGET1_CONSUMED_IN_C2)

    context = ParentContext(
        direction=Direction.BEARISH,
        c1=c1,
        c2=c2,
        c3=c3,
        key_level=c1.high,
        midpoint_50=midpoint,
        parent_structural_high=c2.high,
    )
    return Evaluation(DecisionState.NO_SIGNAL, ReasonCode.ELIGIBLE, context=context)


def is_bearish_model1_core(
    candle: ClosedCandle,
    reference_high: float,
    parameters: FreezeParameters = DEFAULT_PARAMETERS,
) -> bool:
    """Frozen Model-1-core project interpretation used only by v0.1."""
    return (
        is_canonical_h1(candle)
        and candle.close > candle.open
        and candle.low <= reference_high < candle.high
        and candle.body_fraction >= parameters.model1_min_body_fraction
    )


def evaluate_bearish_c3(
    c1: ClosedCandle,
    c2: ClosedCandle,
    c3: CandleWindow,
    h1_candles: Sequence[ClosedCandle],
    *,
    tick_size: float,
    parameters: FreezeParameters = DEFAULT_PARAMETERS,
) -> Evaluation:
    """Evaluate the frozen v0.1 setup using only completed information available at each step."""
    if not isfinite(tick_size) or tick_size <= 0.0:
        raise ValueError("tick_size must be positive and finite")

    parent_result = qualify_bearish_parent(c1, c2, c3)
    if parent_result.context is None:
        return parent_result
    context = parent_result.context

    ordered = tuple(sorted(h1_candles, key=lambda item: item.open_time))
    for candle in ordered:
        if not is_canonical_h1(candle):
            return Evaluation(
                DecisionState.NO_SIGNAL,
                ReasonCode.INVALID_CALENDAR,
                context=context,
            )
        if candle.open_time < c3.open_time or candle.close_time > c3.close_time:
            return Evaluation(
                DecisionState.NO_SIGNAL,
                ReasonCode.EXECUTION_DATA_OUTSIDE_C3,
                context=context,
            )

    active_model: ClosedCandle | None = None

    for candle in ordered:
        if candle.low <= context.midpoint_50:
            return Evaluation(
                DecisionState.NO_SIGNAL,
                ReasonCode.TARGET1_CONSUMED_PRE_ENTRY,
                context=context,
            )

        if active_model is not None:
            if candle.high > active_model.high:
                active_model = None
            else:
                confirmation_level = min(active_model.low, context.parent_structural_high)
                if candle.close < confirmation_level:
                    entry_price = candle.close
                    stop_reference = active_model.high
                    stop_price = stop_reference + (parameters.stop_buffer_ticks * tick_size)
                    target_price = context.midpoint_50
                    if not target_price < entry_price < stop_price:
                        return Evaluation(
                            DecisionState.NO_SIGNAL,
                            ReasonCode.INVALID_TRADE_GEOMETRY,
                            context=context,
                        )
                    plan = TradePlan(
                        strategy_version=STRATEGY_VERSION,
                        doctrine_version=DOCTRINE_VERSION,
                        freeze_parameter_version=FREEZE_PARAMETER_VERSION,
                        direction=Direction.BEARISH,
                        entry_time=candle.close_time,
                        entry_price=entry_price,
                        stop_reference_price=stop_reference,
                        stop_price=stop_price,
                        target_price=target_price,
                        key_level=context.key_level,
                        parent_c1_open_time=c1.open_time,
                        parent_c2_open_time=c2.open_time,
                        c3_open_time=c3.open_time,
                        model1_open_time=active_model.open_time,
                        evidence_ids=(
                            "ROMEO-2024-CRT",
                            "ROMEO-2024-TS",
                            "ROMEO-2025-S1",
                            "ROMEO-2025-S7",
                            "P0-FIX-002",
                            "P2-PARAM-M1-THICK-050",
                            "P2-PARAM-STOP-1TICK",
                        ),
                    )
                    return Evaluation(
                        DecisionState.TRADE_PLAN,
                        ReasonCode.ELIGIBLE,
                        context=context,
                        trade_plan=plan,
                    )

        if active_model is None and is_bearish_model1_core(
            candle,
            context.parent_structural_high,
            parameters,
        ):
            active_model = candle

    return Evaluation(
        DecisionState.NO_SIGNAL,
        ReasonCode.NO_MODEL1_CONFIRMATION,
        context=context,
    )
