from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal, InvalidOperation
from hashlib import sha256
from typing import Any, cast
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from romeo_crt_engine.market_data.quality import DataQualityCode, DataQualityError

PROVIDER = "OANDA_V20"
VENUE = "OANDA_FXTRADE"
PRACTICE_BASE_URL = "https://api-fxpractice.oanda.com"
LIVE_BASE_URL = "https://api-fxtrade.oanda.com"
SUPPORTED_PRICE_COMPONENTS = frozenset({"M", "B", "A"})


@dataclass(frozen=True, slots=True)
class OandaCommissionRecord:
    commission: Decimal
    units_traded: Decimal
    minimum_commission: Decimal

    def __post_init__(self) -> None:
        values = (self.commission, self.units_traded, self.minimum_commission)
        if not all(value.is_finite() and value >= 0 for value in values):
            raise ValueError("commission values must be non-negative and finite")
        if self.units_traded <= 0:
            raise ValueError("commission units_traded must be positive")


@dataclass(frozen=True, slots=True)
class OandaFinancingDayRecord:
    day_of_week: str
    days_charged: int

    def __post_init__(self) -> None:
        if not self.day_of_week:
            raise ValueError("financing day_of_week must not be empty")
        if self.days_charged < 0:
            raise ValueError("financing days_charged must be >= 0")


@dataclass(frozen=True, slots=True)
class OandaFinancingRecord:
    long_rate: Decimal
    short_rate: Decimal
    financing_days: tuple[OandaFinancingDayRecord, ...]

    def __post_init__(self) -> None:
        if not self.long_rate.is_finite() or not self.short_rate.is_finite():
            raise ValueError("financing rates must be finite")
        days = [item.day_of_week for item in self.financing_days]
        if len(days) != len(set(days)):
            raise ValueError("financing day_of_week entries must be unique")


@dataclass(frozen=True, slots=True)
class OandaInstrumentRecord:
    """Provider metadata captured without pretending display precision is a tick size."""

    name: str
    display_name: str
    instrument_type: str
    display_precision: int
    pip_location: int
    trade_units_precision: int
    minimum_trade_size: Decimal
    observed_at: datetime
    raw_sha256: str
    maximum_order_units: Decimal | None = None
    maximum_position_size: Decimal | None = None
    margin_rate: Decimal | None = None
    commission: OandaCommissionRecord | None = None
    financing: OandaFinancingRecord | None = None
    guaranteed_stop_loss_order_mode: str | None = None

    def __post_init__(self) -> None:
        if not self.name or not self.instrument_type or not self.raw_sha256:
            raise ValueError("OANDA instrument identity fields must not be empty")
        if self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")
        if self.display_precision < 0 or self.trade_units_precision < 0:
            raise ValueError("precision fields must be >= 0")
        if not self.minimum_trade_size.is_finite() or self.minimum_trade_size <= 0:
            raise ValueError("minimum_trade_size must be positive and finite")
        for label, value in (
            ("maximum_order_units", self.maximum_order_units),
            ("maximum_position_size", self.maximum_position_size),
            ("margin_rate", self.margin_rate),
        ):
            if value is not None and (not value.is_finite() or value < 0):
                raise ValueError(f"{label} must be non-negative and finite when provided")
        if len(self.raw_sha256) != 64:
            raise ValueError("raw_sha256 must be a SHA-256 digest")

    @property
    def provider_unit_precision_step(self) -> Decimal:
        """Smallest unit increment implied by OANDA's tradeUnitsPrecision field."""

        return Decimal(1).scaleb(-self.trade_units_precision)


