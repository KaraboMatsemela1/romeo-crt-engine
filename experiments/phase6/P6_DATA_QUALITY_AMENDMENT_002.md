# P6 Data Quality Amendment 002 — Provider-Authenticated Archive Exclusion

Status: **FROZEN BEFORE DEV DETECTOR / P&L ACCESS**  
Protocol: `P6-VALIDATION-PROTOCOL-v1`  
Window: `P6-DEV-001` (`2019-01-01` through `2022-12-31`)  
Evidence run: GitHub Actions `31680131009`, job `94383466267`

## Trigger

The Phase-6 DEV workflow intentionally failed during trusted-data construction, before detector or backtest steps executed. A checksum-authenticated scan of all requested Binance Spot BTCUSDT daily 1-minute archives found additional incomplete or malformed provider days beyond the independently evidenced 2019-03-12 venue closure already governed by `P6-DATA-QUALITY-AMENDMENT-001`.

No Phase-6 DEV detector count, TradePlan count, trade result, P&L, expectancy, drawdown, or cost-scenario outcome had been accessed when this amendment was written.

## General policy

For `P6-DEV-001` and every later Phase-6 window unless superseded **before that window is opened**:

1. Every requested daily archive must first pass the provider-published SHA-256 checksum.
2. A checksum-authenticated archive is then tested against the strict canonical provider contract: exact 12-column schema, supported timestamp units, exact one-minute kline close semantics, and expected minute chronology after separately evidenced venue closures.
3. If an archive fails that strict contract with `INCOMPLETE_BUCKET` or `PROVIDER_SCHEMA`, the **entire UTC archive is excluded from normalization**.
4. Exclusion is conservative. Good-looking minutes from that UTC archive are not salvaged.
5. The excluded raw archive remains immutable and auditable with its provider checksum, date, filename, SHA-256, failure code, and chronology diagnostic.
6. Excluded archives receive checksum verification evidence only; they are not used as REST sample archives because they cannot first satisfy the strict canonical parser.
7. No missing or malformed minute is interpolated, forward-filled, back-filled, synthesized, or inferred.
8. H1 bars are built only from 60 actual accepted M1 observations.
9. Any New-York D1 intersecting an excluded UTC archive is omitted. No partial D1 may become C1, C2, or C3.
10. The frozen CRT strategy already requires C1/C2/C3 to be consecutive New-York D1 candles. Therefore a data gap cannot be bridged into a valid parent sequence.
11. An archive exclusion is **not** called an exchange/venue closure unless independent first-party evidence establishes that fact. `P6-DATA-QUALITY-AMENDMENT-001` remains the separately evidenced venue-closure case.
12. If Binance later publishes corrected bytes for an excluded archive, its SHA-256 changes and the resulting dataset must be a new immutable dataset version; this amendment must not silently reinterpret the old version.
13. OOS and CONFIRM remain unopened while DEV data quality is being resolved.

This rule is outcome-independent: it is based only on provider-authenticated data integrity, not on whether excluding a date improves or harms strategy results.

## Complete DEV anomaly inventory discovered before outcomes

The scan identified the following provider-authenticated archives. Times are UTC. For records marked `irregular`, the preceding provider kline also had a non-60-second raw close duration and therefore the whole archive is excluded rather than attempting a partial repair.

| UTC archive | Provider diagnostic |
|---|---|
| 2019-05-15 | 840 rows; missing `03:00–13:00` (600m) |
| 2019-06-07 | 1,379 rows; missing `21:14–22:15` (61m); irregular 21:13 row |
| 2019-08-15 | 960 rows; missing `02:00–10:00` (480m) |
| 2019-11-13 | 1,297 rows; missing `02:00–04:20` (140m) and `05:30–05:33` (3m) |
| 2019-11-25 | 1,320 rows; missing `02:00–04:00` (120m) |
| 2020-02-09 | 1,380 rows; missing `02:00–03:00` (60m) |
| 2020-02-19 | 1,086 rows; missing `11:36–17:30` (354m); irregular 11:35 row |
| 2020-03-04 | 1,312 rows; missing `09:22–11:30` (128m); irregular 09:21 row |
| 2020-04-25 | 1,290 rows; missing `02:00–04:30` (150m) |
| 2020-06-28 | 1,230 rows; missing `02:00–05:30` (210m) |
| 2020-11-30 | 1,380 rows; missing `06:00–07:00` (60m) |
| 2020-12-21 | 1,188 rows; missing `13:48–18:00` (252m); irregular 13:47 row |
| 2020-12-25 | 1,380 rows; missing `02:00–03:00` (60m) |
| 2021-02-11 | 1,361 rows; missing `03:41–05:00` (79m); irregular 03:40 row |
| 2021-03-06 | 1,350 rows; missing `02:00–03:30` (90m) |
| 2021-04-20 | 1,290 rows; missing `02:00–04:30` (150m) |
| 2021-04-25 | 1,156 rows; missing `04:01–08:45` (284m); irregular 04:00 row |
| 2021-08-13 | 1,170 rows; missing `02:00–06:30` (270m); irregular 01:59 row |
| 2021-09-29 | 1,320 rows; missing `07:00–09:00` (120m) |
| 2021-12-24 | 1,440 rows but malformed raw close semantics at 04:59 row |

No additional strict-provider anomalies were reported in the requested DEV archives for 2022 by this scan.

## Relationship to Amendment 001

`2019-03-12 02:00–08:00 UTC` remains handled under `P6-DATA-QUALITY-AMENDMENT-001` as an independently evidenced scheduled Binance trading suspension. Unaffected minutes on that archive may remain because the exact closure interval is independently specified.

The 20 records above use the more conservative whole-archive exclusion policy because the authenticated provider bytes establish missing/malformed observations but do not, by themselves, establish the operational cause.

## Outcome-access gate

`P6_DEV_OUTCOME_ACCESS_AUTHORIZED = false` remains mandatory until all of the following are committed and CI-green:

- whole-archive exclusion implementation;
- tests proving excluded raw bytes are preserved but never normalized;
- tests proving affected New-York D1 parents are removed;
- tests proving detector parent chronology cannot bridge the resulting gaps;
- deterministic monthly REST sampling selects only strict-parser-eligible archives;
- the exact post-exclusion M1/H1/D1 row counts and exclusion-ledger SHA are captured by a **data-only** workflow run and frozen in this experiment history.

Only after those data-only facts are frozen may the same preregistered DEV window reach detector/backtest execution.

## Safety

This amendment does not authorize paper, shadow, or live trading and makes no profitability claim.
