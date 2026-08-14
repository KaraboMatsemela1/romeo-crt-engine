from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal

import pytest

from romeo_crt_engine.market_data.providers.oanda_account import OandaAccountQualificationRecord
from romeo_crt_engine.market_data.providers.oanda_v20 import OandaInstrumentRecord
from romeo_crt_engine.oanda_readonly_smoke import (
    SmokeGuardError,
    SmokeRuntimeConfig,
    failure_report,
    json_report,
    redact_sensitive_text,
    run_read_only_smoke,
    safe_error_message,
    validate_practice_endpoint,
)


def _environment(**overrides: str) -> dict[str, str]:
    return {
        "OANDA_ENV": "practice",
        "OANDA_ACCOUNT_ID": "001-001-SECRET-ACCOUNT",
        "OANDA_API_TOKEN": "secret-token-value",
    } | overrides


@pytest.mark.parametrize(
    "endpoint",
    (
        "http://api-fxpractice.oanda.com",
        "https://api-fxtrade.oanda.com",
        "https://api-fxpractice.oanda.com/v3/accounts",
        "https://api-fxpractice.oanda.com?redirect=example",
        "https://user@api-fxpractice.oanda.com",
        "https://api-fxpractice.oanda.com//",
    ),
)
def test_practice_endpoint_guard_rejects_non_exact_urls(endpoint: str) -> None:
    with pytest.raises(SmokeGuardError, match="exact_practice_endpoint_required"):
        validate_practice_endpoint(endpoint)


def test_runtime_configuration_fails_closed_for_missing_live_or_override_values() -> None:
    for environment in (
        _environment(OANDA_ENV="live"),
        _environment(OANDA_ENV=" practice"),
        _environment(OANDA_ACCOUNT_ID=""),
        _environment(OANDA_ACCOUNT_ID="account/changes-path"),
        _environment(OANDA_API_TOKEN=""),
        _environment(OANDA_BASE_URL="https://api-fxtrade.oanda.com"),
    ):
        with pytest.raises(SmokeGuardError):
            SmokeRuntimeConfig.from_environment(environment)


def test_account_mismatch_stops_before_account_or_instrument_reads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = SmokeRuntimeConfig.from_environment(_environment())
    calls: list[str] = []

    def authorized_accounts(**_: object) -> tuple[str, ...]:
        calls.append("accounts")
        return ("another-account",)

    monkeypatch.setattr(
        "romeo_crt_engine.oanda_readonly_smoke.fetch_authorized_account_ids", authorized_accounts
    )
    monkeypatch.setattr(
        "romeo_crt_engine.oanda_readonly_smoke.fetch_account_summary",
        lambda **_: pytest.fail("summary request must not occur"),
    )
    monkeypatch.setattr(
        "romeo_crt_engine.oanda_readonly_smoke.fetch_account_instruments",
        lambda **_: pytest.fail("instrument request must not occur"),
    )

    with pytest.raises(SmokeGuardError, match="configured_account_not_authorized"):
        run_read_only_smoke(config)
    assert calls == ["accounts"]


@pytest.mark.parametrize(
    ("account_id", "token"),
    (
        ("account/changes-path", "secret-token-value"),
        (" account-with-space", "secret-token-value"),
        ("001-001-SECRET-ACCOUNT", " secret-token-value"),
    ),
)
def test_malformed_runtime_credentials_stop_before_any_read(
    monkeypatch: pytest.MonkeyPatch,
    account_id: str,
    token: str,
) -> None:
    calls: list[str] = []
    config = SmokeRuntimeConfig("practice", account_id, token)
    monkeypatch.setattr(
        "romeo_crt_engine.oanda_readonly_smoke.fetch_authorized_account_ids",
        lambda **_: calls.append("accounts"),
    )

    with pytest.raises(SmokeGuardError):
        run_read_only_smoke(config)
    assert calls == []


def test_smoke_uses_only_read_operations_and_non_secret_report(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    config = SmokeRuntimeConfig.from_environment(_environment())
    calls: list[str] = []
    observed_at = datetime(2026, 8, 14, 12, 0, tzinfo=UTC)

    def authorized_accounts(**_: object) -> tuple[str, ...]:
        calls.append("accounts")
        return (config.account_id,)

    def summary(**_: object) -> OandaAccountQualificationRecord:
        calls.append("summary")
        return OandaAccountQualificationRecord(
            "USD", Decimal(0), False, None, observed_at, "a" * 64
        )

    def instruments(**_: object) -> tuple[OandaInstrumentRecord, ...]:
        calls.append("instruments")
        return ()

    monkeypatch.setattr(
        "romeo_crt_engine.oanda_readonly_smoke.fetch_authorized_account_ids", authorized_accounts
    )
    monkeypatch.setattr("romeo_crt_engine.oanda_readonly_smoke.fetch_account_summary", summary)
    monkeypatch.setattr(
        "romeo_crt_engine.oanda_readonly_smoke.fetch_account_instruments", instruments
    )

    report = run_read_only_smoke(config, observed_at=observed_at)

    assert calls == ["accounts", "summary", "instruments"]
    assert report["status"] == "PASS"
    assert report["observed_at"] == observed_at.isoformat()
    assert report["execution_enabled"] is False
    assert report["permitted_requests"] == [
        "GET /v3/accounts",
        "GET /v3/accounts/[REDACTED]/summary",
        "GET /v3/accounts/[REDACTED]/instruments",
    ]
    serialized = json_report(report)
    assert config.account_id not in serialized
    assert config.token not in serialized


def test_redaction_and_failure_artifacts_never_include_configured_secrets() -> None:
    config = SmokeRuntimeConfig.from_environment(_environment())
    observed_at = datetime(2026, 8, 14, 12, 0, tzinfo=UTC)
    leaked = (
        f"Authorization: Bearer {config.token}; "
        f"https://api-fxpractice.oanda.com/v3/accounts/{config.account_id}/summary"
    )

    redacted = redact_sensitive_text(leaked, token=config.token, account_id=config.account_id)
    report = failure_report(RuntimeError(leaked), observed_at=observed_at)
    message = safe_error_message(RuntimeError(leaked))

    assert config.token not in redacted
    assert config.account_id not in redacted
    assert config.token not in json_report(report)
    assert config.account_id not in json_report(report)
    assert config.token not in message
    assert config.account_id not in message
    assert report["failure_code"] == "read_only_connectivity_check_failed"
    assert report["observed_at"] == observed_at.isoformat()
    assert config.token not in json_report(failure_report(SmokeGuardError(leaked)))


def test_redaction_handles_overlapping_configured_secret_values() -> None:
    account_id = "account-secret-token"
    token = "secret-token"
    leaked = f"Authorization: Bearer {token}; account={account_id}"
    redacted = redact_sensitive_text(
        leaked,
        token=token,
        account_id=account_id,
    )

    assert token not in redacted
    assert account_id not in redacted
    artifact = json_report(failure_report(SmokeGuardError(leaked)))
    assert token not in artifact
    assert account_id not in artifact
