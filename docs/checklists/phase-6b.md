# Phase 6B — Candidate Revision Checklist

**Status:** **IN PROGRESS — TRUSTED DATASET CONSTRUCTION**  
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
- [x] Persist V2 reconciliation evidence for all 16 shards in CI artifacts.
- [x] Inventory every missing interval from the persisted V2 evidence set.
- [x] Probe every XAU_USD M1 gap of 60 minutes or less for 2019-2022 at S5 granularity.
- [x] Confirm all 17,490 probed XAU_USD short gaps are `NO_PRICE_OBSERVATION` with zero `UNRESOLVED_PROVIDER_GAP` classifications.
- [x] Preserve the remaining 477 longer XAU_USD gaps as unqualified rather than extrapolating the short-gap result.
- [x] Add a fail-closed all-gap S5 probe path that reuses provider-safe six-hour request buckets.
- [x] Require an all-gap evidence run to classify exactly the raw M1 missing-interval count before it can support qualification.
- [x] Complete the controlled XAU_USD/2022 all-gap S5 pilot: 827/827 gaps, 172,923/172,923 minutes, 0 unresolved.
- [x] Expand all-gap finer-granularity classification to every frozen instrument/year shard using the pilot-validated method.
- [x] Reconcile every omitted observation using finer-granularity `NO_PRICE_OBSERVATION` evidence without inventing session/holiday closures.
- [x] Preserve the fail-closed unresolved/provider-missing policy; final universe result contains zero unresolved intervals.
- [x] Implement a fail-closed adapter from complete S5 evidence to approved `MarketGapV2(NO_PRICE_OBSERVATION)` policy.
- [x] Reject partial, unresolved, coordinate-mismatched or digest-unbound S5 evidence at the aggregation boundary.
- [ ] Re-fetch/reconstruct complete canonical MID/M1 history for each raw-gap-qualified instrument and bind it to the sealed evidence.
- [ ] Build deterministic H1 and New-York-midnight D1 datasets only after approved gap-policy construction succeeds.
- [ ] Freeze provider/instrument/session/price-quantum identity for each accepted instrument.
- [ ] Freeze normalized H1/D1 digest and row counts for each accepted instrument.
- [ ] Freeze one detector-facing `P6B_CANONICAL_PRICE_DATASET_V2` identity with `quality_status = TRUSTED` per accepted instrument.
- [ ] Freeze the exact trusted instrument set before detector activity counts are opened.

### Sealed V2 raw evidence inventory

```text
complete M1 candles       5,529,393
missing intervals           122,626
missing minutes           2,885,967
V2 evidence shards            16/16
raw price artifacts        EPHEMERAL / DELETED
```

Per instrument raw inventory:

```text
EUR_USD      1,428,155 complete M1 | 37,770 gaps | 675,685 missing minutes
XAU_USD      1,394,064 complete M1 | 17,967 gaps | 709,776 missing minutes
NAS100_USD   1,392,496 complete M1 | 11,111 gaps | 711,344 missing minutes
SPX500_USD   1,314,678 complete M1 | 55,778 gaps | 789,162 missing minutes
```

### Universe-wide all-gap result

OANDA Provider Qualification run #27 (`31778696775`) completed successfully on attempt #2 at evidence commit `b04899e03931eda642af12e39926a84c310482f6`.

```text
all-gap evidence shards             16 / 16 PASS
raw missing intervals               122,626
S5 classified intervals             122,626
NO_PRICE_OBSERVATION intervals      122,626
UNRESOLVED_PROVIDER_GAP intervals         0
raw missing minutes               2,885,967
NO_PRICE_OBSERVATION minutes      2,885,967
UNRESOLVED_PROVIDER_GAP minutes           0
raw-gap-qualified instruments          4 / 4
```

Per instrument:

```text
EUR_USD      37,770 / 37,770 gaps | 675,685 / 675,685 minutes | unresolved 0
XAU_USD      17,967 / 17,967 gaps | 709,776 / 709,776 minutes | unresolved 0
NAS100_USD   11,111 / 11,111 gaps | 711,344 / 711,344 minutes | unresolved 0
SPX500_USD   55,778 / 55,778 gaps | 789,162 / 789,162 minutes | unresolved 0
```

