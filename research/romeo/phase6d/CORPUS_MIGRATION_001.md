# Phase 6D — Existing First-Party Corpus Migration 001

**Date:** 2026-08-14  
**Mode:** research/provenance only  
**Input:** bounded six-source Phase-6C acquisition set  
**Remote reacquisition:** not used; migration is limited to repository-preserved evidence  
**Candidate / detector / P&L / OOS / CONFIRM:** prohibited

## Objective

Apply the Phase-6D provenance contracts to the strongest existing Phase-6C first-party evidence without upgrading summaries, paraphrases, or qualitative claims into executable rules.

The migration asks a narrower question than Phase 6C:

> Which previously documented first-party claims are replayable from an exact source identity, exact evidence payload, deterministic SHA-256, and exact locator?

Only replayable evidence may enter the artifact corpus or predicate ledger.

## Acquisition migration

| Source ID | Phase-6C role | Migration status | Replayable technical artifact | Manifest SHA-256 |
|---|---|---|---|---|
| `ROMEO-2026-TG-TIME-TS-6361` | Time + Turtle Soup doctrine | `CAPTURED` | YES — legacy exact quoted first-party text preserved in canonical gate | `2b7ee573004c5e5fe8a284fa19a6b0aa9f705ab40815abc31e94faf3565a639c` |
| `ROMEO-2026-CRTOLOGY-01` | SS / CRTology Episode 1 | `PARTIAL` | NO — source identity only; no direct technical transcript/caption/frame payload | `4175fffb1cfbc1f1b2fb3830e66845131eb027f166a1e34c1351d9eda3918f1a` |
| `ROMEO-2025-S6` | SMT | `PARTIAL` | NO — semantic/direct-claim records lack replayable exact artifact + locator | `6df089c9f9376ddb2fe75280ce30b1c032abfcec0e0923791184829f58288f62` |
| `ROMEO-2025-S9` | Model #1 / true MSS / SMT usage | `PARTIAL` | NO — scope is documented, technical source payload is not | `b6e089683456dcd2df7a42c74292d57d98397981a04b1125caba7d1e178a8e6f` |
| `ROMEO-2024-TS` | Turtle Soup | `PARTIAL` | NO — existing transcript/summary evidence remains provisional | `e3723a33bb97d17c97c3f56bc036715be474749011c76aed4151feb0c0109e45` |
| `ROMEO-2025-S5` | Key level | `PARTIAL` | NO — direct technical payload + exact locator are not preserved | `8dab0de549391302917da4c00f7098b623e729bd731e3cb28217ed80b09b1552` |

Result:

```text
acquisition manifests       6
CAPTURED                     1
PARTIAL                      5
replayable corpus sources    1
replayable corpus artifacts  1
```

## Replayable artifact

Source:

```text
ROMEO-2026-TG-TIME-TS-6361
https://t.me/officialRomeotpt/6361
```

The canonical Phase-6C gate preserved the exact direct first-party sentence:

```text
T symbolises Time and Turtle soup.
```

Migration artifact:

```text
capture kind     TEXT
byte length      35
payload SHA-256  2f414608bccd9319eb996b5bce47354d022b192b256d606ab92a735ea5248a33
locator          legacy-capture:research/romeo/phase6c/TIME_TURTLE_SOUP_EVIDENCE_GATE.md#Direct evidence captured
```

This is explicitly a **legacy direct-capture migration**, not a fresh remote fetch. The artifact is used only to preserve the prior first-party claim with deterministic chain of custody.

Corpus index:

```text
schema           P6D_EVIDENCE_CORPUS_INDEX_V1
index SHA-256    2ce747487990c1f883c8c93fe910cf37dc552dbcf2552bf0c82f27f857415b89
sources          1
artifacts        1
```

## Why Predicate Ledger V2 was required

`P6D_PREDICATE_LEDGER_V1` had binary field semantics: any evidence attached to a field made that whole field satisfied.

That is too coarse for the existing corpus. Direct first-party evidence can be relevant to a field while still failing to define the complete deterministic rule.

V2 therefore adds:

```text
EvidenceCoverage.PARTIAL
EvidenceCoverage.CLOSING
```

