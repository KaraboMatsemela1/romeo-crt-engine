# Project Closeout — 2026-08-23

## Disposition

`romeo-crt-engine` is closed as an evidence-constrained research and engineering project.

This is **not** a declaration that the Romeo strategy was validated, profitable, paper-ready, or live-ready. The project is being retired because the evidence gates worked as designed and no complete deterministic successor predicate could be justified from directly verifiable first-party material.

Terminal project disposition:

```text
PROJECT_STATE                           = CLOSED_EVIDENCE_GATE
ENGINEERING_FOUNDATION                  = COMPLETE
V0_1_VALIDATION                         = INSUFFICIENT_EVIDENCE
PHASE_6B_MULTI_MARKET                   = INSUFFICIENT_MULTI_MARKET_SAMPLE
VERIFIED_FIRST_PARTY_PREDICATE_CLOSURES = 0
CANDIDATE_READY_ROWS                    = 0
NEXT_DETERMINISTIC_CANDIDATE            = NOT_JUSTIFIED
OOS                                     = UNOPENED
CONFIRM                                 = UNOPENED
PAPER_EXECUTION_INFRASTRUCTURE          = COMPLETE_DISABLED
PAPER_TRADING_AUTHORIZED                = false
SHADOW_TRADING_AUTHORIZED               = false
LIVE_TRADING_AUTHORIZED                 = false
```

## What was completed

The repository successfully delivered the reusable engineering and governance platform required to test an evidence-backed CRT strategy without silently changing the hypothesis after seeing outcomes:

- engineering foundation, CI, deterministic logging/storage and experiment contracts;
- first-party Romeo corpus, reconciliation records and provenance controls;
- frozen CRT v0.1 specification and detector;
- trusted market-data contracts and deterministic backtester;
- preregistered validation gates and sequential DEV → OOS → CONFIRM access controls;
- independent leakage/specification review tooling;
- candidate preregistration and promotion evaluation tooling;
- OANDA practice-only adapter boundary;
- hard risk engine, kill switch, persistent order/position state and reconciliation;
- observability, alerts, runbook and execution-disabled paper-stack integration;
- Phase 6D provenance infrastructure with content-addressed evidence handling and fail-closed predicate accounting.

The latest completed repository work before closeout was PR #125. Its CI run `32148283657` completed successfully.

## Frozen validation results

### Phase 6 — v0.1

```text
strategy      CRT-C3-D1-H1-M1-BEAR-v0.1
candidates    1,416
TradePlans    4
required      30
decision      INSUFFICIENT_EVIDENCE
```

The DEV sample did not meet the preregistered minimum. OOS and CONFIRM were therefore not opened.

### Phase 6B — multi-market revision

```text
candidate     CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH
TradePlans    7
required      30
decision      INSUFFICIENT_MULTI_MARKET_SAMPLE
```

The activity threshold was not lowered after observing results and no performance-based rule selection was used to rescue the candidate.

## Terminal Phase 6C / 6D evidence result

Repeated bounded first-party recovery passes materially improved provenance and recovered useful partial doctrine, including Model #1, True MSS, SMT, Turtle Soup, key-level, dynamic-bias and weekday-role evidence.

However the closing test remained unchanged:

```text
verified predicate closures = 0
candidate-ready rows         = 0
```

The missing fields are not unfinished software tasks. They are semantic/evidence gaps such as deterministic selector construction, ownership, timing, confirmation, invalidation and expiry rules that Romeo's currently captured first-party material does not define sufficiently for two independent engineers to implement identically.

The correct scientific result is therefore to stop rather than infer the missing rules from generic ICT knowledge, third-party summaries, observed backtest outcomes or post-hoc tuning.

## Why the project is being retired

The project has reached a clean stopping point:

1. there are no open implementation PRs or failed CI lanes requiring service;
2. all engineering infrastructure needed for safe research and future practice execution is complete;
3. the canonical remaining strategy path depends on first-party semantic closure that is not currently available;
4. creating another candidate anyway would violate the project's evidence and anti-overfitting rules;
5. downstream validation, paper, learning, shadow and live phases therefore cannot be truthfully marked complete.

Standing downstream issues are retired as `not_planned`, not `completed`, so repository history does not imply that their gates passed.

## Preserved assets

The repository should remain available as an archive/reference implementation. In particular, preserve:

- `PROJECT_BIBLE.md` and `AGENTS.md`;
- `strategy/CRT_V0.1_SPEC.md` and freeze manifests;
- `docs/MARKET_DATA.md`, `docs/DETECTOR.md`, `docs/BACKTESTER.md`;
- `experiments/phase6/` frozen validation records;
- `research/romeo/phase6d/` provenance manifests, payloads, corpus index and predicate ledger;
- paper-execution infrastructure, risk, reconciliation and observability code in its execution-disabled state.

Historical Phase 6/6B results remain immutable.

## Reactivation criteria

This project may be reopened only if a materially new first-party evidence event occurs. A valid reactivation event must satisfy at least one of the following:

1. a new official Romeo/CRTology technical publication directly defines a currently missing deterministic field;
2. an original first-party caption, transcript, audio or technical frame becomes replayably recoverable and is not already represented by the admitted corpus;
3. a first-party Telegram/X/website statement directly closes a named predicate field with sufficient ownership/timing/lifecycle semantics;
4. a source-capability change makes currently locator-only first-party evidence replayably capturable;
5. a complete predicate passes the repository's two-engineer and fixture gates without consulting protected OOS/CONFIRM outcomes.

Reactivation does **not** inherit permission to trade. It must reopen the research gate first, create a new preregistered candidate/version, then repeat DEV → OOS → CONFIRM and the Phase-7 qualification sequence.

## Final safety state

```text
CREATE_NEW_ALPHA_CANDIDATE             = false
RUN_DETECTOR_OR_COUNTS                 = false
RUN_BACKTEST_OR_PNL                    = false
OPEN_OOS_CONFIRM                       = false
INFER_MISSING_ROMEO_SEMANTICS          = false
PAPER_TRADING_AUTHORIZED               = false
SHADOW_TRADING_AUTHORIZED              = false
LIVE_TRADING_AUTHORIZED                = false
```

The project closes with its most important integrity property intact: it did not convert insufficient evidence into a claimed profitable trading system.