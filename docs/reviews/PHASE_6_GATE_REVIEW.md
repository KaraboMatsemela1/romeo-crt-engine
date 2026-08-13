# Phase 6 Gate Review

Date: 2026-08-13  
Protocol: `P6-VALIDATION-PROTOCOL-v1`  
Candidate: `CRT-C3-D1-H1-M1-BEAR-v0.1`  
Disposition: **INSUFFICIENT_EVIDENCE**

## Review question

Did the frozen v0.1 candidate produce enough preregistered DEV evidence to justify opening OOS validation or progressing toward paper trading?

**Answer: No.**

## Evidence reviewed

- Phase-6 protocol was merged before DEV results were accessed.
- DEV window was fixed at `2019-01-01` through `2022-12-31`.
- OOS, September quarantine, and CONFIRM windows were predeclared and remained unopened during DEV data remediation.
- Data-quality Amendments 001 and 002 were written before DEV outcome access.
- The DEV dataset was sealed while detector/P&L access was disabled.
- A second provider retrieval reproduced the sealed dataset byte-for-byte before DEV outcome access was authorized.
- Normal CI passed locked install, Ruff, strict MyPy and tests on the outcome-enabled head.
- The previously frozen September 2025 integration smoke remained green.
- DEV outcome workflow run `31682441984`, job `94390737742`, completed successfully.

## Data integrity decision

Sealed DEV dataset:

```text
dataset_version          3e8a39fec1062ef902e8a1ad
manifest_sha256          761b561885f94cdb440be02d3a84169549d7bafd8e820bb9654c77ed8aed9e97
normalized_sha256        46682c2d793dbdd0a0939862f444d19b4817559c8989a7fde031598d52cb29f5
M1                       2,074,680
H1                       34,578
complete NY D1           1,418
excluded UTC archives    20
REST verification        48
checksum verification    1,413
```

No missing observations were synthesized. The known 2019-03-12 venue closure is separately evidenced; 20 other checksum-authenticated malformed/incomplete daily archives are conservatively excluded whole without inventing an operational cause.

## Semantic-drift review

The DEV branch does **not** change:

- `strategy/CRT_V0.1_SPEC.md`;
- `src/romeo_crt_engine/crt/v0_1.py`;
- `src/romeo_crt_engine/crt/detector.py`;
- entry logic;
- stop geometry;
- target geometry;
- Model #1 threshold;
- Candle-3 eligibility;
- direction;
- cost-scenario definitions;
- risk fraction used by the preregistered DEV run.

The simulator patch `CRT-BACKTEST-v0.1.1` changes only the H1 input continuity contract from globally gapless to strictly ordered/non-overlapping so independently governed market-data gaps can be represented without synthetic bars. Existing entry/fill/stop/target/sizing/cost semantics remain unchanged and regression tests pass.

## DEV result

```text
rolling detector candidates   1,416
valid TradePlans                  4
BASE closed trades                4
required DEV minimum             30
activity gate     INSUFFICIENT_DEV_SAMPLE
```

The four cost scenarios all closed the same four trades. Their P&L is negative in this tiny sample and becomes worse as friction increases, but the decisive gate failure is **sample size**, not the sign of P&L.

## Protocol decision

Because BASE closed trades are below 30:

- sensitivity optimization is prohibited;
- walk-forward inference is not meaningful;
- Monte Carlo inference is not meaningful;
- OOS outcome access remains prohibited;
- CONFIRM remains untouched;
- paper promotion is prohibited;
- the default Phase-6 disposition is `INSUFFICIENT_EVIDENCE`.

This is consistent with the protocol frozen before results.

## Required next move

Do **not** proceed to Phase 7 with v0.1.

Any attempt to improve trade frequency must be one of:

1. a demonstrated implementation/data defect corrected with version-impact review; or
2. a new evidence-backed strategy candidate/version, e.g. v0.2, researched and frozen before fresh validation.

The current v0.1 result must remain immutable historical evidence.

## Authorization

```text
OOS_OUTCOME_ACCESS_AUTHORIZED     = false
CONFIRM_OUTCOME_ACCESS_AUTHORIZED = false
PAPER_TRADING_AUTHORIZED          = false
SHADOW_TRADING_AUTHORIZED         = false
LIVE_TRADING_AUTHORIZED           = false
```
