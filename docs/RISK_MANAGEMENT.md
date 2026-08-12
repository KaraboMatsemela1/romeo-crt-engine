# Risk Management

The risk engine owns authorization. Strategy and AI components cannot override it.

## Policy classes

- per-trade risk
- daily/weekly loss budget
- drawdown budget
- concurrent-position limit
- correlated exposure
- per-instrument exposure
- spread/slippage tolerance
- stale-data protection
- consecutive-loss/circuit-breaker behavior
- portfolio/broker reconciliation state
- emergency kill switch

## Design rule

Any missing or invalid critical risk input means `REJECT` rather than “best effort.”

## Research parameters

Illustrative values such as 0.5% risk per trade may be used as experiment defaults, but are not project conclusions and must remain configurable/versioned.
