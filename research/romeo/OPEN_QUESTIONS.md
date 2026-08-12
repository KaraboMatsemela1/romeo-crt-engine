# Open Strategy Questions — Post-Phase-2 Evidence-Debt Ledger

**Updated:** 2026-08-12  
**Phase 1:** COMPLETE  
**Phase 2:** COMPLETE  
**Frozen strategy:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Lifecycle:** `FROZEN_FOR_VALIDATION`

## Purpose

The first executable strategy candidate no longer contains an unresolved active-path term. This ledger therefore tracks **future strategy expansion and validation debts**, not blockers that may silently default inside v0.1.

Anything still unresolved here is either:

- `DEFERRED` — intentionally outside v0.1;
- `VERSIONED` — belongs to a later strategy/doctrine version; or
- `VALIDATION` — a frozen parameter/assumption that must be stress-tested without rewriting v0.1 in place.

The governing rule remains:

```text
required state missing/unknown/ambiguous -> NO_SIGNAL
```

---

# Closed for `CRT-C3-D1-H1-M1-BEAR-v0.1`

| Former debt | v0.1 disposition | Closure mechanism |
|---|---|---|
| Parent CRT / Candle-1 selector | CLOSED FOR V0.1 | enumerate every consecutive canonical D1 C1/C2 pair; no hindsight ranking |
| Parent lifecycle | CLOSED FOR V0.1 | one C1/C2/C3 three-candle instance; new-entry eligibility expires at C3 close |
| Key-level selector | CLOSED FOR V0.1 | reaction level fixed to selected C1 `CRTH` |
| Calendar | CLOSED FOR SELECTED ROUTE | D1 = NY midnight to next NY midnight; H1 execution; H4/W1 parent routes excluded |
| Broad Turtle Soup confirmation | CLOSED AS NARROW SUBTYPE | strict C1-high sweep + no C1-low sweep + C2 close reclaim |
| Broad HTF direction resolver | REMOVED FROM ACTIVE PATH | completed bearish D1 parent CRT is v0.1 execution context; multi-HTF bias resolver deferred |
| First entry family | CLOSED | Model #1 core selected; true MSS excluded |
| `thick` Model #1 adjective | EXPLICIT PARAMETER | `body/full_range >= 0.50`, parameter `P2-PARAM-M1-THICK-050` |
| Target hierarchy | CLOSED FOR V0.1 | one primary target = C1 midpoint / 50% |
| Structural stop | CLOSED | Model-1-core high |
| Stop execution buffer | EXPLICIT PARAMETER | one instrument tick, parameter `P2-PARAM-STOP-1TICK` |
| Candle-3 confirmation | CLOSED | later completed H1 close below the frozen confirmation reference |
| Candle-3 expiry | CLOSED | no new entry after C3 close |
| Target consumption | CLOSED CONSERVATIVELY | any C2 midpoint touch rejects; C3 midpoint touch before entry rejects |
| Unknown-state behavior | CLOSED | `NO_SIGNAL` |
| Risk boundary | CLOSED ARCHITECTURALLY | immutable `TradePlan -> independent Risk Engine` |

These decisions are specified in:

- `strategy/CRT_V0.1_SPEC.md`
- `strategy/CRT_V0.1_FREEZE_MANIFEST.json`
- `docs/adr/ADR-004-freeze-narrow-d1-h1-model1-subset.md`
- `strategy/reviews/CRT_V0.1_FREEZE_REVIEW.md`

---

# VALIDATION — frozen assumptions that must be attacked, not silently tuned

## V-01 — Model #1 body threshold

Frozen v0.1:

```text
body / full_range >= 0.50
```

This is a project formalization of Romeo's qualitative `thick` adjective, not a claimed Romeo numerical rule.

Later validation must:

- report sensitivity around the threshold;
- avoid choosing the final threshold against final OOS results;
- preserve v0.1 results even if a later candidate changes it.

A material change creates a new candidate/version.

## V-02 — Stop buffer

Frozen v0.1:

```text
stop = Model-1-core high + 1 instrument tick
```

The structural reference is source-derived; one tick is a project execution parameter.

Later validation must separate:

- source-defined structural invalidation;
- instrument tick size;
- spread/slippage;
- any additional execution tolerance.

## V-03 — Conservative midpoint-consumption rule

v0.1 rejects any C2 that touches the C1 midpoint because D1 OHLC cannot reveal intrabar ordering by itself.

