# Phase 6D — First-Party Artifact Recovery Pass 002

**Date:** 2026-08-14  
**Mode:** research/provenance only  
**Tracking:** Issue #24  
**Decision:** **RECOVERY_COMPLETE_NO_PREDICATE_CLOSURE**

## Objective

Recover original first-party Romeo payloads and exact source locators for claims that were previously preserved only as semantic Phase-6C research notes. Admit only replayable, SHA-256-bound first-party evidence into the Phase-6D corpus.

This pass does not create a strategy candidate, alter Phase 6B, run detector/count/P&L work, or open OOS/CONFIRM.

## Recovery result

```text
new direct first-party source records       15
acquisition manifests total                 21
captured manifests                          16
partial identity-only manifests              5
replayable corpus sources                   16
replayable corpus artifacts                 18
payload files independently verifiable      18
predicate rows                               8
predicate rows with artifact evidence        7
observed PARTIAL field evidence             17
CLOSING field evidence                       0
candidate_ready_rows                         0
```

The previously replayable `ROMEO-2026-TG-TIME-TS-6361` chain is preserved and augmented with one additional exact first-party excerpt. Fifteen additional first-party Telegram source identities were recovered with exact post URLs and payload bytes.

## Recovered provenance coverage

| Source ID | Exact locator | Evidence area | Ledger effect |
|---|---|---|---|
| `ROMEO-TG-MODEL1-6180` | `https://t.me/officialRomeotpt/6180` | Model #1 prioritization | `MODEL_1_GEOMETRY.EXACT_PREDICATE = PARTIAL` |
| `ROMEO-TG-TS-6219` | `https://t.me/officialRomeotpt/6219` | Turtle Soup entry example label | `TURTLE_SOUP_CONFIRMATION.EXACT_PREDICATE = PARTIAL` |
| `ROMEO-TG-TS-D1-6221` | `https://t.me/officialRomeotpt/6221` | example-specific D1 context | `TURTLE_SOUP_CONFIRMATION.DIRECTION_TIMEFRAME_OWNERSHIP = PARTIAL` |
| `ROMEO-TG-KEYLEVEL-6273` | `https://t.me/officialRomeotpt/6273` | journey vs reaction taxonomy | `KEY_LEVEL_SELECTOR.EXACT_PREDICATE = PARTIAL` |
| `ROMEO-TG-KEYLEVEL-6274` | `https://t.me/officialRomeotpt/6274` | Episode-5 ownership | context only |
| `ROMEO-TG-KEYTIME-6289` | `https://t.me/officialRomeotpt/6289` | five published clock times | `TIME_SELECTOR` partial coverage |
| `ROMEO-TG-KEYTIME-6290` | `https://t.me/officialRomeotpt/6290` | time synchronization guidance | `TIME_SELECTOR.EXACT_PREDICATE = PARTIAL` |
| `ROMEO-TG-BIAS-6357` | `https://t.me/officialRomeotpt/6357` | opposite-CRT bias change | `DYNAMIC_BIAS_TRANSITION` partial coverage |
| `ROMEO-TG-SMT-PAIRS-6363` | `https://t.me/officialRomeotpt/6363` | basic SMT pair registry | `SMT_EXECUTABLE_SEMANTICS.DATA_REQUIREMENTS = PARTIAL` |
| `ROMEO-TG-SMT-SUB-6520` | `https://t.me/officialRomeotpt/6520` | SMT role when expected local TS is absent | `SMT_EXECUTABLE_SEMANTICS.EXACT_PREDICATE = PARTIAL` |
| `ROMEO-TG-EP9-SCOPE-6536` | `https://t.me/officialRomeotpt/6536` | Episode-9 SMT source ownership | context only |
| `ROMEO-TG-CRTOLOGY01-6905` | `https://t.me/officialRomeotpt/6905` | exact CRTology Episode-1 video link | context/provenance only |
| `ROMEO-TG-SS-CONTEXT-6912` | `https://t.me/officialRomeotpt/6912` | organized application clue | `SS_MEANING_AND_CAUSAL_RULE.EXACT_PREDICATE = PARTIAL` |
| `ROMEO-TG-SS-NOFORCE-6914` | `https://t.me/officialRomeotpt/6914` | do-not-force absence principle | `SS_MEANING_AND_CAUSAL_RULE.CONFIRMATION = PARTIAL` |
| `ROMEO-TG-TREND-6915` | `https://t.me/officialRomeotpt/6915` | trend-change warning guidance | `DYNAMIC_BIAS_TRANSITION.CONFIRMATION = PARTIAL` |

