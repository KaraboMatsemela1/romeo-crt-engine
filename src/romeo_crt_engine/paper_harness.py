"""Deterministic, execution-disabled paper-infrastructure composition harness.

This module is deliberately a contract harness, not a paper-trading service.  It
uses a supplied synthetic/frozen ``TradePlan`` and never calls an OANDA HTTP
endpoint or ``PracticeAdapter.execute``.  Its fake broker exists solely to
exercise the order, persistence, reconciliation, and observability boundaries.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path

from romeo_crt_engine.crt.v0_1 import Direction, TradePlan
from romeo_crt_engine.oanda_practice import OrderIntent
from romeo_crt_engine.observability import AuditEvent, EventType
from romeo_crt_engine.order_state import (
    OrderEvent,
    OrderRecord,
    OrderStatus,
    PositionRecord,
    ReconciliationStatus,
    apply_event,
    reconcile,
)
from romeo_crt_engine.risk_controls import OrderSafetyInput, RiskConfig, RiskDecision, check_order


class HarnessOutcome(StrEnum):
    ACCEPTED = "ACCEPTED"
    REJECTED_RISK = "REJECTED_RISK"
    REJECTED_AUTHORIZATION = "REJECTED_AUTHORIZATION"
    DUPLICATE_INTENT = "DUPLICATE_INTENT"
    BROKER_ERROR = "BROKER_ERROR"
    RECONCILIATION_MISMATCH = "RECONCILIATION_MISMATCH"


class FakeBrokerMode(StrEnum):
    FILL = "FILL"
    ERROR = "ERROR"
    POSITION_MISMATCH = "POSITION_MISMATCH"


@dataclass(frozen=True, slots=True)
class HarnessRequest:
    client_order_id: str
    instrument: str
    trade_plan: TradePlan
    risk_input: OrderSafetyInput
    occurred_at: str
    execution_authorized: bool = False


@dataclass(frozen=True, slots=True)
class HarnessResult:
    outcome: HarnessOutcome
    client_order_id: str
    order_status: OrderStatus | None
    reconciliation_status: ReconciliationStatus | None
    audit_events: tuple[AuditEvent, ...]
    report: dict[str, object]


class PersistentLifecycle:
    """Small JSON lifecycle journal, restart-safe for synthetic harness runs only."""

    def __init__(self, root: Path) -> None:
        self._path = root / "paper-harness-lifecycle.json"
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._orders: dict[str, OrderRecord] = {}
        self._positions: dict[str, PositionRecord] = {}
        if self._path.exists():
            self._load()

    def contains(self, client_order_id: str) -> bool:
        return client_order_id in self._orders

    def order(self, client_order_id: str) -> OrderRecord:
        return self._orders[client_order_id]

    def position(self, instrument: str) -> PositionRecord | None:
        return self._positions.get(instrument)

    def save_order(self, record: OrderRecord) -> None:
        self._orders[record.client_order_id] = record
        self._write()

    def save_position(self, position: PositionRecord) -> None:
        self._positions[position.instrument] = position
        self._write()

    def _load(self) -> None:
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        self._orders = {
            item["client_order_id"]: OrderRecord(
                client_order_id=item["client_order_id"],
                status=OrderStatus(item["status"]),
                requested_units=item["requested_units"],
                filled_units=item["filled_units"],
                broker_order_id=item["broker_order_id"],
                events=tuple(
                    OrderEvent(
                        client_order_id=event["client_order_id"],
                        status=OrderStatus(event["status"]),
                        filled_units=event["filled_units"],
                        broker_order_id=event["broker_order_id"],
                    )
                    for event in item["events"]
                ),
            )
            for item in raw["orders"]
        }
        self._positions = {item["instrument"]: PositionRecord(**item) for item in raw["positions"]}

    def _write(self) -> None:
        payload = {
            "orders": [
                {
                    **asdict(record),
                    "status": record.status.value,
                    "events": [
                        {**asdict(event), "status": event.status.value} for event in record.events
                    ],
                }
                for _, record in sorted(self._orders.items())
            ],
            "positions": [asdict(position) for _, position in sorted(self._positions.items())],
        }
        self._path.write_text(
            json.dumps(payload, sort_keys=True, separators=(",", ":")), encoding="utf-8"
        )


class FakeBroker:
    """No-network deterministic broker response source for contract tests."""

    def __init__(self, mode: FakeBrokerMode = FakeBrokerMode.FILL) -> None:
        self.mode = mode
        self.submissions: list[OrderIntent] = []

    def submit(self, intent: OrderIntent) -> tuple[OrderEvent, ...]:
        self.submissions.append(intent)
        if self.mode is FakeBrokerMode.ERROR:
            raise RuntimeError("synthetic broker error")
        broker_order_id = f"fake-{intent.client_order_id}"
        return (
            OrderEvent(
                intent.client_order_id,
                OrderStatus.ACCEPTED,
                broker_order_id=broker_order_id,
            ),
            OrderEvent(
                intent.client_order_id,
                OrderStatus.FILLED,
                filled_units=abs(intent.units),
                broker_order_id=broker_order_id,
            ),
        )

    def position_for(self, intent: OrderIntent, plan: TradePlan) -> PositionRecord:
        units = intent.units
        if self.mode is FakeBrokerMode.POSITION_MISMATCH:
            units = 0
        return PositionRecord(intent.instrument, units, plan.entry_price)


class PaperInfrastructureHarness:
    """Compose public safety contracts with a fake broker; execution remains disabled."""

    def __init__(self, lifecycle: PersistentLifecycle, broker: FakeBroker) -> None:
        self._lifecycle = lifecycle
        self._broker = broker
        self.kill_switch_engaged = False

    def run(self, request: HarnessRequest, config: RiskConfig) -> HarnessResult:
        events = [self._event(EventType.DECISION, request, "synthetic frozen TradePlan received")]
        if self._lifecycle.contains(request.client_order_id):
            return self._result(HarnessOutcome.DUPLICATE_INTENT, request, None, None, events)

        effective_config = RiskConfig(
            risk_per_trade=config.risk_per_trade,
            max_concurrent_positions=config.max_concurrent_positions,
            max_session_loss=config.max_session_loss,
            max_stale_seconds=config.max_stale_seconds,
            max_spread=config.max_spread,
            unit_precision=config.unit_precision,
            kill_switch_engaged=config.kill_switch_engaged or self.kill_switch_engaged,
        )
        risk = check_order(effective_config, request.risk_input)
        if risk.decision is RiskDecision.REJECT:
            events.append(self._event(EventType.RISK_REJECTION, request, "; ".join(risk.reasons)))
            return self._result(HarnessOutcome.REJECTED_RISK, request, None, None, events)
        if not request.execution_authorized:
            events.append(
                self._event(EventType.KILL_SWITCH, request, "execution authorization absent")
            )
            return self._result(HarnessOutcome.REJECTED_AUTHORIZATION, request, None, None, events)

        # Contract-only intent: this is delivered to FakeBroker, never PracticeAdapter.execute.
        intent_units = (
            -risk.units if request.trade_plan.direction is Direction.BEARISH else risk.units
        )
        intent = OrderIntent(request.client_order_id, request.instrument, intent_units)
        record = apply_event(
            OrderRecord(request.client_order_id, requested_units=risk.units),
            OrderEvent(request.client_order_id, OrderStatus.SUBMITTED),
        )
        self._lifecycle.save_order(record)
        events.append(self._event(EventType.ORDER, request, "fake-broker intent submitted"))
        try:
            for broker_event in self._broker.submit(intent):
                record = apply_event(record, broker_event)
                self._lifecycle.save_order(record)
                events.append(
                    self._event(EventType.BROKER_RESPONSE, request, broker_event.status.value)
                )
        except RuntimeError as error:
            events.append(self._event(EventType.BROKER_RESPONSE, request, str(error)))
            return self._result(HarnessOutcome.BROKER_ERROR, request, record.status, None, events)

        expected_position = PositionRecord(
            request.instrument, intent.units, request.trade_plan.entry_price
        )
        self._lifecycle.save_position(expected_position)
        broker_position = self._broker.position_for(intent, request.trade_plan)
        reconciliation = reconcile(record, record, expected_position, broker_position)
        events.append(self._event(EventType.POSITION, request, "synthetic position persisted"))
        events.append(self._event(EventType.RECONCILIATION, request, reconciliation.status.value))
        if reconciliation.status is ReconciliationStatus.MISMATCH:
            self.kill_switch_engaged = True
            events.append(self._event(EventType.KILL_SWITCH, request, "reconciliation mismatch"))
            return self._result(
                HarnessOutcome.RECONCILIATION_MISMATCH,
                request,
                record.status,
                reconciliation.status,
                events,
            )
        return self._result(
            HarnessOutcome.ACCEPTED, request, record.status, reconciliation.status, events
        )

    @staticmethod
    def _event(event_type: EventType, request: HarnessRequest, message: str) -> AuditEvent:
        return AuditEvent(
            event_type=event_type,
            event_id=f"{request.client_order_id}:{event_type.value}",
            occurred_at=request.occurred_at,
            candidate_id=request.trade_plan.strategy_version,
            message=message,
        )

    @staticmethod
    def _result(
        outcome: HarnessOutcome,
        request: HarnessRequest,
        order_status: OrderStatus | None,
        reconciliation_status: ReconciliationStatus | None,
        events: list[AuditEvent],
    ) -> HarnessResult:
        report: dict[str, object] = {
            "schema_version": "PAPER-INFRA-HARNESS-v1",
            "outcome": outcome.value,
            "client_order_id": request.client_order_id,
            "strategy_version": request.trade_plan.strategy_version,
            "execution_authorized": request.execution_authorized,
            "execution_disabled": True,
            "oanda_order_endpoint_called": False,
            "order_status": order_status.value if order_status else None,
            "reconciliation_status": reconciliation_status.value if reconciliation_status else None,
            "audit_event_types": [event.event_type.value for event in events],
        }
        return HarnessResult(
            outcome,
            request.client_order_id,
            order_status,
            reconciliation_status,
            tuple(events),
            report,
        )
