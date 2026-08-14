from romeo_crt_engine.risk_controls import (
    OrderSafetyInput,
    RiskConfig,
    RiskDecision,
    check_order,
    rounded_units,
)


def safe_request(**overrides):
    values = {
        "equity": 10000,
        "requested_risk": 0.01,
        "concurrent_positions": 0,
        "session_loss": 0,
        "market_age_seconds": 1,
        "spread": 0.0001,
        "session_eligible": True,
        "stop_distance": 10,
        "value_per_unit": 1,
    }
    return OrderSafetyInput(**(values | overrides))


def enabled_config(**overrides):
    return RiskConfig(kill_switch_engaged=False, **overrides)


def test_fail_closed_by_default():
    result = check_order(RiskConfig(), safe_request())
    assert result.decision is RiskDecision.REJECT
    assert "kill switch is engaged" in result.reasons


def test_every_rejection_path_is_hard():
    config = enabled_config()
    for field, value in (
        ("requested_risk", 0.011),
        ("concurrent_positions", 1),
        ("session_loss", 0.02),
        ("market_age_seconds", 61),
        ("spread", 0.0006),
        ("session_eligible", False),
    ):
        result = check_order(config, safe_request(**{field: value}))
        assert result.decision is RiskDecision.REJECT


def test_safe_order_is_sized_and_accepted():
    result = check_order(enabled_config(), safe_request())
    assert result.decision is RiskDecision.ACCEPT
    assert result.units == 10


def test_invalid_sizing_rejects():
    result = check_order(enabled_config(), safe_request(stop_distance=0))
    assert result.decision is RiskDecision.REJECT
    assert "position sizing inputs must be positive" in result.reasons


def test_rounding_never_rounds_up():
    assert rounded_units(10000, 0.01, 3, 1, 0) == 33
