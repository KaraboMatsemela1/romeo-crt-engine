# P6 DEV Result 001

Status: **SEALED — INSUFFICIENT DEV SAMPLE**  
Protocol: `P6-VALIDATION-PROTOCOL-v1`  
Window: `P6-DEV-001` (`2019-01-01` through `2022-12-31`)  
Workflow: run `31682441984`, job `94390737742`

## Result

The sealed DEV dataset reproduced exactly before outcome access, then the frozen strategy/detector/simulator chain was run unchanged across all four preregistered cost scenarios.

```text
trusted M1                    2,074,680
trusted H1                       34,578
complete New-York D1              1,418
rolling detector candidates       1,416
valid TradePlans                      4
BASE closed trades                    4
required DEV minimum                 30
DEV gate            INSUFFICIENT_DEV_SAMPLE
```

The preregistered activity gate therefore fails. This is a **sample-size failure**, not authorization to relax the strategy.

## Frozen chain

```text
strategy         CRT-C3-D1-H1-M1-BEAR-v0.1
detector         CRT-DETECTOR-v0.1
detector run SHA dc8f74314692cdc15be8976ee56052f48d36ca86153ed653972f9dce537ea705
simulator        CRT-BACKTEST-v0.1.1
simulator SHA    193efe934cfadee6fe7bf979f69fa864da739f6daeadfec78866b171c9e2008c
dataset          3e8a39fec1062ef902e8a1ad
manifest SHA     761b561885f94cdb440be02d3a84169549d7bafd8e820bb9654c77ed8aed9e97
```

## Cost-scenario observations

Because only four trades exist, the following figures are descriptive only and are not statistically sufficient to establish edge.

| Scenario | Trades | Win rate | Avg / expectancy R | Net P&L | Profit factor | Final realized equity |
|---|---:|---:|---:|---:|---:|---:|
| IDEAL | 4 | 50% | -0.0130 R | -31.03 | 0.969 | 99,968.97 |
| BASE | 4 | 50% | -0.1264 R | -256.36 | 0.743 | 99,743.64 |
| STRESSED | 4 | 50% | -0.1963 R | -395.18 | 0.604 | 99,604.82 |
| SEVERE | 4 | 50% | -0.2659 R | -533.42 | 0.465 | 99,466.58 |

The observed direction of transaction-cost sensitivity is adverse, but four trades are insufficient for robustness inference.

## Protocol consequence

The protocol was frozen before results:

```text
BASE closed trades < 30
    -> INSUFFICIENT_DEV_SAMPLE
    -> no parameter optimization
    -> no OOS outcome access
    -> no CONFIRM outcome access
    -> default Phase-6 disposition = INSUFFICIENT_EVIDENCE
```

Therefore:

```text
P6_OOS_OUTCOME_ACCESS_AUTHORIZED     = false
P6_CONFIRM_OUTCOME_ACCESS_AUTHORIZED = false
PARAMETER_OPTIMIZATION_AUTHORIZED    = false
PAPER_TRADING_AUTHORIZED             = false
LIVE_TRADING_AUTHORIZED              = false
```

The predeclared OOS and CONFIRM windows remain untouched. September 2025 remains quarantined.

## Interpretation

This result does **not** prove that CRT is unprofitable and does **not** prove that Romeo's broader discretionary methodology lacks edge. It says something narrower and more important for this engineering project:

> The exact frozen reproduction candidate `CRT-C3-D1-H1-M1-BEAR-v0.1`, under its current deterministic interpretation, is too selective on BTCUSDT over the preregistered four-year DEV window to support statistical validation.

A future attempt to increase activity must be a **new strategy version backed by new source evidence or an independently demonstrated implementation defect**. It may not mutate v0.1 in place after observing this result.

## Phase-6 disposition

```text
INSUFFICIENT_EVIDENCE
```

No OOS, confirmatory, paper, shadow, or live promotion is permitted from this candidate.
