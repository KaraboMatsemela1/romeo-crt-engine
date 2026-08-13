from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from hashlib import sha256
from pathlib import Path
from typing import Any, Final, cast

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
from romeo_crt_engine.market_data.dataset import normalized_digest
from romeo_crt_engine.market_data.models import BarTimeframe, CanonicalBar

DETECTOR_VERSION: Final = "CRT-DETECTOR-v0.1"
TRUSTED_QUALITY_STATUS: Final = "TRUSTED"
PHASE3_MANIFEST_SCHEMA: Final = "PHASE3_DATASET_MANIFEST_V1"


class DetectorRunStatus(StrEnum):
    COMPLETE = "COMPLETE"
    INSUFFICIENT_D1_HISTORY = "INSUFFICIENT_D1_HISTORY"


@dataclass(frozen=True, slots=True)
class DetectorDatasetIdentity:
    dataset_version: str
    manifest_sha256: str
    normalized_sha256: str
    provider: str
    venue: str
    symbol: str
    tick_size: Decimal
    h1_rows: int
    d1_rows: int
    quality_status: str
    schema_version: str

    def __post_init__(self) -> None:
        if not self.dataset_version or not self.provider or not self.venue or not self.symbol:
            raise ValueError("dataset identity fields must not be empty")
        for field_name, digest in (
            ("manifest_sha256", self.manifest_sha256),
            ("normalized_sha256", self.normalized_sha256),
        ):
            if len(digest) != 64:
                raise ValueError(f"{field_name} must be a SHA-256 digest")
            try:
                int(digest, 16)
            except ValueError as error:
                raise ValueError(f"{field_name} must be hexadecimal") from error
        if not self.tick_size.is_finite() or self.tick_size <= 0:
            raise ValueError("tick_size must be positive and finite")
        if self.h1_rows < 0 or self.d1_rows < 0:
            raise ValueError("dataset row counts must be non-negative")
        if self.quality_status != TRUSTED_QUALITY_STATUS:
            raise ValueError("CRT detector accepts TRUSTED datasets only")
        if self.schema_version != PHASE3_MANIFEST_SCHEMA:
            raise ValueError("unsupported trusted dataset manifest schema")


@dataclass(frozen=True, slots=True)
class DetectorCandidate:
    candidate_id: str
    strategy_version: str
    detector_version: str
    dataset_version: str
    manifest_sha256: str
    provider: str
    venue: str
    symbol: str
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
        if len(self.causal_input_sha256) != 64:
            raise ValueError("causal_input_sha256 must be a SHA-256 digest")
        if self.state is DecisionState.TRADE_PLAN and self.trade_plan is None:
            raise ValueError("TRADE_PLAN candidate requires trade_plan")
        if self.state is DecisionState.NO_SIGNAL and self.trade_plan is not None:
            raise ValueError("NO_SIGNAL candidate cannot carry trade_plan")


@dataclass(frozen=True, slots=True)
class DetectorRun:
    strategy_version: str
    detector_version: str
    dataset: DetectorDatasetIdentity
    status: DetectorRunStatus
    candidates: tuple[DetectorCandidate, ...]
    run_sha256: str

    @property
    def trade_plan_count(self) -> int:
        return sum(candidate.state is DecisionState.TRADE_PLAN for candidate in self.candidates)

    @property
    def no_signal_count(self) -> int:
        return sum(candidate.state is DecisionState.NO_SIGNAL for candidate in self.candidates)


@dataclass(frozen=True, slots=True)
class DetectorDataset:
    identity: DetectorDatasetIdentity
    h1: tuple[CanonicalBar, ...]
    d1: tuple[CanonicalBar, ...]

    def __post_init__(self) -> None:
        if len(self.h1) != self.identity.h1_rows or len(self.d1) != self.identity.d1_rows:
            raise ValueError("canonical row counts do not match trusted manifest")
        _validate_bar_identity(self.identity, self.h1, BarTimeframe.H1)
        _validate_bar_identity(self.identity, self.d1, BarTimeframe.D1)
        observed_digest = normalized_digest(self.h1, self.d1)
        if observed_digest != self.identity.normalized_sha256:
            raise ValueError("canonical H1/D1 content does not match trusted manifest digest")


