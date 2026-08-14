from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from time import sleep
from typing import cast
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from romeo_crt_engine.market_data.providers.oanda_v20 import (
    SUPPORTED_PRICE_COMPONENTS,
    OandaPriceCandle,
    parse_m1_candles,
    request_fingerprint,
)
from romeo_crt_engine.market_data.quality import DataQualityCode, DataQualityError

DEFAULT_PAGE_MINUTES = 4500
MAX_OANDA_CANDLES_PER_RESPONSE = 5000
REDACTED_ACCOUNT_PATH_TOKEN = "{ACCOUNT}"


@dataclass(frozen=True, slots=True)
class OandaHistoryRequestWindow:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.start.utcoffset() is None or self.end.utcoffset() is None:
            raise ValueError("history request boundaries must be timezone-aware")
        if self.end <= self.start:
            raise ValueError("history request end must be after start")
        if self.end - self.start > timedelta(minutes=MAX_OANDA_CANDLES_PER_RESPONSE):
            raise ValueError("history request window exceeds OANDA candle response limit")


@dataclass(frozen=True, slots=True)
class OandaHistoryPage:
    instrument: str
    price_component: str
    window: OandaHistoryRequestWindow
    retrieved_at: datetime
    request_sha256: str
    raw_response_sha256: str
    candles: tuple[OandaPriceCandle, ...]

    def __post_init__(self) -> None:
        if not self.instrument or self.price_component not in SUPPORTED_PRICE_COMPONENTS:
            raise ValueError("invalid OANDA history page identity")
        if self.retrieved_at.utcoffset() is None:
            raise ValueError("retrieved_at must be timezone-aware")
        for digest in (self.request_sha256, self.raw_response_sha256):
            if len(digest) != 64:
                raise ValueError("history provenance digests must be SHA-256 values")
        for candle in self.candles:
            if candle.instrument != self.instrument or candle.price_component != self.price_component:
                raise ValueError("history page candle identity mismatch")


@dataclass(frozen=True, slots=True)
class OandaHistoryRetrieval:
    instrument: str
    price_component: str
    requested_start: datetime
    requested_end: datetime
    pages: tuple[OandaHistoryPage, ...]
    candles: tuple[OandaPriceCandle, ...]
    retrieval_sha256: str

    def __post_init__(self) -> None:
        if not self.pages or not self.candles:
            raise ValueError("history retrieval must contain pages and candles")
        if len(self.retrieval_sha256) != 64:
            raise ValueError("retrieval_sha256 must be a SHA-256 value")


def build_m1_request_windows(
    start: datetime,
    end: datetime,
    *,
    page_minutes: int = DEFAULT_PAGE_MINUTES,
) -> tuple[OandaHistoryRequestWindow, ...]:
    if start.utcoffset() is None or end.utcoffset() is None:
        raise ValueError("history boundaries must be timezone-aware")
    start_utc = start.astimezone(UTC)
    end_utc = end.astimezone(UTC)
    if end_utc <= start_utc:
        raise ValueError("history end must be after start")
    if page_minutes <= 0 or page_minutes > MAX_OANDA_CANDLES_PER_RESPONSE:
        raise ValueError("page_minutes must be in 1..5000")

    windows: list[OandaHistoryRequestWindow] = []
    current = start_utc
    step = timedelta(minutes=page_minutes)
    while current < end_utc:
        window_end = min(current + step, end_utc)
        windows.append(OandaHistoryRequestWindow(start=current, end=window_end))
        current = window_end
    return tuple(windows)


def _candle_equivalent(first: OandaPriceCandle, second: OandaPriceCandle) -> bool:
    return (
        first.instrument == second.instrument
        and first.price_component == second.price_component
        and first.open_time == second.open_time
        and first.close_time == second.close_time
        and first.open == second.open
        and first.high == second.high
        and first.low == second.low
        and first.close == second.close
        and first.price_count == second.price_count
        and first.complete == second.complete
    )


def merge_m1_pages(
    pages: tuple[OandaHistoryPage, ...],
    *,
    requested_start: datetime,
    requested_end: datetime,
) -> tuple[OandaPriceCandle, ...]:
    if not pages:
        raise ValueError("history merge requires at least one page")
    start = requested_start.astimezone(UTC)
    end = requested_end.astimezone(UTC)
    identity = (pages[0].instrument, pages[0].price_component)
    by_open: dict[datetime, OandaPriceCandle] = {}

    for page in pages:
        if (page.instrument, page.price_component) != identity:
            raise ValueError("history pages must share one instrument and price component")
        for candle in page.candles:
            if candle.open_time < start or candle.open_time >= end:
                continue
            previous = by_open.get(candle.open_time)
            if previous is not None:
                if not _candle_equivalent(previous, candle):
                    raise ValueError(
                        f"conflicting provider candles across pages at {candle.open_time.isoformat()}"
                    )
                continue
            by_open[candle.open_time] = candle

    candles = tuple(by_open[timestamp] for timestamp in sorted(by_open))
    if not candles:
        raise ValueError("history pages contain no candles inside requested interval")
    return candles


