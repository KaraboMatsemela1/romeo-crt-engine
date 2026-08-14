"""Run the synthetic, execution-disabled paper infrastructure harness."""

from __future__ import annotations

import json
import tempfile
from datetime import UTC, datetime
from pathlib import Path

from romeo_crt_engine.crt.v0_1 import Direction, TradePlan
from romeo_crt_engine.paper_harness import (
    FakeBroker,
    FakeBrokerMode,
    HarnessRequest,
    PaperInfrastructureHarness,
    PersistentLifecycle,
)
from romeo_crt_engine.risk_controls import OrderSafetyInput, RiskConfig


def _plan() -> TradePlan:
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


def main() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        config = RiskConfig(kill_switch_engaged=False)

        def run(
            client_order_id: str,
            *,
            authorized: bool = True,
            market_age_seconds: int = 1,
            mode: FakeBrokerMode = FakeBrokerMode.FILL,
        ) -> dict[str, object]:
            request = HarnessRequest(
                client_order_id=client_order_id,
                instrument="EUR_USD",
                trade_plan=_plan(),
                risk_input=OrderSafetyInput(
                    10000, 0.01, 0, 0, market_age_seconds, 0.0001, True, 10, 1
                ),
                occurred_at="2026-01-01T00:00:00Z",
                execution_authorized=authorized,
            )
            return (
                PaperInfrastructureHarness(
                    PersistentLifecycle(root / client_order_id), FakeBroker(mode)
                )
                .run(request, config)
                .report
            )

        accepted = run("harness-accepted-001")
        duplicate_root = root / "duplicate"
        duplicate_harness = PaperInfrastructureHarness(
            PersistentLifecycle(duplicate_root), FakeBroker()
        )
        duplicate_request = HarnessRequest(
            "harness-duplicate-001",
            "EUR_USD",
            _plan(),
            OrderSafetyInput(10000, 0.01, 0, 0, 1, 0.0001, True, 10, 1),
            "2026-01-01T00:00:00Z",
            True,
        )
        duplicate_harness.run(duplicate_request, config)
        duplicate = duplicate_harness.run(duplicate_request, config).report
        report = {
            "schema_version": "PAPER-INFRA-HARNESS-INTEGRATION-v1",
            "execution_disabled": True,
            "oanda_order_endpoint_called": False,
            "fixtures": [
                accepted,
                run("harness-stale-001", market_age_seconds=61),
                run("harness-authorization-001", authorized=False),
                duplicate,
                run("harness-broker-error-001", mode=FakeBrokerMode.ERROR),
                run("harness-reconciliation-001", mode=FakeBrokerMode.POSITION_MISMATCH),
            ],
        }
        print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
