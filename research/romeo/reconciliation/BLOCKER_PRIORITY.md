# Blocker Priority — Phase 1 Reconciliation

**Candidate:** `CRT-C3-ALIGNED-v0.1-DRAFT`  
**Status:** STRATEGY FREEZE BLOCKED  
**Date:** 2026-08-12

## Priority policy

- `P0` — blocks any credible deterministic backtest of the first candidate
- `P1` — blocks faithful entry/exit/risk implementation but can be isolated after P0 context exists
- `P2` — advanced/setup-expansion blocker; can be explicitly excluded from v0.1
- `P3` — research enhancement; does not block first narrow candidate

A blocker is closed only when its acceptance criteria are met from direct evidence or an explicit scope exclusion is recorded.

## P0 — blocks first deterministic strategy candidate

### P0-01 — Parent CRT / Candle-1 selector

**Problem:** The engine does not yet have a causal algorithm that selects the parent CRT/range without hindsight.

**Why critical:** Every downstream object—direction, midpoint, Candle 2/3, target state, Turtle Soup and entry—depends on the correct parent.

**Required evidence:**
- direct source examples showing what candle is selected and why
- positive and negative examples
- handling of inside/nested/overlapping candles
- exact moment selection becomes knowable

**Acceptance criteria:**
- deterministic inputs/outputs documented
- no future candle data
- at least 5 positive + 5 negative annotated fixtures
- unit-test cases for ambiguous overlaps

**Likely source targets:** 2024 CRT foundation, Episode 1, Episode 4, Episode 7, live tape-reading.

---

### P0-02 — KeyLevelSelector and ranking

**Problem:** Key level is repeatedly first-order context, but exact level construction/ranking is not defined.

**Why critical:** Episodes 5/7/9/10 warn that convincing LTF signals away from the true key level can be traps.

**Required evidence:**
- eligible level types
- W1/D1/H4 priority/conflict rules
- price vs time key-level semantics
- reached/consumed/invalidated state
- tolerance around a level

**Acceptance criteria:**
- deterministic level registry
- ranking algorithm fixed before backtest
- no hindsight selection based on later reaction
- negative fixtures where an apparent LTF reversal is rejected before true key level

**Likely source targets:** Episodes 5, 7, 9, 10; live tape-reading.

---

### P0-03 — H4/D1/W1 candle construction

**Problem:** Candle anatomy depends on open/close time, but canonical timezone/session/DST anchors are unresolved.

**Why critical:** Different bar boundaries create different CRT candles, ranges, midpoints and phase labels.

**Required evidence:**
- canonical Daily open/close
- Weekly open/close
- H4 anchor sequence
- DST treatment
- instrument-class differences

**Acceptance criteria:**
- timezone-aware calendar spec
- reproducible bar builder
- tests around DST transitions
- provider bars cross-checked against canonical construction

**Likely source targets:** 2024 foundation timing examples, Episode 4, Episode 9, live tape-reading.

---

### P0-04 — Turtle Soup deterministic primitive

**Problem:** Structural concept is clear, but executable reference/confirmation rules are not.

**Required evidence:**
- qualifying old high/low criteria
- sweep condition
- close-back/failure requirement
- maximum/minimum event spacing
- consumed-reference logic

**Acceptance criteria:**
- causal `TurtleSoupEvent` predicate
- bullish and bearish definitions
- positive/negative fixtures
- no generic `sweep == trade` shortcut

**Likely source targets:** `What is turtle soup?`, 2024 CRT foundation, Episodes 2/7/9.

---

### P0-05 — Context direction algorithm

**Problem:** Directional alignment is high-confidence doctrine, but `context_direction` itself is not deterministic.

**Why critical:** v0.1 intends to reject countertrend setups and filter SMT direction using HTF context.

**Required evidence:**
- exact bullish/bearish/neutral selector
- which timeframe owns direction
- close vs wick logic
- conflict resolution across W1/D1/H4

**Acceptance criteria:**
- deterministic enum `BULLISH | BEARISH | NEUTRAL | UNKNOWN`
- no future HTF close usage
- conflict cases fail closed or follow a documented rule

**Likely source targets:** 2024 foundation, Episodes 3/7/8/9.

---

## P1 — blocks faithful entry and management

### P1-01 — Model #1 geometry

**Problem:** Specific-candle concept is cross-supported; exact geometry is missing.

**Need:**
- meaning of `thick`
- eligible wick/body shape
- old-high/old-low relation
- required close
- retrace zone/entry price
- bullish mirror
- FVG required vs optional

**Acceptance criteria:** exact algorithm + fixtures + no discretionary adjectives.

**Likely source targets:** Episodes 1 and 9, plus examples in 2/3.

---

### P1-02 — True MSS algorithm

**Problem:** Must not substitute generic BOS/MSS.

**Need:**
- swing construction
- exact reference high/low
- wick vs close break
- entry region after shift
- role of SMT/Turtle Soup/FVG

