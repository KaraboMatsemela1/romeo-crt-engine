from __future__ import annotations

from collections import deque
from collections.abc import Sequence
from statistics import median

from romeo_crt_engine.alpha_lab.models import Bar
from romeo_crt_engine.alpha_lab.models_v3 import V3Config, V3Signal


def _ema(values: Sequence[float], period: int) -> list[float | None]:
    result: list[float | None] = [None] * len(values)
    if len(values) < period:
        return result
    seed = sum(values[:period]) / period
    result[period - 1] = seed
    multiplier = 2.0 / (period + 1.0)
    previous = seed
    for index in range(period, len(values)):
        previous = ((values[index] - previous) * multiplier) + previous
        result[index] = previous
    return result


def _atr(bars: Sequence[Bar], period: int) -> list[float | None]:
    result: list[float | None] = [None] * len(bars)
    if len(bars) < period + 1:
        return result
    true_ranges: list[float] = []
    for index, bar in enumerate(bars):
        if index == 0:
            true_ranges.append(bar.high - bar.low)
            continue
        previous_close = bars[index - 1].close
        true_ranges.append(
            max(
                bar.high - bar.low,
                abs(bar.high - previous_close),
                abs(bar.low - previous_close),
            )
        )
    seed = sum(true_ranges[1 : period + 1]) / period
    result[period] = seed
    previous = seed
    for index in range(period + 1, len(bars)):
        previous = ((previous * (period - 1)) + true_ranges[index]) / period
        result[index] = previous
    return result


def _rolling_highs(bars: Sequence[Bar], lookback: int) -> list[float | None]:
    highs: list[float | None] = [None] * len(bars)
    queue: deque[int] = deque()
    for index, bar in enumerate(bars):
        while queue and queue[0] < index - lookback:
            queue.popleft()
        if index >= lookback and queue:
            highs[index] = bars[queue[0]].high
        while queue and bars[queue[-1]].high <= bar.high:
            queue.pop()
        queue.append(index)
    return highs


def generate_v3_signals(bars: Sequence[Bar], config: V3Config) -> tuple[V3Signal, ...]:
    ema_period = 200 if config.use_ema200_regime else 0
    warmup = max(
        config.lookback_hours,
        config.atr_period + config.volatility_lookback + 1,
        ema_period,
    )
    if len(bars) < warmup + 2:
        return ()

    rolling_highs = _rolling_highs(bars, config.lookback_hours)
    atr_values = _atr(bars, config.atr_period)
    ema200 = _ema([bar.close for bar in bars], 200) if config.use_ema200_regime else None
    buffer_rate = config.breakout_buffer_bps / 10_000.0

    signals: list[V3Signal] = []
    for index in range(warmup, len(bars) - 1):
        reference_high = rolling_highs[index]
        atr_value = atr_values[index]
        if reference_high is None or atr_value is None:
            continue

        prior_atrs = atr_values[index - config.volatility_lookback : index]
        if len(prior_atrs) != config.volatility_lookback or any(
            value is None for value in prior_atrs
        ):
            continue
        comparable_atrs = [value for value in prior_atrs if value is not None]
        baseline_atr = median(comparable_atrs)
        if baseline_atr <= 0:
            continue
        observed_ratio = atr_value / baseline_atr
        if observed_ratio < config.volatility_ratio_min:
            continue

        bar = bars[index]
        candle_range = bar.high - bar.low
        if candle_range <= 0:
            continue
        close_location = (bar.close - bar.low) / candle_range
        if close_location < config.close_location_min:
            continue

        if config.use_ema200_regime:
            assert ema200 is not None
            regime_value = ema200[index]
            if regime_value is None or bar.close <= regime_value:
                continue

        if bar.close <= reference_high * (1.0 + buffer_rate):
            continue
        signals.append(
            V3Signal(
                signal_index=index,
                direction="long",
                atr=atr_value,
                reference_level=reference_high,
                observed_volatility_ratio=observed_ratio,
                close_location=close_location,
            )
        )
    return tuple(signals)
