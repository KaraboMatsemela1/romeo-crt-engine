# Pre-Phase-3 Gate Review

**Date:** 2026-08-12  
**Repository:** `KaraboMatsemela1/romeo-crt-engine`  
**Frozen strategy:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Review purpose:** verify Phases 0–2, frozen strategy implementation, governance and safety before starting the trusted market-data layer.

## Decision

Phase 3 may start **only after this review branch passes CI and is merged**.

The review found two strategy-implementation calendar defects and three engineering/governance gaps. All release-blocking findings were corrected on this branch without changing the already-frozen v0.1 trading semantics.

## Scope reviewed

- `PROJECT_BIBLE.md`
- `STATUS.md` and `README.md`
- `docs/ROADMAP.md`, phase checklists and ADRs
- `AGENTS.md` and live-trading safety boundary
- `strategy/CRT_V0.1_SPEC.md`
- `strategy/CRT_V0.1_FREEZE_MANIFEST.json`
- `strategy/PHASE_2_COMPLETION_REPORT.md`
- `strategy/reviews/CRT_V0.1_FREEZE_REVIEW.md`
- `research/romeo/OPEN_QUESTIONS.md`
- `src/romeo_crt_engine/crt/v0_1.py`
- strategy fixtures and unit tests
- CI workflow
- Phase-0 logging/storage/experiment foundation
- data-ignore/secrets conventions

## Release-blocking findings corrected

### GATE-001 — C3 D1 window duration was under-validated

**Severity:** High  
**Status:** FIXED

The frozen specification defines C3 as one New-York wall-clock Daily candle. The implementation previously checked only that C3 opened and closed at local midnight. A malformed two-day window could therefore satisfy the calendar check.

Correction:

```text
C3 D1 window = local midnight -> next local-date midnight exactly
```

The rule remains DST-aware: a valid D1 window may have 23, 24 or 25 elapsed hours while still spanning exactly one New-York local calendar day.

A negative regression test now rejects a multi-day C3 window.

### GATE-002 — H1 chronology was unsafe across DST transitions

**Severity:** High  
**Status:** FIXED

Python wall-clock comparison/subtraction of datetimes sharing the same `ZoneInfo` can misrepresent elapsed time at DST transitions. In particular:

- spring-forward `01:00 -> 03:00` is one elapsed hour even though wall-clock subtraction can appear as two;
- fall-back `01:00 fold=0 -> 01:00 fold=1` is one elapsed hour even though wall-clock comparison can treat the two local datetimes as equal.

Correction:

- ordering and elapsed-time checks use absolute timestamps;
- H1 validity requires exactly 3,600 elapsed seconds plus whole local-hour boundaries;
- H1 candle sorting uses absolute timestamps;
- instant-contiguity checks use absolute timestamps.

Regression tests cover both spring-forward and repeated fall-back H1 candles.

## Foundation gaps corrected

### GATE-003 — logging contract missing

**Severity:** Medium  
**Status:** FIXED

Phase 0 required logging but only documentation existed. Added a provider-neutral structured logging utility with a reserved immutable `event` field.

No external logging vendor is selected by this contract.

### GATE-004 — storage/integrity contract missing

**Severity:** Medium  
**Status:** FIXED

Added provider-neutral contracts for:

- immutable artifact references;
- SHA-256 integrity metadata;
- versioned dataset references;
- an `ArtifactStore` protocol.

Phase 3 may now implement local/object/database adapters without coupling strategy code to a storage vendor.

### GATE-005 — experiment provenance convention missing

**Severity:** Medium  
**Status:** FIXED

Added `experiments/README.md` defining immutable experiment IDs, strategy/data/git provenance, assumptions, artifacts and preservation of failed/inconclusive results.

## Strategy consistency review

### C1 CRTH versus C2 structural high

**Result:** CONSISTENT — NO CHANGE

This initially looked like a possible spec/runtime mismatch but ADR-004 confirms the roles are intentionally different:

1. `C1.high` is the parent CRT reaction level (`CRTH`).
2. C2 must sweep that C1 CRTH and close back inside C1.
3. After C2 closes, `C2.high` is a completed/pre-existing structural high for C3.
4. H1 Model #1 during C3 must sweep the C2 structural high.

