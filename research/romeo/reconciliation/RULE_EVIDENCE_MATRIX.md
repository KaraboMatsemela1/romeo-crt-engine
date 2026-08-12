# Rule Evidence Matrix — Phase 1 Reconciliation

**Doctrine snapshot:** `CRT_SECRETS_2025`  
**Candidate strategy:** `CRT-C3-ALIGNED-v0.1-DRAFT`  
**Status:** RECONCILIATION / NOT FROZEN / NOT LIVE  
**Date:** 2026-08-12

## Purpose

This matrix consolidates the first-pass Romeo CRT evidence into canonical strategy statements. It does **not** convert every provisional observation into code. The purpose is to separate:

- architecture-safe findings
- candidate trading rules
- unresolved deterministic semantics
- research hypotheses that must not enter a frozen strategy

Confidence vocabulary:

- `VERIFIED` — primary evidence is direct and the predicate is deterministic enough to test
- `HIGH_CONFIDENCE` — strongly cross-supported; narrow direct-source verification still required
- `PROVISIONAL` — source-backed but materially ambiguous
- `HYPOTHESIS` — inference that requires explicit testing/evidence
- `UNRESOLVED` — do not encode
- `ENGINEERING_CONSTRAINT` — project safety/causality rule rather than Romeo alpha logic

## Canonical evidence matrix

