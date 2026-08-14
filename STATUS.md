# Project Status

Updated: 2026-08-14

| Phase | Status | Primary exit condition |
|---|---|---|
| 0 — Engineering foundation | **COMPLETE** | Reproducible dev + CI + logging/storage/experiment contracts |
| 1 — Romeo corpus / reconciliation | **COMPLETE** | Evidence-indexed corpus + explicit evidence debts |
| 2 — Formal CRT spec | **COMPLETE — v0.1 FROZEN** | Deterministic v0.1 order path |
| 3 — Market data | **COMPLETE FOR BINANCE/BTCUSDT v0.1 ROUTE** | Trusted/reproducible D1/H1 dataset |
| 4 — CRT detector | **COMPLETE FOR v0.1** | Frozen deterministic detector |
| 5 — Backtester | **COMPLETE FOR v0.1** | Deterministic cost-aware simulator |
| 6 — Validation | **COMPLETE — INSUFFICIENT_EVIDENCE** | Terminal preregistered v0.1 DEV decision |
| 6B — Candidate revision | **COMPLETE — INSUFFICIENT_MULTI_MARKET_SAMPLE** | Terminal preregistered multi-market activity decision |
| 6C — Doctrine research | **IN PROGRESS — 2026 SOURCE RECONCILIATION** | Close a first-party deterministic rule delta before candidate selection |
| 7 — Paper trading | **BLOCKED** | Requires a future candidate that passes full validation |
| 8 — Learning engine | Not started | Requires sufficient deterministic labels |
| 9 — Shadow trading | Not started | Requires paper readiness |
| 10 — Controlled live | **NOT AUTHORIZED** | Explicit future approval + canary gates |

## Frozen v0.1 result

```text
strategy   CRT-C3-D1-H1-M1-BEAR-v0.1
detector   CRT-DETECTOR-v0.1
simulator  CRT-BACKTEST-v0.1.1
DEV        2019-01-01 .. 2022-12-31
candidates 1,416
TradePlans 4
required   30
decision   INSUFFICIENT_EVIDENCE
```

The Phase-6 v0.1 result remains historical evidence and is not overwritten by Phase 6B or Phase 6C. v0.1 OOS and CONFIRM remain unopened. Parameter optimization and paper/shadow/live promotion remain unauthorized.

## Phase 6B terminal result

```text
candidate_version      CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH
alpha_strategy_version CRT-C3-D1-H1-M1-BEAR-v0.1
detector_version       CRT-DETECTOR-v0.2-MULTI-MARKET
signal_component       MID
final decision         INSUFFICIENT_MULTI_MARKET_SAMPLE
```

Frozen exact OANDA universe:

```text
EUR_USD
XAU_USD
NAS100_USD
SPX500_USD
```

### Provider/data qualification

All 16 preregistered 2019-2022 MID/M1 instrument/year shards passed provider qualification. Raw price data remained ephemeral; only credential-free evidence was persisted.

```text
complete M1 candles                    5,529,393
raw missing intervals                    122,626
raw missing minutes                    2,885,967
S5 classified intervals                  122,626
NO_PRICE_OBSERVATION intervals           122,626
UNRESOLVED_PROVIDER_GAP intervals              0
NO_PRICE_OBSERVATION minutes           2,885,967
UNRESOLVED_PROVIDER_GAP minutes                0
raw-gap-qualified instruments               4/4
independent refetch                   PASS 4/4 per instrument
```

### Trusted canonical datasets

OANDA Trusted Dataset Build run #3 (`31799895592`) completed successfully and produced four `P6B_CANONICAL_PRICE_DATASET_V2` identities with `quality_status = TRUSTED`.

| Instrument | H1 rows | NY-D1 rows | Price quantum | Normalized H1/D1 SHA-256 |
|---|---:|---:|---:|---|
| `EUR_USD` | 24,902 | 1,249 | `0.00001` | `b141c402fc4a69456fa56ab074b7bf37c75465b2e1e92a4c98c8516a08f96dd8` |
| `XAU_USD` | 23,660 | 1,244 | `0.001` | `ec349ca0f77c3827666519bb234466ff1ff3e0ba2a30e46795c597a1df79fcdd` |
| `NAS100_USD` | 23,604 | 1,245 | `0.1` | `4c46987b424f6616116299132664ea298dab55697d240f089fe0867c5cf19181` |
| `SPX500_USD` | 23,605 | 1,245 | `0.1` | `dae1825b057fdc1acf87278a2163b570d9f2ae3fa870484c775eec78de37c19f` |

