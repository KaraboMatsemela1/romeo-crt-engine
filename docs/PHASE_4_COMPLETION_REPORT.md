# Phase 4 Completion Report — CRT Detection Engine

**Project:** `romeo-crt-engine`  
**Date:** 2026-08-13  
**Phase:** 4 — CRT detection engine  
**Status:** **COMPLETE**  
**Strategy:** `CRT-C3-D1-H1-M1-BEAR-v0.1` — unchanged  
**Detector:** `CRT-DETECTOR-v0.1`  
**Trusted integration dataset:** `ee1300f0da50e4debcbbc3b7`  
**Profitability:** **NOT ESTABLISHED**  
**Paper / shadow / live trading:** **NOT AUTHORIZED**

## Completion decision

Phase 4 is complete for the first frozen CRT route.

The project can now consume trusted canonical H1/D1 data, enforce dataset identity/integrity, enumerate every rolling C1/C2/C3 instance, execute the frozen deterministic v0.1 strategy, and emit auditable accepted/rejected detector records without LLM judgement, P&L feedback, or broker/risk authority.

This phase proves **detector integrity and strategy/data integration**. It does not prove that the strategy has an edge.

## Frozen Phase-5 handoff

```text
strategy  CRT-C3-D1-H1-M1-BEAR-v0.1
detector  CRT-DETECTOR-v0.1
dataset   ee1300f0da50e4debcbbc3b7
```

Machine-readable handoff:

```text
strategy/CRT_V0.1_DETECTOR_FREEZE_MANIFEST.json
```

The dataset is a compact provider-backed integration fixture, not the eventual full historical/OOS validation dataset.

## Delivered detector architecture

```text
trusted dataset directory
        |
        v
manifest identity parser
        |
        v
manifest/content integrity verification
        |
        v
canonical H1/D1 loader
        |
        v
rolling C1/C2/C3 enumerator
        |
        +----> C3 gate uses open/time only
        |
        v
frozen evaluate_bearish_c3()
        |
        v
DetectorCandidate
  - state/reason
  - rule trace
  - evidence IDs
  - causal input hash
  - TradePlan | null
        |
        v
DetectorRun + run SHA-256
```

The actual strategy predicates remain in the already-frozen Phase-2 executable contract. Phase 4 does not maintain a second implementation.

## Exit-criterion results

| Exit criterion | Result |
|---|---|
| Frozen v0.1 strategy reused rather than reinterpreted | PASS |
| Trusted dataset manifest required | PASS |
| Loaded canonical content must reproduce normalized SHA-256 | PASS |
| Provider/venue/symbol identity enforced | PASS |
| Rolling C1/C2/C3 enumeration deterministic | PASS |
| C3 final D1 high/low/close excluded from decision | PASS |
| Completed in-window H1 only | PASS |
| Future-C3 D1 mutation regression | PASS |
| Phase-2 positive/negative fixture parity | PASS |
| Exact reason-code preservation | PASS |
| Candidate explanation/audit object | PASS |
| Immutable TradePlan preserved | PASS |
| Deterministic causal-input hash | PASS |
| Deterministic run hash | PASS |
| Exact frozen dataset reconstruction | PASS |
| Provider-backed detector integration | PASS |
| Locked install / Ruff / strict MyPy / tests | PASS |
| Independent leakage/spec-drift review | PASS |
| Backtest/P&L logic present in detector | **NO — prohibited** |
| Strategy parameters changed | **NO** |
| Profitability established | **NO — not a Phase-4 criterion** |

## Frozen-fixture parity

The Phase-2 machine-readable fixture corpus remains the semantic oracle for the frozen strategy.

Phase 4 converts each case into provider-neutral canonical bars, then runs the same detector entry point used for trusted historical data.

Result distribution:

```text
7 frozen cases
1 TRADE_PLAN
6 NO_SIGNAL
```

Positive fixture remains:

```text
entry   106.0
stop    113.25
target  100.0
```

The six negative fixtures preserve their existing frozen reason codes, including no parent sweep, double/opposite sweep, failed reclaim, consumed T1 and no qualifying Model-1 confirmation.

No fixture expectation was changed to make Phase 4 pass.

## Causality protection

### C1 and C2

The detector passes completed canonical D1 OHLC only after those candles are closed.

### C3

The detector constructs the strategy C3 window from:

```text
open_time
calendar close_time
open_price
```

It does **not** pass:

```text
final C3 daily high
final C3 daily low
final C3 daily close
```

A dedicated regression mutates those future D1 price values to extreme values and requires unchanged:

- detector state;
- reason code;
- TradePlan entry;
- stop;
- target;
- causal-input SHA-256.

### H1

Only completed H1 observations fully contained inside the C3 window enter the strategy evaluator.

This keeps the lower-timeframe decision path causal even though a historical dataset is available in batch form.

## Dataset integrity gate

The detector accepts only datasets whose loaded canonical content agrees with its trusted manifest.

Required checks include:

