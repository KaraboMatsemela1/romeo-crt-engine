"""Structured paper-readiness telemetry and synthetic alert evaluation."""

from dataclasses import dataclass
from enum import StrEnum


class EventType(StrEnum):
    DECISION = "DECISION"
    ORDER = "ORDER"
    BROKER_RESPONSE = "BROKER_RESPONSE"
    POSITION = "POSITION"
    RISK_REJECTION = "RISK_REJECTION"
    KILL_SWITCH = "KILL_SWITCH"
    RECONCILIATION = "RECONCILIATION"


class AlertType(StrEnum):
    STALE_DATA = "STALE_DATA"
    RECONCILIATION_FAILURE = "RECONCILIATION_FAILURE"
    ORDER_ERROR = "ORDER_ERROR"
    RISK_LIMIT = "RISK_LIMIT"


@dataclass(frozen=True)
class AuditEvent:
    event_type: EventType
    event_id: str
    occurred_at: str
    candidate_id: str | None = None
    detector_hash: str | None = None
    data_hash: str | None = None
    message: str = ""


@dataclass(frozen=True)
class AlertThresholds:
    max_data_age_seconds: int = 60
    max_order_errors: int = 3
    max_risk_rejections: int = 1


@dataclass(frozen=True)
class Alert:
    alert_type: AlertType
    message: str


def evaluate_alerts(
    *,
    data_age_seconds: int,
    reconciliation_ok: bool,
    order_errors: int,
    risk_rejections: int,
    thresholds: AlertThresholds,
) -> tuple[Alert, ...]:
    alerts: list[Alert] = []
    if data_age_seconds > thresholds.max_data_age_seconds:
        alerts.append(Alert(AlertType.STALE_DATA, "market data is stale"))
    if not reconciliation_ok:
        alerts.append(Alert(AlertType.RECONCILIATION_FAILURE, "broker reconciliation failed"))
    if order_errors >= thresholds.max_order_errors:
        alerts.append(Alert(AlertType.ORDER_ERROR, "repeated broker order errors"))
    if risk_rejections >= thresholds.max_risk_rejections:
        alerts.append(Alert(AlertType.RISK_LIMIT, "risk rejection threshold reached"))
    return tuple(alerts)


def daily_summary(events: tuple[AuditEvent, ...]) -> dict[str, int]:
    summary = {event_type.value: 0 for event_type in EventType}
    for event in events:
        summary[event.event_type.value] += 1
    return summary