Phase 3/4 may reconstruct finer chronology from trusted H1/lower data, but changing the qualification rule requires a later strategy version rather than silently altering v0.1.

## V-04 — Bearish-only representativeness

v0.1 is deliberately bearish-only. Validation results cannot be generalized to bullish CRT setups.

---

# DEFERRED — future strategy variants

## Bullish mirror

Open questions include:

- direct source verification of `old CRTL` as the bullish mirror of old CRTH;
- bullish Model #1 geometry;
- bullish stop/target symmetry;
- whether the same project parameterization is appropriate.

Do not add the mirror to v0.1 merely by code symmetry.

## H4 parent route

Still unresolved for future versions:

- exact Romeo H4 clock anchors;
- asset/venue-specific timing semantics;
- provider-native equivalence;
- maintenance/holiday handling.

v0.1 avoids this debt by using D1 only.

## W1 parent route

The Sunday 17:00 New-York reference is evidence-backed, but W1 execution mapping and venue handling still require a separately versioned implementation/fixture pass.

## Broad market/context direction

Future full-doctrine work must still determine:

- exact bullish/bearish/neutral predicate outside the narrow completed D1 parent state;
- timeframe ownership;
- W1/D1/H4 conflict resolution;
- bias-transition semantics;
- exact relation between market direction and parent CRT direction.

No moving-average, voting or hindsight resolver may be introduced as a shortcut.

## General key-level registry

v0.1 fixes the key level to C1 CRTH. Future setup families must still define:

- eligible price/time key-level types;
- ranking;
- reached/consumed/invalid lifecycle;
- tolerance;
- destination vs reaction-origin state transitions.

## Full Turtle Soup family

v0.1 implements one conservative bearish close-reclaim subtype. Future work may resolve:

- old-high/old-low taxonomy beyond C1 CRTH;
- freshness and reuse;
- same-candle vs later-candle failure confirmation;
- timeout;
- true-breakout invalidation;
- other source-demonstrated variants.

## True MSS

Deferred until a deterministic Romeo-specific structural definition exists for:

- swing construction;
- reference high/low;
- wick versus close break;
- entry region;
- relationship to Turtle Soup/SMT/FVG.

Generic BOS/MSS remains prohibited as a substitute.

## SMT

v0.1:

```text
allow_smt_substitution = False
SMTEvent -> OrderIntent = prohibited
```

Future version must resolve pair registry/polarity, corresponding extremes, synchronization, stale-data behavior and traded-instrument selection.

## Kiss of Death

Deferred until an ex-ante classifier exists.

Never define a historical signal as:

```text
last_turtle_soup_before_target
```

using future target knowledge.

## FVG / OTE

Neither is an active requirement in v0.1. A later confluence/entry variant requires its own evidence, parameters and validation.

## Candle-2 trading

Deferred until the simpler Candle-3 candidate has completed validation.

## Time exits

No source-backed deterministic time exit is active in v0.1. Do not invent one to make historical positions convenient to close.

## Journey-to-key-level trading

v0.1 is reaction-from-CRTH only. Journey-to-level entries/targets require a later separately measured variant.

## Countertrend CRT

Excluded. Any countertrend candidate must be separately specified and validated.

---

# VERSIONED doctrine evolution

Preserve doctrine snapshots:

```text
CRT_FOUNDATION_2024
CRT_SECRETS_2025
CRTOLOGY_2026
```

The frozen candidate uses:

```text
CRT_SECRETS_2025
```

Later Romeo material may motivate a new candidate, but it may not silently rewrite historical v0.1 semantics.

---

# Information-set safety — resolved engineering invariants

These remain mandatory across every future version:

- no final higher-timeframe OHLC before close;
- no future swing/reference points;
- no hindsight parent/key-level selection;
- no retrospective KOD;
- no target chosen after outcome;
- no final Candle-3 state at Candle-3 open;
- no post-expiry confirmation backdated into an earlier entry;
- synchronized causal timestamps for cross-market data;
- stale/missing required data => `UNKNOWN` / fail closed;
- provider candle-boundary mismatch is an error;
- strategy decisions retain strategy/rule/evidence/data-version provenance.

---

# Current gate

There are **no open evidence-debt placeholders on the `CRT-C3-D1-H1-M1-BEAR-v0.1` order path**.

The next project work is not to reinterpret v0.1. It is to build trusted market data and deterministic detection around the frozen candidate, then validate or reject it honestly.
