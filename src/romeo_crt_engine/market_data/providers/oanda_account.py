from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from hashlib import sha256
from typing import Any, cast
from urllib.request import Request, urlopen

from romeo_crt_engine.market_data.quality import DataQualityCode, DataQualityError


@dataclass(frozen=True, slots=True)
class OandaAccountQualificationRecord:
    """Execution-relevant account metadata with account identity deliberately omitted."""

    home_currency: str
    margin_rate: Decimal
    hedging_enabled: bool
    guaranteed_stop_loss_order_mode: str | None
    observed_at: datetime
    raw_sha256: str

    def __post_init__(self) -> None:
        if not self.home_currency:
            raise ValueError("home_currency must not be empty")
        if not self.margin_rate.is_finite() or self.margin_rate < 0:
            raise ValueError("margin_rate must be non-negative and finite")
        if self.observed_at.utcoffset() is None:
            raise ValueError("observed_at must be timezone-aware")
        if len(self.raw_sha256) != 64:
            raise ValueError("raw_sha256 must be a SHA-256 digest")


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


def parse_authorized_account_ids(payload: bytes) -> tuple[str, ...]:
    """Parse token-authorized account IDs for in-memory authorization preflight only."""

    try:
        document = cast(dict[str, Any], json.loads(payload))
    except json.JSONDecodeError as error:
        raise DataQualityError(
            DataQualityCode.PROVIDER_SCHEMA,
            "invalid OANDA authorized-account JSON",
        ) from error

    accounts = document.get("accounts")
    if not isinstance(accounts, list):
        raise DataQualityError(
            DataQualityCode.PROVIDER_SCHEMA,
            "OANDA authorized-account list missing",
        )

    account_ids: list[str] = []
    for account in accounts:
        if not isinstance(account, dict):
            raise DataQualityError(
                DataQualityCode.PROVIDER_SCHEMA,
                "invalid OANDA authorized-account entry",
            )
        account_id = account.get("id")
        if not isinstance(account_id, str) or not account_id:
            raise DataQualityError(
                DataQualityCode.PROVIDER_SCHEMA,
                "OANDA authorized-account ID missing",
            )
        account_ids.append(account_id)

    if len(set(account_ids)) != len(account_ids):
        raise DataQualityError(
            DataQualityCode.PROVIDER_SCHEMA,
            "duplicate OANDA authorized-account ID",
        )
    return tuple(account_ids)


def fetch_authorized_account_ids(
    *,
    base_url: str,
    token: str,
    timeout_seconds: float = 30.0,
) -> tuple[str, ...]:
    """Fetch token-authorized accounts without persisting or printing their identifiers."""

    if not token:
        raise ValueError("OANDA token must not be empty")
    request = Request(
        f"{base_url.rstrip('/')}/v3/accounts",
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    with urlopen(request, timeout=timeout_seconds) as response:
        payload = cast(bytes, response.read())
    return parse_authorized_account_ids(payload)


def parse_account_summary(
    payload: bytes,
    *,
    observed_at: datetime,
) -> OandaAccountQualificationRecord:
    if observed_at.utcoffset() is None:
        raise ValueError("observed_at must be timezone-aware")
    try:
        document = cast(dict[str, Any], json.loads(payload))
    except json.JSONDecodeError as error:
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "invalid OANDA account JSON") from error

    account = document.get("account")
    if not isinstance(account, dict):
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "OANDA account summary missing")
    currency = account.get("currency")
    hedging_enabled = account.get("hedgingEnabled")
    if not isinstance(currency, str) or not currency:
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "account currency missing")
    if not isinstance(hedging_enabled, bool):
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "hedgingEnabled missing")
    gslo_mode = account.get("guaranteedStopLossOrderMode")
    if gslo_mode is not None and not isinstance(gslo_mode, str):
        raise DataQualityError(DataQualityCode.PROVIDER_SCHEMA, "invalid account GSLO mode")

    return OandaAccountQualificationRecord(
        home_currency=currency,
        margin_rate=_decimal(account.get("marginRate"), "account.marginRate"),
        hedging_enabled=hedging_enabled,
        guaranteed_stop_loss_order_mode=gslo_mode,
        observed_at=observed_at,
        raw_sha256=sha256(payload).hexdigest(),
    )


def fetch_account_summary(
    *,
    base_url: str,
    account_id: str,
    token: str,
    observed_at: datetime,
    timeout_seconds: float = 30.0,
) -> OandaAccountQualificationRecord:
    """Fetch execution-relevant account metadata without returning the account ID/token."""

    if not account_id:
        raise ValueError("account_id must not be empty")
    if not token:
        raise ValueError("OANDA token must not be empty")
    path = f"/v3/accounts/{account_id}/summary"
    request = Request(
        f"{base_url.rstrip('/')}{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept-Datetime-Format": "RFC3339",
        },
        method="GET",
    )
    with urlopen(request, timeout=timeout_seconds) as response:
        payload = cast(bytes, response.read())
    return parse_account_summary(payload, observed_at=observed_at.astimezone(UTC))
