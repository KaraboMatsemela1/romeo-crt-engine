# P0 Scope-Reduction Options

**Candidate:** `CRT-C3-ALIGNED-v0.1-DRAFT`  
**Status:** DECISION SUPPORT ONLY / NO STRATEGY FREEZE  
**Date:** 2026-08-12

## Why this document exists

The public textual corpus has narrowed all P0 blockers but has not fully closed them. Continuing to search indefinitely risks research drift.

This document defines safe ways to reduce v0.1 scope **without claiming unresolved Romeo doctrine is false**.

## Option A — D1-only parent candidate

Temporarily exclude H4 and W1 parent trades from the first executable research candidate.

Why it helps:
- D1 open is high-confidence at New York midnight;
- avoids unresolved H4 clock semantics;
- limits parent ownership conflicts;
- simplifies Candle-1/2/3 fixture construction.

Still blocked by:
- exact Candle-1 selector;
- key-level selector;
- direction resolver;
- Turtle Soup confirmation;
- entry model.

This does NOT solve P0, but it removes one major calendar ambiguity.

## Option B — bearish-only `OLD_CRTH` reaction candidate

Temporarily research only the explicit source-backed bearish subtype:

```text
bearish context
→ candle opens
→ stabs old CRTH
→ dumps / confirmation
```

Why it helps:
- avoids inventing bullish symmetry;
- creates a clean one-sided fixture family;
- gives a concrete reference subtype.

Still blocked by:
- definition of `old`;
- owning timeframe;
- exact confirmation;
- key-level relationship;
- entry model.

## Option C — reaction-from-key-level only

Already recommended in prior reconciliation.

Why it helps:
- Episode 5 provides an explicit negative fixture class: convincing LTF reversal before true level must be rejected;
- avoids the less-defined journey-to-level entry path.

Still blocked by:
- exact eligible level subtype;
- reach predicate;
- timing qualification.

## Option D — one entry family only

After P0 closes enough, choose either:

```text
MODEL_1
```

or

```text
TRUE_MSS
```

for v0.1, not both.

This prevents entry-family blending during the first confirmatory validation.

## Recommended narrow research profile

If manual visual evidence cannot close the remaining public-source gaps quickly, the safest first candidate boundary is:

```text
PARENT: D1 only
SETUP ROLE: reaction from key level only
DIRECTION: aligned only
SIDE: bearish-only research initially if OLD_CRTH is the only source-backed reference subtype
MANIPULATION: local Turtle Soup required
SMT SUBSTITUTION: disabled
KOD: excluded
ENTRY: one family only, selected after direct evidence
TIME EXIT: excluded until defined
```

This is not a production strategy. It is the narrowest candidate likely to make the remaining questions testable without silently inventing broad doctrine.

## Prohibited use of scope reduction

Do not select a scope because it has the best historical PnL.

Scope may be reduced only because:
- evidence is stronger;
- causality is cleaner;
- ambiguity is lower;
- testing is more reproducible.

## Decision gate

Before any reduced-scope candidate is coded as an executable strategy, every remaining active-path predicate still needs a deterministic definition and fixtures.

Scope reduction decreases the blocker surface; it does not waive the blocker standard.