from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from hashlib import sha256
from typing import Final

from romeo_crt_engine.crt.v0_1 import (
    STRATEGY_VERSION,
    CandleWindow,
    ClosedCandle,
    DecisionState,
    Evaluation,
    ReasonCode,
    Timeframe,
    TradePlan,
    evaluate_bearish_c3,
)
from romeo_crt_engine.market_data.models import BarTimeframe
from romeo_crt_engine.market_data.price_data_v2 import (
    CanonicalPriceBarV2,
    PriceComponent,
    PriceDatasetIdentityV2,
    normalized_price_digest_v2,
)

MULTI_MARKET_CANDIDATE_VERSION: Final = "CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH"
ALPHA_STRATEGY_VERSION: Final = STRATEGY_VERSION
DETECTOR_VERSION_V2: Final = "CRT-DETECTOR-v0.2-MULTI-MARKET"
FROZEN_SIGNAL_PRICE_COMPONENT: Final = PriceComponent.MID


class DetectorRunStatusV2(StrEnum):
    COMPLETE = "COMPLETE"
    INSUFFICIENT_D1_HISTORY = "INSUFFICIENT_D1_HISTORY"


@dataclass(frozen=True, slots=True)
class DetectorDatasetV2:
    identity: PriceDatasetIdentityV2
    h1: tuple[CanonicalPriceBarV2, ...]
    d1: tuple[CanonicalPriceBarV2, ...]

    def __post_init__(self) -> None:
        if self.identity.price_component is not FROZEN_SIGNAL_PRICE_COMPONENT:
            raise ValueError("multi-market detector accepts frozen MID signal data only")
        if len(self.h1) != self.identity.h1_rows or len(self.d1) != self.identity.d1_rows:
            raise ValueError("canonical price row counts do not match trusted v2 identity")
        _validate_bar_identity(self.identity, self.h1, BarTimeframe.H1)
        _validate_bar_identity(self.identity, self.d1, BarTimeframe.D1)
        observed_digest = normalized_price_digest_v2(self.h1, self.d1)
        if observed_digest != self.identity.normalized_sha256:
            raise ValueError("canonical price H1/D1 content does not match trusted v2 digest")


@dataclass(frozen=True, slots=True)
class DetectorCandidateV2:
    candidate_id: str
    candidate_version: str
    alpha_strategy_version: str
    detector_version: str
    dataset_version: str
    dataset_identity_sha256: str
    provider: str
    venue: str
    instrument: str
    price_component: PriceComponent
    c1_open_time: datetime
    c2_open_time: datetime
    c3_open_time: datetime
    h1_observation_count: int
    state: DecisionState
    reason: ReasonCode
    rule_trace: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    causal_input_sha256: str
    trade_plan: TradePlan | None

    def __post_init__(self) -> None:
        if not self.candidate_id:
            raise ValueError("candidate_id must not be empty")
        if self.candidate_version != MULTI_MARKET_CANDIDATE_VERSION:
            raise ValueError("unexpected multi-market candidate version")
        if self.alpha_strategy_version != ALPHA_STRATEGY_VERSION:
            raise ValueError("multi-market detector must preserve the frozen v0.1 alpha version")
        if self.detector_version != DETECTOR_VERSION_V2:
            raise ValueError("unexpected multi-market detector version")
        for digest in (self.dataset_identity_sha256, self.causal_input_sha256):
            if len(digest) != 64:
                raise ValueError("candidate digests must be SHA-256 values")
        if self.state is DecisionState.TRADE_PLAN and self.trade_plan is None:
            raise ValueError("TRADE_PLAN candidate requires trade_plan")
        if self.state is DecisionState.NO_SIGNAL and self.trade_plan is not None:
            raise ValueError("NO_SIGNAL candidate cannot carry trade_plan")
        if self.trade_plan is not None and self.trade_plan.strategy_version != ALPHA_STRATEGY_VERSION:
            raise ValueError("trade plan must retain the frozen v0.1 alpha strategy version")


