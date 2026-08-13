from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from hashlib import sha256
from pathlib import Path
from typing import Final

from romeo_crt_engine.crt.detector import DetectorCandidate
from romeo_crt_engine.crt.v0_1 import Direction, TradePlan

SIMULATOR_VERSION: Final = "CRT-BACKTEST-v0.1.1"
EXECUTION_ASSUMPTION_VERSION: Final = "SYNTHETIC_LINEAR_SHORT_RESEARCH_V1"


class ExitReason(StrEnum):
    TARGET = "TARGET"
    STOP = "STOP"
    STOP_SAME_BAR_AMBIGUITY = "STOP_SAME_BAR_AMBIGUITY"
    STOP_GAP = "STOP_GAP"
    TARGET_GAP = "TARGET_GAP"


class RejectionReason(StrEnum):
    POSITION_LIMIT = "POSITION_LIMIT"
    MISSING_ENTRY_CLOCK = "MISSING_ENTRY_CLOCK"
    ENTRY_REFERENCE_MISMATCH = "ENTRY_REFERENCE_MISMATCH"
    SIMULTANEOUS_PLAN_CONFLICT = "SIMULTANEOUS_PLAN_CONFLICT"
    SIZE_BELOW_MIN_STEP = "SIZE_BELOW_MIN_STEP"
    UNSUPPORTED_DIRECTION = "UNSUPPORTED_DIRECTION"


class JournalEventType(StrEnum):
    PLAN_REJECTED = "PLAN_REJECTED"
    ENTRY_FILLED = "ENTRY_FILLED"
    EXIT_FILLED = "EXIT_FILLED"
    POSITION_OPEN_AT_END = "POSITION_OPEN_AT_END"


@dataclass(frozen=True, slots=True)
class CostModel:
    version: str
    fee_bps_per_side: Decimal
    half_spread_bps_per_side: Decimal
    slippage_bps_per_side: Decimal

    def __post_init__(self) -> None:
        if not self.version:
            raise ValueError("cost-model version must not be empty")
        for name, value in (
            ("fee_bps_per_side", self.fee_bps_per_side),
            ("half_spread_bps_per_side", self.half_spread_bps_per_side),
            ("slippage_bps_per_side", self.slippage_bps_per_side),
        ):
            if not value.is_finite() or value < 0:
                raise ValueError(f"{name} must be finite and non-negative")

    @property
    def fee_rate(self) -> Decimal:
        return self.fee_bps_per_side / Decimal(10_000)

    @property
    def adverse_price_rate(self) -> Decimal:
        return (self.half_spread_bps_per_side + self.slippage_bps_per_side) / Decimal(10_000)


IDEAL_COSTS: Final = CostModel(
    version="P5-COST-IDEAL-V1",
    fee_bps_per_side=Decimal(0),
    half_spread_bps_per_side=Decimal(0),
    slippage_bps_per_side=Decimal(0),
)

BASE_COSTS: Final = CostModel(
    version="P5-COST-BASE-V1",
    fee_bps_per_side=Decimal(10),
    half_spread_bps_per_side=Decimal(1),
    slippage_bps_per_side=Decimal(2),
)

STRESSED_COSTS: Final = CostModel(
    version="P5-COST-STRESSED-V1",
    fee_bps_per_side=Decimal(15),
    half_spread_bps_per_side=Decimal(3),
    slippage_bps_per_side=Decimal(5),
)

SEVERE_COSTS: Final = CostModel(
    version="P5-COST-SEVERE-V1",
    fee_bps_per_side=Decimal(20),
    half_spread_bps_per_side=Decimal(5),
    slippage_bps_per_side=Decimal(10),
)


@dataclass(frozen=True, slots=True)
class BacktestConfig:
    initial_equity: Decimal = Decimal(100_000)
    risk_fraction: Decimal = Decimal("0.005")
    max_concurrent_positions: int = 1
    cost_model: CostModel = BASE_COSTS
    execution_assumption_version: str = EXECUTION_ASSUMPTION_VERSION
    same_bar_policy: str = "STOP_FIRST_CONSERVATIVE"
    target_gap_price_improvement: bool = False
    force_close_at_dataset_end: bool = False

    def __post_init__(self) -> None:
        if not self.initial_equity.is_finite() or self.initial_equity <= 0:
            raise ValueError("initial_equity must be positive and finite")
        if not self.risk_fraction.is_finite() or not Decimal(0) < self.risk_fraction <= Decimal(1):
            raise ValueError("risk_fraction must be in (0, 1]")
        if self.max_concurrent_positions <= 0:
            raise ValueError("max_concurrent_positions must be > 0")
        if not self.execution_assumption_version:
            raise ValueError("execution_assumption_version must not be empty")
        if self.same_bar_policy != "STOP_FIRST_CONSERVATIVE":
            raise ValueError("v0.1 supports STOP_FIRST_CONSERVATIVE only")
        if self.target_gap_price_improvement:
            raise ValueError("v0.1 intentionally disables favorable target-gap improvement")
        if self.force_close_at_dataset_end:
            raise ValueError("v0.1 does not invent a strategy time exit at dataset end")

    @property
    def config_sha256(self) -> str:
        payload = {
            "simulator_version": SIMULATOR_VERSION,
            "initial_equity": str(self.initial_equity),
            "risk_fraction": str(self.risk_fraction),
            "max_concurrent_positions": self.max_concurrent_positions,
            "execution_assumption_version": self.execution_assumption_version,
            "same_bar_policy": self.same_bar_policy,
            "target_gap_price_improvement": self.target_gap_price_improvement,
            "force_close_at_dataset_end": self.force_close_at_dataset_end,
            "cost_model": {
                "version": self.cost_model.version,
                "fee_bps_per_side": str(self.cost_model.fee_bps_per_side),
                "half_spread_bps_per_side": str(self.cost_model.half_spread_bps_per_side),
                "slippage_bps_per_side": str(self.cost_model.slippage_bps_per_side),
            },
        }
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return sha256(encoded).hexdigest()


