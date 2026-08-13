# Phase 6 Completion Report — Strategy Validation

Date: 2026-08-13  
Protocol: `P6-VALIDATION-PROTOCOL-v1`  
Frozen candidate: `CRT-C3-D1-H1-M1-BEAR-v0.1`  
Detector: `CRT-DETECTOR-v0.1`  
Simulator used for DEV: `CRT-BACKTEST-v0.1.1`  
Final disposition: **INSUFFICIENT_EVIDENCE**

## Executive result

Phase 6 is complete for the frozen v0.1 candidate because the preregistered validation protocol reached an explicit terminal decision at the DEV activity gate.

The four-year DEV window produced only four valid TradePlans / closed trades. The protocol required at least 30 BASE closed trades before deeper robustness analysis or OOS access.

Therefore the correct result is:

```text
INSUFFICIENT_EVIDENCE
```

not optimization, not OOS testing, and not paper promotion.

## Validation chronology

The sequence was deliberately gated:

```text
freeze protocol
 -> declare DEV / OOS / quarantine / CONFIRM windows
 -> encounter provider-data anomalies
 -> resolve data integrity before outcomes
 -> seal DEV dataset with P&L access disabled
 -> independently reproduce sealed dataset with P&L access disabled
 -> authorize DEV-only outcome access
 -> run frozen detector/simulator
 -> evaluate preregistered activity gate
 -> stop because sample < 30
```

OOS and CONFIRM were never opened.

## DEV trusted dataset

```text
window                    2019-01-01 .. 2022-12-31
provider                  Binance Public Data
venue                     Binance Spot
symbol                    BTCUSDT
dataset_version           3e8a39fec1062ef902e8a1ad
manifest_sha256           761b561885f94cdb440be02d3a84169549d7bafd8e820bb9654c77ed8aed9e97
normalized_sha256         46682c2d793dbdd0a0939862f444d19b4817559c8989a7fde031598d52cb29f5
M1 rows                    2,074,680
H1 rows                    34,578
complete NY D1             1,418
raw UTC daily archives     1,461
excluded UTC archives      20
REST exact verification    48
provider checksum evidence 1,413
```

The sealed identity was reproduced by an independent provider retrieval before outcome access.

## Data-quality governance

Two Phase-6 amendments were required and were completed before performance access:

1. `P6-DATA-QUALITY-AMENDMENT-001` — independently evidenced Binance maintenance/trading suspension on 2019-03-12 02:00–08:00 UTC.
2. `P6-DATA-QUALITY-AMENDMENT-002` — conservative whole-archive exclusion of 20 checksum-authenticated incomplete/malformed UTC daily archives.

No missing prices were synthesized. Excluded raw bytes remain preserved and auditable.

## DEV detector activity

```text
complete NY D1             1,418
rolling detector candidates 1,416
valid TradePlans                4
TradePlans / closed trades      4
minimum required               30
```

This candidate is therefore too sparse on the selected first instrument/window for statistically meaningful validation under the frozen protocol.

## Descriptive cost results

These are preserved but must not be overinterpreted because `n=4`.

| Scenario | Trades | Win rate | Avg / expectancy R | Net P&L | Profit factor | Final equity |
|---|---:|---:|---:|---:|---:|---:|
| IDEAL | 4 | 50% | -0.0130 | -31.03 | 0.969 | 99,968.97 |
| BASE | 4 | 50% | -0.1264 | -256.36 | 0.743 | 99,743.64 |
| STRESSED | 4 | 50% | -0.1963 | -395.18 | 0.604 | 99,604.82 |
| SEVERE | 4 | 50% | -0.2659 | -533.42 | 0.465 | 99,466.58 |

The direction of friction sensitivity is unfavorable, but four observations cannot establish a robust expectancy estimate.

## Analyses intentionally not run

The protocol correctly prevented the following because the sample gate failed:

- parameter optimization;
- sensitivity-driven rule selection;
- walk-forward performance inference;
- Monte Carlo performance inference;
- OOS outcome access;
- final confirmatory outcome access;
- paper promotion.

Skipping these is part of correct validation, not incomplete work.

## What this result means

It means:

> `CRT-C3-D1-H1-M1-BEAR-v0.1`, as deterministically frozen and applied to BTCUSDT, generated too few trades over the preregistered DEV period to justify statistical or production claims.

It does **not** establish that all CRT variants are unprofitable, and it does not invalidate Romeo's broader discretionary methodology. The project only tested the exact frozen reproduction candidate.

## Versioning consequence

v0.1 is now historical evidence and should remain frozen.

A more active candidate may only arise through:

- new direct/source-backed strategy evidence;
- resolution of previously deferred doctrine as a new candidate version;
- a separately demonstrated implementation defect with explicit version-impact review.

It must not be created by tuning rules until this DEV history becomes profitable or sufficiently active.

## Phase exit decision

Phase-6 exit criterion requires a written decision. That criterion is satisfied with:

```text
Phase 6                    COMPLETE
Disposition                INSUFFICIENT_EVIDENCE
OOS consumed               NO
CONFIRM consumed           NO
Paper candidate            NO
Paper trading authorized   NO
Shadow trading authorized  NO
Live trading authorized    NO
```

## Recommended project direction

The next legitimate project track is **candidate research/revision**, not Phase 7.

Revisit the Phase-1 evidence debts and later Romeo public doctrine to determine whether a broader, still-source-faithful v0.2 candidate can be specified deterministically. Any v0.2 must repeat specification freeze, fixtures, detector compatibility, trusted-data validation and Phase-6-style preregistration before promotion.
