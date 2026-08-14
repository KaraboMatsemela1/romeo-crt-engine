"""Deterministic order/position state and reconciliation models."""

from dataclasses import dataclass
from enum import StrEnum


class OrderStatus(StrEnum):
    CREATED = "CREATED"
    SUBMITTED = "SUBMITTED"
    ACCEPTED = "ACCEPTED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"
    UNKNOWN = "UNKNOWN"


class ReconciliationStatus(StrEnum):
    MATCH = "MATCH"
    MISMATCH = "MISMATCH"


@dataclass(frozen=True)
class OrderEvent:
    client_order_id: str
    status: OrderStatus
    filled_units: int = 0
    broker_order_id: str | None = None


@dataclass(frozen=True)
class OrderRecord:
    client_order_id: str
    status: OrderStatus = OrderStatus.CREATED
    requested_units: int = 0
    filled_units: int = 0
    broker_order_id: str | None = None
    events: tuple[OrderEvent, ...] = ()


@dataclass(frozen=True)
class PositionRecord:
    instrument: str
    units: int
    average_price: float


@dataclass(frozen=True)
class Reconciliation:
    status: ReconciliationStatus
    reasons: tuple[str, ...]


_ALLOWED = {
    OrderStatus.CREATED: {OrderStatus.SUBMITTED, OrderStatus.CANCELLED},
    OrderStatus.SUBMITTED: {
        OrderStatus.ACCEPTED,
        OrderStatus.REJECTED,
        OrderStatus.UNKNOWN,
    },
    OrderStatus.ACCEPTED: {
        OrderStatus.PARTIALLY_FILLED,
        OrderStatus.FILLED,
        OrderStatus.CANCELLED,
        OrderStatus.UNKNOWN,
    },
    OrderStatus.PARTIALLY_FILLED: {
        OrderStatus.PARTIALLY_FILLED,
        OrderStatus.FILLED,
        OrderStatus.CANCELLED,
        OrderStatus.UNKNOWN,
    },
    OrderStatus.FILLED: set(),
    OrderStatus.CANCELLED: set(),
    OrderStatus.REJECTED: set(),
    OrderStatus.UNKNOWN: set(),
}


def apply_event(record: OrderRecord, event: OrderEvent) -> OrderRecord:
    if event.client_order_id != record.client_order_id:
        raise ValueError("client-order-id does not match the persisted order")
    if event.status not in _ALLOWED[record.status]:
        raise ValueError(f"invalid order transition: {record.status} -> {event.status}")
    if event.filled_units < record.filled_units or event.filled_units > record.requested_units:
        raise ValueError("filled units must be monotonic and bounded by requested units")
    if record.broker_order_id and event.broker_order_id not in {
        None,
        record.broker_order_id,
    }:
        raise ValueError("broker order identity changed")
    broker_id = event.broker_order_id or record.broker_order_id
    return OrderRecord(
        client_order_id=record.client_order_id,
        status=event.status,
        requested_units=record.requested_units,
        filled_units=event.filled_units,
        broker_order_id=broker_id,
        events=record.events + (event,),
    )


def reconcile(
    expected_order: OrderRecord,
    broker_order: OrderRecord | None,
    expected_position: PositionRecord | None,
    broker_position: PositionRecord | None,
) -> Reconciliation:
    reasons: list[str] = []
    if broker_order is None and expected_order.status not in {
        OrderStatus.CANCELLED,
        OrderStatus.REJECTED,
    }:
        reasons.append("expected order is missing at broker")
    if broker_order is not None and (
        broker_order.client_order_id != expected_order.client_order_id
        or broker_order.status != expected_order.status
        or broker_order.filled_units != expected_order.filled_units
    ):
        reasons.append("order state differs from broker")
    if expected_position != broker_position:
        reasons.append("position state differs from broker")
    if reasons:
        return Reconciliation(ReconciliationStatus.MISMATCH, tuple(reasons))
    return Reconciliation(ReconciliationStatus.MATCH, ())
