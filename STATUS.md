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
| 6C — CRTology evidence research | **IN PROGRESS — PRIMARY-SOURCE EVIDENCE GATE** | Close 2026 doctrine semantics before selecting any new candidate |
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

## Phase 6B terminal candidate identity

```text
candidate_version      CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH
alpha_strategy_version CRT-C3-D1-H1-M1-BEAR-v0.1
detector_version       CRT-DETECTOR-v0.2-MULTI-MARKET
signal_component       MID
alpha changes          NONE
```

Frozen exact OANDA universe:

```text
EUR_USD
XAU_USD
NAS100_USD
SPX500_USD
```

No instrument was added, removed, or substituted after detector activity was observed.

## Phase 6B provider qualification — COMPLETE

Historical qualification is governed by `P6B-OANDA-HISTORY-QUALIFICATION-V1` and `P6B_OANDA_OBSERVATION_POLICY_V2`.

All 16 preregistered 2019-2022 MID/M1 instrument/year shards were collected from OANDA practice, independently re-fetched, validated, and reduced to credential-free reconciliation evidence. Raw provider price artifacts were ephemeral and deleted after validation.

```text
complete M1 candles                    5,529,393
raw missing intervals                    122,626
raw missing minutes                    2,885,967
all-gap S5 evidence shards                 16/16 PASS
NO_PRICE_OBSERVATION intervals           122,626
NO_PRICE_OBSERVATION minutes           2,885,967
UNRESOLVED_PROVIDER_GAP intervals              0
UNRESOLVED_PROVIDER_GAP minutes                0
raw-gap-qualified instruments               4/4
independent refetch                   PASS 4/4 per instrument
```

Canonical raw-gap evidence is sealed in `experiments/phase6b/P6B_ALL_GAP_S5_UNIVERSE_001.md`.

## Phase 6B New-York DEV boundary qualification — COMPLETE

The detector-facing DEV window is frozen in New-York wall-clock time and maps to:

```text
2019-01-01T05:00:00Z .. 2023-01-01T05:00:00Z exclusive
```

The five-hour tail from `2023-01-01T00:00:00Z` to `2023-01-01T05:00:00Z` was independently qualified for all four instruments. Each tail contained zero provider M1 and S5 observations, exact empty provider re-fetch, one 300-minute `NO_PRICE_OBSERVATION` interval, and zero unresolved gaps.

## Phase 6B trusted canonical datasets — COMPLETE 4/4

OANDA Trusted Dataset Build run #3 (`31799895592`) completed successfully. Every instrument was freshly reconstructed from OANDA, matched the sealed provider-value and gap evidence, derived deterministic H1 and New-York-midnight D1 data, and emitted `P6B_CANONICAL_PRICE_DATASET_V2` with `quality_status = TRUSTED`.

| Instrument | H1 rows | NY-D1 rows | Price quantum | Normalized H1/D1 SHA-256 |
|---|---:|---:|---:|---|
| `EUR_USD` | 24,902 | 1,249 | `0.00001` | `b141c402fc4a69456fa56ab074b7bf37c75465b2e1e92a4c98c8516a08f96dd8` |
| `XAU_USD` | 23,660 | 1,244 | `0.001` | `ec349ca0f77c3827666519bb234466ff1ff3e0ba2a30e46795c597a1df79fcdd` |
| `NAS100_USD` | 23,604 | 1,245 | `0.1` | `4c46987b424f6616116299132664ea298dab55697d240f089fe0867c5cf19181` |
| `SPX500_USD` | 23,605 | 1,245 | `0.1` | `dae1825b057fdc1acf87278a2163b570d9f2ae3fa870484c775eec78de37c19f` |

The exact trusted set was frozen before detector counts at commit `8214c31e09d53cffadce453727604e0847a4d22e` in:

- `experiments/phase6b/P6B_TRUSTED_DATASET_FREEZE_001.json`
- `experiments/phase6b/P6B_TRUSTED_DATASET_FREEZE_001.md`

## Phase 6B detector-only activity gate — COMPLETE

Frozen preregistered thresholds:

```text
accepted instruments      >= 2
contributing instruments  >= 2
pooled TradePlans         >= 30
backtester                PROHIBITED
P&L                       PROHIBITED
```