@dataclass(frozen=True, slots=True)
class DetectorRunV2:
    candidate_version: str
    alpha_strategy_version: str
    detector_version: str
    dataset: PriceDatasetIdentityV2
    dataset_identity_sha256: str
    status: DetectorRunStatusV2
    candidates: tuple[DetectorCandidateV2, ...]
    run_sha256: str

    @property
    def trade_plan_count(self) -> int:
        return sum(candidate.state is DecisionState.TRADE_PLAN for candidate in self.candidates)

    @property
    def no_signal_count(self) -> int:
        return sum(candidate.state is DecisionState.NO_SIGNAL for candidate in self.candidates)


def _dataset_identity_record(identity: PriceDatasetIdentityV2) -> dict[str, object]:
    return {
        "schema_version": identity.schema_version,
        "dataset_version": identity.dataset_version,
        "provider": identity.provider,
        "venue": identity.venue,
        "instrument": identity.instrument,
        "price_component": identity.price_component.value,
        "price_quantum": format(identity.price_quantum, "f"),
        "price_quantum_source": identity.price_quantum_source.value,
        "price_quantum_observed_at": identity.price_quantum_observed_at.isoformat(),
        "instrument_metadata_sha256": identity.instrument_metadata_sha256,
        "session_policy_version": identity.session_policy_version,
        "normalized_sha256": identity.normalized_sha256,
        "h1_rows": identity.h1_rows,
        "d1_rows": identity.d1_rows,
        "quality_status": identity.quality_status,
    }


def dataset_identity_sha256(identity: PriceDatasetIdentityV2) -> str:
    payload = json.dumps(
        _dataset_identity_record(identity), sort_keys=True, separators=(",", ":")
    ).encode()
    return sha256(payload).hexdigest()


def _validate_bar_identity(
    identity: PriceDatasetIdentityV2,
    bars: Sequence[CanonicalPriceBarV2],
    timeframe: BarTimeframe,
) -> None:
    previous_open: float | None = None
    for bar in bars:
        if bar.timeframe is not timeframe:
            raise ValueError(f"expected {timeframe.value} canonical price bars only")
        if (
            bar.provider,
            bar.venue,
            bar.instrument,
            bar.price_component,
            bar.session_policy_version,
        ) != (
            identity.provider,
            identity.venue,
            identity.instrument,
            identity.price_component,
            identity.session_policy_version,
        ):
            raise ValueError("canonical price bar identity does not match trusted v2 dataset")
        current_open = bar.open_time.timestamp()
        if previous_open is not None and current_open <= previous_open:
            raise ValueError("canonical price bars must be strictly ordered and unique")
        previous_open = current_open


def _closed_candle(bar: CanonicalPriceBarV2) -> ClosedCandle:
    timeframe = Timeframe.D1 if bar.timeframe is BarTimeframe.D1 else Timeframe.H1
    return ClosedCandle(
        timeframe=timeframe,
        open_time=bar.open_time,
        close_time=bar.close_time,
        open=float(bar.open),
        high=float(bar.high),
        low=float(bar.low),
        close=float(bar.close),
    )


def _c3_window(bar: CanonicalPriceBarV2) -> CandleWindow:
    if bar.timeframe is not BarTimeframe.D1:
        raise ValueError("C3 window requires a canonical D1 price bar")
    return CandleWindow(
        timeframe=Timeframe.D1,
        open_time=bar.open_time,
        close_time=bar.close_time,
        open_price=float(bar.open),
    )


def _h1_for_window(
    h1: Sequence[CanonicalPriceBarV2], c3: CanonicalPriceBarV2
) -> tuple[ClosedCandle, ...]:
    start = c3.open_time.timestamp()
    end = c3.close_time.timestamp()
    return tuple(
        _closed_candle(bar)
        for bar in h1
        if bar.open_time.timestamp() >= start and bar.close_time.timestamp() <= end
    )


def _candidate_id(
    dataset_version: str,
    c1: CanonicalPriceBarV2,
    c2: CanonicalPriceBarV2,
    c3: CanonicalPriceBarV2,
) -> str:
    payload = (
        f"{MULTI_MARKET_CANDIDATE_VERSION}|{ALPHA_STRATEGY_VERSION}|{dataset_version}|"
        f"{c1.open_time.isoformat()}|{c2.open_time.isoformat()}|{c3.open_time.isoformat()}"
    )
    return sha256(payload.encode()).hexdigest()[:24]


