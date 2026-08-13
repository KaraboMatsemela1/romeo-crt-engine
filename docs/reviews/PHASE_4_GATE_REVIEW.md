# Phase 4 Gate Review — CRT Detector

**Date:** 2026-08-13  
**Phase:** 4 — CRT detector  
**Strategy:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Detector:** `CRT-DETECTOR-v0.1`  
**Trusted integration dataset:** `ee1300f0da50e4debcbbc3b7`  
**Review decision:** **PASS WITH EXPLICIT PHASE-5 LIMITATIONS**

## Review objective

Determine whether the Phase-4 implementation faithfully connects trusted canonical market data to the frozen CRT v0.1 strategy without introducing hindsight, P&L-driven reinterpretation, hidden data drift, or execution/risk authority.

This review is intentionally adversarial. A green test suite alone is not enough if the architecture could still use future information or silently consume a different dataset.

## Reviewed artifacts

- `strategy/CRT_V0.1_SPEC.md`
- `strategy/CRT_V0.1_FREEZE_MANIFEST.json`
- `src/romeo_crt_engine/crt/v0_1.py`
- `src/romeo_crt_engine/crt/detector.py`
- `tests/strategy/fixtures/crt_v0_1_cases.json`
- `tests/strategy/test_crt_v0_1_fixtures.py`
- `tests/strategy/test_crt_detector_phase4.py`
- `docs/DETECTOR.md`
- `scripts/run_crt_detector.py`
- `scripts/reconstruct_frozen_dataset.py`
- frozen Phase-3 manifest/evidence records
- provider-backed Detector Smoke evidence

## Findings

### 1. Frozen strategy semantics were not moved into the detector

**PASS.**

The detector delegates strategy validity to `evaluate_bearish_c3` in the already-frozen `v0_1.py` rather than copying the sweep, reclaim, target, Model-1, confirmation, stop or target predicates.

This reduces the risk that Phase 4 develops a second subtly different CRT implementation.

### 2. Trusted dataset identity is enforced before evaluation

**PASS.**

The detector requires:

- `PHASE3_DATASET_MANIFEST_V1`;
- `TRUSTED` quality status;
- manifest row-count equality;
- provider/venue/symbol equality;
- strictly ordered/unique canonical bars;
- exact normalized H1/D1 digest reproduction.

A directory cannot become a detector input merely because its filenames look correct.

### 3. Frozen dataset can be reconstructed exactly

**PASS.**

The reconstruction command reuses the committed instrument metadata snapshot, requires the provider raw archive SHA-256 values to remain identical, repeats REST verification, and requires both the frozen dataset version and canonical manifest SHA-256 to reproduce exactly.

The current retrieval event receives a separate acquisition receipt rather than changing canonical dataset identity.

### 4. C3 final D1 price information is excluded from the decision path

**PASS.**

The detector creates the C3 strategy window from:

```text
C3 open_time
C3 close_time calendar boundary
C3 open price
```

It does not pass the final C3 D1 high, low or close to `evaluate_bearish_c3`.

A regression test mutates those three future D1 price fields to extreme values and requires the same state, reason, TradePlan geometry and causal-input SHA-256.

### 5. H1 execution is bounded to Candle 3

**PASS.**

Only completed canonical H1 candles whose entire interval is inside the C3 window are adapted into strategy execution observations.

The frozen strategy retains its own chronological/future-close validation as a second line of defense.

### 6. Parent selection is exhaustive rather than outcome-selected

**PASS.**

For `N` D1 bars, Phase 4 evaluates every rolling C1/C2/C3 triple. It does not search backward for the range that makes the later trade look best.

### 7. Phase-2 fixtures reproduce through the detector boundary

**PASS.**

All seven committed freeze cases are routed through canonical `CanonicalBar` objects and the new detector entry point.

Expected distribution:

```text
7 total cases
1 TRADE_PLAN
6 NO_SIGNAL
```

The detector must preserve each case's frozen reason code.

