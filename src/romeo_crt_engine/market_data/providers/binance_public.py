from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from decimal import Decimal, InvalidOperation
from hashlib import sha256
from io import BytesIO, TextIOWrapper
from typing import Any, cast
from urllib.parse import urlencode
from urllib.request import urlopen
from zipfile import BadZipFile, ZipFile

from romeo_crt_engine.market_data.models import AssetClass, InstrumentMetadata, MinuteBar
from romeo_crt_engine.market_data.quality import DataQualityCode, DataQualityError

PROVIDER = "BINANCE_PUBLIC_DATA"
VENUE = "BINANCE_SPOT"
ARCHIVE_BASE_URL = "https://data.binance.vision"
MARKET_DATA_API_BASE_URL = "https://data-api.binance.vision"


@dataclass(frozen=True, slots=True)
class RawArchive:
    archive_date: date
    filename: str
    source_url: str
    checksum_url: str
    sha256: str
    content: bytes


def daily_kline_filename(symbol: str, day: date) -> str:
    return f"{symbol.upper()}-1m-{day.isoformat()}.zip"


def daily_kline_url(symbol: str, day: date) -> str:
    filename = daily_kline_filename(symbol, day)
    return f"{ARCHIVE_BASE_URL}/data/spot/daily/klines/{symbol.upper()}/1m/{filename}"


def daily_checksum_url(symbol: str, day: date) -> str:
    return f"{daily_kline_url(symbol, day)}.CHECKSUM"


def parse_checksum(text: str, expected_filename: str) -> str:
    parts = text.strip().split()
    if len(parts) != 2 or parts[1].lstrip("*") != expected_filename:
        raise DataQualityError(
            DataQualityCode.PROVIDER_SCHEMA,
            f"invalid checksum record for {expected_filename}",
        )
    digest = parts[0].lower()
    if len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest):
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "invalid SHA-256 checksum")
    return digest


def verify_sha256(content: bytes, expected_sha256: str) -> str:
    actual = sha256(content).hexdigest()
    if actual != expected_sha256.lower():
        raise DataQualityError(
            DataQualityCode.CHECKSUM_MISMATCH,
            f"expected {expected_sha256.lower()}, got {actual}",
        )
    return actual


def _timestamp_scale(value: int) -> int:
    if 10**12 <= value < 10**14:
        return 1_000  # milliseconds
    if 10**15 <= value < 10**17:
        return 1_000_000  # microseconds
    raise DataQualityError(
        DataQualityCode.PROVIDER_SCHEMA,
        f"unsupported Binance archive timestamp magnitude: {value}",
    )


def _epoch_to_utc(value: int, scale: int) -> datetime:
    seconds, remainder = divmod(value, scale)
    microseconds = remainder * (1_000_000 // scale)
    return datetime.fromtimestamp(seconds, UTC).replace(microsecond=microseconds)


def _decimal(value: str, field_name: str) -> Decimal:
    try:
        parsed = Decimal(value)
    except InvalidOperation as error:
        raise DataQualityError(
            DataQualityCode.PROVIDER_SCHEMA,
            f"invalid decimal in {field_name}: {value}",
        ) from error
    if not parsed.is_finite():
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, f"non-finite {field_name}")
    return parsed


