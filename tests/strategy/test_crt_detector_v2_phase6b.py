from __future__ import annotations

import json
from datetime import UTC, datetime
from decimal import Decimal
from hashlib import sha256
from pathlib import Path
from typing import Any, cast

import pytest

from romeo_crt_engine.crt.detector import (
    DetectorDataset,
    DetectorDatasetIdentity,
    detect_dataset,
)
from romeo_crt_engine.crt.detector_v2 import (
    ALPHA_STRATEGY_VERSION,
    DETECTOR_VERSION_V2,
    MULTI_MARKET_CANDIDATE_VERSION,
    DetectorDatasetV2,
    DetectorRunStatusV2,
    detect_dataset_v2,
)
from romeo_crt_engine.crt.v0_1 import DecisionState
from romeo_crt_engine.market_data.dataset import normalized_digest
from romeo_crt_engine.market_data.models import BarTimeframe, CanonicalBar
from romeo_crt_engine.market_data.price_data_v2 import (
    CanonicalPriceBarV2,
    PriceComponent,
    PriceDatasetIdentityV2,
    PriceQuantumSource,
    normalized_price_digest_v2,
)

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "crt_v0_1_cases.json"
PROVIDER = "TEST_PROVIDER"
VENUE = "TEST_VENUE"
INSTRUMENT = "TESTUSD"
SESSION_POLICY = "P6B_TEST_SESSION_POLICY_V1"
METADATA_SHA = "9" * 64


def _utc(value: object) -> datetime:
    return datetime.fromisoformat(str(value)).astimezone(UTC)


def _digest(label: str) -> str:
    return sha256(label.encode()).hexdigest()


def _cases() -> list[dict[str, Any]]:
    raw = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    assert isinstance(raw, list)
    return cast(list[dict[str, Any]], raw)


