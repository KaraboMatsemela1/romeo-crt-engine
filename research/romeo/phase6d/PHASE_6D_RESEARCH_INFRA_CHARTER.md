# Phase 6D — First-Party Research Infrastructure Charter

**Status:** IMPLEMENTATION IN PROGRESS  
**Mode:** research infrastructure only  
**Predecessor:** Phase 6C `BLOCKED_NO_VERIFIED_PREDICATE_CLOSURE`

## Purpose

Phase 6D removes the evidence-acquisition and semantic-governance bottleneck identified in Phase 6C. It does **not** attempt to manufacture more trades or reinterpret the frozen strategy after seeing Phase 6B activity counts.

The workstream provides deterministic tooling to:

1. bind captured first-party artifacts to the repository source registry;
2. hash source payloads and manifests for provenance/auditability;
3. track unresolved strategy predicates field-by-field;
4. classify doctrine changes without silently promoting them to alpha;
5. require causal positive and negative fixtures after a predicate closes;
6. expose a machine-auditable readiness summary while keeping all outcome access false.

## Explicit non-goals

```text
CREATE_NEW_ALPHA_CANDIDATE             = false
ALTER_PHASE6B_RESULT                   = false
LOWER_PHASE6B_ACTIVITY_THRESHOLD       = false
RUN_DETECTOR_OR_COUNTS                 = false
RUN_BACKTEST_OR_PNL                    = false
OPEN_V0_1_OOS                          = false
OPEN_V0_1_CONFIRM                      = false
PARAMETER_OPTIMIZATION                 = false
PAPER_SHADOW_LIVE                      = false
```

## Architecture

### 1. Registry-bound source acquisition

`SOURCE_REGISTRY.csv` remains the source of truth for source identity and URL. A capture cannot enter the Phase-6D manifest path by supplying an arbitrary source URL.

Core types:

- `SourceIdentityV1`
- `SourceArtifactV1`
- `SourceAcquisitionManifestV1`

Every artifact records:

- source ID;
- capture type;
- retrieval timestamp;
- SHA-256 of captured bytes;
- byte length;
- content type;
- causal locator (timestamp/post/frame/chart reference);
- explicit first-party verification.

The manifest is canonicalized and hashed. Raw captured media can remain outside Git when size/copyright constraints require it; the manifest binds the exact evidence used.

### 2. Predicate evidence ledger

Machine-readable ledger:

- `research/romeo/phase6d/PREDICATE_LEDGER_V1.json`

Each strategy-critical predicate declares required causal fields:

```text
EXACT_PREDICATE
INFORMATION_AVAILABILITY_TIME
DIRECTION_TIMEFRAME_OWNERSHIP
CONFIRMATION
INVALIDATION
EXPIRY
DATA_REQUIREMENTS
```

A row cannot become `CLOSED` until every declared field has directly first-party-verified evidence. Qualitative doctrine may leave a row `PARTIAL`; it cannot be treated as executable.

Initial ledger rows are inherited only as unresolved evidence debts from Phase 6C:

- `SS_MEANING_AND_CAUSAL_RULE`
- `SMT_EXECUTABLE_SEMANTICS`
- `MODEL_1_GEOMETRY`
- `TRUE_MSS_ALGORITHM`
- `TURTLE_SOUP_CONFIRMATION`
- `KEY_LEVEL_SELECTOR`
- `TIME_SELECTOR`
- `DYNAMIC_BIAS_TRANSITION`

No row is candidate-ready at Phase-6D start.

### 3. Doctrine delta validation

Allowed classifications remain:

```text
CLARIFICATION
REFINEMENT
NEW_OPTIONAL_BRANCH
SUPERSEDING_RULE
NON_ALPHA_CONTEXT
UNRESOLVED
```

The validator does not use opaque NLP to invent semantic classifications. A research process explicitly chooses the classification; code enforces that `UNRESOLVED` or `NON_ALPHA_CONTEXT` cannot claim a deterministic alpha effect.

### 4. Evidence-to-fixture gate

A closed predicate is still insufficient for implementation. The fixture gate requires at least:

- one causal positive example; and
- one causal negative/counterexample.

Fixtures must record the information available at decision time, observed inputs, expected label, and evidence source IDs. This prevents hindsight-only examples from silently becoming strategy code.

### 5. Readiness audit

`scripts/audit_phase6d_research_readiness.py` validates the source registry and predicate ledger, verifies that every evidence source ID exists in the registry, and prints a counts-only research readiness summary.

The audit explicitly emits:

```text
candidate_creation_authorized = false
detector_activity_authorized  = false
outcome_access_authorized     = false
```

A future closed predicate triggers human/research review; it does not automatically authorize implementation.

## Acquisition workflow

1. Register/verify the first-party source in `SOURCE_REGISTRY.csv`.
2. Capture permitted first-party text/captions/transcript/frame/chart evidence.
3. Run `scripts/build_first_party_capture_manifest.py` with the registered source ID.
4. Store the manifest and exact evidence locator.
5. Add field-specific evidence to the predicate ledger only when the captured artifact directly supports it.
6. Run the readiness audit.
7. If a predicate closes, build positive and negative causal fixtures.
8. Only after a separate preregistered candidate decision may strategy implementation be discussed.

## Version boundary

Phase 6D tooling may improve research quality, but it may not mutate historical strategy identities or decisions:

```text
Phase 6 v0.1 = INSUFFICIENT_EVIDENCE
Phase 6B     = INSUFFICIENT_MULTI_MARKET_SAMPLE
Phase 6C     = BLOCKED_NO_VERIFIED_PREDICATE_CLOSURE
```

These remain immutable evidence.
