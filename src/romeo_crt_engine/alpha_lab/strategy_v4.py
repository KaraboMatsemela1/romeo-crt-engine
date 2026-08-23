from __future__ import annotations

from collections import deque
from collections.abc import Sequence

from romeo_crt_engine.alpha_lab.models import Bar
from romeo_crt_engine.alpha_lab.models_v4 import V4Config, V4Signal


def ema_series(values: Sequence[float], period: int) -> list[float | None]:
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


def atr_series(bars: Sequence[Bar], period: int) -> list[float | None]:
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


def rolling_prior_highs(bars: Sequence[Bar], lookback: int) -> list[float | None]:
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


def generate_v4_signals(bars: Sequence[Bar], config: V4Config) -> tuple[V4Signal, ...]:
    regime_warmup = 224 if config.use_rising_ema200_regime else 0
    warmup = max(config.entry_lookback, config.atr_period + 1, regime_warmup)
    if len(bars) < warmup + 2:
        return ()

    highs = rolling_prior_highs(bars, config.entry_lookback)
    atr_values = atr_series(bars, config.atr_period)
    ema200 = (
        ema_series([bar.close for bar in bars], 200)
        if config.use_rising_ema200_regime
        else None
    )
    buffer_rate = config.breakout_buffer_bps / 10_000.0

    signals: list[V4Signal] = []
    for index in range(warmup, len(bars) - 1):
        reference_high = highs[index]
        atr_value = atr_values[index]
        if reference_high is None or atr_value is None:
            continue
        bar = bars[index]
        if bar.close <= reference_high * (1.0 + buffer_rate):
            continue
        if config.use_rising_ema200_regime:
            assert ema200 is not None
            current_ema = ema200[index]
            prior_ema = ema200[index - 24]
            if (
                current_ema is None
                or prior_ema is None
                or bar.close <= current_ema
                or current_ema <= prior_ema
            ):
                continue
        signals.append(
            V4Signal(
                signal_index=index,
                atr=atr_value,
                reference_high=reference_high,
            )
        )
    return tuple(signals)
