from __future__ import annotations

from romeo_crt_engine.alpha_lab.run_cycle import CONFIRM_START, DEV_END, OOS_END, OOS_START


def test_research_windows_are_non_overlapping() -> None:
    assert DEV_END == OOS_START
    assert OOS_END == CONFIRM_START