def _required_text(document: Mapping[str, Any], key: str) -> str:
    value = document.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"manifest field {key} must be a non-empty string")
    return value


def _required_int(document: Mapping[str, Any], key: str) -> int:
    value = document.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"manifest field {key} must be an integer")
    return value


def identity_from_manifest_bytes(payload: bytes) -> DetectorDatasetIdentity:
    document_raw = json.loads(payload)
    if not isinstance(document_raw, dict):
        raise TypeError("trusted dataset manifest must be a JSON object")
    document = cast(dict[str, Any], document_raw)
    return DetectorDatasetIdentity(
        dataset_version=_required_text(document, "dataset_version"),
        manifest_sha256=sha256(payload).hexdigest(),
        normalized_sha256=_required_text(document, "normalized_sha256"),
        provider=_required_text(document, "provider"),
        venue=_required_text(document, "venue"),
        symbol=_required_text(document, "symbol"),
        tick_size=Decimal(_required_text(document, "price_tick_size")),
        h1_rows=_required_int(document, "h1_rows"),
        d1_rows=_required_int(document, "d1_rows"),
        quality_status=_required_text(document, "quality_status"),
        schema_version=_required_text(document, "schema_version"),
    )


def _canonical_bar_from_record(record: Mapping[str, Any]) -> CanonicalBar:
    return CanonicalBar(
        provider=str(record["provider"]),
        venue=str(record["venue"]),
        symbol=str(record["symbol"]),
        timeframe=BarTimeframe(str(record["timeframe"])),
        open_time=datetime.fromisoformat(str(record["open_time_utc"])),
        close_time=datetime.fromisoformat(str(record["close_time_utc"])),
        open=Decimal(str(record["open"])),
        high=Decimal(str(record["high"])),
        low=Decimal(str(record["low"])),
        close=Decimal(str(record["close"])),
        volume=Decimal(str(record["volume"])),
        quote_volume=Decimal(str(record["quote_volume"])),
        trade_count=int(record["trade_count"]),
        source_count=int(record["source_count"]),
        source_digest=str(record["source_digest"]),
    )


def load_canonical_jsonl(path: Path) -> tuple[CanonicalBar, ...]:
    bars: list[CanonicalBar] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        raw = json.loads(line)
        if not isinstance(raw, dict):
            raise TypeError(f"{path} line {line_number} must be a JSON object")
        bars.append(_canonical_bar_from_record(cast(dict[str, Any], raw)))
    return tuple(bars)


def load_detector_dataset(dataset_dir: Path) -> DetectorDataset:
    manifest_bytes = (dataset_dir / "manifest.json").read_bytes()
    identity = identity_from_manifest_bytes(manifest_bytes)
    h1 = load_canonical_jsonl(dataset_dir / "H1.jsonl")
    d1 = load_canonical_jsonl(dataset_dir / "D1.jsonl")
    return DetectorDataset(identity=identity, h1=h1, d1=d1)


def _validate_bar_identity(
    identity: DetectorDatasetIdentity,
    bars: Sequence[CanonicalBar],
    timeframe: BarTimeframe,
) -> None:
    previous_open: float | None = None
    for bar in bars:
        if bar.timeframe is not timeframe:
            raise ValueError(f"expected {timeframe.value} canonical bars only")
        if (bar.provider, bar.venue, bar.symbol) != (
            identity.provider,
            identity.venue,
            identity.symbol,
        ):
            raise ValueError("canonical bar identity does not match trusted manifest")
        current_open = bar.open_time.timestamp()
        if previous_open is not None and current_open <= previous_open:
            raise ValueError("canonical bars must be strictly ordered and unique")
        previous_open = current_open


