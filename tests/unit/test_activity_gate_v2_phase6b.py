from __future__ import annotations

import pytest

from romeo_crt_engine.validation.activity_gate_v2 import (
    ActivityGateDecision,
    InstrumentActivitySummary,
    evaluate_multi_market_activity,
)


def _summary(
    instrument: str,
    *,
    candidates: int,
    trade_plans: int,
) -> InstrumentActivitySummary:
    no_signals = candidates - trade_plans
    reason_counts: list[tuple[str, int]] = []
    if no_signals:
        reason_counts.append(("NO_MODEL1_CONFIRMATION", no_signals))
    if trade_plans:
        reason_counts.append(("VALID_TRADE_PLAN", trade_plans))
    return InstrumentActivitySummary(
        instrument=instrument,
        dataset_version=f"dataset-{instrument.lower()}",
        detector_candidates=candidates,
        no_signal_count=no_signals,
        trade_plan_count=trade_plans,
        reason_counts=tuple(sorted(reason_counts)),
    )


def test_activity_gate_rejects_single_instrument_as_multi_market_universe() -> None:
    result = evaluate_multi_market_activity(
        (_summary("EUR_USD", candidates=100, trade_plans=40),)
    )

    assert result.decision is ActivityGateDecision.INSUFFICIENT_ELIGIBLE_UNIVERSE
    assert result.accepted_instrument_count == 1
    assert result.pooled_trade_plan_count == 40
    assert result.backtest_executed is False
    assert result.pnl_outcome_access_authorized is False


def test_activity_gate_requires_two_contributing_instruments() -> None:
    result = evaluate_multi_market_activity(
        (
            _summary("EUR_USD", candidates=100, trade_plans=30),
            _summary("XAU_USD", candidates=100, trade_plans=0),
        )
    )

    assert result.decision is ActivityGateDecision.INSUFFICIENT_MULTI_MARKET_SAMPLE
    assert result.accepted_instrument_count == 2
    assert result.contributing_instrument_count == 1
    assert result.pooled_trade_plan_count == 30


def test_activity_gate_retains_original_minimum_30_trade_plan_threshold() -> None:
    insufficient = evaluate_multi_market_activity(
        (
            _summary("EUR_USD", candidates=100, trade_plans=15),
            _summary("XAU_USD", candidates=100, trade_plans=14),
        )
    )
    sufficient = evaluate_multi_market_activity(
        (
            _summary("EUR_USD", candidates=100, trade_plans=15),
            _summary("XAU_USD", candidates=100, trade_plans=15),
        )
    )

    assert insufficient.pooled_trade_plan_count == 29
    assert insufficient.decision is ActivityGateDecision.INSUFFICIENT_MULTI_MARKET_SAMPLE
    assert sufficient.pooled_trade_plan_count == 30
    assert sufficient.decision is ActivityGateDecision.SUFFICIENT_ACTIVITY_FOR_PERFORMANCE_PROTOCOL


def test_activity_report_is_deterministic_regardless_of_input_order() -> None:
    eur = _summary("EUR_USD", candidates=50, trade_plans=16)
    gold = _summary("XAU_USD", candidates=50, trade_plans=14)

    first = evaluate_multi_market_activity((eur, gold))
    second = evaluate_multi_market_activity((gold, eur))

    assert first.instruments == second.instruments
    assert first.report_sha256 == second.report_sha256
    assert first.decision is second.decision


def test_activity_summary_rejects_inconsistent_candidate_counts() -> None:
    with pytest.raises(ValueError, match="must equal detector candidate count"):
        InstrumentActivitySummary(
            instrument="EUR_USD",
            dataset_version="dataset-eur",
            detector_candidates=10,
            no_signal_count=8,
            trade_plan_count=1,
            reason_counts=(("NO_MODEL1_CONFIRMATION", 10),),
        )


def test_activity_gate_rejects_duplicate_instruments() -> None:
    summary = _summary("EUR_USD", candidates=10, trade_plans=2)
    with pytest.raises(ValueError, match="unique instruments"):
        evaluate_multi_market_activity((summary, summary))
