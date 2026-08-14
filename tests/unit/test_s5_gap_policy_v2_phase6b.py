from __future__ import annotations

from copy import deepcopy

import pytest

from romeo_crt_engine.market_data.s5_gap_policy_v2 import (
    OBSERVATION_POLICY_VERSION,
    market_gaps_from_complete_s5_evidence,
)
from romeo_crt_engine.market_data.session_policy_v2 import GapCategory

DIGEST = "a" * 64
REQUEST_SHA = "b" * 64
RESPONSE_SHA = "c" * 64


def _documents() -> tuple[dict[str, object], dict[str, object]]:
    missing = [
        {
            "start_utc": "2022-01-01T00:00:00+00:00",
            "end_utc": "2022-01-01T00:02:00+00:00",
            "missing_minutes": 2,
        },
        {
            "start_utc": "2022-01-08T00:00:00+00:00",
            "end_utc": "2022-01-08T00:01:00+00:00",
            "missing_minutes": 1,
        },
    ]
    reconciliation: dict[str, object] = {
        "schema_version": "P6B_OANDA_RECONCILIATION_EVIDENCE_V2",
        "observation_policy_version": OBSERVATION_POLICY_VERSION,
        "provider": "OANDA_V20",
        "environment": "practice",
        "instrument": "XAU_USD",
        "year": 2022,
        "price_component": "MID",
        "granularity": "M1",
        "missing_interval_count": 2,
        "missing_intervals_sha256": DIGEST,
        "missing_intervals": missing,
    }
    classifications = [
        {
            "gap_index": index,
            "start_utc": gap["start_utc"],
            "end_utc": gap["end_utc"],
            "missing_minutes": gap["missing_minutes"],
            "classification": "NO_PRICE_OBSERVATION",
            "s5_complete_observations_inside_gap": 0,
            "evidence": [
                {
                    "start_utc": gap["start_utc"],
                    "end_utc": gap["end_utc"],
                    "request_sha256": REQUEST_SHA,
                    "raw_response_sha256": RESPONSE_SHA,
                    "complete_s5_count_in_gap": 0,
                }
            ],
        }
        for index, gap in enumerate(missing)
    ]
    s5: dict[str, object] = {
        "schema_version": "P6B_OANDA_S5_GAP_EVIDENCE_V1",
        "observation_policy_version": OBSERVATION_POLICY_VERSION,
        "provider": "OANDA_V20",
        "environment": "practice",
        "instrument": "XAU_USD",
        "year": 2022,
        "source_missing_intervals_sha256": DIGEST,
        "eligible_gap_count": 2,
        "no_price_observation_gap_count": 2,
        "unresolved_provider_gap_count": 0,
        "classifications": classifications,
    }
    return reconciliation, s5


def test_complete_s5_evidence_builds_no_price_gap_policy() -> None:
    reconciliation, s5 = _documents()

    gaps = market_gaps_from_complete_s5_evidence(reconciliation, s5)

    assert len(gaps) == 2
    assert all(gap.category is GapCategory.NO_PRICE_OBSERVATION for gap in gaps)
    assert all(gap.policy_version == OBSERVATION_POLICY_VERSION for gap in gaps)
    assert all(gap.provider == "OANDA_V20" for gap in gaps)
    assert all(gap.venue == "OANDA_FXTRADE" for gap in gaps)
    assert all(gap.evidence_id.startswith("P6B-S5-") for gap in gaps)


def test_partial_s5_inventory_cannot_construct_trusted_gap_policy() -> None:
    reconciliation, s5 = _documents()
    s5["eligible_gap_count"] = 1

    with pytest.raises(ValueError, match="complete all-gap S5 evidence is required"):
        market_gaps_from_complete_s5_evidence(reconciliation, s5)


def test_unresolved_provider_gap_cannot_construct_trusted_gap_policy() -> None:
    reconciliation, s5 = _documents()
    classifications = deepcopy(s5["classifications"])
    assert isinstance(classifications, list)
    assert isinstance(classifications[1], dict)
    classifications[1]["classification"] = "UNRESOLVED_PROVIDER_GAP"
    classifications[1]["s5_complete_observations_inside_gap"] = 1
    s5["classifications"] = classifications
    s5["no_price_observation_gap_count"] = 1
    s5["unresolved_provider_gap_count"] = 1

    with pytest.raises(ValueError, match="UNRESOLVED_PROVIDER_GAP"):
        market_gaps_from_complete_s5_evidence(reconciliation, s5)


def test_tampered_classification_coordinates_are_rejected() -> None:
    reconciliation, s5 = _documents()
    classifications = deepcopy(s5["classifications"])
    assert isinstance(classifications, list)
    assert isinstance(classifications[0], dict)
    classifications[0]["end_utc"] = "2022-01-01T00:03:00+00:00"
    s5["classifications"] = classifications

    with pytest.raises(ValueError, match="end does not match raw gap"):
        market_gaps_from_complete_s5_evidence(reconciliation, s5)


def test_s5_inventory_must_be_bound_to_exact_raw_gap_digest() -> None:
    reconciliation, s5 = _documents()
    s5["source_missing_intervals_sha256"] = "d" * 64

    with pytest.raises(ValueError, match="does not bind"):
        market_gaps_from_complete_s5_evidence(reconciliation, s5)
