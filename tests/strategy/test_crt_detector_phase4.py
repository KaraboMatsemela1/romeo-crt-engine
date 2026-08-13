from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from hashlib import sha256
from pathlib import Path
from typing import Any, cast

import pytest

from romeo_crt_engine.crt.detector import (
    DETECTOR_VERSION,
    DetectorDataset,
    DetectorDatasetIdentity,
    DetectorRunStatus,
    detect_dataset,
    identity_from_manifest_bytes,
)
from romeo_crt_engine.crt.v0_1 import STRATEGY_VERSION, DecisionState, ReasonCode
from romeo_crt_engine.market_data.dataset import normalized_digest
from romeo_crt_engine.market_data.models import BarTimeframe, CanonicalBar

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "crt_v0_1_cases.json"
FROZEN_MANIFEST_PATH = (
    Path(__file__).parents[2]
    / "data"
    / "manifests"
    / "PHASE3_BTCUSDT_EE1300F0DA50E4DEBCBBC3B7.json"
)
PROVIDER = "TEST_PROVIDER"
VENUE = "TEST_VENUE"
SYMBOL = "TESTUSD"


def _utc(value: object) -> datetime:
    return datetime.fromisoformat(str(value)).astimezone(UTC)


def _digest(label: str) -> str:
    return sha256(label.encode("utf-8")).hexdigest()


def _bar_from_fixture(
    payload: dict[str, object],
    *,
    timeframe: BarTimeframe,
    label: str,
) -> CanonicalBar:
    return CanonicalBar(
        provider=PROVIDER,
        venue=VENUE,
        symbol=SYMBOL,
        timeframe=timeframe,
        open_time=_utc(payload["open_time"]),
        close_time=_utc(payload["close_time"]),
        open=Decimal(str(payload["open"])),
        high=Decimal(str(payload["high"])),
        low=Decimal(str(payload["low"])),
        close=Decimal(str(payload["close"])),
        volume=Decimal(0),
        quote_volume=Decimal(0),
        trade_count=0,
        source_count=24 if timeframe is BarTimeframe.D1 else 60,
        source_digest=_digest(label),
    )


def _c3_bar(case: dict[str, Any]) -> CanonicalBar:
    payload = cast(dict[str, object], case["c3"])
    h1 = cast(list[dict[str, object]], case["h1"])
    open_price = Decimal(str(payload["open_price"]))
    if h1:
        high = max([open_price, *(Decimal(str(item["high"])) for item in h1)])
        low = min([open_price, *(Decimal(str(item["low"])) for item in h1)])
        close = Decimal(str(h1[-1]["close"]))
    else:
        high = open_price
        low = open_price
        close = open_price
    return CanonicalBar(
        provider=PROVIDER,
        venue=VENUE,
        symbol=SYMBOL,
        timeframe=BarTimeframe.D1,
        open_time=_utc(payload["open_time"]),
        close_time=_utc(payload["close_time"]),
        open=open_price,
        high=high,
        low=low,
        close=close,
        volume=Decimal(0),
        quote_volume=Decimal(0),
        trade_count=0,
        source_count=24,
        source_digest=_digest(f"{case['id']}:c3"),
    )


def _dataset_for_case(case: dict[str, Any]) -> DetectorDataset:
    c1 = _bar_from_fixture(
        cast(dict[str, object], case["c1"]),
        timeframe=BarTimeframe.D1,
        label=f"{case['id']}:c1",
    )
    c2 = _bar_from_fixture(
        cast(dict[str, object], case["c2"]),
        timeframe=BarTimeframe.D1,
        label=f"{case['id']}:c2",
    )
    c3 = _c3_bar(case)
    h1 = tuple(
        _bar_from_fixture(
            item,
            timeframe=BarTimeframe.H1,
            label=f"{case['id']}:h1:{index}",
        )
        for index, item in enumerate(cast(list[dict[str, object]], case["h1"]))
    )
    d1 = (c1, c2, c3)
    normalized_sha = normalized_digest(h1, d1)
    manifest_sha = _digest(f"{case['id']}:manifest")
    identity = DetectorDatasetIdentity(
        dataset_version=f"fixture-{str(case['id']).lower()}",
        manifest_sha256=manifest_sha,
        normalized_sha256=normalized_sha,
        provider=PROVIDER,
        venue=VENUE,
        symbol=SYMBOL,
        tick_size=Decimal(str(case["tick_size"])),
        h1_rows=len(h1),
        d1_rows=len(d1),
        quality_status="TRUSTED",
        schema_version="PHASE3_DATASET_MANIFEST_V1",
    )
    return DetectorDataset(identity=identity, h1=h1, d1=d1)


def _cases() -> list[dict[str, Any]]:
    raw = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(raw, list)
    return cast(list[dict[str, Any]], raw)


def test_detector_reproduces_all_frozen_phase2_fixtures() -> None:
    for case in _cases():
        run = detect_dataset(_dataset_for_case(case))
        assert run.status is DetectorRunStatus.COMPLETE, case["id"]
        assert run.strategy_version == STRATEGY_VERSION, case["id"]
        assert run.detector_version == DETECTOR_VERSION, case["id"]
        assert len(run.candidates) == 1, case["id"]
        candidate = run.candidates[0]
        assert candidate.state is DecisionState(case["expected_state"]), case["id"]
        assert candidate.reason is ReasonCode(case["expected_reason"]), case["id"]
        assert candidate.rule_trace, case["id"]
        assert candidate.evidence_ids, case["id"]
        assert len(candidate.causal_input_sha256) == 64, case["id"]

        if candidate.state is DecisionState.TRADE_PLAN:
            assert candidate.trade_plan is not None, case["id"]
            assert candidate.trade_plan.entry_price == 106.0, case["id"]
            assert candidate.trade_plan.stop_price == 113.25, case["id"]
            assert candidate.trade_plan.target_price == 100.0, case["id"]