**Acceptance criteria:** deterministic state transition + annotated examples/counterexamples.

**Likely source targets:** Episodes 3, 5, 6, 9.

---

### P1-03 — Target hierarchy

**Problem:** 50%, opposite CRT extreme, prior day high/low and key levels all appear as targets in different narratives.

**Need:**
- setup-family-specific T1/T2 policy
- what makes 50% T1 versus entry/reaction context
- whether T2 exists after T1 and under what revalidation
- narrative target selected before entry

**Acceptance criteria:** immutable `TargetPlan` created before risk approval.

**Likely source targets:** Episodes 2, 7, 8, 9.

---

### P1-04 — Structural stop buffer

**Problem:** Structural reference is supported; exact executable buffer is not.

**Need:**
- bullish/bearish mirror
- tick/spread/price buffer policy
- whether buffer is source rule or execution policy

**Acceptance criteria:** separate `strategy_stop_reference` from `execution_buffer`; buffer frozen before validation.

**Likely source target:** Episode 9 + live examples.

---

### P1-05 — Candle-3 confirmation / entry timing

**Problem:** Candle 2 close gates eligibility, but exact event that turns eligible into confirmed remains dependent on entry model/context.

**Need:**
- whether entry can occur at C3 open or only after LTF confirmation
- required location relative to key level
- signal-expiry rule before parent candle closes

**Acceptance criteria:** explicit `C3_ELIGIBLE -> C3_ENTRY_CONFIRMED | C3_NO_SIGNAL` transitions.

---

## P2 — explicitly excludable from first v0.1

### P2-01 — SMT pair registry and polarity

**Recommendation:** Exclude SMT as a required entry path from first minimal v0.1 if necessary; keep it as recorded context until pair semantics are verified.

Need before activation:
- fixed instrument pairs/groups
- correlated/inverse semantics
- corresponding extreme definition
- synchronization window
- stale-data handling
- traded-instrument selection

Engineering stale-data/synchronized replay constraints remain mandatory even during research.

---

### P2-02 — SMT substitution for local Turtle Soup

**Recommendation:** `allow_smt_substitution=False` in the first narrow candidate.

Close only with direct evidence proving when cross-market behavior replaces local manipulation.

---

### P2-03 — KOD ex-ante classifier

**Recommendation:** Exclude KOD as a required setup label in v0.1.

Never implement `last_turtle_soup_before_target` retrospectively.

Need:
- parent-relative definition
- late-stage causal predicate
- 25%/OTE location semantics
- relation to 50% and key-level path

---

### P2-04 — Incomplete CRT predicate

**Recommendation:** fail closed on `UNKNOWN`; if parent CRT definition becomes strict enough, explicit incomplete filter may be deferred.

---

### P2-05 — Time-exit policy

**Recommendation:** First backtest may use only fully specified price exits if time exits remain unresolved. Do not infer a best historical exit time.

---

## P3 — later research enhancements

- draw-liquidity deterministic algorithm
- strong-trend/retracement-depth regime model
- countertrend CRT variant
- Candle-2 trading variant
- larger parent candles beyond `{H4,D1,W1}`
- optional FVG scoring/confluence model
- KOD specialized variant after base strategy works
- 2026 `CRTology` doctrine comparison

## Minimal executable candidate path

The fastest safe route to a deterministic research backtest is intentionally narrower than the full Romeo doctrine:

```text
1. Fix candle calendar / boundaries                  P0-03
2. Define parent CRT selector                        P0-01
3. Define key-level selector                         P0-02
4. Define HTF context direction                      P0-05
5. Define local Turtle Soup primitive                P0-04
6. Freeze Candle-2-close → Candle-3 eligibility      high-confidence gate
7. Implement ONE entry family first:
      a. Model #1                                    P1-01
      OR
      b. True MSS                                    P1-02
8. Define target plan                                P1-03
9. Define structural stop + execution buffer         P1-04
10. Define C3 confirmation/expiry                    P1-05
11. Backtest without SMT substitution/KOD/time exits
12. Add excluded features only as separately versioned experiments
```

## Recommended implementation order

### Sprint R1 — Source-verification blockers
- P0-03 candle anchors
- P0-01 parent CRT
- P0-02 key levels
- P0-05 direction
- P0-04 Turtle Soup

### Sprint R2 — Entry definition
- choose **one** of Model #1 or true MSS for the first executable candidate
- resolve its P1 blocker completely
- build positive/negative fixtures

### Sprint R3 — Risk/management semantics
- targets
- stop reference + buffer
- C3 expiry/no-signal

### Sprint R4 — Strategy-spec freeze review
- every executable predicate deterministic
- every rule linked to evidence
- contradiction matrix disposition recorded
- no unresolved input in the order path

## Freeze gate

`CRT-C3-ALIGNED-v0.1` may not move from `DRAFT` to `FROZEN_FOR_VALIDATION` while any active-path `P0` or selected-entry `P1` blocker remains open.
