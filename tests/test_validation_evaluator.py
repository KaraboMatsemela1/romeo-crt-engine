from romeo_crt_engine.validation_evaluator import (
    Disposition,
    ValidationMetrics,
    evaluate,
)


def metrics(**overrides):
    values = dict(
        dev_closed_trades=30,
        oos_closed_trades=30,
        confirm_closed_trades=20,
        oos_base_expectancy=0.1,
        confirm_base_expectancy=0.1,
        combined_base_expectancy=0.1,
        stressed_combined_expectancy=0.01,
        combined_profit_factor=1.2,
        max_drawdown=0.10,
        largest_winner_share=0.20,
        top_five_winner_share=0.50,
        independent_review_complete=True,
        reproducible=True,
    )
    return ValidationMetrics(**(values | overrides))


def test_promotion_requires_all_frozen_gates():
    result = evaluate(metrics())
    assert result.disposition is Disposition.PROMOTE_TO_PAPER_CANDIDATE


def test_activity_gate_precedes_performance_interpretation():
    result = evaluate(metrics(dev_closed_trades=29, combined_profit_factor=9))
    assert result.disposition is Disposition.INSUFFICIENT_EVIDENCE


def test_stressed_expectancy_is_hard_gate():
    result = evaluate(metrics(stressed_combined_expectancy=-0.01))
    assert result.disposition is Disposition.REJECT


def test_drawdown_and_concentration_have_distinct_gates():
    assert evaluate(metrics(max_drawdown=0.151)).disposition is Disposition.REJECT
    assert (
        evaluate(metrics(largest_winner_share=0.251)).disposition
        is Disposition.REVISE_AS_NEW_VERSION
    )


def test_review_and_reproducibility_are_required():
    assert (
        evaluate(metrics(independent_review_complete=False)).disposition
        is Disposition.REVISE_AS_NEW_VERSION
    )
    assert evaluate(metrics(reproducible=False)).disposition is Disposition.REVISE_AS_NEW_VERSION
