import pytest
from pydantic import ValidationError

from romeo_crt_engine.candidate import CandidatePrecommitment


def payload():
    return {
        "candidate_id": "CRT-TEST-v0.1",
        "evidence_refs": ("source:1",),
        "changed_rules": ("rule:changed",),
        "positive_fixture_refs": ("fixture:pos",),
        "negative_fixture_refs": ("fixture:neg",),
        "universe": ("EUR_USD",),
        "timeframes": ("H1",),
        "calendar": "New York",
        "timezone": "UTC",
        "data_provider": "fixture",
        "cost_model": "fixed",
        "dev_start": "2020-01-01",
        "dev_end": "2020-12-31",
        "oos_start": "2021-01-01",
        "oos_end": "2021-12-31",
        "confirm_start": "2022-01-01",
        "confirm_end": "2022-12-31",
    }


def test_valid_precommitment_is_frozen_and_outcome_blind():
    candidate = CandidatePrecommitment.from_untrusted(payload())
    with pytest.raises(ValidationError):
        candidate.candidate_id = "CRT-OTHER-v0.1"


def test_outcome_fields_are_rejected_before_model_validation():
    data = payload() | {"pnl": 10}
    with pytest.raises(ValueError, match="historical outcomes"):
        CandidatePrecommitment.from_untrusted(data)


@pytest.mark.parametrize("field", ["dev_min_closed_trades", "oos_min_closed_trades", "confirm_min_closed_trades"])
def test_activity_thresholds_cannot_be_lowered(field):
    data = payload() | {field: 1}
    with pytest.raises(ValidationError):
        CandidatePrecommitment.from_untrusted(data)


def test_windows_must_be_ordered():
    data = payload() | {"oos_start": "2020-06-01"}
    with pytest.raises(ValidationError):
        CandidatePrecommitment.from_untrusted(data)
