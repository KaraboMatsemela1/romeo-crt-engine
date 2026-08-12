# Validation Standard

A strategy is not validated because it is profitable historically.

## Required gates

1. Source/spec fidelity
2. Unit-level strategy semantics
3. Known-example reproduction
4. No-lookahead regression tests
5. In-sample exploration
6. Candidate freeze
7. Out-of-sample evaluation
8. Rolling walk-forward
9. Parameter sensitivity
10. Cost/slippage stress
11. Monte Carlo sequence/fill stress
12. Regime breakdown
13. Cross-market robustness when strategy scope claims it
14. Paper trading
15. Shadow execution

## Mandatory reporting

Return, expectancy, PF, Sharpe/Sortino where meaningful, max drawdown, recovery, trade count, win rate, average win/loss/R, exposure, turnover, worst streaks, and breakdowns by relevant dimensions.

## Red flags

- narrow “magic” optimum
- edge disappears with small cost changes
- profits dominated by very few trades
- OOS collapse
- material dependency on one short regime
- repeated strategy reinterpretation after observing OOS
- implausibly good fills
