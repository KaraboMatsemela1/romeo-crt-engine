# Phase 6B — Candidate Revision Checklist

**Status:** **IN PROGRESS — RECONCILIATION EVIDENCE V2**  
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

Protocol baseline: `P6B-OANDA-HISTORY-QUALIFICATION-V1`.
Observation/reconciliation correction: `P6B_OANDA_OBSERVATION_POLICY_V2`.

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
- [x] Freeze 16 yearly execution shards: four UTC years for each frozen instrument.
- [x] Preserve one preregistered independent re-fetch window per yearly shard.
- [x] Implement exact raw-gap reconciliation.
- [x] Reject approved closure evidence that leaves raw missing minutes unexplained.
- [x] Reject approved closure evidence that extends into provider-observed minutes.
- [x] Regression-test exact reconciliation and preserve BTCUSDT behavior.
- [x] Implement practice-only yearly-shard collector.
- [x] Restrict collector to the frozen four symbols and years 2019-2022.
- [x] Persist credentials only in runtime environment; manifests retain redacted account scope.
- [x] Preserve page provenance, raw missing intervals and mapped re-fetch result per shard.
- [x] Add local collection runbook and Git-ignore raw output directory.
- [x] Execute first full shard: `EUR_USD / 2019` through GitHub Actions secrets.
- [x] Validate first full-shard manifest/redaction.
- [x] Collect and independently validate all 16 frozen raw shards.
- [x] Achieve 4/4 independent re-fetch comparisons per instrument.
- [x] Discover through cross-granularity probes that absent M1 timestamps can represent zero provider price observations, not only session/holiday gaps.
- [x] Freeze V2 observation states: `EXPECTED_MARKET_CLOSURE`, `NO_PRICE_OBSERVATION`, `UNRESOLVED_PROVIDER_GAP`.
- [x] Keep synthetic prices, forward fill and timestamp-shape-only classification prohibited.
- [x] Extend the collector to emit credential-free `P6B_OANDA_RECONCILIATION_EVIDENCE_V2` with exact missing-interval coordinates and provenance hashes.
- [ ] Persist V2 reconciliation evidence for all 16 shards in CI artifacts.
- [ ] Inventory every missing interval from the persisted V2 evidence set.
- [ ] Reconcile every omitted observation to date-valid session/holiday evidence or finer-granularity `NO_PRICE_OBSERVATION` evidence.
- [ ] Leave unresolved/provider-missing intervals fail-closed.
- [ ] Build trusted H1 and New-York-midnight D1 datasets only for independently `TRUSTED` instruments.
- [ ] Freeze one detector-facing `P6B_CANONICAL_PRICE_DATASET_V2` identity per trusted instrument.

Canonical artifacts:

- `experiments/phase6b/P6B_OANDA_HISTORY_QUALIFICATION_PROTOCOL_V1.md`
- `experiments/phase6b/P6B_OANDA_HISTORY_SHARD_EXECUTION_V1.md`
- `experiments/phase6b/P6B_OANDA_LOCAL_COLLECTION_RUNBOOK_V1.md`
- `experiments/phase6b/P6B_OANDA_HISTORICAL_SESSION_EVIDENCE_001.md`
- `experiments/phase6b/P6B_OANDA_HISTORY_SMOKE_001.md`
- `experiments/phase6b/P6B_OANDA_HISTORY_COLLECTION_GATE_001.md`
- `experiments/phase6b/P6B_OANDA_EUR_USD_2019_2022_COLLECTION_AND_ABSENCE_PROBE_001.md`
- `research/romeo/phase6b/PRIMARY_SOURCE_PASS_003.md`
- `src/romeo_crt_engine/market_data/gap_reconciliation_v2.py`
- `scripts/collect_oanda_history_shard.py`
- `tests/unit/test_history_qualification_v2_phase6b.py`

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
Phase 6B                         IN PROGRESS — RECONCILIATION EVIDENCE V2
Alpha changes                    NONE AUTHORIZED
Frozen OANDA universe            4 SYMBOLS
Historical M1 smoke              PASS 4/4, 60/60 EACH
Yearly raw validation            PASS 16/16
Independent refetch              PASS 4/4 PER INSTRUMENT
Raw artifacts                    EPHEMERAL / DELETED AFTER VALIDATION
V2 reconciliation evidence       CI PERSISTENCE IN PROGRESS
Historical gap reconciliation    PENDING V2 EVIDENCE INVENTORY
Trusted H1 / NY-D1 datasets      PENDING
Detector activity counts         NOT OPENED
Multi-market P&L                 NOT AUTHORIZED
v0.1 OOS / CONFIRM               UNOPENED
Phase 7                          BLOCKED
Live trading                     NOT AUTHORIZED
```
