# Validation and paper-promotion evaluator

The evaluator accepts only preregistered aggregate metrics and explicit review/reproducibility status. It uses synthetic fixtures in tests and does not load market data or inspect hidden OOS/CONFIRM outcomes.

The frozen gates are applied in this order:

1. DEV ≥30, OOS ≥30 and CONFIRM ≥20 closed trades;
2. non-negative BASE expectancy for OOS, CONFIRM and combined samples;
3. non-negative combined STRESSED expectancy;
4. combined BASE profit factor >1;
5. maximum drawdown ≤15%;
6. winner concentration ≤25% for the largest winner and ≤60% for the top five;
7. independent review and reproducibility evidence complete.

The result is one of REJECT, REVISE_AS_NEW_VERSION, INSUFFICIENT_EVIDENCE, or
PROMOTE_TO_PAPER_CANDIDATE. This module does not authorize paper execution; that
remains gated by the Phase-7 issue.