The first XAU_USD/2019 execution was interrupted technically. The failed job alone was rerun on the same frozen evidence commit; attempt #2 passed with 12,331/12,331 gaps and 188,489/188,489 missing minutes classified `NO_PRICE_OBSERVATION`, zero unresolved, and `EXACT_PROVIDER_VALUE_MATCH`.

Raw-gap qualification is sealed in `experiments/phase6b/P6B_ALL_GAP_S5_UNIVERSE_001.md`.

### Canonical artifacts

- `experiments/phase6b/P6B_OANDA_HISTORY_QUALIFICATION_PROTOCOL_V1.md`
- `experiments/phase6b/P6B_OANDA_HISTORY_SHARD_EXECUTION_V1.md`
- `experiments/phase6b/P6B_OANDA_LOCAL_COLLECTION_RUNBOOK_V1.md`
- `experiments/phase6b/P6B_OANDA_HISTORICAL_SESSION_EVIDENCE_001.md`
- `experiments/phase6b/P6B_OANDA_HISTORY_SMOKE_001.md`
- `experiments/phase6b/P6B_OANDA_HISTORY_COLLECTION_GATE_001.md`
- `experiments/phase6b/P6B_OANDA_EUR_USD_2019_2022_COLLECTION_AND_ABSENCE_PROBE_001.md`
- `experiments/phase6b/P6B_ALL_GAP_S5_PILOT_001.md`
- `experiments/phase6b/P6B_ALL_GAP_S5_UNIVERSE_001.md`
- `experiments/phase6b/P6B_RECONCILIATION_STATUS_001.md`
- `research/romeo/phase6b/PRIMARY_SOURCE_PASS_003.md`
- `src/romeo_crt_engine/market_data/gap_reconciliation_v2.py`
- `src/romeo_crt_engine/market_data/s5_gap_policy_v2.py`
- `scripts/collect_oanda_history_shard.py`
- `scripts/probe_oanda_all_gaps_s5.py`
- `tests/unit/test_history_qualification_v2_phase6b.py`
- `tests/unit/test_s5_gap_policy_v2_phase6b.py`

## E. Detector-only activity protocol

Frozen thresholds remain:

```text
accepted instruments      >= 2
contributing instruments  >= 2
pooled TradePlans         >= 30
backtester                PROHIBITED
P&L                       PROHIBITED
```

Detector execution remains blocked until the exact trusted historical dataset set is frozen. `RAW_GAP_QUALIFIED` is not equivalent to `TRUSTED`.

## Current handoff

```text
Phase 6B                         IN PROGRESS — TRUSTED DATASET CONSTRUCTION
Alpha changes                    NONE AUTHORIZED
Frozen OANDA universe            4 SYMBOLS
Historical M1 smoke              PASS 4/4, 60/60 EACH
Yearly raw validation            PASS 16/16
Independent refetch              PASS 4/4 PER INSTRUMENT
Raw artifacts                    EPHEMERAL / DELETED AFTER VALIDATION
V2 reconciliation evidence       PASS 16/16 PERSISTED
Exact missing-interval inventory PASS 122,626 INTERVALS
Universe all-gap classification  PASS 16/16; 122,626 / 122,626; 0 UNRESOLVED
Missing-minute reconciliation    PASS 2,885,967 / 2,885,967; 0 UNRESOLVED
Raw-gap-qualified instruments    PASS 4/4
Historical gap classification    COMPLETE
Trusted H1 / NY-D1 datasets      PENDING / NEXT
Canonical TRUSTED identities     PENDING
Exact trusted universe freeze    PENDING
Detector activity counts         NOT OPENED
Multi-market P&L                 NOT AUTHORIZED
v0.1 OOS / CONFIRM               UNOPENED
Phase 7                          BLOCKED
Live trading                     NOT AUTHORIZED
```
