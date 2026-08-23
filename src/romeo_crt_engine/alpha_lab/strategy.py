from __future__ import annotations

from collections import deque
from collections.abc import Sequence

from romeo_crt_engine.alpha_lab.models import Bar, Signal, StrategyConfig


def _ema(values: Sequence[float], period: int) -> list[float | None]:
    if period <= 0:
        return [None] * len(values)
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


def _rolling_extremes(
    bars: Sequence[Bar],
    lookback: int,
) -> tuple[list[float | None], list[float | None]]:
    highs: list[float | None] = [None] * len(bars)
    lows: list[float | None] = [None] * len(bars)
    high_queue: deque[int] = deque()
    low_queue: deque[int] = deque()

    for index, bar in enumerate(bars):
        while high_queue and high_queue[0] < index - lookback:
            high_queue.popleft()
        while low_queue and low_queue[0] < index - lookback:
            low_queue.popleft()

        if index >= lookback and high_queue and low_queue:
            highs[index] = bars[high_queue[0]].high
            lows[index] = bars[low_queue[0]].low

        while high_queue and bars[high_queue[-1]].high <= bar.high:
            high_queue.pop()
        while low_queue and bars[low_queue[-1]].low >= bar.low:
            low_queue.pop()
        high_queue.append(index)
        low_queue.append(index)

    return highs, lows


def generate_signals(bars: Sequence[Bar], config: StrategyConfig) -> tuple[Signal, ...]:
    """Generate causal close-confirmed false-break signals.

    The rolling reference excludes the current bar. A signal is known only after the signal bar
    closes; the simulator therefore enters no earlier than the next bar open.
    """
    if len(bars) < max(config.lookback_hours, config.atr_period, config.ema_slow) + 2:
        return ()

    rolling_highs, rolling_lows = _rolling_extremes(bars, config.lookback_hours)
    atr_values = _atr(bars, config.atr_period)
    closes = [bar.close for bar in bars]
    fast_values = _ema(closes, config.ema_fast)
    slow_values = _ema(closes, config.ema_slow)
    sweep_rate = config.min_sweep_bps / 10_000.0

    signals: list[Signal] = []
    for index in range(len(bars) - 1):
        reference_high = rolling_highs[index]
        reference_low = rolling_lows[index]
        atr_value = atr_values[index]
        if reference_high is None or reference_low is None or atr_value is None:
            continue

        bar = bars[index]
        bar_range = bar.high - bar.low
        if bar_range <= 0:
            continue

        long_allowed = config.direction_mode in ("both", "long_only")
        short_allowed = config.direction_mode in ("both", "short_only")
        if config.ema_fast:
            fast = fast_values[index]
            slow = slow_values[index]
            if fast is None or slow is None:
                continue
            long_allowed = long_allowed and fast > slow
            short_allowed = short_allowed and fast < slow

        long_reclaim = bar.close >= bar.low + (config.reclaim_fraction * bar_range)
        short_reclaim = bar.close <= bar.high - (config.reclaim_fraction * bar_range)
        swept_low = bar.low <= reference_low * (1.0 - sweep_rate) and bar.close > reference_low
        swept_high = bar.high >= reference_high * (1.0 + sweep_rate) and bar.close < reference_high

        long_signal = long_allowed and swept_low and long_reclaim
        short_signal = short_allowed and swept_high and short_reclaim

        # Outside bars that simultaneously sweep both sides are intentionally skipped. Their
        # intrabar ordering is unknowable from H1 OHLC and should not be guessed.
        if long_signal == short_signal:
            continue
        if long_signal:
            signals.append(
                Signal(
                    signal_index=index,
                    direction="long",
                    reference_level=reference_low,
                    signal_low=bar.low,
                    signal_high=bar.high,
                    atr=atr_value,
                )
            )
        else:
            signals.append(
                Signal(
                    signal_index=index,
                    direction="short",
                    reference_level=reference_high,
                    signal_low=bar.low,
                    signal_high=bar.high,
                    atr=atr_value,
                )
            )

    return tuple(signals)