@dataclass(frozen=True, slots=True)
class OandaPriceCandle:
    """Raw provider price candle used only during OANDA qualification.

    OANDA's `volume` field is documented as the number of prices created during
    the candle, not exchange trade/base volume. It is therefore retained as
    `price_count` and is deliberately not coerced into the project's existing
    Binance-oriented volume/trade-count fields.
    """

    instrument: str
    price_component: str
    open_time: datetime
    close_time: datetime
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    price_count: int
    complete: bool
    source_sha256: str

    def __post_init__(self) -> None:
        if not self.instrument or self.price_component not in SUPPORTED_PRICE_COMPONENTS:
            raise ValueError("invalid OANDA candle identity")
        if self.open_time.utcoffset() != timedelta(0) or self.close_time.utcoffset() != timedelta(0):
            raise ValueError("OANDA candle timestamps must be UTC")
        if self.close_time - self.open_time != timedelta(minutes=1):
            raise ValueError("qualification candle must span exactly one minute")
        values = (self.open, self.high, self.low, self.close)
        if not all(value.is_finite() for value in values):
            raise ValueError("OHLC values must be finite")
        if self.high < max(self.open, self.close) or self.low > min(self.open, self.close):
            raise ValueError("OHLC envelope is invalid")
        if self.high < self.low:
            raise ValueError("high must be >= low")
        if self.price_count < 0:
            raise ValueError("price_count must be >= 0")
        if len(self.source_sha256) != 64:
            raise ValueError("source_sha256 must be a SHA-256 digest")


def _decimal(value: object, field_name: str) -> Decimal:
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, ValueError) as error:
        raise DataQualityError(
            DataQualityCode.PROVIDER_SCHEMA,
            f"invalid decimal in {field_name}: {value!r}",
        ) from error
    if not parsed.is_finite():
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, f"non-finite {field_name}")
    return parsed


def _optional_decimal(value: object, field_name: str) -> Decimal | None:
    if value is None:
        return None
    return _decimal(value, field_name)


def _integer(value: object, field_name: str) -> int:
    if isinstance(value, bool):
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, f"invalid integer in {field_name}")
    try:
        return int(cast(Any, value))
    except (TypeError, ValueError) as error:
        raise DataQualityError(
            DataQualityCode.PROVIDER_SCHEMA,
            f"invalid integer in {field_name}: {value!r}",
        ) from error


def _utc_timestamp(value: object, field_name: str) -> datetime:
    if not isinstance(value, str):
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, f"{field_name} must be a string")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as error:
        raise DataQualityError(
            DataQualityCode.PROVIDER_SCHEMA,
            f"invalid timestamp in {field_name}: {value}",
        ) from error
    if parsed.utcoffset() is None:
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, f"{field_name} lacks timezone")
    return parsed.astimezone(UTC)


def _raw_digest(payload: bytes) -> str:
    return sha256(payload).hexdigest()


def _parse_commission(value: object) -> OandaCommissionRecord | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "invalid commission record")
    return OandaCommissionRecord(
        commission=_decimal(value.get("commission"), "commission.commission"),
        units_traded=_decimal(value.get("unitsTraded"), "commission.unitsTraded"),
        minimum_commission=_decimal(
            value.get("minimumCommission"), "commission.minimumCommission"
        ),
    )


def _parse_financing(value: object) -> OandaFinancingRecord | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "invalid financing record")
    raw_days = value.get("financingDaysOfWeek", [])
    if not isinstance(raw_days, list):
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "invalid financing days")
    days: list[OandaFinancingDayRecord] = []
    for raw_day in raw_days:
        if not isinstance(raw_day, dict):
            raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "invalid financing day record")
        day_of_week = raw_day.get("dayOfWeek")
        if not isinstance(day_of_week, str):
            raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "financing day is missing")
        days.append(
            OandaFinancingDayRecord(
                day_of_week=day_of_week,
                days_charged=_integer(raw_day.get("daysCharged"), "financing.daysCharged"),
            )
        )
    return OandaFinancingRecord(
        long_rate=_decimal(value.get("longRate"), "financing.longRate"),
        short_rate=_decimal(value.get("shortRate"), "financing.shortRate"),
        financing_days=tuple(days),
    )