def parse_1m_archive(archive: RawArchive, *, symbol: str) -> tuple[MinuteBar, ...]:
    source_sha = verify_sha256(archive.content, archive.sha256)
    try:
        with ZipFile(BytesIO(archive.content)) as zipped:
            csv_names = [name for name in zipped.namelist() if name.lower().endswith(".csv")]
            if len(csv_names) != 1:
                raise DataQualityError(
                    DataQualityCode.PROVIDER_SCHEMA,
                    f"archive must contain exactly one CSV, found {len(csv_names)}",
                )
            with zipped.open(csv_names[0]) as raw_file:
                text_file = TextIOWrapper(raw_file, encoding="utf-8", newline="")
                rows = list(csv.reader(text_file))
    except BadZipFile as error:
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "invalid zip archive") from error

    if len(rows) != 1440:
        raise DataQualityError(
            DataQualityCode.INCOMPLETE_BUCKET,
            f"daily crypto archive contains {len(rows)} minutes, expected 1440",
        )

    bars: list[MinuteBar] = []
    for row_number, row in enumerate(rows, start=1):
        if len(row) != 12:
            raise DataQualityError(
                DataQualityCode.PROVIDER_SCHEMA,
                f"row {row_number} has {len(row)} columns, expected 12",
            )
        try:
            raw_open = int(row[0])
            raw_close = int(row[6])
            trade_count = int(row[8])
        except ValueError as error:
            raise DataQualityError(
                DataQualityCode.PROVIDER_SCHEMA,
                f"row {row_number} has invalid integer fields",
            ) from error

        scale = _timestamp_scale(raw_open)
        if _timestamp_scale(raw_close) != scale:
            raise DataQualityError(
                DataQualityCode.PROVIDER_SCHEMA,
                f"row {row_number} mixes timestamp units",
            )
        expected_raw_close = raw_open + (60 * scale) - 1
        if raw_close != expected_raw_close:
            raise DataQualityError(
                DataQualityCode.PROVIDER_SCHEMA,
                f"row {row_number} is not an exact 1-minute provider kline",
            )

        open_time = _epoch_to_utc(raw_open, scale)
        bars.append(
            MinuteBar(
                provider=PROVIDER,
                venue=VENUE,
                symbol=symbol.upper(),
                open_time=open_time,
                close_time=open_time + timedelta(minutes=1),
                open=_decimal(row[1], "open"),
                high=_decimal(row[2], "high"),
                low=_decimal(row[3], "low"),
                close=_decimal(row[4], "close"),
                volume=_decimal(row[5], "volume"),
                quote_volume=_decimal(row[7], "quote_volume"),
                trade_count=trade_count,
                source_sha256=source_sha,
            )
        )

    expected_start = datetime.combine(archive.archive_date, time.min, tzinfo=UTC)
    expected_end = expected_start + timedelta(days=1)
    if bars[0].open_time != expected_start or bars[-1].close_time != expected_end:
        raise DataQualityError(
            DataQualityCode.INCOMPLETE_BUCKET,
            f"archive {archive.filename} does not cover its exact UTC day",
        )
    return tuple(bars)


def fetch_daily_archive(symbol: str, day: date, *, timeout_seconds: float = 30.0) -> RawArchive:
    filename = daily_kline_filename(symbol, day)
    source_url = daily_kline_url(symbol, day)
    checksum_url = daily_checksum_url(symbol, day)
    with urlopen(checksum_url, timeout=timeout_seconds) as checksum_response:
        checksum_text = checksum_response.read().decode("utf-8")
    expected = parse_checksum(checksum_text, filename)
    with urlopen(source_url, timeout=timeout_seconds) as archive_response:
        content = archive_response.read()
    verify_sha256(content, expected)
    return RawArchive(day, filename, source_url, checksum_url, expected, content)


def _filter_decimal(filters: list[dict[str, Any]], filter_type: str, key: str) -> Decimal:
    for filter_record in filters:
        if filter_record.get("filterType") == filter_type:
            value = filter_record.get(key)
            if not isinstance(value, str):
                break
            return _decimal(value, f"{filter_type}.{key}")
    raise DataQualityError(
        DataQualityCode.PROVIDER_SCHEMA,
        f"missing {filter_type}.{key} in exchangeInfo",
    )