Only `CLOSING` evidence satisfies a required field. `PARTIAL` evidence is visible and auditable but cannot make a predicate candidate-ready.

V1 remains preserved as the original infrastructure artifact; V2 is the corpus-application representation.

## Field-by-field migration result

### `TIME_SELECTOR`

Artifact-backed observations:

| Field | Coverage | Evidence consequence |
|---|---|---|
| `EXACT_PREDICATE` | `PARTIAL` | Time + Turtle Soup functional ownership is source-supported; exact weekday/session/key-time selector is not defined. |
| `DATA_REQUIREMENTS` | `PARTIAL` | Time and Turtle Soup must be represented together conceptually; exact calendar/timezone/DST/granularity data contract is not defined. |
| `INFORMATION_AVAILABILITY_TIME` | none | unresolved |
| `DIRECTION_TIMEFRAME_OWNERSHIP` | none | unresolved |
| `CONFIRMATION` | none | unresolved |
| `INVALIDATION` | none | unresolved |
| `EXPIRY` | none | unresolved |

Therefore:

```text
observed fields    2
satisfied fields   0
status             PARTIAL
candidate_ready    false
```

### Other held predicates

No other held predicate currently has a replayable direct technical artifact in the migrated bounded corpus:

```text
SS_MEANING_AND_CAUSAL_RULE    UNRESOLVED
SMT_EXECUTABLE_SEMANTICS      UNRESOLVED
MODEL_1_GEOMETRY              UNRESOLVED
TRUE_MSS_ALGORITHM            UNRESOLVED
TURTLE_SOUP_CONFIRMATION      UNRESOLVED
KEY_LEVEL_SELECTOR            UNRESOLVED
DYNAMIC_BIAS_TRANSITION       UNRESOLVED
```

This does not erase the Phase-6C doctrine records. It means those records are not yet artifact-replayable enough to populate a deterministic predicate field.

## Legacy direct claims that remain quarantined

Phase 6C documented source-supported claims such as:

- the basic SMT research-pair registry;
- SMT sometimes fulfilling the role expected from a local Turtle Soup;
- a convincing opposite CRT justifying bias reconsideration;
- key-level journey-vs-reaction doctrine.

They remain valid **historical research statements** in the Phase-6C records. This migration does not attach them to V2 predicate fields because the repository does not preserve an exact first-party payload and exact source locator for those claims.

Re-entry for those claims is simple: acquire/recover the original first-party post/transcript/frame, hash the exact payload, add its acquisition manifest, admit it to the corpus index, then attach it to the relevant V2 field as `PARTIAL` or `CLOSING` according to what it actually proves.

## Audit result

The deterministic migration audit requires:

1. every acquisition source exists in `SOURCE_REGISTRY.csv`;
2. acquisition URL equals the registered URL;
3. every manifest digest recomputes exactly;
4. every corpus artifact belongs to the indexed source and manifest;
5. every ledger artifact SHA exists in an acquisition manifest;
6. every ledger artifact SHA is admitted to the corpus index;
7. `PARTIAL` evidence never satisfies a required field.

Expected terminal migration state:

```text
acquisition_manifests                 6
captured_manifests                    1
partial_manifests                     5
corpus_sources                        1
corpus_artifacts                      1
predicate_rows                        8
predicate_rows_with_artifact_evidence 1
observed_field_evidence               2
closing_field_evidence                0
candidate_ready_rows                  0
```

## Decision

```text
PHASE6D_CORPUS_MIGRATION = COMPLETE_NO_PREDICATE_CLOSURE
PHASE6C                   = BLOCKED_NO_VERIFIED_PREDICATE_CLOSURE
NEW_ALPHA_CANDIDATE       = NOT_SELECTED
DETECTOR_ACTIVITY         = NOT_AUTHORIZED
BACKTEST_PNL              = NOT_AUTHORIZED
V0_1_OOS_CONFIRM          = UNOPENED
PHASE_7                   = BLOCKED
LIVE_TRADING              = NOT_AUTHORIZED
```

The migration improves provenance quality but does not change strategy readiness.
