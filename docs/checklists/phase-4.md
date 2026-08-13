# Phase 4 Checklist — CRT Detection Engine

Canonical phase definition: [PROJECT_BIBLE.md](../../PROJECT_BIBLE.md).

**Status:** COMPLETE for `CRT-DETECTOR-v0.1` after deterministic CI, frozen-fixture parity, causality tests and provider-backed trusted-data integration.

## Entry gate

- [x] Phase 0 engineering foundation complete
- [x] Phase 1 Romeo corpus/reconciliation complete
- [x] Phase 2 strategy `CRT-C3-D1-H1-M1-BEAR-v0.1` frozen
- [x] Phase 3 trusted market-data route complete
- [x] Frozen Phase-4 dataset identity available: `ee1300f0da50e4debcbbc3b7`
- [x] Paper/shadow/live trading remain unauthorized

## Architecture boundary

- [x] Detector wraps the frozen `v0_1.py` strategy rather than duplicating its predicates
- [x] No P&L/fill/account simulation in detector
- [x] No position sizing or independent-risk authority in detector
- [x] No broker/order path in detector
- [x] No LLM/ML judgement in strategy-validity path
- [x] Strategy parameters remain unchanged

## Trusted dataset input

- [x] Require `PHASE3_DATASET_MANIFEST_V1`
- [x] Require `TRUSTED` quality status
- [x] Validate provider/venue/symbol identity
- [x] Validate tick size
- [x] Validate manifest H1/D1 row counts
- [x] Validate strict canonical ordering/uniqueness
- [x] Recompute normalized H1/D1 digest before detector evaluation
- [x] Reject content that does not reproduce the trusted manifest digest
- [x] Provide exact frozen-dataset reconstruction path using committed metadata snapshot
- [x] Require raw provider SHA-256 equality during frozen reconstruction
- [x] Repeat provider REST cross-checks during reconstruction

## Canonical adaptation / causality

- [x] Convert completed canonical D1 C1/C2 into frozen `ClosedCandle` inputs
- [x] Build C3 gate from open time, calendar close boundary and open price only
- [x] Do not pass final C3 D1 high/low/close into strategy evaluation
- [x] Select only completed H1 observations fully inside C3
- [x] Preserve chronological H1 evaluation
- [x] Regression-test extreme mutation of future C3 D1 high/low/close
- [x] Require identical decision/TradePlan/causal hash after future-C3 mutation

## Candidate enumeration

- [x] Exhaustively evaluate every rolling C1/C2/C3 triple
- [x] Allow overlapping parent instances as frozen by Phase 2
- [x] Never select the historical parent based on later success
- [x] Stable candidate ID includes strategy/data identity and C1/C2/C3 timestamps
- [x] Fewer than three D1 bars returns explicit `INSUFFICIENT_D1_HISTORY`
- [x] Insufficient history is not mislabeled `NO_SIGNAL`

## Explanation / audit contract

- [x] Emit strategy version
- [x] Emit detector version
- [x] Emit dataset version and manifest SHA-256
- [x] Emit provider/venue/symbol
- [x] Emit C1/C2/C3 timestamps
- [x] Emit H1 observation count
- [x] Preserve frozen state and reason code
- [x] Attach relevant strategy rule trace
- [x] Attach evidence IDs
- [x] Compute causal-input SHA-256
- [x] Preserve immutable `TradePlan` when eligible
- [x] Compute deterministic detector-run SHA-256

## Frozen fixture parity

- [x] Route all seven Phase-2 machine fixtures through canonical `CanonicalBar` inputs
- [x] Reproduce one expected `TRADE_PLAN`
- [x] Reproduce six expected `NO_SIGNAL` cases
- [x] Preserve exact expected reason code for each fixture
- [x] Preserve entry = `106.0` for positive fixture
- [x] Preserve stop = `113.25` for positive fixture
- [x] Preserve target = `100.0` for positive fixture

## Provider-backed integration

- [x] Reconstruct exact frozen dataset `ee1300f0da50e4debcbbc3b7`
- [x] Reproduce frozen canonical manifest SHA-256
- [x] Load the reconstructed canonical H1/D1 through detector trust gates
- [x] Require expected result `INSUFFICIENT_D1_HISTORY`
- [x] Require zero candidates and zero TradePlans
- [x] Record external integration run evidence
- [x] Record detector run SHA-256 `26820611750f54736a0caf8755a293f744915e2fd3e241e8247aaef3a723f866`

Provider-backed evidence:

```text
Detector Smoke run  31667680273
Job                94345649883
Result             SUCCESS
Receipt SHA        4554c8e30828a4283c9f28ed78b40829ddd1142f5ad382ddcb551034e92b974a
Detector run SHA   26820611750f54736a0caf8755a293f744915e2fd3e241e8247aaef3a723f866
```

## Quality gates

- [x] Locked Python environment installs successfully
- [x] Ruff passes
- [x] Strict MyPy passes
- [x] Full pytest suite passes
- [x] Causality/future-C3 regression passes
- [x] Manifest-content mismatch regression passes
- [x] Independent Phase-4 gate review complete
- [x] Detector contract documented
- [x] Machine-readable detector freeze manifest committed

## Exit gate

- [x] Frozen strategy fixtures reproduce through detector boundary
- [x] Trusted canonical-data gate is deterministic and fail-closed
- [x] C3 future-price leakage is regression-tested
- [x] Exact frozen provider dataset reconstruction and detector integration pass
- [x] Candidate/rejection explanation contract exists
- [x] Detector version frozen for Phase-5 integration
- [x] Profitability claims remain explicitly prohibited
- [x] Paper/shadow/live authorization remains false

## Phase-5 handoff

Frozen integration triple:

```text
strategy  CRT-C3-D1-H1-M1-BEAR-v0.1
detector  CRT-DETECTOR-v0.1
dataset   ee1300f0da50e4debcbbc3b7
```

The dataset above remains a compact detector-integration fixture. Phase 5 must introduce a larger, separately versioned trusted historical sample before meaningful simulation statistics can be interpreted.

Backtest outcomes may expose implementation defects, but they may not be used to rewrite this frozen detector in place merely to improve P&L.
