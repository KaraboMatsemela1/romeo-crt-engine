from __future__ import annotations

from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo

from romeo_crt_engine.market_data.price_data_v2 import CanonicalPriceBarV2

NEW_YORK = ZoneInfo("America/New_York")

# The Phase-6B activity protocol is frozen in New-York wall-clock time. The
# trusted-dataset workflow consumes these exact bounds without widening DEV.
ACTIVITY_START_NY = datetime(2019, 1, 1, 0, 0, tzinfo=NEW_YORK)
ACTIVITY_END_NY_EXCLUSIVE = datetime(2023, 1, 1, 0, 0, tzinfo=NEW_YORK)

CANONICAL_COVERAGE_START_UTC = ACTIVITY_START_NY.astimezone(UTC)
CANONICAL_COVERAGE_END_UTC = ACTIVITY_END_NY_EXCLUSIVE.astimezone(UTC)

# The raw yearly qualification pass ended at 2023-01-01T00:00:00Z. The
# canonical detector window must extend only far enough to complete the frozen
# 2022-12-31 New-York D1 candle. No detector/OOS access is implied here.
RAW_QUALIFIED_END_UTC = datetime(2023, 1, 1, 0, 0, tzinfo=UTC)
CANONICAL_TAIL_START_UTC = RAW_QUALIFIED_END_UTC
CANONICAL_TAIL_END_UTC = CANONICAL_COVERAGE_END_UTC

CANONICAL_COVERAGE_POLICY_VERSION = "P6B_CANONICAL_COVERAGE_V1"


def eligible_new_york_dates_from_m1(
    m1: tuple[CanonicalPriceBarV2, ...],
) -> tuple[date, ...]:
    """Return provider-observed New-York dates inside the frozen DEV window.

    Date eligibility is derived only from provider observations. It never
    guesses weekends/holidays and it does not inspect detector or performance
    outcomes. A date with no provider price observations is not fabricated as a
    Daily candle.
    """

    for bar in m1:
        if not (
            CANONICAL_COVERAGE_START_UTC <= bar.open_time < CANONICAL_COVERAGE_END_UTC
            and bar.close_time <= CANONICAL_COVERAGE_END_UTC
        ):
            raise ValueError("M1 bar lies outside the frozen Phase-6B canonical coverage")

    return tuple(
        sorted(
            {
                bar.open_time.astimezone(NEW_YORK).date()
                for bar in m1
            }
        )
    )
