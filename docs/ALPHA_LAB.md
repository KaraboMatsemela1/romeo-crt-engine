# Alpha Lab — Profitability Research Track

Alpha Lab is an isolated research lane for discovering robust trading edges inspired by CRT / liquidity-sweep ideas. It does **not** reinterpret the closed `romeo-crt-engine` evidence result and it does not claim to be an exact implementation of Romeo's strategy.

## Research objective

Find a deterministic strategy that remains profitable after realistic research costs and survives an untouched out-of-sample test.

The first route is BTCUSDT H1 because it provides a deep, continuous public history and allows the research machinery to be exercised quickly. Multi-market validation comes after the first route is reproducible.

## Data windows

```text
DEV      2019-01-01T00:00Z .. 2023-01-01T00:00Z   optimization allowed
OOS      2023-01-01T00:00Z .. 2025-01-01T00:00Z   one-shot frozen-candidate evaluation
CONFIRM  2025-01-01T00:00Z onward                 unopened by Phase 0
```

DEV and OOS are downloaded in separate GitHub Actions jobs. The OOS job runs only when the frozen DEV candidate passes the DEV gate. Phase 0 never downloads CONFIRM data.

## Strategy family V1

The first family is a causal H1 false-break / liquidity-sweep model:

1. compute the prior rolling H1 range, excluding the current bar;
2. require the current bar to sweep a prior high or low and close back through that level;
3. optionally require EMA trend alignment;
4. optionally restrict direction to long, short or both;
5. require a configurable close-reclaim fraction within the sweep bar;
6. enter at the **next bar open**, never at the signal close;
7. stop beyond the sweep extreme plus an optional ATR buffer;
8. target a fixed multiple of initial risk;
9. close at stop, target or a fixed maximum holding period;
10. if H1 OHLC shows stop and target hit in the same bar, assume the stop occurred first.

This is CRT-inspired research, not a claim that every parameter or rule comes directly from Romeo.

## Cost and risk assumptions

Default discovery assumptions:

```text
initial equity             100,000 research units
risk per trade             1.0% of realized equity
fee                         4 bps per side
slippage                    2 bps per side
maximum notional leverage   3x
```

Position size includes estimated stop slippage and fees when calculating the risk quantity and is capped by the leverage ceiling.

## DEV search

The deterministic V1 grid searches:

- lookback: 12 / 24 / 48 hours;
- sweep depth: 0 / 5 bps;
- reclaim fraction: 0 / 0.5;
- EMA filter: none / 24-vs-72 aligned;
- direction: both / long only / short only;
- stop ATR buffer: 0 / 0.25;
- target: 1.0R / 1.5R / 2.0R;
- max hold: 12 / 24 H1 bars.

That is 864 preregistered DEV configurations. The selected configuration is frozen into a JSON candidate artifact before OOS is accessible.

## Gates

DEV candidate gate:

```text
closed trades       >= 100
profit factor       >= 1.30
expectancy          > 0R after costs
max drawdown        <= 20%
```

OOS gate:

```text
closed trades       >= 50
profit factor       >= 1.15
expectancy          > 0R after costs
```

A failed OOS result is preserved. It may inspire a **new DEV candidate version**, but OOS parameters are never changed in place to make the failed OOS period profitable.

## Commands

DEV search:

```bash
python -m romeo_crt_engine.alpha_lab.run_cycle dev-search \
  --cache-dir .alpha-cache \
  --candidate-out alpha-dev-candidate.json \
  --metrics-out alpha-dev-metrics.json
```

OOS evaluation requires a DEV-passing frozen candidate:

```bash
python -m romeo_crt_engine.alpha_lab.run_cycle oos-eval \
  --cache-dir .alpha-cache \
  --candidate alpha-dev-candidate.json \
  --result-out alpha-oos-result.json
```

The canonical active queue is GitHub Issue #128. Phase 0 implementation is Issue #129.

## Non-goals

Phase 0 does not authorize paper or live trading, inspect CONFIRM, change historical Romeo Phase 6/6B results, claim execution-quality spread modeling, or claim that a positive DEV result is a validated edge.
