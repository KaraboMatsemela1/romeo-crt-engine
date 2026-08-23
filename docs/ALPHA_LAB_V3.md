# Alpha Lab V3 — Volatility-Qualified Breakout Continuation

V3 is a preregistered DEV-only successor to the V2 H1 breakout-continuation family. V2 was positive after costs but missed the fixed DEV profit-factor gate at 1.281 versus the required 1.30. V3 does not lower that gate and does not use OOS feedback.

## Hypothesis

V2's long breakout edge may be diluted by marginal breakouts. V3 keeps causal close-confirmed range breaks but requires higher signal quality using only information available when the signal H1 bar closes:

1. close above the prior rolling H1 high by a configured breakout buffer;
2. optional trend regime: signal close must be above EMA-200;
3. ATR(14) expansion relative to the median ATR(14) of the prior 48 completed H1 bars;
4. a strong signal-bar close location `(close-low)/(high-low)`;
5. entry only at the next H1 open;
6. ATR stop, fixed-R target, and maximum hold;
7. one position at a time;
8. same-bar stop/target ambiguity resolves to stop.

## Cost and risk model

```text
initial equity             100,000 research units
risk per trade             1.0% of realized equity
fee                         4 bps per side
slippage                    2 bps per side
maximum notional leverage   3x
```

## DEV search

```text
range lookback          24 / 48 H1 bars
breakout buffer         0 / 5 / 10 bps
EMA-200 regime          off / on
ATR expansion ratio     0.8 / 1.0 / 1.2
close-location minimum  0.50 / 0.75
stop                    1.5 / 2.0 ATR
target                  2.0R / 3.0R
maximum hold            24 / 48 H1 bars
direction               long only
```

Exactly **576** configurations are preregistered.

## Data gates

```text
DEV      2019-01-01T00:00Z .. 2023-01-01T00:00Z   optimization allowed
OOS      2023-01-01T00:00Z .. 2025-01-01T00:00Z   one-shot only after DEV pass
CONFIRM  2025-01-01T00:00Z onward                 inaccessible in V3
```

DEV promotion requires all of:

```text
closed trades       >= 100
profit factor       >= 1.30
expectancy          > 0R after costs
max drawdown        <= 20%
```

If DEV passes, the exact candidate is frozen before OOS is downloaded/read. OOS then requires at least 50 trades, PF >= 1.15, and positive expectancy. V3 never reads CONFIRM and does not authorize paper or live trading.