```text
schema_version == PHASE3_DATASET_MANIFEST_V1
quality_status == TRUSTED
provider/venue/symbol match
H1 row count match
D1 row count match
strict ordering/uniqueness
normalized_digest(loaded H1, loaded D1) == manifest.normalized_sha256
```

A deliberate wrong-digest regression fails closed.

## Exact frozen dataset reconstruction

Phase 4 adds:

```text
scripts/reconstruct_frozen_dataset.py
```

The normal Phase-3 ingestion command records a fresh instrument-metadata observation time. That is correct for a new ingestion event but would produce a new dataset identity.

The reconstruction command instead consumes the committed frozen manifest and:

1. reuses the exact instrument metadata snapshot;
2. fetches the declared archive dates;
3. requires identical raw provider SHA-256 values;
4. repeats provider REST verification;
5. rebuilds canonical H1/D1;
6. requires dataset version `ee1300f0da50e4debcbbc3b7`;
7. requires manifest SHA-256 `eaf828ee3acc8adf9e3b931cc6a55d385b0be61b58ae72f01205b3f6034a2141`;
8. creates a new acquisition receipt for the current retrieval event.

This preserves the Phase-3 distinction between canonical dataset identity and acquisition-event identity.

## Provider-backed detector proof

The Phase-4 external detector smoke successfully reconstructed the exact frozen dataset from current provider bytes and passed it through the detector.

```text
workflow        Detector Smoke
workflow run    31667680273
job             94345649883
conclusion      SUCCESS
receipt SHA     4554c8e30828a4283c9f28ed78b40829ddd1142f5ad382ddcb551034e92b974a
detector run SHA26820611750f54736a0caf8755a293f744915e2fd3e241e8247aaef3a723f866
```

Detector output:

```json
{
  "candidate_count": 0,
  "dataset_version": "ee1300f0da50e4debcbbc3b7",
  "detector_version": "CRT-DETECTOR-v0.1",
  "manifest_sha256": "eaf828ee3acc8adf9e3b931cc6a55d385b0be61b58ae72f01205b3f6034a2141",
  "no_signal_count": 0,
  "run_sha256": "26820611750f54736a0caf8755a293f744915e2fd3e241e8247aaef3a723f866",
  "status": "INSUFFICIENT_D1_HISTORY",
  "strategy_version": "CRT-C3-D1-H1-M1-BEAR-v0.1",
  "symbol": "BTCUSDT",
  "trade_plan_count": 0
}
```

This is the correct outcome because the compact frozen Phase-3 dataset contains one complete New-York D1 candle. Three D1 candles are the minimum required to form C1/C2/C3.

`INSUFFICIENT_D1_HISTORY` is intentionally distinct from `NO_SIGNAL`.

## Detector audit record

Every evaluated rolling candidate includes:

```text
candidate_id
strategy_version
detector_version
dataset_version
manifest_sha256
provider
venue
symbol
C1/C2/C3 timestamps
H1 observation count
state
reason
rule_trace
evidence_ids
causal_input_sha256
TradePlan | null
```

This is the stable handoff object for Phase 5 simulation and future journaling.

## Deterministic identities

### Candidate ID

Derived from:

```text
strategy version
+ dataset version
+ C1 open
+ C2 open
+ C3 open
```

### Causal input SHA

Derived from information legitimately visible to the strategy:

```text
completed C1
completed C2
C3 open/calendar gate
completed in-window H1 observations
```

C3 final D1 price state is excluded.

### Run SHA

Derived from:

```text
strategy version
detector version
dataset version
manifest SHA
candidate IDs
causal-input SHAs
states
reason codes
```

## Explicit limitations carried into Phase 5

1. The current real trusted integration fixture contains only one D1, so it proves data/detector integration but cannot exercise a real rolling candidate.
2. The Phase-2 fixtures currently provide the positive/negative semantic examples for a complete C1/C2/C3 path.
3. Meaningful backtesting requires a larger separately versioned trusted historical dataset; do not reinterpret the compact integration fixture as the validation sample.
4. The first provider route is BTCUSDT Spot only.
5. The current source lacks historical bid/ask spread; Phase 5 must model execution friction explicitly and conservatively.
6. A future backtest can expose implementation defects, but poor P&L cannot be used to mutate `CRT-DETECTOR-v0.1` in place.
7. A corrected detector that materially changes output requires a new detector version and revalidation.

## Phase-5 boundary

Phase 5 may consume:

```text
DetectorCandidate
TradePlan
strategy version
detector version
dataset version
causal hashes
reason codes
```

Phase 5 may add:

- event clock;
- account/portfolio state;
- order intents;
- simulated fills;
- spread/commission/slippage;
- stop/target sequencing;
- position sizing under explicit research assumptions;
- trade/result journal;
- performance metrics.

Phase 5 may **not** silently change detector validity because an equity curve is unattractive.

## Final Phase-4 decision

**COMPLETE.**

The deterministic detector is ready for cost-aware backtest integration under a frozen versioned handoff.

This does not authorize real trading and does not represent a profitability claim.
