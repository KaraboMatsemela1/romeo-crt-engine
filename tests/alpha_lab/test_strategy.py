from __future__ import annotations

from datetime import UTC, datetime, timedelta

from romeo_crt_engine.alpha_lab.models import Bar, StrategyConfig
from romeo_crt_engine.alpha_lab.strategy import generate_signals


def _bar(hour: int, o: float, h: float, l: float, c: float) -> Bar:
    return Bar(
        open_time=datetime(2024, 2, 1, tzinfo=UTC) + timedelta(hours=hour),
        open=o,
        high=h,
        low=l,
        close=c,
        volume=1.0,
    )


def test_outside_bar_sweeping_both_sides_is_skipped() -> None:
    bars = [
        _bar(0, 105, 110, 100, 105),
        _bar(1, 105, 109, 101, 105),
        _bar(2, 105, 108, 102, 105),
        _bar(3, 105, 111, 99, 105),
        _bar(4, 105, 106, 104, 105),
        _bar(5, 105, 106, 104, 105),
    ]
    config = StrategyConfig(
        lookback_hours=3,
        min_sweep_bps=0.0,
        reclaim_fraction=0.0,
        ema_fast=0,
        ema_slow=0,
        direction_mode="both",
        atr_period=2,
        stop_buffer_atr=0.0,
        target_r=1.0,
        max_hold_bars=2,
    )
    assert generate_signals(bars, config) == ()