Exact trusted set freeze:

```text
8214c31e09d53cffadce453727604e0847a4d22e
```

### Detector-only activity gate

```text
accepted instruments      >= 2
contributing instruments  >= 2
pooled TradePlans         >= 30
backtester                PROHIBITED
P&L                       PROHIBITED
```

Phase 6B Detector Activity Gate run #1 (`31802738559`) produced:

| Instrument | Complete NY-D1 | Candidates | NO_SIGNAL | TradePlans |
|---|---:|---:|---:|---:|
| `EUR_USD` | 1,249 | 1,247 | 1,244 | 3 |
| `NAS100_USD` | 1,245 | 1,243 | 1,241 | 2 |
| `SPX500_USD` | 1,245 | 1,243 | 1,241 | 2 |
| `XAU_USD` | 1,244 | 1,242 | 1,242 | 0 |
| **Pooled** | — | **4,975** | **4,968** | **7** |

```text
accepted instruments       4   >= 2   PASS
contributing instruments   3   >= 2   PASS
pooled TradePlans           7   >= 30  FAIL
```

The Phase-6B data and universe gates passed; sample activity failed. The result cannot be repaired by lowering the threshold, changing alpha rules after seeing counts, tuning parameters, dropping instruments, or opening P&L.

Canonical Phase-6B decision evidence:

- `experiments/phase6b/P6B_MULTI_MARKET_ACTIVITY_RESULT_001.json`
- `experiments/phase6b/P6B_MULTI_MARKET_ACTIVITY_RESULT_001.md`

## Phase 6C — active 2026 doctrine research

Phase 6C is a fresh evidence-led route, not a continuation of the Phase-6B activity experiment.

```text
research branch            agent/phase-6c-crtology-evidence
doctrine baseline          CRT_SECRETS_2025
new source stream          CRTOLOGY_2026_RESEARCH
new alpha candidate        NOT SELECTED
```

New 2026 statements may not silently rewrite historical rules. Every potential delta is classified as `CLARIFICATION`, `REFINEMENT`, `NEW_OPTIONAL_BRANCH`, `SUPERSEDING_RULE`, `NON_ALPHA_CONTEXT`, or `UNRESOLVED`.

First-party 2026 evidence reinforces that core CRT/Turtle Soup remain stable while the system receives refinements and nuances. Historical v0.1/v0.2 semantics therefore remain immutable unless a separately versioned successor is justified.

### Source gate: CRTology Episode 1

```text
source_id                    ROMEO-2026-CRTOLOGY-01
title                        CRTology episode 1: SS
video_id                     4DZWbCzEvhM
source identity              CONFIRMED
first-party provenance       CONFIRMED
explicit meaning of SS       NOT CAPTURED
new deterministic predicate  NOT CAPTURED
gate result                  TECHNICAL_SOURCE_CAPTURE_INSUFFICIENT
```

The pass preserves first-party clues around an organised recognition lens, not forcing absent setups, strong-trend caution and weekly day-of-week context. These remain non-executable.

Canonical records:

- `research/romeo/phase6c/CRTOLOGY_01_EVIDENCE_GATE.md`
- `research/romeo/phase6c/PRIMARY_SOURCE_PASS_001.md`

### Source gate: Live Tape-Reading Session 2

```text
source_id                    ROMEO-2026-LIVE-02
title                        CRT live tape-reading session (2)
video_id                     Pmmx41M7KhA
source identity              CONFIRMED
first-party provenance       CONFIRMED
new deterministic predicate  NOT CAPTURED
gate result                  TECHNICAL_SOURCE_CAPTURE_INSUFFICIENT
```

The surrounding first-party stream preserves:

- selection-over-availability as a trading principle;
- explicit `exit-entry theory` language without a closed lifecycle;
- `every quarter is a candle` as a possible future fractality branch;
- Model #1/OTE training emphasis;
- stable-core / continuing-refinement doctrine versioning.

Canonical record:

