from __future__ import annotations

import json
from dataclasses import dataclass
from enum import StrEnum
from hashlib import sha256
from typing import Final

from romeo_crt_engine.crt.detector_v2 import (
    ALPHA_STRATEGY_VERSION,
    DETECTOR_VERSION_V2,
    MULTI_MARKET_CANDIDATE_VERSION,
    DetectorRunStatusV2,
    DetectorRunV2,
)

ACTIVITY_PROTOCOL_VERSION: Final = "P6B-MULTI-MARKET-ACTIVITY-PROTOCOL-v1"
MINIMUM_ACCEPTED_INSTRUMENTS: Final = 2
MINIMUM_CONTRIBUTING_INSTRUMENTS: Final = 2
MINIMUM_POOLED_TRADE_PLANS: Final = 30


class ActivityGateDecision(StrEnum):
    INSUFFICIENT_ELIGIBLE_UNIVERSE = "INSUFFICIENT_ELIGIBLE_UNIVERSE"
    INSUFFICIENT_MULTI_MARKET_SAMPLE = "INSUFFICIENT_MULTI_MARKET_SAMPLE"
    SUFFICIENT_ACTIVITY_FOR_PERFORMANCE_PROTOCOL = (
        "SUFFICIENT_ACTIVITY_FOR_PERFORMANCE_PROTOCOL"
    )


@dataclass(frozen=True, slots=True)
class InstrumentActivitySummary:
    instrument: str
    dataset_version: str
    detector_candidates: int
    no_signal_count: int
    trade_plan_count: int
    reason_counts: tuple[tuple[str, int], ...]

    def __post_init__(self) -> None:
        if not self.instrument or not self.dataset_version:
            raise ValueError("instrument activity identity must not be empty")
        if min(self.detector_candidates, self.no_signal_count, self.trade_plan_count) < 0:
            raise ValueError("activity counts must be non-negative")
        if self.no_signal_count + self.trade_plan_count != self.detector_candidates:
            raise ValueError("NO_SIGNAL + TRADE_PLAN must equal detector candidate count")
        if sum(count for _, count in self.reason_counts) != self.detector_candidates:
            raise ValueError("ReasonCode counts must equal detector candidate count")
        if any(not reason or count < 0 for reason, count in self.reason_counts):
            raise ValueError("invalid reason-count entry")
        if tuple(sorted(self.reason_counts)) != self.reason_counts:
            raise ValueError("reason_counts must be sorted for deterministic reporting")


@dataclass(frozen=True, slots=True)
class MultiMarketActivityGateResult:
    protocol_version: str
    candidate_version: str
    alpha_strategy_version: str
    detector_version: str
    accepted_instrument_count: int
    contributing_instrument_count: int
    pooled_detector_candidates: int
    pooled_no_signal_count: int
    pooled_trade_plan_count: int
    instruments: tuple[InstrumentActivitySummary, ...]
    decision: ActivityGateDecision
    report_sha256: str
    backtest_executed: bool = False
    pnl_outcome_access_authorized: bool = False

    def __post_init__(self) -> None:
        if self.protocol_version != ACTIVITY_PROTOCOL_VERSION:
            raise ValueError("unexpected activity protocol version")
        if self.candidate_version != MULTI_MARKET_CANDIDATE_VERSION:
            raise ValueError("unexpected multi-market candidate version")
        if self.alpha_strategy_version != ALPHA_STRATEGY_VERSION:
            raise ValueError("activity gate must preserve v0.1 alpha identity")
        if self.detector_version != DETECTOR_VERSION_V2:
            raise ValueError("activity gate must use frozen multi-market detector")
        if self.backtest_executed or self.pnl_outcome_access_authorized:
            raise ValueError("activity gate must never authorize or execute P&L outcomes")
        if len(self.report_sha256) != 64:
            raise ValueError("report_sha256 must be a SHA-256 digest")


def instrument_activity_from_detector(run: DetectorRunV2) -> InstrumentActivitySummary:
    if run.status is not DetectorRunStatusV2.COMPLETE:
        raise ValueError("accepted activity instruments require COMPLETE detector runs")
    reasons: dict[str, int] = {}
    for candidate in run.candidates:
        reason = candidate.reason.value
        reasons[reason] = reasons.get(reason, 0) + 1
    return InstrumentActivitySummary(
        instrument=run.dataset.instrument,
        dataset_version=run.dataset.dataset_version,
        detector_candidates=len(run.candidates),
        no_signal_count=run.no_signal_count,
        trade_plan_count=run.trade_plan_count,
        reason_counts=tuple(sorted(reasons.items())),
    )


