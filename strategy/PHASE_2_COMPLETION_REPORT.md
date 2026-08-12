# Phase 2 Completion Report — Formal CRT Specification & Freeze

**Project:** `romeo-crt-engine`  
**Date:** 2026-08-12  
**Phase:** 2 — Formal CRT specification  
**Status:** **COMPLETE**  
**Frozen candidate:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Lifecycle:** **FROZEN_FOR_VALIDATION**  
**Live trading:** **NOT AUTHORIZED**

## Completion decision

Phase 2 is complete.

The project now has a deterministic, machine-readable and test-backed first CRT candidate whose active path contains no intentionally vague strategy-critical term.

This completion decision follows the Project Bible's Phase-2 rule: unresolved material must either be excluded or explicitly parameterized before candidate freeze. The project did not use profitability results to choose missing semantics.

## Exit criteria

| Exit criterion | Result |
|---|---|
| Narrow first strategy scope selected | PASS |
| Parent candidate generation deterministic | PASS |
| Calendar deterministic for selected route | PASS |
| Direction/context deterministic for selected route | PASS |
| Key-level role deterministic | PASS |
| Manipulation / Turtle-Soup subtype deterministic | PASS |
| One entry family deterministic | PASS — Model #1 core |
| Target deterministic and immutable pre-trade | PASS |
| Structural stop + buffer deterministic | PASS |
| Candle-3 confirmation/expiry deterministic | PASS |
| Unknown/invalid state fails closed | PASS |
| Strategy/risk boundary preserved | PASS |
| Positive fixture exists | PASS |
| Negative fixtures exist for active rejection paths | PASS |
| Machine-readable fixture corpus exists | PASS |
| Causality / future-confirmation regression exists | PASS |
| Strategy freeze manifest exists | PASS |
| Independent/adversarial freeze review recorded | PASS |
| Active path has no `UNRESOLVED` placeholder | PASS |
| Broader unresolved doctrine is explicitly deferred/versioned | PASS |
| Profitability established | **NO — not a Phase-2 exit condition** |
| Paper/live authorization | **NO — prohibited at this phase** |

## Frozen strategy

```text
CRT-C3-D1-H1-M1-BEAR-v0.1
```

### Active rule flow

```text
CANONICAL NY DAILY DATA
        ↓
ENUMERATE CONSECUTIVE C1/C2 PAIRS
        ↓
C2 STRICTLY SWEEPS C1 HIGH ONLY
        ↓
C2 CLOSES BACK INSIDE C1 RANGE
        ↓
C1 MIDPOINT TARGET STILL PENDING
        ↓
C2 CLOSES → C3 OPENS
        ↓
SCAN COMPLETED H1 CANDLES
        ↓
MODEL-1-CORE UP-CLOSE OLD-HIGH SWEEP
        ↓
LATER H1 CLOSE CONFIRMS BELOW MODEL/REFERENCE
        ↓
BUILD IMMUTABLE TRADE PLAN
        ↓
INDEPENDENT RISK ENGINE
```

The strategy itself stops at `TradePlan`.

## Scope reduction used to remove unresolved active terms

Phase 2 did **not** attempt to make the entire public CRT doctrine executable at once.

The following were removed from the first candidate:

- bullish symmetry;
- H4/W1 parent routes;
- universal W1/D1/H4 bias resolver;
- general key-level ranking;
- true MSS;
- KOD;
- SMT substitution;
- generic BOS/MSS;
- FVG/OTE requirements;
- Candle-2 trading;
- countertrend trading;
- time exits;
- adaptive/retracement heuristics;
- ML-based validity overrides.

This is a deliberate anti-overfitting and evidence-integrity decision.

## Explicit project parameters

Two source-adjacent semantics required a numeric engineering formalization:

### `P2-PARAM-M1-THICK-050`

```text
Model-1 body fraction >= 0.50 of full candle range
```

Romeo's public evidence uses the qualitative term `thick`; `0.50` is the project's frozen interpretation for v0.1, not a claimed Romeo numerical threshold.

### `P2-PARAM-STOP-1TICK`

```text
execution stop = structural Model-1 high + one instrument tick
```

The structural high is strategy logic; one tick is explicit execution tolerance.

Both values were frozen before profitability testing and must be included in later sensitivity analysis.

## Machine artifacts

### Strategy specification

- `strategy/CRT_V0.1_SPEC.md`

### Freeze manifest

- `strategy/CRT_V0.1_FREEZE_MANIFEST.json`

### Deterministic contracts

- `src/romeo_crt_engine/crt/v0_1.py`

### Fixtures

- `tests/strategy/fixtures/crt_v0_1_cases.json`
- `tests/strategy/test_crt_v0_1_fixtures.py`
- `tests/unit/test_crt_v0_1_contracts.py`

### Governance

- `docs/adr/ADR-004-freeze-narrow-d1-h1-model1-subset.md`
- `strategy/reviews/CRT_V0.1_FREEZE_REVIEW.md`
- `research/romeo/OPEN_QUESTIONS.md`

## Causality controls frozen in Phase 2

The candidate explicitly prevents:

- selecting Candle 1 because a later setup won;
- observing the final C2 close before it exists;
- using final C3 high/low/close at C3 open;
- using an H1 Model #1 before the model candle closes;
- using confirmation before the confirming candle closes;
- backdating a confirmation that occurs after C3 expiry;
- changing the target after seeing outcome;
- keeping a consumed 50% premise active;
- turning ambiguous/damaged data into a signal.

## Validation risks carried forward deliberately

Phase 2 freeze is not a claim that the chosen subset has edge.

Important validation risks include:

1. the narrow candidate may be too restrictive;
2. omitting Romeo's broader HTF/context logic may reduce performance;
3. bearish-only results are not symmetric evidence;
4. the 0.50 body threshold may be unstable;
5. the one-tick execution buffer may be inappropriate for some instruments;
6. overlapping rolling parent candidates may produce correlated simultaneous setups;
7. a position can remain open beyond C3 because no unsupported time exit is invented.

These risks must be measured, not repaired retrospectively after final OOS results.

## Promotion decision

Approved lifecycle transition:

```text
CRT-C3-D1-H1-M1-BEAR-v0.1
RESEARCH -> FROZEN_FOR_VALIDATION
```

Not approved:

```text
PAPER
SHADOW
LIVE_CANARY
LIVE_APPROVED
```

No capital deployment is authorized by this report.

## Handoff to Phase 3

Phase 3 should now build the trusted market-data layer required to evaluate the frozen strategy without changing it:

- raw immutable observations;
- normalized instrument metadata;
- canonical New-York D1/H1 construction;
- DST handling;
- missing/duplicate/stale data rejection;
- dataset versioning;
- provider/canonical-boundary verification.

Once trusted data exists, Phase 4 can reproduce this frozen candidate over real historical observations and source-derived fixtures.