- `research/romeo/phase6c/LIVE_02_EVIDENCE_GATE.md`

### 2025-vs-2026 reconciliation ledger

Canonical ledger:

- `research/romeo/phase6c/DOCTRINE_RECONCILIATION_2026.md`

Current result:

```text
candidate_ready_rows = 0
```

No new candidate is selected from a qualitative clue alone.

## Active Phase 6C evidence priority — SMT

Phase 6C has recovered direct first-party evidence that closes two previously unresolved SMT facts:

1. basic pair registry:

```text
EU   <-> DXY
NQ   <-> ES
BTC  <-> ETH
GOLD <-> SILVER
```

2. substitution/role clue: Romeo gives a case where traders expected a local low to be Turtle-Souped but states that SMT was instead performing its Episode-6 role.

These findings materially strengthen the SMT research branch but do not yet authorize it. Remaining strategy-critical fields include:

```text
exact divergence polarity by pair type
corresponding-extreme construction
cross-market timestamp synchronization
stale/missing-data behavior
direction ownership
which paired instrument anchors confirmation
exact Model #1 / true-MSS interaction
when SMT may substitute for local Turtle Soup
traded-instrument selection
confirmation / invalidation / expiry
```

The next Phase-6C task is to close these fields from direct Romeo evidence where possible. Third-party Episode-6 summaries may guide discovery but cannot independently authorize executable SMT logic.

## Current handoff

```text
Phase 6B                         COMPLETE — INSUFFICIENT_MULTI_MARKET_SAMPLE
Phase 6C                         IN PROGRESS — 2026 SOURCE RECONCILIATION
Episode-1 source gate            CLOSED — TECHNICAL CAPTURE INSUFFICIENT
Live-02 source gate              CLOSED — TECHNICAL CAPTURE INSUFFICIENT
2025 doctrine                    PRESERVED
2026 reconciliation ledger       ACTIVE
SMT basic pair registry          DIRECT FIRST-PARTY EVIDENCE CAPTURED
SMT substitution role            DIRECT FIRST-PARTY CLUE CAPTURED
SMT full executable semantics    UNRESOLVED
New alpha candidate              NOT SELECTED
Alpha implementation             NOT AUTHORIZED
Detector activity                NOT AUTHORIZED
Performance protocol             NOT AUTHORIZED
Backtest / P&L                   NOT AUTHORIZED
v0.1 OOS / CONFIRM               UNOPENED
Phase 7                          BLOCKED
Live trading                     NOT AUTHORIZED
```

## Authorization

```text
V0_1_MUTATION_AUTHORIZED                    = false
V0_1_OOS_OUTCOME_ACCESS_AUTHORIZED          = false
V0_1_CONFIRM_OUTCOME_ACCESS_AUTHORIZED      = false
PARAMETER_OPTIMIZATION_AUTHORIZED           = false
PHASE6B_ACTIVITY_GATE_COMPLETED              = true
NEW_PHASE6B_ACTIVITY_TUNING_AUTHORIZED       = false
PHASE6C_NEW_ALPHA_CANDIDATE_SELECTED         = false
PHASE6C_ALPHA_IMPLEMENTATION_AUTHORIZED      = false
PHASE6C_DETECTOR_ACTIVITY_AUTHORIZED         = false
PERFORMANCE_PROTOCOL_AUTHORIZED              = false
BACKTEST_AUTHORIZED                          = false
MULTI_MARKET_PNL_OUTCOME_ACCESS              = false
PAPER_TRADING_AUTHORIZED                     = false
SHADOW_TRADING_AUTHORIZED                    = false
LIVE_TRADING_AUTHORIZED                      = false
```

## Canonical Phase 6C records

- `research/romeo/phase6c/PHASE_6C_RESEARCH_CHARTER.md`
- `research/romeo/phase6c/CRTOLOGY_01_EVIDENCE_GATE.md`
- `research/romeo/phase6c/PRIMARY_SOURCE_PASS_001.md`
- `research/romeo/phase6c/LIVE_02_EVIDENCE_GATE.md`
- `research/romeo/phase6c/DOCTRINE_RECONCILIATION_2026.md`
- `docs/checklists/phase-6c.md`
- `research/romeo/SOURCE_REGISTRY.csv`
