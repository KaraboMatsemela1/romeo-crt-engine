import pytest

from romeo_crt_engine.order_state import (
    OrderEvent,
    OrderRecord,
    OrderStatus,
    PositionRecord,
    ReconciliationStatus,
    apply_event,
    reconcile,
)


def test_idempotent_client_order_identity_and_transition_audit():
    record = OrderRecord("client-1", requested_units=10)
    record = apply_event(record, OrderEvent("client-1", OrderStatus.SUBMITTED))
    record = apply_event(record, OrderEvent("client-1", OrderStatus.ACCEPTED, broker_order_id="broker-1"))
    record = apply_event(record, OrderEvent("client-1", OrderStatus.FILLED, filled_units=10))
    assert record.status is OrderStatus.FILLED
    assert record.broker_order_id == "broker-1"
    assert len(record.events) == 3


def test_invalid_or_duplicate_state_fails_closed():
    record = OrderRecord("client-1", requested_units=10)
    with pytest.raises(ValueError):
        apply_event(record, OrderEvent("other", OrderStatus.SUBMITTED))
    record = apply_event(record, OrderEvent("client-1", OrderStatus.SUBMITTED))
    with pytest.raises(ValueError):
        apply_event(record, OrderEvent("client-1", OrderStatus.CREATED))


def test_partial_fill_cannot_exceed_request():
    record = OrderRecord("client-1", requested_units=10)
    record = apply_event(record, OrderEvent("client-1", OrderStatus.SUBMITTED))
    with pytest.raises(ValueError):
        apply_event(record, OrderEvent("client-1", OrderStatus.ACCEPTED, filled_units=11))


def test_reconciliation_mismatch_fails_closed():
    order = OrderRecord("client-1", OrderStatus.FILLED, 10, 10, "broker-1")
    broker = OrderRecord("client-1", OrderStatus.ACCEPTED, 10, 5, "broker-1")
    result = reconcile(order, broker, None, None)
    assert result.status is ReconciliationStatus.MISMATCH


def test_reconciliation_matches_complete_state():
    position = PositionRecord("EUR_USD", 10, 1.1)
    order = OrderRecord("client-1", OrderStatus.FILLED, 10, 10, "broker-1")
    result = reconcile(order, order, position, position)
    assert result.status is ReconciliationStatus.MATCH