def parse_account_instruments(
    payload: bytes,
    *,
    observed_at: datetime,
) -> tuple[OandaInstrumentRecord, ...]:
    """Parse account-specific instrument discovery without deriving tick size."""

    if observed_at.utcoffset() is None:
        raise ValueError("observed_at must be timezone-aware")
    try:
        document = cast(dict[str, Any], json.loads(payload))
    except json.JSONDecodeError as error:
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "invalid OANDA JSON") from error

    raw_instruments = document.get("instruments")
    if not isinstance(raw_instruments, list):
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "OANDA instruments array missing")

    digest = _raw_digest(payload)
    records: list[OandaInstrumentRecord] = []
    seen: set[str] = set()
    for raw in raw_instruments:
        if not isinstance(raw, dict):
            raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "invalid OANDA instrument record")
        name = raw.get("name")
        instrument_type = raw.get("type")
        if not isinstance(name, str) or not isinstance(instrument_type, str):
            raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "instrument name/type missing")
        if name in seen:
            raise DataQualityError(DataQualityCode.DUPLICATE_TIMESTAMP, f"duplicate instrument {name}")
        seen.add(name)

        display_name = raw.get("displayName")
        gslo_mode = raw.get("guaranteedStopLossOrderMode")
        if gslo_mode is not None and not isinstance(gslo_mode, str):
            raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "invalid GSLO mode")
        records.append(
            OandaInstrumentRecord(
                name=name,
                display_name=display_name if isinstance(display_name, str) else name,
                instrument_type=instrument_type,
                display_precision=_integer(raw.get("displayPrecision"), "displayPrecision"),
                pip_location=_integer(raw.get("pipLocation"), "pipLocation"),
                trade_units_precision=_integer(
                    raw.get("tradeUnitsPrecision"), "tradeUnitsPrecision"
                ),
                minimum_trade_size=_decimal(raw.get("minimumTradeSize"), "minimumTradeSize"),
                observed_at=observed_at,
                raw_sha256=digest,
                maximum_order_units=_optional_decimal(
                    raw.get("maximumOrderUnits"), "maximumOrderUnits"
                ),
                maximum_position_size=_optional_decimal(
                    raw.get("maximumPositionSize"), "maximumPositionSize"
                ),
                margin_rate=_optional_decimal(raw.get("marginRate"), "marginRate"),
                commission=_parse_commission(raw.get("commission")),
                financing=_parse_financing(raw.get("financing")),
                guaranteed_stop_loss_order_mode=gslo_mode,
            )
        )

    return tuple(sorted(records, key=lambda item: item.name))


def parse_m1_candles(
    payload: bytes,
    *,
    instrument: str,
    price_component: str = "M",
    require_complete: bool = True,
) -> tuple[OandaPriceCandle, ...]:
    """Parse one OANDA M1 candle response without filling market/session gaps."""

    if price_component not in SUPPORTED_PRICE_COMPONENTS:
        raise ValueError(f"unsupported price_component: {price_component}")
    try:
        document = cast(dict[str, Any], json.loads(payload))
    except json.JSONDecodeError as error:
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "invalid OANDA candle JSON") from error

    response_instrument = document.get("instrument")
    if response_instrument != instrument:
        raise DataQualityError(
            DataQualityCode.IDENTITY_MISMATCH,
            f"expected instrument {instrument}, got {response_instrument}",
        )
    if document.get("granularity") != "M1":
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "OANDA response is not M1")

    raw_candles = document.get("candles")
    if not isinstance(raw_candles, list):
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "OANDA candles array missing")

    component_key = {"M": "mid", "B": "bid", "A": "ask"}[price_component]
    digest = _raw_digest(payload)
    candles: list[OandaPriceCandle] = []
    prior_open: datetime | None = None

    for raw in raw_candles:
        if not isinstance(raw, dict):
            raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "invalid OANDA candle record")
        complete = raw.get("complete")
        if not isinstance(complete, bool):
            raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "candle complete flag missing")
        if require_complete and not complete:
            continue

        price = raw.get(component_key)
        if not isinstance(price, dict):
            raise DataQualityError(
                DataQualityCode.PROVIDER_SCHEMA,
                f"requested price component {component_key} missing",
            )

        open_time = _utc_timestamp(raw.get("time"), "candle.time")
        if prior_open is not None:
            if open_time == prior_open:
                raise DataQualityError(
                    DataQualityCode.DUPLICATE_TIMESTAMP,
                    f"duplicate OANDA candle at {open_time.isoformat()}",
                )
            if open_time < prior_open:
                raise DataQualityError(
                    DataQualityCode.OUT_OF_ORDER,
                    f"out-of-order OANDA candle at {open_time.isoformat()}",
                )
        prior_open = open_time

        candles.append(
            OandaPriceCandle(
                instrument=instrument,
                price_component=price_component,
                open_time=open_time,
                close_time=open_time + timedelta(minutes=1),
                open=_decimal(price.get("o"), f"{component_key}.o"),
                high=_decimal(price.get("h"), f"{component_key}.h"),
                low=_decimal(price.get("l"), f"{component_key}.l"),
                close=_decimal(price.get("c"), f"{component_key}.c"),
                price_count=_integer(raw.get("volume", 0), "volume"),
                complete=complete,
                source_sha256=digest,
            )
        )

    if not candles:
        raise DataQualityError(DataQualityCode.EMPTY, "OANDA response contains no complete M1 candles")
    return tuple(candles)


