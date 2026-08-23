# Alpha Lab V1 — DEV Result

## Disposition

`REJECT_V1_RETURN_TO_DEV_NEW_HYPOTHESIS`

The first profitability-focused Alpha Lab hypothesis family did **not** produce a candidate eligible for OOS. This negative result is preserved rather than altering the OOS gate or exposing the protected OOS window.

## Reproducible run

```text
GitHub Actions run    32636465454
symbol                BTCUSDT
bar interval          H1
DEV                    2019-01-01T00:00Z .. 2023-01-01T00:00Z
DEV dataset SHA-256   16932863ee4ba3b60e4094abdf27834ff71414cd056c784a465d30f5f2dc7e0a
configurations        864
candidate id          8efb192202f03f448267
```

## Best V1 DEV configuration

```text
lookback              48 H1 bars
minimum sweep         0 bps
close reclaim         0.5 of sweep-bar range
EMA filter            24 / 72
side                   short only
ATR period             14
stop buffer            0.25 ATR
target                 1.0R
maximum hold           12 H1 bars
risk                   1% realized equity
fee                    4 bps / side
slippage               2 bps / side
max notional leverage  3x
```

## DEV metrics

| Metric | Result | V1 DEV gate |
|---|---:|---:|
| Closed trades | 107 | >= 100 |
| Win rate | 52.34% | — |
| Profit factor | **0.818** | >= 1.30 |
| Expectancy | **-0.0707R** | > 0R |
| Return | **-7.62%** | — |
| Max drawdown | 15.58% | <= 20% |
| Final equity | 92,377.69 | — |

The sample-size and drawdown requirements were met, but profitability was not. The best configuration in the entire registered V1 grid remained negative after the research cost model.

## Protected data state

```text
DEV_GATE_PASS               = false
OOS_ACCESS_AUTHORIZED       = false
OOS_ACCESSED                = false
CONFIRM_ACCESS_AUTHORIZED   = false
CONFIRM_ACCESSED            = false
```

The workflow skipped the OOS job automatically. No 2023–2024 OOS result was consulted, and 2025+ CONFIRM remains untouched.

## Interpretation

V1 falsifies the simple proposition that this H1 rolling-range sweep/reclaim family, over the registered 864 parameter combinations and stated costs, contains a sufficiently robust BTCUSDT DEV edge.

This does **not** prove that all CRT-inspired approaches are unprofitable. It does mean the next iteration must be a new preregistered DEV hypothesis rather than a parameter tweak made in response to OOS.

Reasonable next DEV hypotheses include stronger market-regime ownership, volatility normalization, time/session structure, higher-timeframe trend/location context, and alternative causal exit management. Those changes belong to a new Alpha Lab version and must be evaluated on DEV before OOS is reopened.