## Payload-store hardening

Every corpus-admitted text artifact is now stored as:

```text
research/romeo/phase6d/payloads/<artifact_sha256>.txt
```

The migration audit independently verifies:

1. the payload file exists;
2. its bytes hash to the manifest artifact SHA-256;
3. its byte length matches the manifest;
4. the manifest hash matches its canonical representation;
5. the manifest source URL matches `SOURCE_REGISTRY.csv`;
6. the corpus index binds the manifest and artifact;
7. every ledger evidence SHA resolves to the correct corpus artifact.

A semantic research note is therefore insufficient by itself to enter the executable-evidence ledger.

## Predicate coverage after recovery

```text
SS_MEANING_AND_CAUSAL_RULE   PARTIAL / 0 satisfied fields
SMT_EXECUTABLE_SEMANTICS     PARTIAL / 0 satisfied fields
MODEL_1_GEOMETRY             PARTIAL / 0 satisfied fields
TRUE_MSS_ALGORITHM           UNRESOLVED / 0 satisfied fields
TURTLE_SOUP_CONFIRMATION     PARTIAL / 0 satisfied fields
KEY_LEVEL_SELECTOR           PARTIAL / 0 satisfied fields
TIME_SELECTOR                PARTIAL / 0 satisfied fields
DYNAMIC_BIAS_TRANSITION      PARTIAL / 0 satisfied fields
```

All recovered evidence is intentionally `PARTIAL`. No artifact independently defines an entire required causal field strongly enough to be classified `CLOSING`.

## Exhausted direct paths in this pass

Direct first-party YouTube watch/timed-text acquisition was attempted for:

- CRTology Episode 1 / SS;
- CRT Secrets Episode 6 / SMT;
- CRT Secrets Episode 9 / Connecting the Dots;
- the original Turtle Soup video.

The current research environment did not expose usable original captions/transcripts through those direct routes.

The official Romeo Telegram corpus was also searched for an explicit `true MSS` / market-structure-shift algorithm. No direct text defining the required swing construction, break rule, ownership, confirmation, invalidation and expiry was recovered.

Therefore the remaining blockers are evidence availability, not an engineering task left undone.

## Remaining deterministic debts

```text
SS
  exact meaning / referent
  causal geometry
  ownership / lifecycle

SMT
  corresponding-extreme construction
  same-direction and inverse polarity
  synchronization window
  traded/confirmation leg ownership
  exact TS-substitution condition
  invalidation / expiry

MODEL_1
  exact geometry
  information timing
  confirmation / invalidation / expiry

TRUE_MSS
  no replayable direct algorithm recovered

TURTLE_SOUP
  qualifying old-extreme rule
  excursion and confirmation event
  invalidation / expiry

KEY_LEVEL
  deterministic selector / hierarchy
  arrival/reaction qualification

TIME
  timezone and DST anchor
  instrument/session scope
  hard-filter vs context semantics
  confirmation / expiry

DYNAMIC_BIAS
  deterministic `convincing CRT`
  owning timeframe
  transition timestamp
  confirmation / expiry
  deterministic trend slowdown/warning-sign definition
```

## Decision

```text
RECOVERY_COMPLETE_NO_PREDICATE_CLOSURE

CLOSING_FIELD_EVIDENCE       = 0
CANDIDATE_READY_ROWS         = 0
NEW_ALPHA_CANDIDATE          = NOT_SELECTED
DETECTOR_ACTIVITY            = NOT_AUTHORIZED
BACKTEST_PNL                 = NOT_AUTHORIZED
V0_1_OOS_CONFIRM             = UNOPENED
PHASE_7                      = BLOCKED
```

Phase 6C remains blocked. Re-entry requires a newly available first-party technical artifact that closes one of the held causal predicates; recovered context alone is not sufficient.
