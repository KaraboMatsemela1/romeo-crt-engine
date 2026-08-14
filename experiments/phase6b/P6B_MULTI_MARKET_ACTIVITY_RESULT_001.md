# Phase 6B Multi-Market Activity Result 001

**Protocol:** `P6B-MULTI-MARKET-ACTIVITY-PROTOCOL-v1`  
**Trusted-universe freeze:** `experiments/phase6b/P6B_TRUSTED_DATASET_FREEZE_001.json`  
**Freeze commit:** `8214c31e09d53cffadce453727604e0847a4d22e`  
**Activity workflow:** Phase 6B Detector Activity Gate run #1 (`31802738559`)  
**Activity workflow head:** `377fed2ffb7da7dcfef10109d39658de6516bddb`  
**Machine-readable result:** `experiments/phase6b/P6B_MULTI_MARKET_ACTIVITY_RESULT_001.json`

## Decision

```text
INSUFFICIENT_MULTI_MARKET_SAMPLE
```

The trusted-data gate passed **4/4 instruments**, and **3/4 instruments** contributed at least one TradePlan. However, the frozen detector produced only **7 pooled TradePlans** versus the preregistered minimum of **30**.

This is a terminal Phase 6B sample-size decision for the current candidate. It is not a performance result and it does not authorize backtesting, P&L access, parameter optimization, paper trading, shadow trading, or live trading.

## Counts-only result

| Instrument | Complete NY-D1 | Candidates | NO_SIGNAL | TradePlans |
|---|---:|---:|---:|---:|
| `EUR_USD` | 1,249 | 1,247 | 1,244 | 3 |
| `NAS100_USD` | 1,245 | 1,243 | 1,241 | 2 |
| `SPX500_USD` | 1,245 | 1,243 | 1,241 | 2 |
| `XAU_USD` | 1,244 | 1,242 | 1,242 | 0 |
| **Pooled** | — | **4,975** | **4,968** | **7** |

Threshold comparison:

```text
accepted instruments       4   >= 2   PASS
contributing instruments   3   >= 2   PASS
pooled TradePlans           7   >= 30  FAIL
```

The decision therefore follows directly from the frozen protocol:

```text
accepted >= 2
contributors >= 2
pooled TradePlans < 30
=> INSUFFICIENT_MULTI_MARKET_SAMPLE
```

## ReasonCode inventory

### EUR_USD

```text
DOUBLE_OR_OPPOSITE_SWEEP      190
ELIGIBLE                        3
NON_CONSECUTIVE_PARENT        416
NO_BEARISH_PARENT_SWEEP       367
NO_MODEL1_CONFIRMATION          9
PARENT_CLOSE_NOT_RECLAIMED    174
TARGET1_CONSUMED_IN_C2         77
TARGET1_CONSUMED_PRE_ENTRY     11
```

### NAS100_USD

```text
DOUBLE_OR_OPPOSITE_SWEEP      179
ELIGIBLE                        2
NON_CONSECUTIVE_PARENT        416
NO_BEARISH_PARENT_SWEEP       312
NO_MODEL1_CONFIRMATION         20
PARENT_CLOSE_NOT_RECLAIMED    231
TARGET1_CONSUMED_IN_C2         64
TARGET1_CONSUMED_PRE_ENTRY     19
```

### SPX500_USD

```text
DOUBLE_OR_OPPOSITE_SWEEP      167
ELIGIBLE                        2
NON_CONSECUTIVE_PARENT        416
NO_BEARISH_PARENT_SWEEP       333
NO_MODEL1_CONFIRMATION         19
PARENT_CLOSE_NOT_RECLAIMED    220
TARGET1_CONSUMED_IN_C2         68
TARGET1_CONSUMED_PRE_ENTRY     18
```

### XAU_USD

```text
DOUBLE_OR_OPPOSITE_SWEEP      159
NON_CONSECUTIVE_PARENT        416
NO_BEARISH_PARENT_SWEEP       368
NO_MODEL1_CONFIRMATION         12
PARENT_CLOSE_NOT_RECLAIMED    179
TARGET1_CONSUMED_IN_C2         88
TARGET1_CONSUMED_PRE_ENTRY     20
```

No candidate timestamps, entry/stop/target geometry, trade details, or performance outcomes were persisted.

## Audit binding

The activity workflow first proved that freeze commit `8214c31e...` was an ancestor of the execution head, then independently downloaded and verified the exact frozen trusted artifacts before invoking the detector.

Counts artifact:

```text
artifact id        9219943258
artifact zip sha   ad5f6bd04d124344e99aaecafd19ad2a5c7480b973984aa3bc78934e814d0b66
aggregate file sha effa269e1a55cd1643c6d5c8f2dff7128a9ac6188ada6d48079efc2e511538b4
```

Detector run SHA-256 values:

```text
EUR_USD      6aa0ba5c9f01c5b9db0488ef9023ea5c836ce7fc17a3f4f6a0a2ca70f78c498b
NAS100_USD   1716a8c2af14b269dcd5aaef3ab56db5f87e31dd82f4929249d35c1fd8d0c64b
SPX500_USD   7f91ac7e422914579c4f38219ea78e6a78c936794d44d9c542fa11221fec99c1
XAU_USD      6de2ea68bd4bd62e0ccb808f484f642c498bfb7ce2387cc248cacfb1a02050c3
```

## Authorization after decision

```text
ALPHA_MUTATION                      false
PARAMETER_OPTIMIZATION              false
PERFORMANCE_PROTOCOL                false
BACKTESTER                          false
MULTI_MARKET_PNL_OUTCOME_ACCESS     false
V0_1_OOS / CONFIRM                  unopened
PAPER_TRADING                       false
SHADOW_TRADING                      false
LIVE_TRADING                        false
PHASE_7                             blocked
```

The current Phase 6B candidate may not be promoted by lowering the 30-TradePlan threshold, dropping zero/low-activity instruments after seeing counts, or otherwise changing preregistered rules based on this outcome.