### 8. Candidate outputs are auditable

**PASS.**

Every evaluated candidate carries:

- strategy version;
- detector version;
- dataset version and manifest SHA;
- provider/venue/symbol;
- rolling parent timestamps;
- reason/state;
- rule trace;
- evidence IDs;
- causal-input SHA;
- immutable TradePlan when eligible.

### 9. Detector run identity is deterministic

**PASS.**

`run_sha256` is derived from declared strategy/detector/data identities plus candidate IDs, causal-input hashes, states and reasons.

No random seed or LLM output participates in detector validity.

### 10. The real frozen dataset result is interpreted correctly

**PASS.**

The Phase-3 detector-integration dataset contains:

```text
H1 rows = 48
D1 rows = 1
```

It therefore cannot produce even one C1/C2/C3 instance.

The correct result is:

```text
INSUFFICIENT_D1_HISTORY
candidate_count = 0
no_signal_count = 0
trade_plan_count = 0
```

It would be incorrect to call this `NO_SIGNAL`, a strategy loss, or evidence against/for profitability.

### 11. Provider-backed integration passed

**PASS.**

Detector Smoke:

```text
workflow run  31667680273
job           94345649883
result        SUCCESS
receipt SHA   4554c8e30828a4283c9f28ed78b40829ddd1142f5ad382ddcb551034e92b974a
run SHA       26820611750f54736a0caf8755a293f744915e2fd3e241e8247aaef3a723f866
```

The workflow reconstructed the exact frozen canonical manifest and executed the detector with required dataset/version hashes.

### 12. No backtest or execution authority was introduced

**PASS.**

The Phase-4 detector does not:

- model fills;
- compute returns/P&L;
- choose position size;
- model account balance;
- approve risk;
- send broker orders;
- use ML/LLM judgement for validity.

## Leakage/adversarial checklist

| Risk | Finding |
|---|---|
| Use C3 final D1 high/low/close | BLOCKED + regression tested |
| Use H1 after C3 close | BLOCKED by window filter and frozen evaluator |
| Pick successful parent retrospectively | BLOCKED by rolling enumeration |
| Use untrusted canonical files | BLOCKED by manifest/content verification |
| Change strategy based on real-data scarcity | NOT DONE |
| Treat insufficient history as no-signal | NOT DONE |
| Let detector compute P&L | NOT PRESENT |
| Let detector authorize risk/live order | NOT PRESENT |
| Let fresh metadata silently change frozen dataset | BLOCKED by exact reconstruction path |
| Hide negative fixture results | NOT DONE |

## Accepted limitations for Phase 5

1. The frozen Phase-3 integration dataset has only one complete D1 and cannot exercise a real C1/C2/C3 candidate.
2. Positive/negative strategy-path semantics are therefore currently demonstrated by the frozen synthetic fixtures, while the real dataset demonstrates trusted integration/reconstruction only.
3. Phase 5 or a later data expansion must create a larger **separately versioned trusted historical dataset** before meaningful trade-frequency or P&L conclusions can be made.
4. The first route remains BTCUSDT Spot; it does not establish behavior on Forex, index futures or metals.
5. The chosen archive route lacks historical bid/ask spread, so Phase 5 must define execution-cost data/assumptions explicitly rather than treating spot OHLC closes as frictionless fills.
6. A backtest may expose bugs. A proven implementation/spec mismatch may be corrected transparently, but disappointing P&L is not permission to alter the frozen detector in place.

## Gate decision

**PASS.**

Phase 4 has met the detector-integrity objective for `CRT-DETECTOR-v0.1` and may hand its immutable candidate/TradePlan outputs to Phase 5.

The handoff triple is:

```text
strategy  CRT-C3-D1-H1-M1-BEAR-v0.1
detector  CRT-DETECTOR-v0.1
dataset   ee1300f0da50e4debcbbc3b7  # compact integration fixture
```

This gate does **not** establish profitability and does not authorize paper, shadow or live trading.