@dataclass(frozen=True, slots=True)
class SimulatedFill:
    timestamp: datetime
    reference_price: Decimal
    fill_price: Decimal
    quantity: Decimal
    fee: Decimal

    def __post_init__(self) -> None:
        if self.timestamp.utcoffset() is None:
            raise ValueError("fill timestamp must be timezone-aware")
        for name, value in (
            ("reference_price", self.reference_price),
            ("fill_price", self.fill_price),
            ("quantity", self.quantity),
        ):
            if not value.is_finite() or value <= 0:
                raise ValueError(f"{name} must be positive and finite")
        if not self.fee.is_finite() or self.fee < 0:
            raise ValueError("fee must be finite and non-negative")


@dataclass(frozen=True, slots=True)
class OpenPosition:
    candidate_id: str
    plan: TradePlan
    entry_fill: SimulatedFill
    risk_budget: Decimal
    estimated_stop_loss: Decimal


@dataclass(frozen=True, slots=True)
class CompletedTrade:
    candidate_id: str
    plan: TradePlan
    entry_fill: SimulatedFill
    exit_fill: SimulatedFill
    exit_reason: ExitReason
    risk_budget: Decimal
    gross_pnl: Decimal
    total_fees: Decimal
    net_pnl: Decimal
    r_multiple: Decimal
    equity_after: Decimal


@dataclass(frozen=True, slots=True)
class PlanRejection:
    candidate_id: str
    timestamp: datetime
    reason: RejectionReason


@dataclass(frozen=True, slots=True)
class OpenAtEnd:
    candidate_id: str
    plan: TradePlan
    entry_fill: SimulatedFill
    final_mark_time: datetime
    final_mark_price: Decimal
    unrealized_gross_pnl: Decimal


@dataclass(frozen=True, slots=True)
class JournalEvent:
    timestamp: datetime
    event_type: JournalEventType
    candidate_id: str
    detail: str


@dataclass(frozen=True, slots=True)
class BacktestMetrics:
    closed_trades: int
    wins: int
    losses: int
    win_rate: Decimal | None
    gross_pnl: Decimal
    net_pnl: Decimal
    total_fees: Decimal
    average_r: Decimal | None
    expectancy_r: Decimal | None
    profit_factor: Decimal | None
    max_realized_drawdown: Decimal


@dataclass(frozen=True, slots=True)
class BacktestResult:
    simulator_version: str
    simulator_code_sha256: str
    strategy_version: str
    detector_version: str
    detector_run_sha256: str
    dataset_version: str
    dataset_manifest_sha256: str
    symbol: str
    quantity_step: Decimal
    config: BacktestConfig
    completed_trades: tuple[CompletedTrade, ...]
    rejections: tuple[PlanRejection, ...]
    open_at_end: tuple[OpenAtEnd, ...]
    journal: tuple[JournalEvent, ...]
    metrics: BacktestMetrics
    final_realized_equity: Decimal
    run_sha256: str

    def __post_init__(self) -> None:
        for name, digest in (
            ("simulator_code_sha256", self.simulator_code_sha256),
            ("detector_run_sha256", self.detector_run_sha256),
            ("dataset_manifest_sha256", self.dataset_manifest_sha256),
            ("run_sha256", self.run_sha256),
        ):
            if len(digest) != 64:
                raise ValueError(f"{name} must be a SHA-256 digest")
        if not self.quantity_step.is_finite() or self.quantity_step <= 0:
            raise ValueError("quantity_step must be positive and finite")

    def to_summary_dict(self) -> dict[str, object]:
        return {
            "simulator_version": self.simulator_version,
            "simulator_code_sha256": self.simulator_code_sha256,
            "strategy_version": self.strategy_version,
            "detector_version": self.detector_version,
            "detector_run_sha256": self.detector_run_sha256,
            "dataset_version": self.dataset_version,
            "dataset_manifest_sha256": self.dataset_manifest_sha256,
            "symbol": self.symbol,
            "quantity_step": str(self.quantity_step),
            "config_sha256": self.config.config_sha256,
            "completed_trades": len(self.completed_trades),
            "rejections": len(self.rejections),
            "open_at_end": len(self.open_at_end),
            "final_realized_equity": str(self.final_realized_equity),
            "metrics": asdict(self.metrics),
            "run_sha256": self.run_sha256,
        }


def simulator_code_sha256() -> str:
    root = Path(__file__).resolve().parent
    files = sorted(root.glob("*.py"))
    if not files:
        raise RuntimeError("backtest source files not found")
    digest = sha256()
    for path in files:
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def trade_plan_decimal_prices(plan: TradePlan) -> tuple[Decimal, Decimal, Decimal]:
    if plan.direction is not Direction.BEARISH:
        raise ValueError("v0.1 simulator supports the frozen bearish route only")
    return (
        Decimal(str(plan.entry_price)),
        Decimal(str(plan.stop_price)),
        Decimal(str(plan.target_price)),
    )


def candidate_trade_plan(candidate: DetectorCandidate) -> TradePlan | None:
    return candidate.trade_plan
