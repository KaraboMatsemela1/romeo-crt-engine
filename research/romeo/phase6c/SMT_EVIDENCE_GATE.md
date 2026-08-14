# Phase 6C — SMT Semantics / Substitution Evidence Gate

**Date:** 2026-08-14  
**Primary doctrine sources:** `ROMEO-2025-S6`, `ROMEO-2025-S9`, first-party Romeo follow-up posts  
**Gate status:** **CLOSED — `TECHNICAL_SOURCE_CAPTURE_INSUFFICIENT` FOR EXECUTABLE SMT LOGIC**  
**Partial first-party closure:** **YES**  
**New alpha candidate selected:** **NO**

## Objective

Determine whether the project's deferred SMT branch can now be promoted into a deterministic Phase-6C strategy delta without using generic ICT conventions, third-party interpretations, or the Phase-6B sparse-activity result to fill missing rules.

The gate specifically tests:

- pair registry;
- take/non-take divergence semantics;
- inverse-pair polarity;
- cross-market synchronization;
- direction ownership;
- Model #1 / true-MSS confirmation interaction;
- local Turtle-Soup substitution;
- traded-instrument ownership;
- invalidation/expiry.

## Direct first-party evidence — closed facts

### 1. Basic SMT pair registry

Romeo directly published:

```text
SMT pairs (basic):
EU - DXY
NQ - ES
BTC - ETH
GOLD - SILVER
```

This closes the basic **research pair registry** for these four relationships.

It does not define signal polarity or execution.

### 2. SMT may fulfill a role when expected local Turtle Soup is absent

Romeo directly posted, in a live/example context, that traders expected a low to be Turtle-Souped but that this did not occur because SMT was playing its role exactly as taught in CRT Secrets Episode 6.

This is important evidence against the overly narrow assumption:

```text
valid manipulation always requires a local traded-instrument Turtle Soup
```

It supports the weaker source-backed statement:

```text
SMT can, in at least some Romeo setups, fulfill a manipulation/context role even when the expected local Turtle Soup does not print.
```

The post does **not** expose the deterministic condition that decides when substitution is valid.

### 3. Episode 9 is the intended first-party source for correct SMT use

Romeo directly advertised CRT Secrets Episode 9 as answering:

```text
How to use SMT correctly while trading
```

This confirms the intended source ownership and that SMT is not meant to be interpreted from pair divergence alone.

The accessible first-party public text does not reproduce the full Episode-9 rule set.

## Direct-source search performed

The gate searched:

1. Romeo official Telegram for SMT + high/low/take/non-take terms;
2. Romeo official Telegram for the basic pair registry;
3. Romeo official Telegram for SMT + Turtle Soup / Episode 6;
4. Romeo official Telegram for SMT + Model #1 / true MSS;
5. Romeo official Telegram for bullish/bearish SMT language;
6. Romeo official Telegram for higher-timeframe direction and manipulation terms;
7. Romeo X/Twitter indexing for SMT-specific posts;
8. exact Episode-6 and Episode-9 video IDs/titles in transcript/search indexes;
9. direct YouTube caption/timed-text retrieval attempts.

The original Episode-6/Episode-9 caption payload was not retrievable through the available research environment. No first-party indexed text closed the remaining strategy-critical semantics.

## Secondary discovery evidence — quarantined

Third-party transcript/summary indexes for Episodes 6 and 9 provide useful search hypotheses. They describe, among other things:

- one paired asset taking a corresponding high/low while the other does not;
- Model #1 and true MSS as confirmation families;
- special handling for inverse relationships;
- filtering SMT by higher-timeframe direction;
- using confirmation rather than blindly trading the divergence.

These claims are **DISCOVERY ONLY**.

They are not promoted because the project has not captured the original Romeo transcript/frame evidence needed to prove the exact wording, polarity, timing and ownership semantics.

The gate explicitly prohibits turning a third-party summary into the implementation specification.

## Partial evidence-debt closure

The following Phase-1/2 debt is now closed:

```text
BASIC_SMT_PAIR_REGISTRY = {
    EU_DXY,
    NQ_ES,
    BTC_ETH,
    GOLD_SILVER,
}
```

The following is source-supported but not deterministic:

```text
SMT_MAY_SUBSTITUTE_FOR_EXPECTED_LOCAL_TURTLE_SOUP_ROLE = true
```

No stronger machine rule is authorized.

## Strategy-critical fields still unresolved

### 1. Corresponding-extreme construction

Unknown:

- whether extrema must belong to the same named candle/session/window;
- whether timestamps must match exactly;
- whether nearest swing, parent CRT extreme, session high/low, or another object owns the comparison.

### 2. Positively correlated pair polarity

For pairs such as NQ/ES, BTC/ETH and Gold/Silver, the exact Romeo rule for:

```text
one takes high / other does not
one takes low / other does not
```

and which condition maps to bullish versus bearish expectation is not sufficiently direct-source captured.

### 3. Inverse-pair polarity

EU/DXY requires an explicitly source-defined inverse mapping. Generic inverse-correlation intuition is prohibited as a substitute.

### 4. Synchronization window

No first-party executable value is captured for:

- exact timestamp equality;
- same lower-timeframe candle;
- same session;
- allowed lag;
- stale-data cutoff.

### 5. Direction ownership

The project lacks a direct-source executable rule establishing which higher-timeframe object owns SMT direction and exactly when opposite SMT is ignored or invalidating.

### 6. Confirmation ownership

Model #1 and true MSS are source-associated with SMT in the broader corpus, but this gate does not have direct-source closure for:

- which paired instrument must confirm;
- whether confirmation is required on both;
- timeframe mapping;
- exact sequence after divergence.

### 7. Turtle-Soup substitution predicate

The direct example proves that substitution can occur. It does not specify:

```text
IF <exact SMT state> THEN local Turtle Soup may be omitted
```

without hindsight.

### 8. Traded-instrument selection

When two paired markets diverge, the direct evidence captured here does not define which instrument is eligible to trade and why.

### 9. Invalidation / expiry

No exact Romeo rule is captured for:

- divergence expiry;
- pair reconvergence;
- new high/low invalidation;
- context change;
- confirmation timeout.

## Fail-closed decision

Because unresolved fields lie directly on the signal path, the gate closes:

```text
TECHNICAL_SOURCE_CAPTURE_INSUFFICIENT
```

This is not a rejection of SMT. It is a rejection of inventing a precise algorithm from incomplete direct evidence.

The following are therefore prohibited:

```text
GENERIC_ICT_SMT_IMPLEMENTATION             = false
SMT_DIRECT_ENTRY                           = false
SMT_TURTLE_SOUP_SUBSTITUTION_IMPLEMENTED   = false
PHASE6C_NEW_ALPHA_CANDIDATE_SELECTED       = false
PHASE6C_ALPHA_IMPLEMENTATION_AUTHORIZED    = false
PHASE6C_DETECTOR_ACTIVITY_AUTHORIZED       = false
BACKTEST_AUTHORIZED                        = false
PNL_OUTCOME_ACCESS_AUTHORIZED              = false
```

## Re-entry condition

Reopen SMT only if direct evidence closes the missing semantics, for example:

- original Episode-6 or Episode-9 transcript/captions;
- first-party chart frames plus spoken/text explanation of the pair relationship;
- Romeo posts explicitly defining take/non-take polarity and confirmation ownership;
- a later CRTology source that explicitly restates SMT with causal rules.

Any future reopening must preserve this partial-closure/insufficient gate as historical evidence.

## Next Phase-6C branch

SMT cannot currently become the new alpha candidate.

The next evidence-led branch is **dynamic context / bias transition**, where direct first-party Romeo material already establishes that a convincing opposite CRT can justify changing bias and that strong trends should not be faded without warning signs. The gate must determine whether `convincing`, trend strength, slowdown and transition ownership can be specified deterministically without outcome-based fitting.
