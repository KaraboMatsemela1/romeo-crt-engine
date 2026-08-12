from datetime import datetime
from zoneinfo import ZoneInfo

from romeo_crt_engine.crt.v0_1 import (
    CandleWindow,
    ClosedCandle,
    DecisionState,
    ReasonCode,
    Timeframe,
    evaluate_bearish_c3,
    is_canonical_daily,
    is_canonical_daily_window,
    is_canonical_h1,
    rolling_parent_pairs,
)

NY = ZoneInfo("America/New_York")


def _daily(open_time: datetime, close_time: datetime, high: float, low: float) -> ClosedCandle:
    midpoint = (high + low) / 2.0
    return ClosedCandle(
        timeframe=Timeframe.D1,
        open_time=open_time,
        close_time=close_time,
        open=midpoint,
        high=high,
        low=low,
        close=midpoint,
    )


def _h1(open_time: datetime, close_time: datetime) -> ClosedCandle:
    return ClosedCandle(
        timeframe=Timeframe.H1,
        open_time=open_time,
        close_time=close_time,
        open=100.0,
        high=102.0,
        low=99.0,
        close=101.0,
    )


def test_daily_calendar_preserves_new_york_midnight_through_spring_dst() -> None:
    candle = _daily(
        datetime(2026, 3, 8, 0, 0, tzinfo=NY),
        datetime(2026, 3, 9, 0, 0, tzinfo=NY),
        110.0,
        90.0,
    )
    assert is_canonical_daily(candle)
    assert candle.close_time.timestamp() - candle.open_time.timestamp() == 23 * 60 * 60


def test_daily_calendar_preserves_new_york_midnight_through_fall_dst() -> None:
    candle = _daily(
        datetime(2026, 11, 1, 0, 0, tzinfo=NY),
        datetime(2026, 11, 2, 0, 0, tzinfo=NY),
        110.0,
        90.0,
    )
    assert is_canonical_daily(candle)
    assert candle.close_time.timestamp() - candle.open_time.timestamp() == 25 * 60 * 60


def test_h1_calendar_accepts_spring_forward_elapsed_hour() -> None:
    candle = _h1(
        datetime(2026, 3, 8, 1, 0, tzinfo=NY),
        datetime(2026, 3, 8, 3, 0, tzinfo=NY),
    )
    assert is_canonical_h1(candle)
    assert candle.close_time.timestamp() - candle.open_time.timestamp() == 60 * 60


def test_h1_calendar_accepts_repeated_fall_back_hour() -> None:
    candle = _h1(
        datetime(2026, 11, 1, 1, 0, tzinfo=NY, fold=0),
        datetime(2026, 11, 1, 1, 0, tzinfo=NY, fold=1),
    )
    assert is_canonical_h1(candle)
    assert candle.close_time.timestamp() - candle.open_time.timestamp() == 60 * 60


def test_daily_window_rejects_two_local_days_even_with_midnight_endpoints() -> None:
    window = CandleWindow(
        Timeframe.D1,
        datetime(2026, 1, 7, 0, 0, tzinfo=NY),
        datetime(2026, 1, 9, 0, 0, tzinfo=NY),
        108.0,
    )
    assert not is_canonical_daily_window(window)


def test_rolling_parent_pairs_enumerate_all_consecutive_daily_candidates() -> None:
    first = _daily(
        datetime(2026, 1, 5, 0, 0, tzinfo=NY),
        datetime(2026, 1, 6, 0, 0, tzinfo=NY),
        110.0,
        90.0,
    )
    second = _daily(
        datetime(2026, 1, 6, 0, 0, tzinfo=NY),
        datetime(2026, 1, 7, 0, 0, tzinfo=NY),
        112.0,
        100.0,
    )
    third = _daily(
        datetime(2026, 1, 7, 0, 0, tzinfo=NY),
        datetime(2026, 1, 8, 0, 0, tzinfo=NY),
        113.0,
        101.0,
    )

    pairs = rolling_parent_pairs((first, second, third))
    assert pairs == ((first, second), (second, third))


def test_future_h1_confirmation_outside_c3_cannot_authorize_entry() -> None:
    c1 = ClosedCandle(
        Timeframe.D1,
        datetime(2025, 9, 15, 0, 0, tzinfo=NY),
        datetime(2025, 9, 16, 0, 0, tzinfo=NY),
        100.0,
        110.0,
        90.0,
        105.0,
    )
    c2 = ClosedCandle(
        Timeframe.D1,
        datetime(2025, 9, 16, 0, 0, tzinfo=NY),
        datetime(2025, 9, 17, 0, 0, tzinfo=NY),
        105.0,
        112.0,
        103.0,
        108.0,
    )
    c3 = CandleWindow(
        Timeframe.D1,
        datetime(2025, 9, 17, 0, 0, tzinfo=NY),
        datetime(2025, 9, 18, 0, 0, tzinfo=NY),
        108.0,
    )
    model = ClosedCandle(
        Timeframe.H1,
        datetime(2025, 9, 17, 23, 0, tzinfo=NY),
        datetime(2025, 9, 18, 0, 0, tzinfo=NY),
        108.0,
        113.0,
        107.0,
        112.0,
    )
    future_confirmation = ClosedCandle(
        Timeframe.H1,
        datetime(2025, 9, 18, 0, 0, tzinfo=NY),
        datetime(2025, 9, 18, 1, 0, tzinfo=NY),
        112.0,
        112.0,
        105.0,
        106.0,
    )

    result = evaluate_bearish_c3(
        c1,
        c2,
        c3,
        (model, future_confirmation),
        tick_size=0.25,
    )
    assert result.state is DecisionState.NO_SIGNAL
    assert result.reason is ReasonCode.EXECUTION_DATA_OUTSIDE_C3
