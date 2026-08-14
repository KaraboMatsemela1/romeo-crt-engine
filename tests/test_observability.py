from romeo_crt_engine.observability import (
    AlertThresholds,
    AlertType,
    AuditEvent,
    EventType,
    daily_summary,
    evaluate_alerts,
)


def test_alerts_cover_operational_failure_paths():
    alerts = evaluate_alerts(
        data_age_seconds=61,
        reconciliation_ok=False,
        order_errors=3,
        risk_rejections=1,
        thresholds=AlertThresholds(),
    )
    assert {alert.alert_type for alert in alerts} == {
        AlertType.STALE_DATA,
        AlertType.RECONCILIATION_FAILURE,
        AlertType.ORDER_ERROR,
        AlertType.RISK_LIMIT,
    }


def test_healthy_inputs_do_not_alert():
    assert evaluate_alerts(
        data_age_seconds=1,
        reconciliation_ok=True,
        order_errors=0,
        risk_rejections=0,
        thresholds=AlertThresholds(),
    ) == ()


def test_daily_summary_is_deterministic():
    events = (
        AuditEvent(EventType.DECISION, "d1", "2026-01-01T00:00:00Z"),
        AuditEvent(EventType.ORDER, "o1", "2026-01-01T00:00:01Z"),
        AuditEvent(EventType.ORDER, "o2", "2026-01-01T00:00:02Z"),
    )
    summary = daily_summary(events)
    assert summary[EventType.DECISION.value] == 1
    assert summary[EventType.ORDER.value] == 2
    assert sum(summary.values()) == 3