Phase 6B Detector Activity Gate run #1 (`31802738559`) verified freeze ancestry, exact trusted artifact ZIP hashes, exact H1/D1 file hashes, and trusted identities before invoking the frozen detector. It persisted counts and ReasonCode inventories only; no candidate timestamps, trade geometry, P&L, or simulator outcomes were opened.

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

## Terminal Phase 6B decision

```text
INSUFFICIENT_MULTI_MARKET_SAMPLE
```

The data-quality and eligible-universe gates passed. The candidate terminates because the frozen strategy produced only **7 pooled TradePlans**, materially below the preregistered minimum of **30**.

This result must not be repaired by lowering the threshold, changing alpha rules, selecting instruments based on observed counts, optimizing parameters, or opening P&L. Any future research route requires a separately justified and preregistered candidate/protocol.

Canonical decision evidence:

- `experiments/phase6b/P6B_MULTI_MARKET_ACTIVITY_RESULT_001.json`
- `experiments/phase6b/P6B_MULTI_MARKET_ACTIVITY_RESULT_001.md`

Activity evidence binding:

```text
freeze commit              8214c31e09d53cffadce453727604e0847a4d22e
activity workflow run      31802738559
activity workflow head     377fed2ffb7da7dcfef10109d39658de6516bddb
counts artifact id         9219943258
counts artifact zip SHA    ad5f6bd04d124344e99aaecafd19ad2a5c7480b973984aa3bc78934e814d0b66
aggregate result file SHA  effa269e1a55cd1643c6d5c8f2dff7128a9ac6188ada6d48079efc2e511538b4
```

## Phase 6C — active evidence route

Phase 6C is a fresh source-research route, not a repair or extension of the Phase 6B activity test.

```text
doctrine stream            CRTOLOGY_2026_RESEARCH
primary source              ROMEO-2026-CRTOLOGY-01
source title                CRTology episode 1: SS
video id                    4DZWbCzEvhM
source identity             CONFIRMED
first-party provenance      CONFIRMED
technical meaning of SS     UNRESOLVED
new alpha candidate         NOT SELECTED
```

The existing 2025 doctrine remains versioned as `CRT_SECRETS_2025`. New 2026 statements may not silently rewrite the frozen historical strategy. Any extracted delta must first be classified as `CLARIFICATION`, `REFINEMENT`, `NEW_OPTIONAL_BRANCH`, `SUPERSEDING_RULE`, `NON_ALPHA_CONTEXT`, or `UNRESOLVED`.

Gate 6C-1 remains open until direct first-party transcript/caption/frame evidence is sufficient to define the technical meaning and causal semantics of `SS` without acronym guessing or secondary-source substitution.

Canonical Phase 6C records:

- `research/romeo/phase6c/PHASE_6C_RESEARCH_CHARTER.md`
- `research/romeo/phase6c/CRTOLOGY_01_EVIDENCE_GATE.md`
- `docs/checklists/phase-6c.md`
- `research/romeo/SOURCE_REGISTRY.csv`

## Current handoff

```text
Phase 6B                         COMPLETE — INSUFFICIENT_MULTI_MARKET_SAMPLE
Phase 6C                         IN PROGRESS — PRIMARY-SOURCE EVIDENCE GATE
Phase 6C branch                  agent/phase-6c-crtology-evidence
2025 doctrine                    PRESERVED
2026 doctrine stream             CRTOLOGY_2026_RESEARCH
Primary source                   ROMEO-2026-CRTOLOGY-01
Source identity                  CONFIRMED
Technical meaning of SS          UNRESOLVED
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

## Canonical Phase 6B records

- `docs/checklists/phase-6b.md`
- `experiments/phase6b/P6B_MULTI_MARKET_ACTIVITY_PROTOCOL_V1.md`
- `experiments/phase6b/P6B_ALL_GAP_S5_UNIVERSE_001.md`
- `experiments/phase6b/P6B_TRUSTED_DATASET_FREEZE_001.json`
- `experiments/phase6b/P6B_TRUSTED_DATASET_FREEZE_001.md`
- `experiments/phase6b/P6B_MULTI_MARKET_ACTIVITY_RESULT_001.json`
- `experiments/phase6b/P6B_MULTI_MARKET_ACTIVITY_RESULT_001.md`
- `src/romeo_crt_engine/market_data/trusted_oanda_dataset_v2.py`
- `scripts/build_oanda_trusted_dataset.py`
- `scripts/run_phase6b_detector_activity.py`
