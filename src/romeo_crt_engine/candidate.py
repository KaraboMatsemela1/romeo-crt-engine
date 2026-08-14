"""Outcome-blind candidate preregistration contract."""

from datetime import date

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CandidatePrecommitment(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    candidate_id: str = Field(pattern=r"^CRT-[A-Z0-9-]+-v[0-9]+\.[0-9]+$")
    evidence_refs: tuple[str, ...] = Field(min_length=1)
    inherited_rules: tuple[str, ...] = ()
    changed_rules: tuple[str, ...] = Field(min_length=1)
    excluded_rules: tuple[str, ...] = ()
    positive_fixture_refs: tuple[str, ...] = Field(min_length=1)
    negative_fixture_refs: tuple[str, ...] = Field(min_length=1)
    universe: tuple[str, ...] = Field(min_length=1)
    timeframes: tuple[str, ...] = Field(min_length=1)
    calendar: str = Field(min_length=1)
    timezone: str = Field(min_length=1)
    data_provider: str = Field(min_length=1)
    cost_model: str = Field(min_length=1)
    dev_start: date
    dev_end: date
    oos_start: date
    oos_end: date
    confirm_start: date
    confirm_end: date
    dev_min_closed_trades: int = Field(ge=30)
    oos_min_closed_trades: int = Field(ge=30)
    confirm_min_closed_trades: int = Field(ge=20)
    reserved_outcome_fields: tuple[str, ...] = (
        "trade_count",
        "closed_trades",
        "pnl",
        "return",
        "profit_factor",
        "drawdown",
        "win_rate",
        "expectancy",
    )

    @model_validator(mode="after")
    def validate_windows(self) -> "CandidatePrecommitment":
        if not self.dev_start < self.dev_end < self.oos_start < self.oos_end < self.confirm_start < self.confirm_end:
            raise ValueError("DEV, OOS and CONFIRM windows must be strictly ordered and non-overlapping")
        if not self.evidence_refs or any(not ref.strip() for ref in self.evidence_refs):
            raise ValueError("evidence_refs must contain non-empty provenance references")
        return self

    @classmethod
    def from_untrusted(cls, payload: dict[str, object]) -> "CandidatePrecommitment":
        forbidden = set(payload) & set(cls.model_fields["reserved_outcome_fields"].default)
        if forbidden:
            raise ValueError(f"candidate selection cannot consume historical outcomes: {sorted(forbidden)}")
        return cls.model_validate(payload)