| Canonical ID | Strategy area | Canonical statement | Supporting candidate rules / sources | Confidence | Deterministic now? | Freeze action |
|---|---|---|---|---|---|---|
| REC-001 | Object model | A selected candle can be treated as the parent CRT range/context object. | CRT-P001/P003; ANA-P001; ROMEO-2024-CRT, S4 | HIGH_CONFIDENCE | Partially | Directly verify exact parent-candle selection predicate. |
| REC-002 | Timeframes | Initial parent-candle scope is `{H4, D1, W1}`; when expressing hierarchy use `W1 → D1 → H4`. | ANA-P003; ROMEO-2025-S4 | HIGH_CONFIDENCE | Scope only | Freeze scope only; do not assume every trade must traverse all three levels. |
| REC-003 | Causality | Active parent candles may expose only information known at timestamp `t`; final OHLC is unavailable before close. | ANA-P006; Candle Snapshot constraint | ENGINEERING_CONSTRAINT | Yes | Freeze immediately. |
| REC-004 | Hierarchy | Higher-timeframe context/narrative is established before lower-timeframe execution. | JRN-P002; KOD-P009; DOT-P001 | HIGH_CONFIDENCE | Architecture only | Freeze orchestration, not exact HTF/LTF mappings. |
| REC-005 | Context | Key level is context/location, not an entry signal by itself. | KL-P001; C3-P003; CLN-P002 | HIGH_CONFIDENCE | Architecture only | Freeze ordering; block KeyLevelSelector until exact hierarchy is resolved. |
| REC-006 | Setup families | `JOURNEY_TO_KEY_LEVEL` and `REACTION_FROM_KEY_LEVEL` are distinct opportunity families. | KL-P005 | PROVISIONAL | No | Keep taxonomy; first v0.1 should select only one family if needed. |
| REC-007 | Liquidity primitive | Turtle Soup is a failed excursion beyond a qualifying reference extreme followed by reversal/failure of continuation. | TS-P001..P004; ROMEO-2024-TS | PROVISIONAL | No | Exact reference eligibility, close/confirmation, and timing remain blockers. |
| REC-008 | Journey | CRT is stateful progression, not a static screenshot pattern. | JRN-P001; ROMEO-2025-S3 | HIGH_CONFIDENCE | Architecture only | Freeze state-machine design. |
| REC-009 | Phase | Candle 1/2/3 broadly map to accumulation/manipulation/distribution, but live transition predicates remain unresolved. | CRT-P006; KOD-P002; JRN-P004; ROMEO-2024-CRT, S2, S3 | PROVISIONAL | No | Do not code retrospective labels as signal inputs. |
| REC-010 | Candle 3 gate | Candle 2 must complete before Candle 3 becomes eligible; Candle-3 open is eligibility, not entry. | C3-P001/P002; ROMEO-2025-S7 | HIGH_CONFIDENCE | Temporal gate only | Freeze temporal gate after direct-source check. |
| REC-011 | Candle 3 context | Candle 3 requires valid parent/key-level narrative and cannot be traded as ordinal pattern alone. | C3-P003; ROMEO-2025-S7 | HIGH_CONFIDENCE | No | Block until KeyLevelSelector and parent CRT are deterministic. |
| REC-012 | Direction | First candidate should trade directionally aligned CRTs and exclude countertrend setups. | FAIL-P006/P007; DOT-P005 | HIGH_CONFIDENCE | Filter concept only | Freeze `allow_countertrend=False` only after direction algorithm is defined. |
| REC-013 | 50% | Parent CRT midpoint is a major Target-1/state-transition level. | KOD-P004; C3-P005; FAIL-P003/P005 | HIGH_CONFIDENCE | Calculation yes; semantics conditional | Freeze midpoint calculation; direct-verify when it is T1 versus location/reaction context. |
| REC-014 | 50% consumption | Once T1/50% is reached, the original untouched setup state is consumed and continuation requires reassessment. | FAIL-P003/P004/P005 | HIGH_CONFIDENCE | State transition concept | Freeze state-machine transition after direct-source check. |
| REC-015 | 50% flexibility | Exact 50% touch must not be forced globally; key-level/Turtle-Soup or strong-trend context may produce valid shallower behavior. | C3-P005/P006/P007 | PROVISIONAL | No | Do not invent `near_50` tolerance or trend threshold. |
| REC-016 | SMT object | SMT requires explicitly related markets and compares corresponding high/low behavior across them. | SMT-P001/P002 | PROVISIONAL | No | Relationship registry and synchronization semantics are P0 blockers. |
| REC-017 | SMT governance | SMT is context/confirmation/state modification, not a direct order trigger. | SMT-P003/P004; DOT-P006 | HIGH_CONFIDENCE | Architecture yes | Freeze `SMTEvent -> no direct OrderIntent`. |
| REC-018 | SMT direction | SMT direction must be interpreted within established HTF direction. | DOT-P005; ROMEO-2025-S9 | HIGH_CONFIDENCE | No | Requires explicit pair polarity/directional mapping. |
| REC-019 | SMT conflict | Confirmed SMT against a pending CRT expectation can invalidate/downgrade the remaining target expectation. | FAIL-P001/P002 | PROVISIONAL-HIGH | No | Exact qualifying SMT + confirmation must be defined first. |
| REC-020 | Manipulation substitution | A related-market SMT event may sometimes satisfy manipulation evidence when local Turtle Soup is absent. | SMT-P007 | HYPOTHESIS | No | Explicitly exclude from v0.1 unless direct evidence resolves substitution. |
| REC-021 | Entry scope | First public execution-family scope is `MODEL_1` or `TRUE_MSS`. | DOT-P002; ROMEO-2025-S9 | HIGH_CONFIDENCE | Taxonomy yes | Freeze entry-family whitelist, not internal predicates. |
| REC-022 | Model #1 | Model #1 is anchored to a specific candle, not a broad arbitrary zone. | CRT-P010..P015; DOT-P003 | PROVISIONAL-HIGH | No | Exact geometry/close/retrace definition is P0 blocker. |
| REC-023 | True MSS | True MSS is context-qualified lower-timeframe structural confirmation, not generic BOS/MSS. | JRN-P006; KL-P006; DOT-P004 | PROVISIONAL-HIGH | No | Exact swing/break/entry-zone algorithm is P0 blocker. |
| REC-024 | KOD taxonomy | KOD is a Turtle-Soup subtype associated with a late-stage parent CRT journey. | KOD-P001/P005; JRN-P008 | PROVISIONAL | No | Do not implement `last_turtle_soup_before_target`; ex-ante classifier required. |
| REC-025 | KOD causality | Retrospective `final Turtle Soup before target` labeling is prohibited because it leaks future information. | KOD look-ahead finding | ENGINEERING_CONSTRAINT | Yes | Freeze immediately. |
| REC-026 | Stop | Stop reference is structural; Episode 9 demonstrates bullish protection below Turtle-Soup low. | DOT-P007 | PROVISIONAL-HIGH | Reference only | Exact buffer and bearish mirror remain unresolved. |
| REC-027 | Target selection | Price target must be predeclared from the trade narrative, not chosen after outcome. | DOT-P009; anti-look-ahead rule | ENGINEERING_CONSTRAINT + PROVISIONAL alpha | Yes for governance | Freeze predeclaration; target hierarchy remains P1 blocker. |
| REC-028 | Exit types | Strategy may use price-based and time-based exits. | DOT-P008 | PROVISIONAL | No | Time-exit predicate unresolved; exclude until defined. |
| REC-029 | Failure state | Incomplete CRT is a source-backed trap concept requiring explicit completeness state. | FAIL-P008 | UNRESOLVED | No | `UNKNOWN -> NO TRADE`; predicate is P1/P2 blocker. |
| REC-030 | No-trade | `NO_SIGNAL` is a valid terminal outcome; never force a trade because context exists. | C3-P009; CLN process guidance | HIGH_CONFIDENCE / GOVERNANCE | Yes | Freeze immediately. |
| REC-031 | Outcome analytics | CRT outcomes must be multi-stage: pre-entry invalidation, stopped before T1, T1 reached, T1+T2 reached, T1 reached without T2, etc. | FAIL-P005 + project analytics | ENGINEERING_CONSTRAINT | Yes | Freeze analytics schema. |
| REC-032 | Journaling | Candidates, rejections, no-signals, failures and trades must all be journaled. | CLN-P004/P005 | PROCESS / HIGH_CONFIDENCE | Yes | Freeze operating model. |
| REC-033 | Strategy versioning | Rule corrections create new strategy versions and must be retested; do not mutate a strategy after seeing outcomes. | CLN-P005/P007/P008 | ENGINEERING_CONSTRAINT | Yes | Freeze immediately. |
| REC-034 | Doctrine version | Preserve `CRT_SECRETS_2025` separately from 2026 `CRTology` refinements. | CLN-P008 | VERSIONING_GOVERNANCE | Yes | Freeze doctrine versioning. |
| REC-035 | Candle boundaries | H4/D1/W1 construction is strategy-critical and timezone/session/DST semantics must be explicit. | ANA-P002 + Candle Boundary constraint | UNRESOLVED / CRITICAL | No | P0 blocker before causal backtesting. |
| REC-036 | Multi-market replay | SMT-enabled tests require synchronized causal replay with stale-data/session guards; stale comparison data yields `UNKNOWN`. | SMT engineering constraints | ENGINEERING_CONSTRAINT | Yes | Freeze before SMT implementation. |