The runtime follows that exact frozen flow. It must not be changed to use C1 high for the H1 Model #1 reference without a new strategy version.

### Model #1 confirmation

**Result:** CONSISTENT

The runtime confirmation threshold is:

```python
close < min(model1.low, C2.high)
```

Because a valid Model-1 core spans the C2 structural high, this implements the ADR requirement that the later close be below both the selected model-candle low and swept structural high.

### C3 target-consumption behavior

**Result:** CONSISTENT / CONSERVATIVE

Any completed H1 touching the C1 midpoint before entry terminates the candidate. This matches the frozen rule that the primary objective may not already have printed before the entry.

### Model invalidation

**Result:** CONSISTENT / CONSERVATIVE

A higher H1 high before confirmation invalidates the active Model #1. The same completed candle may become a new Model-1 candidate only if it independently satisfies the frozen predicate.

## Provenance review

The runtime uses shorthand evidence ID `P0-FIX-002`; the canonical fixture ID is `P0-FIX-002-BEARISH-OLD-CRTH-CLARIFICATION`.

The freeze manifest now contains an explicit alias mapping so journal evidence can resolve deterministically rather than relying on undocumented naming knowledge.

## Safety review

Confirmed:

```text
LIVE_TRADING_AUTHORIZED = false
paper_trading_authorized = false
profitability_claims_authorized = false
```

The v0.1 module emits an immutable strategy `TradePlan`; it does not size positions, call a broker or bypass the independent risk boundary.

No Phase-3 work is authorized to weaken this boundary.

## Phase-0 closure review

Phase 0 is now considered complete because the repository has:

- Python 3.12+ package metadata;
- CI with lint, strict typing and tests;
- safe secret/environment conventions;
- structured logging contract;
- storage/integrity contracts;
- docs + ADRs + AI-agent contract;
- experiment provenance convention;
- project check script;
- test coverage for the added foundation contracts.

Concrete database/object-store/provider implementations are intentionally Phase-3 work.

## Documentation cleanup

Corrected stale state in:

- `README.md`;
- Phase-0 checklist;
- Phase-1 checklist;
- Phase-2 checklist;
- Phase-3 checklist;
- `STATUS.md`;
- `PROJECT_BIBLE.md` current-state and next-action sections.

## CI/reproducibility hardening

GitHub Actions dependencies are pinned to the exact action commit revisions observed in the last successful CI baseline rather than floating only on `@v4` / `@v5` tags.

## Non-blocking technical debt

These do **not** block Phase 3, but they must remain visible:

### DEBT-001 — full dependency lock

`pyproject.toml` currently declares version ranges rather than a fully resolved lockfile. Phase 3 will add material data dependencies, so the project should choose one reproducible lock workflow (for example `uv.lock` or an equivalent fully resolved approach) before the first Phase-3 dataset is frozen.

**Deadline:** before freezing the first trusted dataset version.

### DEBT-002 — immutable Git strategy tag/release

The frozen strategy is currently identified by strategy version, freeze manifest and Git history/merge SHA. A dedicated immutable Git tag or release is desirable for validation provenance.

**Deadline:** before formal Phase-6 confirmatory/OOS validation.

### DEBT-003 — no concrete market-data provider yet

This is expected Phase-3 work, not a missed Phase-2 task. Provider selection must be explicit and must not redefine strategy candle semantics.

## Phase-3 entry constraints

Phase 3 must:

1. preserve raw provider provenance;
2. normalize internal timestamps to UTC;
3. construct analytical D1/H1 using frozen New-York semantics;
4. use absolute-time chronology through DST;
5. make instrument/venue/tick-size metadata explicit;
6. detect duplicates, gaps, stale/out-of-order data and impossible OHLC;
7. version every trusted dataset with a manifest digest;
8. create a new dataset version for corrections instead of silently mutating history;
9. keep provider-native bars untrusted until boundary equivalence is proven;
10. never modify frozen v0.1 strategy rules because a provider makes another interpretation easier.

## Final gate

The pre-Phase-3 decision is:

```text
Phases 0–2: COMPLETE
CRT-C3-D1-H1-M1-BEAR-v0.1: FROZEN_FOR_VALIDATION
Phase 3: READY TO START after review PR CI + merge
Paper/Shadow/Live: NOT AUTHORIZED
```