def _redacted_candle_path(instrument: str) -> str:
    return f"/v3/accounts/{REDACTED_ACCOUNT_PATH_TOKEN}/instruments/{instrument}/candles"


def _request_parameters(
    window: OandaHistoryRequestWindow,
    *,
    price_component: str,
) -> dict[str, object]:
    return {
        "price": price_component,
        "granularity": "M1",
        "from": window.start.astimezone(UTC).isoformat().replace("+00:00", "Z"),
        "to": window.end.astimezone(UTC).isoformat().replace("+00:00", "Z"),
        "smooth": "false",
        "includeFirst": "true",
    }


def _parse_history_page_candles(
    payload: bytes,
    *,
    instrument: str,
    price_component: str,
) -> tuple[OandaPriceCandle, ...]:
    """Allow only a provider-confirmed empty candle array as a valid empty page."""

    try:
        return parse_m1_candles(
            payload,
            instrument=instrument,
            price_component=price_component,
            require_complete=True,
        )
    except DataQualityError as error:
        if error.code is not DataQualityCode.EMPTY:
            raise
        document = json.loads(payload)
        if (
            isinstance(document, dict)
            and document.get("instrument") == instrument
            and document.get("granularity") == "M1"
            and document.get("candles") == []
        ):
            return ()
        raise


def fetch_m1_history_page(
    *,
    base_url: str,
    account_id: str,
    token: str,
    instrument: str,
    window: OandaHistoryRequestWindow,
    price_component: str = "M",
    timeout_seconds: float = 30.0,
) -> OandaHistoryPage:
    if not account_id or not token:
        raise ValueError("OANDA runtime account credentials are required")
    if price_component not in SUPPORTED_PRICE_COMPONENTS:
        raise ValueError(f"unsupported price_component: {price_component}")

    parameters = _request_parameters(window, price_component=price_component)
    real_path = f"/v3/accounts/{account_id}/instruments/{instrument}/candles"
    redacted_path = _redacted_candle_path(instrument)
    url = f"{base_url.rstrip('/')}{real_path}?{urlencode(parameters)}"
    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept-Datetime-Format": "RFC3339",
        },
        method="GET",
    )
    with urlopen(request, timeout=timeout_seconds) as response:
        payload = cast(bytes, response.read())
    retrieved_at = datetime.now(UTC)
    return OandaHistoryPage(
        instrument=instrument,
        price_component=price_component,
        window=window,
        retrieved_at=retrieved_at,
        request_sha256=request_fingerprint(redacted_path, parameters),
        raw_response_sha256=sha256(payload).hexdigest(),
        candles=_parse_history_page_candles(
            payload,
            instrument=instrument,
            price_component=price_component,
        ),
    )


def retrieve_m1_history(
    *,
    base_url: str,
    account_id: str,
    token: str,
    instrument: str,
    start: datetime,
    end: datetime,
    price_component: str = "M",
    page_minutes: int = DEFAULT_PAGE_MINUTES,
    timeout_seconds: float = 30.0,
    request_delay_seconds: float = 0.0,
) -> OandaHistoryRetrieval:
    if request_delay_seconds < 0:
        raise ValueError("request_delay_seconds must be >= 0")
    windows = build_m1_request_windows(start, end, page_minutes=page_minutes)
    pages_list: list[OandaHistoryPage] = []
    for index, window in enumerate(windows):
        pages_list.append(
            fetch_m1_history_page(
                base_url=base_url,
                account_id=account_id,
                token=token,
                instrument=instrument,
                window=window,
                price_component=price_component,
                timeout_seconds=timeout_seconds,
            )
        )
        if request_delay_seconds and index < len(windows) - 1:
            sleep(request_delay_seconds)
    pages = tuple(pages_list)
    candles = merge_m1_pages(pages, requested_start=start, requested_end=end)
    digest = sha256()
    digest.update(instrument.encode())
    digest.update(b"\0")
    digest.update(price_component.encode())
    digest.update(b"\0")
    digest.update(start.astimezone(UTC).isoformat().encode())
    digest.update(b"\0")
    digest.update(end.astimezone(UTC).isoformat().encode())
    digest.update(b"\0")
    for page in pages:
        digest.update(page.request_sha256.encode())
        digest.update(b"|")
        digest.update(page.raw_response_sha256.encode())
        digest.update(b"\n")
    return OandaHistoryRetrieval(
        instrument=instrument,
        price_component=price_component,
        requested_start=start.astimezone(UTC),
        requested_end=end.astimezone(UTC),
        pages=pages,
        candles=candles,
        retrieval_sha256=digest.hexdigest(),
    )
