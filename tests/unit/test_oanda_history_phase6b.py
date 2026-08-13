from __future__ import annotations

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest

from romeo_crt_engine.market_data.providers.oanda_history import (
    OandaHistoryPage,
    OandaHistoryRequestWindow,
    build_m1_request_windows,
    merge_m1_pages,
)
from romeo_crt_engine.market_data.providers.oanda_v20 import OandaPriceCandle


def _candle(open_time: datetime, *, close: str = "1.1002") -> OandaPriceCandle:
    return OandaPriceCandle(
        instrument="EUR_USD",
        price_component="M",
        open_time=open_time,
        close_time=open_time + timedelta(minutes=1),
        open=Decimal("1.1000"),
        high=Decimal("1.1005"),
        low=Decimal("1.0995"),
        close=Decimal(close),
        price_count=5,
        complete=True,
        source_sha256="a" * 64,
    )


def _page(
    start: datetime,
    end: datetime,
    candles: tuple[OandaPriceCandle, ...],
    *,
    response_sha: str,
) -> OandaHistoryPage:
    return OandaHistoryPage(
        instrument="EUR_USD",
        price_component="M",
        window=OandaHistoryRequestWindow(start=start, end=end),
        retrieved_at=datetime(2026, 8, 13, 11, 30, tzinfo=UTC),
        request_sha256="b" * 64,
        raw_response_sha256=response_sha,
        candles=candles,
    )


def test_request_windows_respect_5000_candle_limit_and_cover_range_exactly() -> None:
    start = datetime(2020, 1, 1, tzinfo=UTC)
    end = start + timedelta(minutes=10001)

    windows = build_m1_request_windows(start, end, page_minutes=4500)

    assert [window.end - window.start for window in windows] == [
        timedelta(minutes=4500),
        timedelta(minutes=4500),
        timedelta(minutes=1001),
    ]
    assert windows[0].start == start
    assert windows[-1].end == end
    for first, second in zip(windows, windows[1:], strict=True):
        assert first.end == second.start


def test_request_windows_reject_page_size_above_provider_limit() -> None:
    start = datetime(2020, 1, 1, tzinfo=UTC)
    with pytest.raises(ValueError, match="1..5000"):
        build_m1_request_windows(start, start + timedelta(days=1), page_minutes=5001)


def test_merge_pages_deduplicates_identical_boundary_candle() -> None:
    start = datetime(2020, 1, 1, tzinfo=UTC)
    boundary = start + timedelta(minutes=2)
    first = _page(
        start,
        boundary + timedelta(minutes=1),
        (_candle(start), _candle(start + timedelta(minutes=1)), _candle(boundary)),
        response_sha="c" * 64,
    )
    second = _page(
        boundary,
        boundary + timedelta(minutes=3),
        (_candle(boundary), _candle(boundary + timedelta(minutes=1))),
        response_sha="d" * 64,
    )

    merged = merge_m1_pages(
        (first, second),
        requested_start=start,
        requested_end=boundary + timedelta(minutes=2),
    )

    assert [candle.open_time for candle in merged] == [
        start,
        start + timedelta(minutes=1),
        boundary,
        boundary + timedelta(minutes=1),
    ]


def test_merge_pages_rejects_conflicting_boundary_candle() -> None:
    start = datetime(2020, 1, 1, tzinfo=UTC)
    boundary = start + timedelta(minutes=1)
    first = _page(
        start,
        boundary + timedelta(minutes=1),
        (_candle(start), _candle(boundary, close="1.1002")),
        response_sha="c" * 64,
    )
    second = _page(
        boundary,
        boundary + timedelta(minutes=2),
        (_candle(boundary, close="1.1010"),),
        response_sha="d" * 64,
    )

    with pytest.raises(ValueError, match="conflicting provider candles"):
        merge_m1_pages(
            (first, second),
            requested_start=start,
            requested_end=boundary + timedelta(minutes=1),
        )
