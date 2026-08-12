import json
from datetime import datetime
from pathlib import Path

from romeo_crt_engine.crt.v0_1 import (
    CandleWindow,
    ClosedCandle,
    DecisionState,
    ReasonCode,
    Timeframe,
    evaluate_bearish_c3,
)

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "crt_v0_1_cases.json"


def _closed_candle(payload: dict[str, object]) -> ClosedCandle:
    return ClosedCandle(
        timeframe=Timeframe(str(payload["timeframe"])),
        open_time=datetime.fromisoformat(str(payload["open_time"])),
        close_time=datetime.fromisoformat(str(payload["close_time"])),
        open=float(payload["open"]),
        high=float(payload["high"]),
        low=float(payload["low"]),
        close=float(payload["close"]),
    )


def _window(payload: dict[str, object]) -> CandleWindow:
    return CandleWindow(
        timeframe=Timeframe(str(payload["timeframe"])),
        open_time=datetime.fromisoformat(str(payload["open_time"])),
        close_time=datetime.fromisoformat(str(payload["close_time"])),
        open_price=float(payload["open_price"]),
    )


def test_machine_readable_freeze_fixtures() -> None:
    cases = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    for case in cases:
        result = evaluate_bearish_c3(
            _closed_candle(case["c1"]),
            _closed_candle(case["c2"]),
            _window(case["c3"]),
            tuple(_closed_candle(item) for item in case["h1"]),
            tick_size=float(case["tick_size"]),
        )
        assert result.state is DecisionState(case["expected_state"]), case["id"]
        assert result.reason is ReasonCode(case["expected_reason"]), case["id"]

        if result.state is DecisionState.TRADE_PLAN:
            assert result.trade_plan is not None, case["id"]
            assert result.trade_plan.target_price == 100.0, case["id"]
            assert result.trade_plan.entry_price == 106.0, case["id"]
            assert result.trade_plan.stop_reference_price == 113.0, case["id"]
            assert result.trade_plan.stop_price == 113.25, case["id"]