def _decision(
    *,
    accepted_instrument_count: int,
    contributing_instrument_count: int,
    pooled_trade_plan_count: int,
) -> ActivityGateDecision:
    if accepted_instrument_count < MINIMUM_ACCEPTED_INSTRUMENTS:
        return ActivityGateDecision.INSUFFICIENT_ELIGIBLE_UNIVERSE
    if (
        contributing_instrument_count < MINIMUM_CONTRIBUTING_INSTRUMENTS
        or pooled_trade_plan_count < MINIMUM_POOLED_TRADE_PLANS
    ):
        return ActivityGateDecision.INSUFFICIENT_MULTI_MARKET_SAMPLE
    return ActivityGateDecision.SUFFICIENT_ACTIVITY_FOR_PERFORMANCE_PROTOCOL


def _report_record(
    summaries: tuple[InstrumentActivitySummary, ...],
    *,
    decision: ActivityGateDecision,
) -> dict[str, object]:
    return {
        "protocol_version": ACTIVITY_PROTOCOL_VERSION,
        "candidate_version": MULTI_MARKET_CANDIDATE_VERSION,
        "alpha_strategy_version": ALPHA_STRATEGY_VERSION,
        "detector_version": DETECTOR_VERSION_V2,
        "thresholds": {
            "minimum_accepted_instruments": MINIMUM_ACCEPTED_INSTRUMENTS,
            "minimum_contributing_instruments": MINIMUM_CONTRIBUTING_INSTRUMENTS,
            "minimum_pooled_trade_plans": MINIMUM_POOLED_TRADE_PLANS,
        },
        "accepted_instrument_count": len(summaries),
        "contributing_instrument_count": sum(
            summary.trade_plan_count > 0 for summary in summaries
        ),
        "pooled_detector_candidates": sum(
            summary.detector_candidates for summary in summaries
        ),
        "pooled_no_signal_count": sum(summary.no_signal_count for summary in summaries),
        "pooled_trade_plan_count": sum(summary.trade_plan_count for summary in summaries),
        "instruments": [
            {
                "instrument": summary.instrument,
                "dataset_version": summary.dataset_version,
                "detector_candidates": summary.detector_candidates,
                "no_signal_count": summary.no_signal_count,
                "trade_plan_count": summary.trade_plan_count,
                "reason_counts": dict(summary.reason_counts),
            }
            for summary in summaries
        ],
        "decision": decision.value,
        "backtest_executed": False,
        "pnl_outcome_access_authorized": False,
    }


def evaluate_multi_market_activity(
    summaries: tuple[InstrumentActivitySummary, ...],
) -> MultiMarketActivityGateResult:
    ordered = tuple(sorted(summaries, key=lambda item: item.instrument))
    if len({summary.instrument for summary in ordered}) != len(ordered):
        raise ValueError("activity summaries must contain unique instruments")

    accepted = len(ordered)
    contributing = sum(summary.trade_plan_count > 0 for summary in ordered)
    candidates = sum(summary.detector_candidates for summary in ordered)
    no_signals = sum(summary.no_signal_count for summary in ordered)
    trade_plans = sum(summary.trade_plan_count for summary in ordered)
    decision = _decision(
        accepted_instrument_count=accepted,
        contributing_instrument_count=contributing,
        pooled_trade_plan_count=trade_plans,
    )
    record = _report_record(ordered, decision=decision)
    encoded = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    report_sha = sha256(encoded).hexdigest()

    return MultiMarketActivityGateResult(
        protocol_version=ACTIVITY_PROTOCOL_VERSION,
        candidate_version=MULTI_MARKET_CANDIDATE_VERSION,
        alpha_strategy_version=ALPHA_STRATEGY_VERSION,
        detector_version=DETECTOR_VERSION_V2,
        accepted_instrument_count=accepted,
        contributing_instrument_count=contributing,
        pooled_detector_candidates=candidates,
        pooled_no_signal_count=no_signals,
        pooled_trade_plan_count=trade_plans,
        instruments=ordered,
        decision=decision,
        report_sha256=report_sha,
    )