def test_detector_ignores_future_c3_daily_ohlc_in_strategy_decision() -> None:
    case = _cases()[0]
    first_dataset = _dataset_for_case(case)
    original_c3 = first_dataset.d1[2]
    mutated_c3 = CanonicalBar(
        provider=original_c3.provider,
        venue=original_c3.venue,
        symbol=original_c3.symbol,
        timeframe=original_c3.timeframe,
        open_time=original_c3.open_time,
        close_time=original_c3.close_time,
        open=original_c3.open,
        high=Decimal(999999),
        low=Decimal(1),
        close=Decimal(500000),
        volume=original_c3.volume,
        quote_volume=original_c3.quote_volume,
        trade_count=original_c3.trade_count,
        source_count=original_c3.source_count,
        source_digest=_digest("mutated-future-c3"),
    )
    second_d1 = (first_dataset.d1[0], first_dataset.d1[1], mutated_c3)
    second_identity = DetectorDatasetIdentity(
        dataset_version="future-c3-mutation",
        manifest_sha256=_digest("future-c3-mutated-manifest"),
        normalized_sha256=normalized_digest(first_dataset.h1, second_d1),
        provider=PROVIDER,
        venue=VENUE,
        symbol=SYMBOL,
        tick_size=first_dataset.identity.tick_size,
        h1_rows=len(first_dataset.h1),
        d1_rows=3,
        quality_status="TRUSTED",
        schema_version="PHASE3_DATASET_MANIFEST_V1",
    )
    second_dataset = DetectorDataset(
        identity=second_identity,
        h1=first_dataset.h1,
        d1=second_d1,
    )

    first = detect_dataset(first_dataset).candidates[0]
    second = detect_dataset(second_dataset).candidates[0]
    assert first.state is second.state
    assert first.reason is second.reason
    assert first.trade_plan is not None
    assert second.trade_plan is not None
    assert first.trade_plan.entry_time == second.trade_plan.entry_time
    assert first.trade_plan.entry_price == second.trade_plan.entry_price
    assert first.trade_plan.stop_price == second.trade_plan.stop_price
    assert first.trade_plan.target_price == second.trade_plan.target_price
    assert first.causal_input_sha256 == second.causal_input_sha256


def test_detector_rejects_canonical_content_that_does_not_match_manifest_digest() -> None:
    dataset = _dataset_for_case(_cases()[0])
    bad_identity = DetectorDatasetIdentity(
        dataset_version=dataset.identity.dataset_version,
        manifest_sha256=dataset.identity.manifest_sha256,
        normalized_sha256="0" * 64,
        provider=dataset.identity.provider,
        venue=dataset.identity.venue,
        symbol=dataset.identity.symbol,
        tick_size=dataset.identity.tick_size,
        h1_rows=dataset.identity.h1_rows,
        d1_rows=dataset.identity.d1_rows,
        quality_status="TRUSTED",
        schema_version="PHASE3_DATASET_MANIFEST_V1",
    )
    with pytest.raises(ValueError, match="trusted manifest digest"):
        DetectorDataset(identity=bad_identity, h1=dataset.h1, d1=dataset.d1)


def test_detector_requires_three_daily_bars_before_any_candidate_exists() -> None:
    dataset = _dataset_for_case(_cases()[0])
    d1 = dataset.d1[:1]
    identity = DetectorDatasetIdentity(
        dataset_version="one-d1-only",
        manifest_sha256=_digest("one-d1-manifest"),
        normalized_sha256=normalized_digest((), d1),
        provider=PROVIDER,
        venue=VENUE,
        symbol=SYMBOL,
        tick_size=dataset.identity.tick_size,
        h1_rows=0,
        d1_rows=1,
        quality_status="TRUSTED",
        schema_version="PHASE3_DATASET_MANIFEST_V1",
    )
    run = detect_dataset(DetectorDataset(identity=identity, h1=(), d1=d1))
    assert run.status is DetectorRunStatus.INSUFFICIENT_D1_HISTORY
    assert run.candidates == ()
    assert run.trade_plan_count == 0
    assert run.no_signal_count == 0


def test_frozen_phase3_manifest_identity_is_exactly_consumable() -> None:
    payload = FROZEN_MANIFEST_PATH.read_bytes()
    identity = identity_from_manifest_bytes(payload)

    assert identity.dataset_version == "ee1300f0da50e4debcbbc3b7"
    assert identity.manifest_sha256 == (
        "eaf828ee3acc8adf9e3b931cc6a55d385b0be61b58ae72f01205b3f6034a2141"
    )
    assert identity.normalized_sha256 == (
        "86f6f69176e68655032f3d12910572214de2fa04266c5615146ae03e9f414fc2"
    )
    assert identity.provider == "BINANCE_PUBLIC_DATA"
    assert identity.venue == "BINANCE_SPOT"
    assert identity.symbol == "BTCUSDT"
    assert identity.tick_size == Decimal("0.01000000")
    assert identity.h1_rows == 48
    assert identity.d1_rows == 1
    assert identity.quality_status == "TRUSTED"
