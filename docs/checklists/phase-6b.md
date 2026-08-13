# Phase 6B — Candidate Revision Checklist

**Status:** **IN PROGRESS — HISTORICAL OANDA DATA QUALIFICATION**  
**Active research target:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`  
**Underlying frozen alpha:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Preserved failed research path:** `CRT-C3-D1-H1-M1-BULL-v0.2-RESEARCH` -> `EVIDENCE_INSUFFICIENT`  
**Phase 7:** **BLOCKED UNTIL A FUTURE CANDIDATE PASSES FULL VALIDATION**

## A. Historical integrity

- [x] Preserve v0.1 strategy, detector, simulator and Phase-6 evidence unchanged.
- [x] Preserve v0.1 `INSUFFICIENT_EVIDENCE` result.
- [x] Keep v0.1 OOS unopened.
- [x] Keep v0.1 CONFIRM unopened.
- [x] Keep v0.1 parameter optimization prohibited.
- [x] Keep paper, shadow and live trading unauthorized.

## B. Bullish successor evidence gate

- [x] Close Gate 6B-1 as **`EVIDENCE_INSUFFICIENT`** without opening bullish outcomes.

## C. Active successor — multi-market observation expansion

- [x] Preserve the frozen bearish v0.1 alpha rules without relaxation.
- [x] Freeze the source-supported OANDA universe before detector activity:
  - [x] `EUR_USD`
  - [x] `XAU_USD`
  - [x] `NAS100_USD`
  - [x] `SPX500_USD`
- [x] Prohibit post-count or post-P&L instrument cherry-picking.

## D. Historical-data qualification

Protocol: `P6B-OANDA-HISTORY-QUALIFICATION-V1`.

- [x] Freeze MID/M1, unsmoothed retrieval.
- [x] Freeze UTC raw interval `2019-01-01T00:00:00Z .. 2023-01-01T00:00:00Z` exclusive.
- [x] Freeze deterministic 4500-minute pages with 5000-candle hard maximum.
- [x] Support account-redacted request/raw-response hashes.
- [x] Support provider-confirmed empty-page provenance without synthetic prices.
- [x] Support raw leading/internal/trailing missing-interval enumeration.
- [x] Freeze four independent one-hour provider-value re-fetch windows before complete collection.
- [x] Execute real 2019 historical MID/M1 smoke against all four frozen symbols.
- [x] Confirm the smoke returns 60/60 complete M1 candles for each symbol.
- [x] Preserve only counts/hashes in repository smoke evidence.
- [x] Record dated OANDA evidence that index hours changed inside DEV on 2021-06-28.
- [x] Prohibit projecting current OANDA hours backward across the complete DEV interval.
- [ ] Collect complete sealed raw DEV M1 history for all four instruments.
- [ ] Execute 4/4 independent re-fetch comparisons per instrument.
- [ ] Inventory every missing interval.
- [ ] Reconcile every removed expected observation to date-valid session/holiday evidence.
- [ ] Leave unresolved/provider-missing intervals fail-closed.
- [ ] Build trusted H1 and New-York-midnight D1 datasets.
- [ ] Freeze one detector-facing `P6B_CANONICAL_PRICE_DATASET_V2` identity per trusted instrument.

Canonical artifacts:

- `experiments/phase6b/P6B_OANDA_HISTORY_QUALIFICATION_PROTOCOL_V1.md`
- `experiments/phase6b/P6B_OANDA_HISTORICAL_SESSION_EVIDENCE_001.md`
- `experiments/phase6b/P6B_OANDA_HISTORY_SMOKE_001.md`
- `experiments/phase6b/P6B_OANDA_HISTORY_COLLECTION_GATE_001.md`
- `research/romeo/phase6b/PRIMARY_SOURCE_PASS_003.md`

## E. Detector-only activity protocol

Frozen thresholds remain:

```text
accepted instruments      >= 2
contributing instruments  >= 2
pooled TradePlans         >= 30
backtester                PROHIBITED
P&L                       PROHIBITED
```

Detector execution remains blocked until trusted historical datasets exist.

## Current handoff

```text
Phase 6B                     IN PROGRESS
Alpha changes                NONE AUTHORIZED
Frozen OANDA universe        4 SYMBOLS
Historical M1 smoke          PASS 4/4, 60/60 EACH
Full raw 2019-2022 M1        PENDING
Historical gap reconciliation PENDING
Trusted H1 / NY-D1 datasets  PENDING
Detector activity counts     NOT OPENED
Multi-market P&L             NOT AUTHORIZED
v0.1 OOS / CONFIRM           UNOPENED
Phase 7                      BLOCKED
Live trading                 NOT AUTHORIZED
```
