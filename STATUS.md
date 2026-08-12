# Project Status

Updated: 2026-08-12

| Phase | Status | Primary exit condition |
|---|---|---|
| 0 — Engineering foundation | **COMPLETE** | Reproducible dev + CI + logging/storage/experiment contracts |
| 1 — Romeo corpus / reconciliation | **COMPLETE** | Evidence-indexed corpus + reconciled doctrine + explicit evidence debts |
| 2 — Formal CRT spec | **COMPLETE — FROZEN_FOR_VALIDATION** | Deterministic CRT v0.1 with no unresolved active-path predicates |
| 3 — Market data | **COMPLETE** | Provider-backed trusted/reproducible D1/H1 dataset |
| 4 — CRT detector | **READY TO START** | Reproduce frozen strategy and fixtures on canonical data |
| 5 — Backtester | Not started | Deterministic cost-aware simulator |
| 6 — Validation | Not started | Written robustness decision |
| 7 — Paper trading | Not started | Stable realtime semantics |
| 8 — Learning engine | Not started | OOS incremental value |
| 9 — Shadow trading | Not started | Production-like readiness |
| 10 — Controlled live | **NOT AUTHORIZED** | Explicit approval + canary gates |

## Current frozen pair

```text
Strategy  CRT-C3-D1-H1-M1-BEAR-v0.1
Dataset   ee1300f0da50e4debcbbc3b7
```

Neither identifier is a profitability claim.

## Phase 3 completion

Phase 3 is complete for the first approved provider route.

Route:

```text
Binance Public Data
 -> Binance Spot BTCUSDT
 -> DAILY 1m provider archives
 -> checksum + REST verification
 -> normalized UTC M1
 -> exact elapsed-hour H1
 -> New-York local-midnight D1
 -> immutable manifest/receipt
```

Frozen Phase-4 reproduction dataset:

```text
dataset_version         ee1300f0da50e4debcbbc3b7
manifest_sha256          eaf828ee3acc8adf9e3b931cc6a55d385b0be61b58ae72f01205b3f6034a2141
normalized_sha256        86f6f69176e68655032f3d12910572214de2fa04266c5615146ae03e9f414fc2
market_data_code_sha256  8fbcbb435ce47a405f3500a66935f633136669750cfbe2e014ce1649d4b6140d
dependency_lock_sha256   13653ec2f358aa078fb3a4189299cc8e1f4b71e930cdc3141a8e044de14effa5
```

Provider-backed smoke evidence:

```text
Provider Smoke run  31642788087
Job                 94269168670
Result              SUCCESS
Raw M1              2,880
Canonical H1        48
Complete NY D1      1
```

Canonical Phase-3 artifacts:

- `docs/MARKET_DATA.md`
- `docs/adr/ADR-005-binance-btcusdt-first-market-data-route.md`
- `docs/PHASE_3_COMPLETION_REPORT.md`
- `docs/reviews/PHASE_3_GATE_REVIEW.md`
- `data/manifests/PHASE3_BTCUSDT_EE1300F0DA50E4DEBCBBC3B7.json`
- `data/manifests/PHASE3_BTCUSDT_EE1300F0DA50E4DEBCBBC3B7_EVIDENCE.json`
- `src/romeo_crt_engine/market_data/`
- `src/romeo_crt_engine/storage/local.py`
- `scripts/ingest_binance_spot.py`
- `requirements.lock`

### Phase-3 guarantees

- provider raw files are SHA-256 verified and retained immutably;
- checksum-only trust is insufficient; provider REST verification is required per raw archive;
- duplicate, out-of-order, gap, future and illegal-OHLC states fail closed;
- internal chronology is UTC;
- H1 spans exactly 3,600 elapsed seconds;
- D1 follows `America/New_York` local midnight and correctly supports 23/24/25-hour days;
- provider-native H1/D1 are not substituted for canonical bars;
- data correction creates a new dataset version;
- canonical dataset identity is separated from acquisition receipt identity;
- dependency and market-data code fingerprints are part of dataset identity;
- no strategy outcome is used to select or repair data.

### Accepted Phase-3 limitations

- first route is BTCUSDT Spot only;
- no bid/ask or spread history in the chosen archive route;
- `exchangeInfo` is snapshot-at-ingestion, not historical exchange-filter history;
- `ee1300...` is a compact detector-reproduction dataset, not the full later OOS/validation sample;
- non-24/7 instruments need venue-aware closure/session policies in future provider routes.

## Phase 2 frozen strategy

Frozen candidate:

```text
CRT-C3-D1-H1-M1-BEAR-v0.1
```

Lifecycle:

```text
FROZEN_FOR_VALIDATION
```

Core frozen boundary:

```text
Doctrine                    CRT_SECRETS_2025
Direction                   BEARISH ONLY
Parent timeframe            D1
Execution timeframe         H1
Source timezone             America/New_York
Setup family                Candle-3 reaction from C1 CRTH
Entry model                 Model #1 core
Primary target              C1 midpoint / 50%
Unknown required state      NO_SIGNAL
Countertrend                disabled
SMT substitution            disabled
KOD                         excluded
True MSS                    excluded
Time exits                  excluded
```

Frozen project parameters remain:

```text
P2-PARAM-M1-THICK-050 = body/full_range >= 0.50
P2-PARAM-STOP-1TICK   = structural high + one instrument tick
```

No Phase-3 implementation changed them.

## What completion does NOT mean

The project is still:

- **NOT proven profitable**;
- **NOT paper-ready**;
- **NOT shadow-ready**;
- **NOT live-ready**.

`LIVE_TRADING_AUTHORIZED = false` remains unchanged.

## Phase 4 entry gate

Phase 4 may start with these hard constraints:

1. consume only canonical bars from a declared trusted dataset version;
2. start with strategy `CRT-C3-D1-H1-M1-BEAR-v0.1` and dataset `ee1300f0da50e4debcbbc3b7`;
3. do not reinterpret strategy predicates because the real dataset yields few/no signals;
4. convert canonical data into detector inputs without changing timestamps/OHLC;
5. produce deterministic accepted/rejected reason codes and rule evidence;
6. reproduce existing synthetic strategy fixtures first;
7. add real-data positive/negative fixtures without hindsight labeling;
8. keep detection separate from backtest fill/P&L logic;
9. preserve strategy version, dataset version, code version and evidence IDs in detector outputs;
10. do not begin profitability claims until detector/data integrity gates pass.

## Immediate next actions — Phase 4

1. Define canonical-bar-to-CRT detector input adapters.
2. Implement deterministic rolling C1/C2/C3 detection over trusted D1/H1 chronology.
3. Emit an explanation object for every candidate/rejection.
4. Reproduce committed Phase-2 positive/negative fixtures through the detector entry point.
5. Run the detector over `ee1300f0da50e4debcbbc3b7` as a data-integration fixture.
6. Add source-derived real-market fixtures when evidence is available.
7. Independently audit for future-bar leakage and detector/spec drift.
8. Freeze Phase-4 detector version only after those gates pass.
