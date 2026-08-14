import pytest

from romeo_crt_engine.oanda_practice import (
    PRACTICE_URL,
    Environment,
    OandaConfig,
    OrderIntent,
    PracticeAdapter,
)


def config(**overrides):
    values = {
        "environment": Environment.PRACTICE,
        "base_url": PRACTICE_URL,
        "account_id": "practice-account",
        "token": "test-token",
    }
    return OandaConfig(**(values | overrides))


def test_practice_config_is_validated_and_health_is_read_only():
    adapter = PracticeAdapter(config())
    health = adapter.health_check()
    assert health.environment is Environment.PRACTICE
    assert health.read_only is True


def test_live_environment_and_live_url_are_rejected():
    with pytest.raises(ValueError):
        PracticeAdapter(config(environment=Environment.LIVE))
    with pytest.raises(ValueError):
        PracticeAdapter(config(base_url="https://api-fxtrade.oanda.com"))


def test_execution_is_disabled_by_default_and_rejects_orders():
    adapter = PracticeAdapter(config())
    with pytest.raises(PermissionError):
        adapter.execute(OrderIntent("client-1", "EUR_USD", 1))


def test_explicit_execution_enablement_is_rejected():
    with pytest.raises(ValueError):
        PracticeAdapter(config(execution_enabled=True))


def test_instrument_metadata_is_normalized():
    metadata = PracticeAdapter(config()).normalize_instrument("EUR_USD", 5, 0, 1)
    assert metadata.instrument == "EUR_USD"
