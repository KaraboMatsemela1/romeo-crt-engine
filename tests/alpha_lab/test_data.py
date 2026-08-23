from __future__ import annotations

from datetime import UTC, datetime

from romeo_crt_engine.alpha_lab.data import _months


def test_dev_month_enumeration_does_not_touch_oos_month() -> None:
    months = _months(
        datetime(2019, 1, 1, tzinfo=UTC),
        datetime(2023, 1, 1, tzinfo=UTC),
    )
    assert months[0].isoformat() == "2019-01-01"
    assert months[-1].isoformat() == "2022-12-01"
    assert len(months) == 48
