"""Practice-only, credential-redacted OANDA connectivity smoke check.

This module is intentionally limited to the three GET requests needed to confirm
that a practice token can access its configured account and its instrument
metadata.  It contains no order capability and must only be invoked explicitly
by the manual GitHub Actions workflow.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from urllib.parse import quote, urlsplit

from romeo_crt_engine.market_data.providers.oanda_account import (
    fetch_account_summary,
    fetch_authorized_account_ids,
)
from romeo_crt_engine.market_data.providers.oanda_v20 import (
    PRACTICE_BASE_URL,
    fetch_account_instruments,
)
from romeo_crt_engine.market_data.quality import DataQualityError

REPORT_SCHEMA_VERSION = "OANDA_PRACTICE_READ_ONLY_SMOKE_V1"
PRACTICE_ENVIRONMENT = "practice"
_UNAPPROVED_ENDPOINT_ENVIRONMENT_VARIABLES = ("OANDA_BASE_URL", "OANDA_ENDPOINT")
_SAFE_GUARD_FAILURE_CODES = frozenset(
    {
        "configured_account_not_authorized",
        "exact_practice_endpoint_required",
        "missing_or_ambiguous_oanda_account_id",
        "missing_or_ambiguous_oanda_api_token",
        "missing_or_ambiguous_oanda_env",
        "practice_environment_required",
        "unapproved_endpoint_override",
    }
)


class SmokeGuardError(ValueError):
    """A fail-closed configuration or authorization guard rejected the run."""


class SmokeReadError(RuntimeError):
    """A provider read failed without preserving potentially sensitive transport text."""


@dataclass(frozen=True, slots=True)
class SmokeRuntimeConfig:
    environment: str
    account_id: str
    token: str
    base_url: str = PRACTICE_BASE_URL

    @classmethod
    def from_environment(cls, environment: Mapping[str, str]) -> SmokeRuntimeConfig:
        for name in _UNAPPROVED_ENDPOINT_ENVIRONMENT_VARIABLES:
            if environment.get(name):
                raise SmokeGuardError("unapproved_endpoint_override")

        oanda_environment = _required_environment_value(environment, "OANDA_ENV")
        if oanda_environment != PRACTICE_ENVIRONMENT:
            raise SmokeGuardError("practice_environment_required")

        account_id = _required_environment_value(environment, "OANDA_ACCOUNT_ID")
        token = _required_environment_value(environment, "OANDA_API_TOKEN")
        _validate_runtime_account_id(account_id)
        _validate_runtime_token(token)

        return cls(
            environment=oanda_environment,
            account_id=account_id,
            token=token,
        )


def _required_environment_value(environment: Mapping[str, str], name: str) -> str:
    value = environment.get(name)
    if not isinstance(value, str) or not value or value != value.strip():
        raise SmokeGuardError(f"missing_or_ambiguous_{name.lower()}")
    return value


def _validate_runtime_account_id(account_id: str) -> None:
    """Reject account values that could alter a provider request path."""

    if (
        not account_id
        or account_id != account_id.strip()
        or quote(account_id, safe="") != account_id
    ):
        raise SmokeGuardError("missing_or_ambiguous_oanda_account_id")


def _validate_runtime_token(token: str) -> None:
    if not token or token != token.strip():
        raise SmokeGuardError("missing_or_ambiguous_oanda_api_token")


def validate_practice_endpoint(base_url: str) -> None:
    """Accept only the exact HTTPS OANDA practice origin, before any request."""

    try:
        parsed = urlsplit(base_url)
        port = parsed.port
    except ValueError:
        raise SmokeGuardError("exact_practice_endpoint_required") from None
    if (
        parsed.scheme != "https"
        or parsed.hostname != "api-fxpractice.oanda.com"
        or port not in (None, 443)
        or parsed.username is not None
        or parsed.password is not None
        or parsed.path not in ("", "/")
        or parsed.query
        or parsed.fragment
        or base_url != PRACTICE_BASE_URL
    ):
        raise SmokeGuardError("exact_practice_endpoint_required")


def redact_sensitive_text(value: object, *, token: str, account_id: str) -> str:
    """Redact configured credentials and account paths from exception/log text."""

    redacted = str(value)
    secrets = (token, account_id, quote(token, safe=""), quote(account_id, safe=""))
    for secret in sorted(set(secrets), key=len, reverse=True):
        if secret:
            redacted = redacted.replace(secret, "[REDACTED]")
    return redacted


def _utc_iso8601(observed_at: datetime) -> str:
    """Serialize an observation time as an explicit UTC ISO-8601 value."""

    return observed_at.astimezone(UTC).isoformat()


def run_read_only_smoke(
    config: SmokeRuntimeConfig,
    *,
    observed_at: datetime | None = None,
) -> dict[str, object]:
    """Perform the permitted GET-only reads after all safety guards pass."""

    validate_practice_endpoint(config.base_url)
    if config.environment != PRACTICE_ENVIRONMENT:
        raise SmokeGuardError("practice_environment_required")
    _validate_runtime_account_id(config.account_id)
    _validate_runtime_token(config.token)

    try:
        authorized_account_ids = fetch_authorized_account_ids(
            base_url=config.base_url,
            token=config.token,
        )
    except (DataQualityError, OSError, ValueError):
        raise SmokeReadError("authorization_read_failed") from None
    if config.account_id not in authorized_account_ids:
        raise SmokeGuardError("configured_account_not_authorized")

    timestamp = observed_at or datetime.now(UTC)
    try:
        account = fetch_account_summary(
            base_url=config.base_url,
            account_id=config.account_id,
            token=config.token,
            observed_at=timestamp,
        )
    except (DataQualityError, OSError, ValueError):
        raise SmokeReadError("account_summary_read_failed") from None
    try:
        instruments = fetch_account_instruments(
            base_url=config.base_url,
            account_id=config.account_id,
            token=config.token,
            observed_at=timestamp,
        )
    except (DataQualityError, OSError, ValueError):
        raise SmokeReadError("instrument_metadata_read_failed") from None
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "status": "PASS",
        "observed_at": _utc_iso8601(timestamp),
        "environment": PRACTICE_ENVIRONMENT,
        "endpoint": PRACTICE_BASE_URL,
        "account_scope": "REDACTED_RUNTIME_ACCOUNT",
        "authorized_account_match": True,
        "account_summary_read": True,
        "account_home_currency": account.home_currency,
        "instrument_metadata_read": True,
        "instrument_count": len(instruments),
        "permitted_requests": [
            "GET /v3/accounts",
            "GET /v3/accounts/[REDACTED]/summary",
            "GET /v3/accounts/[REDACTED]/instruments",
        ],
        "execution_enabled": False,
        "live_trading_authorized": False,
    }


def _failure_code(error: BaseException) -> str:
    if isinstance(error, SmokeGuardError) and str(error) in _SAFE_GUARD_FAILURE_CODES:
        return str(error)
    return "read_only_connectivity_check_failed"


def failure_report(
    error: BaseException,
    *,
    observed_at: datetime | None = None,
) -> dict[str, object]:
    """Return a deliberately non-secret failure artifact without exception detail."""

    timestamp = observed_at or datetime.now(UTC)
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "status": "FAIL",
        "observed_at": _utc_iso8601(timestamp),
        "environment": PRACTICE_ENVIRONMENT,
        "account_scope": "REDACTED_RUNTIME_ACCOUNT",
        "failure_code": _failure_code(error),
        "execution_enabled": False,
        "live_trading_authorized": False,
    }


def safe_error_message(error: BaseException) -> str:
    """Produce a log-safe failure line that intentionally omits transport detail."""

    return f"oanda_read_only_smoke=FAIL code={_failure_code(error)}"


def json_report(report: dict[str, object]) -> str:
    """Serialize the small report through a single testable artifact boundary."""

    import json

    return json.dumps(report, sort_keys=True, indent=2) + "\n"
