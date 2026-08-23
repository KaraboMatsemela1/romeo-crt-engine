# Alpha Lab V2 — Range-Breakout Trend Continuation

## Hypothesis

V1's sweep/reclaim mean-reversion family failed its DEV profitability gate. V2 tests a materially different hypothesis: H1 range breaks that close beyond a prior causal range may exhibit continuation when entered on the next H1 open, especially when aligned with a broader EMA regime.

V2 is optimized on the existing BTCUSDT 2019–2022 DEV window only. OOS 2023–2024 remains inaccessible unless a frozen V2 DEV candidate passes the unchanged gate. CONFIRM 2025+ is not accessed by V2.

## Causal signal

For each H1 signal bar:

1. construct the highest high and lowest low of the previous `N` H1 bars, excluding the current bar;
2. long when the close is above the previous range high plus the configured breakout buffer;
3. short when the close is below the previous range low minus the configured breakout buffer;
4. optionally require fast EMA > slow EMA for longs and fast EMA < slow EMA for shorts;
5. the signal exists only after that bar closes;
6. enter on the next H1 open.

Risk is ATR-normalized from the signal bar. Stop and target are fixed from entry. Same-bar stop/target ambiguity is resolved against the strategy by taking the stop first.

## Preregistered grid

```text
lookback H1 bars       6, 12, 24, 48
breakout buffer        0, 5 bps
EMA regime             none, 24/72, 48/200
direction              both, long-only, short-only
ATR stop               1.0, 1.5, 2.0 ATR
target                 1.5R, 2.0R, 3.0R
max hold               24, 48 H1 bars
```

Total configurations: **1,296**.

## Costs and risk

V2 inherits V1's frozen research assumptions:

```text
risk per trade             1% of realized equity
fee                         4 bps per side
slippage                    2 bps per side
maximum notional leverage   3x
```

## Gates

DEV:

```text
closed trades       >= 100
profit factor       >= 1.30
expectancy          > 0R after costs
max drawdown        <= 20%
```

OOS, only after a DEV pass:

```text
closed trades       >= 50
profit factor       >= 1.15
expectancy          > 0R after costs
```

No OOS-driven parameter changes are allowed. CONFIRM remains unopened in this issue.