def request_fingerprint(path: str, parameters: dict[str, object]) -> str:
    """Hash a canonical, secret-free provider request description."""

    canonical = urlencode(sorted((key, str(value)) for key, value in parameters.items()))
    return sha256(f"{path}?{canonical}".encode()).hexdigest()


def _authorized_get(
    url: str,
    *,
    token: str,
    timeout_seconds: float,
) -> bytes:
    if not token:
        raise ValueError("OANDA token must not be empty")
    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept-Datetime-Format": "RFC3339",
        },
        method="GET",
    )
    with urlopen(request, timeout=timeout_seconds) as response:
        return cast(bytes, response.read())


def fetch_account_instruments(
    *,
    base_url: str,
    account_id: str,
    token: str,
    observed_at: datetime,
    timeout_seconds: float = 30.0,
) -> tuple[OandaInstrumentRecord, ...]:
    """Fetch the account/division-specific instrument universe.

    The bearer token is used only as an HTTP header and is never returned,
    serialized, hashed into provenance, or included in the request fingerprint.
    """

    if not account_id:
        raise ValueError("account_id must not be empty")
    path = f"/v3/accounts/{account_id}/instruments"
    payload = _authorized_get(
        f"{base_url.rstrip('/')}{path}",
        token=token,
        timeout_seconds=timeout_seconds,
    )
    return parse_account_instruments(payload, observed_at=observed_at)


def fetch_m1_candles(
    *,
    base_url: str,
    account_id: str,
    token: str,
    instrument: str,
    start: datetime,
    end: datetime,
    price_component: str = "M",
    timeout_seconds: float = 30.0,
) -> tuple[OandaPriceCandle, ...]:
    """Fetch one bounded OANDA M1 response page.

    Callers are responsible for pagination/window sizing (OANDA documents a
    maximum of 5000 historical candles per response) and for classifying gaps.
    No missing interval is filled or synthesized here.
    """

    if start.utcoffset() is None or end.utcoffset() is None:
        raise ValueError("start/end must be timezone-aware")
    start_utc = start.astimezone(UTC)
    end_utc = end.astimezone(UTC)
    if end_utc <= start_utc:
        raise ValueError("end must be after start")
    if price_component not in SUPPORTED_PRICE_COMPONENTS:
        raise ValueError(f"unsupported price_component: {price_component}")

    path = f"/v3/accounts/{account_id}/instruments/{instrument}/candles"
    parameters: dict[str, object] = {
        "price": price_component,
        "granularity": "M1",
        "from": start_utc.isoformat().replace("+00:00", "Z"),
        "to": end_utc.isoformat().replace("+00:00", "Z"),
        "smooth": "false",
        "includeFirst": "true",
    }
    url = f"{base_url.rstrip('/')}{path}?{urlencode(parameters)}"
    payload = _authorized_get(url, token=token, timeout_seconds=timeout_seconds)
    return parse_m1_candles(
        payload,
        instrument=instrument,
        price_component=price_component,
        require_complete=True,
    )