def _causal_input_digest(
    c1: CanonicalPriceBarV2,
    c2: CanonicalPriceBarV2,
    c3: CanonicalPriceBarV2,
    h1: Sequence[ClosedCandle],
) -> str:
    payload = {
        "c1": {
            "open_time": c1.open_time.isoformat(),
            "close_time": c1.close_time.isoformat(),
            "open": str(c1.open),
            "high": str(c1.high),
            "low": str(c1.low),
            "close": str(c1.close),
            "source_digest": c1.source_digest,
        },
        "c2": {
            "open_time": c2.open_time.isoformat(),
            "close_time": c2.close_time.isoformat(),
            "open": str(c2.open),
            "high": str(c2.high),
            "low": str(c2.low),
            "close": str(c2.close),
            "source_digest": c2.source_digest,
        },
        "c3_gate": {
            "open_time": c3.open_time.isoformat(),
            "close_time": c3.close_time.isoformat(),
            "open_price": str(c3.open),
        },
        "h1": [
            {
                "open_time": candle.open_time.isoformat(),
                "close_time": candle.close_time.isoformat(),
                "open": candle.open,
                "high": candle.high,
                "low": candle.low,
                "close": candle.close,
            }
            for candle in h1
        ],
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return sha256(encoded).hexdigest()


def _rule_trace(evaluation: Evaluation) -> tuple[str, ...]:
    reason = evaluation.reason
    if reason in {ReasonCode.INVALID_CALENDAR, ReasonCode.NON_CONSECUTIVE_PARENT}:
        return ("CRT-V01-002-ROLLING-PARENT-ENUMERATION", "CRT-V01-012-FAIL-CLOSED")
    if reason is ReasonCode.NO_BEARISH_PARENT_SWEEP:
        return ("CRT-V01-003-BEARISH-C2-SWEEP",)
    if reason is ReasonCode.DOUBLE_OR_OPPOSITE_SWEEP:
        return ("CRT-V01-003-BEARISH-C2-SWEEP", "CRT-V01-012-FAIL-CLOSED")
    if reason is ReasonCode.PARENT_CLOSE_NOT_RECLAIMED:
        return ("CRT-V01-004-C2-CLOSE-RECLAIM",)
    if reason is ReasonCode.TARGET1_CONSUMED_IN_C2:
        return ("CRT-V01-005-T1-PENDING",)
    if reason is ReasonCode.EXECUTION_DATA_OUTSIDE_C3:
        return ("CRT-V01-006-C3-GATE", "CRT-V01-012-FAIL-CLOSED")
    if reason is ReasonCode.TARGET1_CONSUMED_PRE_ENTRY:
        return ("CRT-V01-006-C3-GATE", "SPEC-SECTION-11-TARGET-CONSUMPTION-GUARD")
    if reason is ReasonCode.NO_MODEL1_CONFIRMATION:
        return (
            "CRT-V01-007-MODEL1-CORE",
            "CRT-V01-008-MODEL1-CONFIRMATION",
            "CRT-V01-011-C3-EXPIRY",
        )
    if reason is ReasonCode.INVALID_TRADE_GEOMETRY:
        return (
            "CRT-V01-008-MODEL1-CONFIRMATION",
            "CRT-V01-009-STRUCTURAL-STOP",
            "CRT-V01-010-PRIMARY-TARGET",
            "CRT-V01-012-FAIL-CLOSED",
        )
    return (
        "CRT-V01-002-ROLLING-PARENT-ENUMERATION",
        "CRT-V01-003-BEARISH-C2-SWEEP",
        "CRT-V01-004-C2-CLOSE-RECLAIM",
        "CRT-V01-005-T1-PENDING",
        "CRT-V01-006-C3-GATE",
        "CRT-V01-007-MODEL1-CORE",
        "CRT-V01-008-MODEL1-CONFIRMATION",
        "CRT-V01-009-STRUCTURAL-STOP",
        "CRT-V01-010-PRIMARY-TARGET",
    )


def _evidence_ids(evaluation: Evaluation) -> tuple[str, ...]:
    if evaluation.trade_plan is not None:
        return evaluation.trade_plan.evidence_ids
    return (
        "ROMEO-2024-CRT",
        "ROMEO-2024-TS",
        "ROMEO-2025-S1",
        "ROMEO-2025-S7",
        "P0-FIX-002",
    )


def detect_dataset_v2(dataset: DetectorDatasetV2) -> DetectorRunV2:
    identity_sha = dataset_identity_sha256(dataset.identity)
    if len(dataset.d1) < 3:
        seed = (
            f"{DETECTOR_VERSION_V2}|{MULTI_MARKET_CANDIDATE_VERSION}|"
            f"{ALPHA_STRATEGY_VERSION}|{identity_sha}|EMPTY"
        )
        return DetectorRunV2(
            candidate_version=MULTI_MARKET_CANDIDATE_VERSION,
            alpha_strategy_version=ALPHA_STRATEGY_VERSION,
            detector_version=DETECTOR_VERSION_V2,
            dataset=dataset.identity,
            dataset_identity_sha256=identity_sha,
            status=DetectorRunStatusV2.INSUFFICIENT_D1_HISTORY,
            candidates=(),
            run_sha256=sha256(seed.encode()).hexdigest(),
        )

    candidates: list[DetectorCandidateV2] = []
    price_quantum = float(dataset.identity.price_quantum)
    for index in range(len(dataset.d1) - 2):
        c1 = dataset.d1[index]
        c2 = dataset.d1[index + 1]
        c3 = dataset.d1[index + 2]
        h1 = _h1_for_window(dataset.h1, c3)
        evaluation = evaluate_bearish_c3(
            _closed_candle(c1),
            _closed_candle(c2),
            _c3_window(c3),
            h1,
            tick_size=price_quantum,
        )
        candidates.append(
            DetectorCandidateV2(
                candidate_id=_candidate_id(dataset.identity.dataset_version, c1, c2, c3),
                candidate_version=MULTI_MARKET_CANDIDATE_VERSION,
                alpha_strategy_version=ALPHA_STRATEGY_VERSION,
                detector_version=DETECTOR_VERSION_V2,
                dataset_version=dataset.identity.dataset_version,
                dataset_identity_sha256=identity_sha,
                provider=dataset.identity.provider,
                venue=dataset.identity.venue,
                instrument=dataset.identity.instrument,
                price_component=dataset.identity.price_component,
                c1_open_time=c1.open_time,
                c2_open_time=c2.open_time,
                c3_open_time=c3.open_time,
                h1_observation_count=len(h1),
                state=evaluation.state,
                reason=evaluation.reason,
                rule_trace=_rule_trace(evaluation),
                evidence_ids=_evidence_ids(evaluation),
                causal_input_sha256=_causal_input_digest(c1, c2, c3, h1),
                trade_plan=evaluation.trade_plan,
            )
        )

    run_seed = {
        "candidate_version": MULTI_MARKET_CANDIDATE_VERSION,
        "alpha_strategy_version": ALPHA_STRATEGY_VERSION,
        "detector_version": DETECTOR_VERSION_V2,
        "dataset_version": dataset.identity.dataset_version,
        "dataset_identity_sha256": identity_sha,
        "candidate_ids": [candidate.candidate_id for candidate in candidates],
        "candidate_inputs": [candidate.causal_input_sha256 for candidate in candidates],
        "states": [candidate.state.value for candidate in candidates],
        "reasons": [candidate.reason.value for candidate in candidates],
    }
    run_sha = sha256(
        json.dumps(run_seed, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return DetectorRunV2(
        candidate_version=MULTI_MARKET_CANDIDATE_VERSION,
        alpha_strategy_version=ALPHA_STRATEGY_VERSION,
        detector_version=DETECTOR_VERSION_V2,
        dataset=dataset.identity,
        dataset_identity_sha256=identity_sha,
        status=DetectorRunStatusV2.COMPLETE,
        candidates=tuple(candidates),
        run_sha256=run_sha,
    )