def parse_exchange_info(
    payload: bytes,
    *,
    symbol: str,
    observed_at: datetime,
) -> InstrumentMetadata:
    if observed_at.utcoffset() is None:
        raise ValueError("observed_at must be timezone-aware")
    document = cast(dict[str, Any], json.loads(payload))
    raw_symbols = document.get("symbols")
    if not isinstance(raw_symbols, list):
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "exchangeInfo symbols missing")

    for raw_symbol in raw_symbols:
        if not isinstance(raw_symbol, dict) or raw_symbol.get("symbol") != symbol.upper():
            continue
        filters = raw_symbol.get("filters")
        if not isinstance(filters, list):
            raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "exchangeInfo filters missing")
        typed_filters = cast(list[dict[str, Any]], filters)
        tick_size = _filter_decimal(typed_filters, "PRICE_FILTER", "tickSize")
        quantity_step = _filter_decimal(typed_filters, "LOT_SIZE", "stepSize")
        metadata_seed = f"{PROVIDER}|{VENUE}|{symbol.upper()}|{tick_size}|{quantity_step}"
        return InstrumentMetadata(
            provider=PROVIDER,
            venue=VENUE,
            symbol=symbol.upper(),
            asset_class=AssetClass.CRYPTO_SPOT,
            price_tick_size=tick_size,
            quantity_step=quantity_step,
            observed_at=observed_at,
            metadata_version=sha256(metadata_seed.encode("utf-8")).hexdigest()[:16],
        )
    raise DataQualityError(
        DataQualityCode.PROVIDER_SCHEMA,
        f"symbol {symbol.upper()} missing from exchangeInfo",
    )


def fetch_exchange_info(
    symbol: str,
    *,
    observed_at: datetime,
    timeout_seconds: float = 30.0,
) -> InstrumentMetadata:
    url = f"{MARKET_DATA_API_BASE_URL}/api/v3/exchangeInfo?symbol={symbol.upper()}"
    with urlopen(url, timeout=timeout_seconds) as response:
        payload = response.read()
    return parse_exchange_info(payload, symbol=symbol, observed_at=observed_at)


def _fetch_api_1m_row(symbol: str, open_time: datetime, timeout_seconds: float) -> list[Any]:
    query = urlencode(
        {
            "symbol": symbol.upper(),
            "interval": "1m",
            "startTime": int(open_time.timestamp() * 1000),
            "limit": 1,
        }
    )
    url = f"{MARKET_DATA_API_BASE_URL}/api/v3/klines?{query}"
    with urlopen(url, timeout=timeout_seconds) as response:
        payload = cast(list[list[Any]], json.loads(response.read()))
    if len(payload) != 1 or len(payload[0]) < 9:
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "unexpected REST kline response")
    return payload[0]


def crosscheck_bars_with_rest(
    bars: tuple[MinuteBar, ...],
    *,
    timeout_seconds: float = 30.0,
) -> None:
    if not bars:
        raise ValueError("bars must not be empty")
    sample_indexes = sorted({0, len(bars) // 2, len(bars) - 1})
    for index in sample_indexes:
        bar = bars[index]
        row = _fetch_api_1m_row(bar.symbol, bar.open_time, timeout_seconds)
        observed_open_ms = int(row[0])
        expected_open_ms = int(bar.open_time.timestamp() * 1000)
        comparisons = (
            (observed_open_ms, expected_open_ms, "open_time"),
            (_decimal(str(row[1]), "api.open"), bar.open, "open"),
            (_decimal(str(row[2]), "api.high"), bar.high, "high"),
            (_decimal(str(row[3]), "api.low"), bar.low, "low"),
            (_decimal(str(row[4]), "api.close"), bar.close, "close"),
            (_decimal(str(row[5]), "api.volume"), bar.volume, "volume"),
            (_decimal(str(row[7]), "api.quote_volume"), bar.quote_volume, "quote_volume"),
            (int(row[8]), bar.trade_count, "trade_count"),
        )
        for observed, expected, field_name in comparisons:
            if observed != expected:
                raise DataQualityError(
                    DataQualityCode.PROVIDER_SCHEMA,
                    f"REST/archive mismatch at {bar.open_time.isoformat()} field={field_name}",
                )