def _legacy_bar(
    payload: dict[str, object],
    *,
    timeframe: BarTimeframe,
    label: str,
) -> CanonicalBar:
    return CanonicalBar(
        provider=PROVIDER,
        venue=VENUE,
        symbol=INSTRUMENT,
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


def _v2_bar(
    payload: dict[str, object],
    *,
    timeframe: BarTimeframe,
    label: str,
) -> CanonicalPriceBarV2:
    return CanonicalPriceBarV2(
        provider=PROVIDER,
        venue=VENUE,
        instrument=INSTRUMENT,
        price_component=PriceComponent.MID,
        timeframe=timeframe,
        open_time=_utc(payload["open_time"]),
        close_time=_utc(payload["close_time"]),
        open=Decimal(str(payload["open"])),
        high=Decimal(str(payload["high"])),
        low=Decimal(str(payload["low"])),
        close=Decimal(str(payload["close"])),
        source_count=24 if timeframe is BarTimeframe.D1 else 60,
        source_digest=_digest(label),
        session_policy_version=SESSION_POLICY,
    )


def _c3_payload(case: dict[str, Any]) -> dict[str, object]:
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
    return {
        "open_time": payload["open_time"],
        "close_time": payload["close_time"],
        "open": str(open_price),
        "high": str(high),
        "low": str(low),
        "close": str(close),
    }


def _legacy_dataset(case: dict[str, Any]) -> DetectorDataset:
    c1 = _legacy_bar(
        cast(dict[str, object], case["c1"]),
        timeframe=BarTimeframe.D1,
        label=f"{case['id']}:c1",
    )
    c2 = _legacy_bar(
        cast(dict[str, object], case["c2"]),
        timeframe=BarTimeframe.D1,
        label=f"{case['id']}:c2",
    )
    c3 = _legacy_bar(
        _c3_payload(case),
        timeframe=BarTimeframe.D1,
        label=f"{case['id']}:c3",
    )
    h1 = tuple(
        _legacy_bar(
            item,
            timeframe=BarTimeframe.H1,
            label=f"{case['id']}:h1:{index}",
        )
        for index, item in enumerate(cast(list[dict[str, object]], case["h1"]))
    )
    d1 = (c1, c2, c3)
    identity = DetectorDatasetIdentity(
        dataset_version=f"parity-{str(case['id']).lower()}",
        manifest_sha256=_digest(f"{case['id']}:legacy-manifest"),
        normalized_sha256=normalized_digest(h1, d1),
        provider=PROVIDER,
        venue=VENUE,
        symbol=INSTRUMENT,
        tick_size=Decimal(str(case["tick_size"])),
        h1_rows=len(h1),
        d1_rows=len(d1),
        quality_status="TRUSTED",
        schema_version="PHASE3_DATASET_MANIFEST_V1",
    )
    return DetectorDataset(identity=identity, h1=h1, d1=d1)


def _v2_dataset(
    case: dict[str, Any],
    *,
    price_component: PriceComponent = PriceComponent.MID,
) -> DetectorDatasetV2:
    c1 = _v2_bar(
        cast(dict[str, object], case["c1"]),
        timeframe=BarTimeframe.D1,
        label=f"{case['id']}:c1",
    )
    c2 = _v2_bar(
        cast(dict[str, object], case["c2"]),
        timeframe=BarTimeframe.D1,
        label=f"{case['id']}:c2",
    )
    c3 = _v2_bar(
        _c3_payload(case),
        timeframe=BarTimeframe.D1,
        label=f"{case['id']}:c3",
    )
    h1 = tuple(
        _v2_bar(
            item,
            timeframe=BarTimeframe.H1,
            label=f"{case['id']}:h1:{index}",
        )
        for index, item in enumerate(cast(list[dict[str, object]], case["h1"]))
    )
    if price_component is not PriceComponent.MID:
        h1 = tuple(
            CanonicalPriceBarV2(
                provider=bar.provider,
                venue=bar.venue,
                instrument=bar.instrument,
                price_component=price_component,
                timeframe=bar.timeframe,
                open_time=bar.open_time,
                close_time=bar.close_time,
                open=bar.open,
                high=bar.high,
                low=bar.low,
                close=bar.close,
                source_count=bar.source_count,
                source_digest=bar.source_digest,
                session_policy_version=bar.session_policy_version,
                activity=bar.activity,
            )
            for bar in h1
        )
        d1_source = (c1, c2, c3)
        d1 = tuple(
            CanonicalPriceBarV2(
                provider=bar.provider,
                venue=bar.venue,
                instrument=bar.instrument,
                price_component=price_component,
                timeframe=bar.timeframe,
                open_time=bar.open_time,
                close_time=bar.close_time,
                open=bar.open,
                high=bar.high,
                low=bar.low,
                close=bar.close,
                source_count=bar.source_count,
                source_digest=bar.source_digest,
                session_policy_version=bar.session_policy_version,
                activity=bar.activity,
            )
            for bar in d1_source
        )
    else:
        d1 = (c1, c2, c3)

    identity = PriceDatasetIdentityV2(
        dataset_version=f"parity-{str(case['id']).lower()}",
        provider=PROVIDER,
        venue=VENUE,
        instrument=INSTRUMENT,
        price_component=price_component,
        price_quantum=Decimal(str(case["tick_size"])),
        price_quantum_source=PriceQuantumSource.PROJECT_EXECUTION_PARAMETER,
        price_quantum_observed_at=datetime(2026, 8, 13, 10, 0, tzinfo=UTC),
        instrument_metadata_sha256=METADATA_SHA,
        session_policy_version=SESSION_POLICY,
        normalized_sha256=normalized_price_digest_v2(h1, d1),
        h1_rows=len(h1),
        d1_rows=len(d1),
        quality_status="TRUSTED",
    )
    return DetectorDatasetV2(identity=identity, h1=h1, d1=d1)


def test_v2_detector_has_full_alpha_parity_with_all_frozen_v0_1_fixtures() -> None:
    for case in _cases():
        legacy = detect_dataset(_legacy_dataset(case))
        v2 = detect_dataset_v2(_v2_dataset(case))

        assert v2.status is DetectorRunStatusV2.COMPLETE, case["id"]
        assert v2.candidate_version == MULTI_MARKET_CANDIDATE_VERSION, case["id"]
        assert v2.alpha_strategy_version == ALPHA_STRATEGY_VERSION, case["id"]
        assert v2.detector_version == DETECTOR_VERSION_V2, case["id"]
        assert len(legacy.candidates) == len(v2.candidates) == 1, case["id"]

        legacy_candidate = legacy.candidates[0]
        v2_candidate = v2.candidates[0]
        assert v2_candidate.state is legacy_candidate.state, case["id"]
        assert v2_candidate.reason is legacy_candidate.reason, case["id"]
        assert v2_candidate.rule_trace == legacy_candidate.rule_trace, case["id"]
        assert v2_candidate.evidence_ids == legacy_candidate.evidence_ids, case["id"]
        assert v2_candidate.causal_input_sha256 == legacy_candidate.causal_input_sha256, case["id"]
        assert v2_candidate.trade_plan == legacy_candidate.trade_plan, case["id"]

        if v2_candidate.state is DecisionState.TRADE_PLAN:
            assert v2_candidate.trade_plan is not None, case["id"]
            assert v2_candidate.trade_plan.strategy_version == ALPHA_STRATEGY_VERSION, case["id"]


def test_v2_detector_rejects_non_frozen_signal_price_component() -> None:
    case = _cases()[0]
    with pytest.raises(ValueError, match="MID signal data only"):
        _v2_dataset(case, price_component=PriceComponent.BID)


def test_v2_detector_rejects_content_digest_mismatch() -> None:
    dataset = _v2_dataset(_cases()[0])
    identity = PriceDatasetIdentityV2(
        dataset_version=dataset.identity.dataset_version,
        provider=dataset.identity.provider,
        venue=dataset.identity.venue,
        instrument=dataset.identity.instrument,
        price_component=dataset.identity.price_component,
        price_quantum=dataset.identity.price_quantum,
        price_quantum_source=dataset.identity.price_quantum_source,
        price_quantum_observed_at=dataset.identity.price_quantum_observed_at,
        instrument_metadata_sha256=dataset.identity.instrument_metadata_sha256,
        session_policy_version=dataset.identity.session_policy_version,
        normalized_sha256="0" * 64,
        h1_rows=dataset.identity.h1_rows,
        d1_rows=dataset.identity.d1_rows,
        quality_status="TRUSTED",
    )

    with pytest.raises(ValueError, match="trusted v2 digest"):
        DetectorDatasetV2(identity=identity, h1=dataset.h1, d1=dataset.d1)


def test_v2_detector_requires_three_daily_bars_before_candidate_enumeration() -> None:
    dataset = _v2_dataset(_cases()[0])
    d1 = dataset.d1[:1]
    identity = PriceDatasetIdentityV2(
        dataset_version="v2-one-d1",
        provider=dataset.identity.provider,
        venue=dataset.identity.venue,
        instrument=dataset.identity.instrument,
        price_component=dataset.identity.price_component,
        price_quantum=dataset.identity.price_quantum,
        price_quantum_source=dataset.identity.price_quantum_source,
        price_quantum_observed_at=dataset.identity.price_quantum_observed_at,
        instrument_metadata_sha256=dataset.identity.instrument_metadata_sha256,
        session_policy_version=dataset.identity.session_policy_version,
        normalized_sha256=normalized_price_digest_v2((), d1),
        h1_rows=0,
        d1_rows=1,
        quality_status="TRUSTED",
    )
    run = detect_dataset_v2(DetectorDatasetV2(identity=identity, h1=(), d1=d1))

    assert run.status is DetectorRunStatusV2.INSUFFICIENT_D1_HISTORY
    assert run.candidates == ()
    assert run.trade_plan_count == 0
    assert run.no_signal_count == 0