def _closed_candle(bar: CanonicalBar) -> ClosedCandle:
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


def _c3_window(bar: CanonicalBar) -> CandleWindow:
    if bar.timeframe is not BarTimeframe.D1:
        raise ValueError("C3 window requires a canonical D1 bar")
    return CandleWindow(
        timeframe=Timeframe.D1,
        open_time=bar.open_time,
        close_time=bar.close_time,
        open_price=float(bar.open),
    )


def _h1_for_window(h1: Sequence[CanonicalBar], c3: CanonicalBar) -> tuple[ClosedCandle, ...]:
    start = c3.open_time.timestamp()
    end = c3.close_time.timestamp()
    return tuple(
        _closed_candle(bar)
        for bar in h1
        if bar.open_time.timestamp() >= start and bar.close_time.timestamp() <= end
    )


def _candidate_id(dataset_version: str, c1: CanonicalBar, c2: CanonicalBar, c3: CanonicalBar) -> str:
    payload = (
        f"{STRATEGY_VERSION}|{dataset_version}|{c1.open_time.isoformat()}|"
        f"{c2.open_time.isoformat()}|{c3.open_time.isoformat()}"
    )
    return sha256(payload.encode("utf-8")).hexdigest()[:24]


def _causal_input_digest(
    c1: CanonicalBar,
    c2: CanonicalBar,
    c3: CanonicalBar,
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
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(encoded).hexdigest()


def _rule_trace(evaluation: Evaluation) -> tuple[str, ...]:
    reason = evaluation.reason
    if reason is ReasonCode.INVALID_CALENDAR:
        return ("CRT-V01-002-ROLLING-PARENT-ENUMERATION", "CRT-V01-012-FAIL-CLOSED")
    if reason is ReasonCode.NON_CONSECUTIVE_PARENT:
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


def detect_dataset(dataset: DetectorDataset) -> DetectorRun:
    if len(dataset.d1) < 3:
        seed = f"{DETECTOR_VERSION}|{STRATEGY_VERSION}|{dataset.identity.manifest_sha256}|EMPTY"
        return DetectorRun(
            strategy_version=STRATEGY_VERSION,
            detector_version=DETECTOR_VERSION,
            dataset=dataset.identity,
            status=DetectorRunStatus.INSUFFICIENT_D1_HISTORY,
            candidates=(),
            run_sha256=sha256(seed.encode("utf-8")).hexdigest(),
        )

    candidates: list[DetectorCandidate] = []
    tick_size = float(dataset.identity.tick_size)
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
            tick_size=tick_size,
        )
        candidates.append(
            DetectorCandidate(
                candidate_id=_candidate_id(dataset.identity.dataset_version, c1, c2, c3),
                strategy_version=STRATEGY_VERSION,
                detector_version=DETECTOR_VERSION,
                dataset_version=dataset.identity.dataset_version,
                manifest_sha256=dataset.identity.manifest_sha256,
                provider=dataset.identity.provider,
                venue=dataset.identity.venue,
                symbol=dataset.identity.symbol,
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
        "strategy_version": STRATEGY_VERSION,
        "detector_version": DETECTOR_VERSION,
        "dataset_version": dataset.identity.dataset_version,
        "manifest_sha256": dataset.identity.manifest_sha256,
        "candidate_ids": [candidate.candidate_id for candidate in candidates],
        "candidate_inputs": [candidate.causal_input_sha256 for candidate in candidates],
        "states": [candidate.state.value for candidate in candidates],
        "reasons": [candidate.reason.value for candidate in candidates],
    }
    run_sha = sha256(
        json.dumps(run_seed, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return DetectorRun(
        strategy_version=STRATEGY_VERSION,
        detector_version=DETECTOR_VERSION,
        dataset=dataset.identity,
        status=DetectorRunStatus.COMPLETE,
        candidates=tuple(candidates),
        run_sha256=run_sha,
    )
