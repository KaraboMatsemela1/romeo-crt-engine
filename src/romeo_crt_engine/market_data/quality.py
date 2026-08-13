from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from enum import StrEnum

from romeo_crt_engine.market_data.closures import VenueClosure, exact_gap_is_approved
from romeo_crt_engine.market_data.models import MinuteBar


class DataQualityCode(StrEnum):
    EMPTY = "EMPTY"
    IDENTITY_MISMATCH = "IDENTITY_MISMATCH"
    DUPLICATE_TIMESTAMP = "DUPLICATE_TIMESTAMP"
    OUT_OF_ORDER = "OUT_OF_ORDER"
    GAP = "GAP"
    FUTURE_TIMESTAMP = "FUTURE_TIMESTAMP"
    INCOMPLETE_BUCKET = "INCOMPLETE_BUCKET"
    PROVIDER_SCHEMA = "PROVIDER_SCHEMA"
    CHECKSUM_MISMATCH = "CHECKSUM_MISMATCH"


class DataQualityError(ValueError):
    def __init__(self, code: DataQualityCode, message: str) -> None:
        super().__init__(f"{code.value}: {message}")
        self.code = code


def validate_minute_series(
    bars: Sequence[MinuteBar],
    *,
    as_of: datetime | None = None,
    allowed_closures: tuple[VenueClosure, ...] = (),
) -> None:
    if not bars:
        raise DataQualityError(DataQualityCode.EMPTY, "minute series must not be empty")

    identity = (bars[0].provider, bars[0].venue, bars[0].symbol)
    prior_open: datetime | None = None
    prior_close: datetime | None = None

    if as_of is not None and as_of.utcoffset() is None:
        raise ValueError("as_of must be timezone-aware")

    for bar in bars:
        if (bar.provider, bar.venue, bar.symbol) != identity:
            raise DataQualityError(
                DataQualityCode.IDENTITY_MISMATCH,
                "all bars in one trusted series must have the same identity",
            )

        if prior_open is not None:
            if bar.open_time == prior_open:
                raise DataQualityError(
                    DataQualityCode.DUPLICATE_TIMESTAMP,
                    f"duplicate minute open at {bar.open_time.isoformat()}",
                )
            if bar.open_time < prior_open:
                raise DataQualityError(
                    DataQualityCode.OUT_OF_ORDER,
                    f"out-of-order minute open at {bar.open_time.isoformat()}",
                )
            if (
                prior_close is not None
                and bar.open_time != prior_close
                and not exact_gap_is_approved(prior_close, bar.open_time, allowed_closures)
            ):
                raise DataQualityError(
                    DataQualityCode.GAP,
                    (
                        f"expected next minute at {prior_close.isoformat()}, "
                        f"got {bar.open_time.isoformat()}"
                    ),
                )

        if as_of is not None and bar.close_time > as_of:
            raise DataQualityError(
                DataQualityCode.FUTURE_TIMESTAMP,
                f"bar closes after trusted as_of: {bar.close_time.isoformat()}",
            )

        prior_open = bar.open_time
        prior_close = bar.close_time
