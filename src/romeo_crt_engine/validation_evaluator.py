"""Deterministic synthetic-metrics promotion gate evaluator."""

from dataclasses import dataclass
from enum import StrEnum


class Disposition(StrEnum):
    REJECT = "REJECT"
    REVISE_AS_NEW_VERSION = "REVISE_AS_NEW_VERSION"
    INSUFFICIENT_EVIDENCE = "INSUFFICIENT_EVIDENCE"
    PROMOTE_TO_PAPER_CANDIDATE = "PROMOTE_TO_PAPER_CANDIDATE"


@dataclass(frozen=True)
class ValidationMetrics:
    dev_closed_trades: int
    oos_closed_trades: int
    confirm_closed_trades: int
    oos_base_expectancy: float
    confirm_base_expectancy: float
    combined_base_expectancy: float
    stressed_combined_expectancy: float
    combined_profit_factor: float
    max_drawdown: float
    largest_winner_share: float
    top_five_winner_share: float
    independent_review_complete: bool
    reproducible: bool


@dataclass(frozen=True)
class Evaluation:
    disposition: Disposition
    reasons: tuple[str, ...]


def evaluate(metrics: ValidationMetrics) -> Evaluation:
    if metrics.dev_closed_trades < 30:
        return Evaluation(
            Disposition.INSUFFICIENT_EVIDENCE,
            ("DEV closed-trade minimum is 30",),
        )
    if metrics.oos_closed_trades < 30:
        return Evaluation(
            Disposition.INSUFFICIENT_EVIDENCE,
            ("OOS closed-trade minimum is 30",),
        )
    if metrics.confirm_closed_trades < 20:
        return Evaluation(
            Disposition.INSUFFICIENT_EVIDENCE,
            ("CONFIRM closed-trade minimum is 20",),
        )
    if metrics.oos_base_expectancy < 0 or metrics.confirm_base_expectancy < 0:
        return Evaluation(
            Disposition.REJECT,
            ("BASE expectancy must be non-negative in OOS and CONFIRM",),
        )
    if metrics.combined_base_expectancy < 0:
        return Evaluation(
            Disposition.REJECT,
            ("combined BASE expectancy must be non-negative",),
        )
    if metrics.stressed_combined_expectancy < 0:
        return Evaluation(
            Disposition.REJECT,
            ("combined STRESSED expectancy must be non-negative",),
        )
    if metrics.combined_profit_factor <= 1:
        return Evaluation(
            Disposition.REJECT,
            ("combined BASE profit factor must be greater than 1",),
        )
    if metrics.max_drawdown > 0.15:
        return Evaluation(
            Disposition.REJECT,
            ("maximum drawdown must be at most 15 percent",),
        )
    if metrics.largest_winner_share > 0.25 or metrics.top_five_winner_share > 0.60:
        return Evaluation(
            Disposition.REVISE_AS_NEW_VERSION,
            ("winner-concentration limit exceeded",),
        )
    if not metrics.independent_review_complete:
        return Evaluation(
            Disposition.REVISE_AS_NEW_VERSION,
            ("independent leakage/spec review is incomplete",),
        )
    if not metrics.reproducible:
        return Evaluation(
            Disposition.REVISE_AS_NEW_VERSION,
            ("reproducibility evidence is incomplete",),
        )
    return Evaluation(Disposition.PROMOTE_TO_PAPER_CANDIDATE, ("all frozen gates passed",))