## Architecture-safe rules eligible for early implementation

The following may guide scaffolding before alpha predicates are finalized because they are safety/orchestration constraints rather than discretionary trading rules:

1. causal candle snapshots (`REC-003`)
2. HTF-context-before-entry architecture (`REC-004`)
3. key-level-before-pattern ordering (`REC-005`)
4. state-machine rather than static pattern architecture (`REC-008`)
5. no retrospective KOD classification (`REC-025`)
6. SMT cannot directly emit orders (`REC-017`)
7. target must be chosen before outcome (`REC-027`)
8. `NO_SIGNAL` as valid terminal state (`REC-030`)
9. multi-stage outcome schema (`REC-031`)
10. journaling/version discipline (`REC-032`–`REC-034`)
11. synchronized/stale-safe multi-market infrastructure (`REC-036`)

These do **not** authorize a trading signal.

## Core alpha blockers

The draft strategy cannot be frozen until these are either directly resolved or explicitly excluded:

- parent CRT / Candle-1 selection
- key-level selection and ranking
- exact Candle-1/Candle-2 live semantics
- Model #1 geometry
- true MSS algorithm
- Turtle Soup reference/confirmation semantics
- H4/D1/W1 candle anchors
- SMT pair/polarity/synchronization semantics if SMT is retained
- exact target hierarchy
- exact stop buffer
- incomplete-CRT predicate if used as hard filter
- KOD ex-ante classifier if KOD is retained
- time-exit semantics if retained

## Reconciliation decision

The evidence supports continuing with a narrowly scoped candidate named:

`CRT-C3-ALIGNED-v0.1-DRAFT`

It does **not** yet support marking any end-to-end trade predicate `VERIFIED`.
