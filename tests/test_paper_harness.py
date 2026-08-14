from __future__ import annotations

from dataclasses import replace
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

from romeo_crt_engine.crt.v0_1 import Direction, TradePlan
from romeo_crt_engine.paper_harness import (
    FakeBroker,
    FakeBrokerMode,
    HarnessOutcome,
    HarnessRequest,
    PaperInfrastructureHarness,
    PersistentLifecycle,
)
from romeo_crt_engine.risk_controls import OrderSafetyInput, RiskConfig


def plan() -> TradePlan:
    timestamp = datetime(2026, 1, 1, tzinfo=UTC)
    return TradePlan(
        strategy_version="CRT-C3-D1-H1-M1-BEAR-v0.1",
        doctrine_version="CRT_SECRETS_2025",
        freeze_parameter_version="P2_FREEZE_2026_08_12",
        direction=Direction.BEARISH,
        entry_time=timestamp,
        entry_price=1.1,
        stop_reference_price=1.11,
        stop_price=1.11001,
        target_price=1.09,
        key_level=1.1,
        parent_c1_open_time=timestamp,
        parent_c2_open_time=timestamp,
        c3_open_time=timestamp,
        model1_open_time=timestamp,
        evidence_ids=("synthetic-harness-only",),
    )


def request(
    *,
    client_order_id: str = "intent-001",
    risk_input: OrderSafetyInput | None = None,
    execution_authorized: bool = True,
) -> HarnessRequest:
    return HarnessRequest(
        client_order_id=client_order_id,
        instrument="EUR_USD",
        trade_plan=plan(),
        risk_input=risk_input or OrderSafetyInput(10000, 0.01, 0, 0, 1, 0.0001, True, 10, 1),
        occurred_at="2026-01-01T00:00:00Z",
        execution_authorized=execution_authorized,
    )


def harness(
    tmp_path: Path, mode: FakeBrokerMode = FakeBrokerMode.FILL
) -> tuple[PaperInfrastructureHarness, FakeBroker]:
    broker = FakeBroker(mode)
    return PaperInfrastructureHarness(PersistentLifecycle(tmp_path), broker), broker


def test_happy_path_persists_lifecycle_and_emits_compact_machine_report(tmp_path: Path) -> None:
    runner, broker = harness(tmp_path)
    result = runner.run(request(), RiskConfig(kill_switch_engaged=False))
    assert result.outcome is HarnessOutcome.ACCEPTED
    assert result.report["execution_disabled"] is True
    assert result.report["oanda_order_endpoint_called"] is False
    assert len(broker.submissions) == 1
    assert PersistentLifecycle(tmp_path).order("intent-001").filled_units == 10


def test_fake_intent_units_follow_supplied_trade_plan_direction(tmp_path: Path) -> None:
    bearish_runner, bearish_broker = harness(tmp_path / "bearish")
    bearish_runner.run(request(), RiskConfig(kill_switch_engaged=False))

    bullish_runner, bullish_broker = harness(tmp_path / "bullish")
    bullish_plan = replace(plan(), direction=cast(Direction, "BULLISH"))
    bullish_request = replace(request(client_order_id="intent-002"), trade_plan=bullish_plan)
    bullish_runner.run(bullish_request, RiskConfig(kill_switch_engaged=False))

    assert bearish_broker.submissions[0].units == -10
    assert bullish_broker.submissions[0].units == 10


def test_positive_and_negative_risk_and_absent_authorization_never_submit(tmp_path: Path) -> None:
    runner, broker = harness(tmp_path)
    stale = runner.run(
        request(risk_input=OrderSafetyInput(10000, 0.01, 0, 0, 61, 0.0001, True, 10, 1)),
        RiskConfig(kill_switch_engaged=False),
    )
    assert stale.outcome is HarnessOutcome.REJECTED_RISK
    unauthorized = runner.run(
        request(client_order_id="intent-002", execution_authorized=False),
        RiskConfig(kill_switch_engaged=False),
    )
    assert unauthorized.outcome is HarnessOutcome.REJECTED_AUTHORIZATION
    killed = runner.run(request(client_order_id="intent-003"), RiskConfig())
    assert killed.outcome is HarnessOutcome.REJECTED_RISK
    assert broker.submissions == []


def test_duplicate_intent_is_idempotently_rejected_without_second_broker_submission(
    tmp_path: Path,
) -> None:
    runner, broker = harness(tmp_path)
    assert (
        runner.run(request(), RiskConfig(kill_switch_engaged=False)).outcome
        is HarnessOutcome.ACCEPTED
    )
    assert (
        runner.run(request(), RiskConfig(kill_switch_engaged=False)).outcome
        is HarnessOutcome.DUPLICATE_INTENT
    )
    assert len(broker.submissions) == 1


def test_broker_error_engages_kill_switch_and_blocks_later_authorized_submission(
    tmp_path: Path,
) -> None:
    errored, broker = harness(tmp_path, FakeBrokerMode.ERROR)
    result = errored.run(request(), RiskConfig(kill_switch_engaged=False))

    assert result.outcome is HarnessOutcome.BROKER_ERROR
    assert errored.kill_switch_engaged is True
    assert len(broker.submissions) == 1
    later_request = errored.run(
        request(client_order_id="intent-002", execution_authorized=True),
        RiskConfig(kill_switch_engaged=False),
    )
    assert later_request.outcome is HarnessOutcome.REJECTED_RISK
    assert len(broker.submissions) == 1


def test_reconciliation_mismatch_engages_kill_switch(tmp_path: Path) -> None:
    mismatch, _ = harness(tmp_path / "mismatch", FakeBrokerMode.POSITION_MISMATCH)
    result = mismatch.run(request(), RiskConfig(kill_switch_engaged=False))
    assert result.outcome is HarnessOutcome.RECONCILIATION_MISMATCH
    assert mismatch.kill_switch_engaged is True
