# Phase 6B OANDA Historical Data Qualification Protocol v1

**Protocol ID:** `P6B-OANDA-HISTORY-QUALIFICATION-V1`  
**Status:** FROZEN BEFORE RAW DEV DATA ACCESS  
**Date frozen:** 2026-08-13  
**Candidate:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`  
**Alpha:** `CRT-C3-D1-H1-M1-BEAR-v0.1` unchanged

## 1. Purpose

Qualify OANDA practice historical price data for the already-frozen four-instrument Phase-6B universe before any multi-market detector activity count or strategy outcome is opened.

This protocol is a **data-quality protocol**, not a strategy performance protocol.

## 2. Frozen universe

No post-data instrument inclusion/exclusion is allowed.

```text
EUR_USD
XAU_USD
NAS100_USD
SPX500_USD
```

Universe source: `experiments/phase6b/P6B_OANDA_UNIVERSE_FREEZE_001.md`.

## 3. Frozen observation contract

```text
provider             OANDA_V20
environment          practice
account scope        runtime-only / redacted
price component      MID / price=M
granularity          M1
smooth               false
DEV start             2019-01-01T00:00:00Z
DEV end               2023-01-01T00:00:00Z (exclusive)
default page window   4500 minutes
max page window       5000 minutes
synthetic prices      prohibited
```

The strategy D1 remains project-owned New-York-midnight D1; provider-native Daily candles may not redefine it.

## 4. Frozen raw-page provenance

Every request page must retain, at minimum:

- instrument;
- MID/M1 identity;
- requested UTC start/end;
- retrieval timestamp;
- secret/account-redacted request SHA-256;
- raw response SHA-256;
- complete-candle count.

A provider-confirmed response with the correct instrument, `M1` granularity and an empty `candles` array may represent a legitimate fully closed request window and must be retained as an **empty provenance page**, not fabricated into price data.

Any malformed identity/schema response remains fail-closed.

## 5. Frozen canonical raw-value stream

The normalized M1 value stream contains only:

```text
instrument
price_component
open_time_utc
close_time_utc
open
high
low
close
price_count
complete
```

Page-response SHA values are deliberately excluded from the normalized provider-value digest so an independent provider re-fetch can be compared by values rather than by HTTP payload serialization.

OANDA `volume` remains typed as provider `PRICE_COUNT`; it is not converted into exchange volume or trade count.

## 6. Frozen independent re-fetch samples

These four one-hour windows were selected before provider-backed DEV activity access:

```text
2019-03-12T14:00:00Z .. 2019-03-12T15:00:00Z
2020-09-15T14:00:00Z .. 2020-09-15T15:00:00Z
2021-04-13T14:00:00Z .. 2021-04-13T15:00:00Z
2022-10-18T14:00:00Z .. 2022-10-18T15:00:00Z
```

Each accepted instrument must independently re-request each window after the primary pull.

Gate condition:

```text
4 / 4 re-fetch windows per instrument = exact provider-value match
```

A mismatch blocks `TRUSTED` status until explained and resolved without modifying strategy rules.

## 7. Missing-interval treatment

The raw M1 stream is first treated as a timestamp observation problem.

Every missing interval between the requested boundaries must be enumerated mechanically, including:

- leading boundary gap;
- internal gap;
- trailing boundary gap.

Initial classification for every interval is:

```text
UNRECONCILED
```

A missing interval may be removed from expected observations only after evidence maps it to one of the already-approved categories:

```text
MARKET_CLOSED
SESSION_BREAK
HOLIDAY_OR_EARLY_CLOSE
```

The following remain hard failures for detector-facing trusted data:

```text
PROVIDER_MISSING
UNKNOWN_GAP
UNRECONCILED
```

## 8. Historical session evidence rule

Current OANDA hours may not automatically be backfilled across 2019-2022.

First-party evidence already proves that US Nas 100 / US SPX 500 hours changed during DEV on 2021-06-28. Therefore historical session rules must be date-segmented and reconciled against actual provider gaps.

Canonical evidence ledger:

- `experiments/phase6b/P6B_OANDA_HISTORICAL_SESSION_EVIDENCE_001.md`

## 9. Provider price quantum

Frozen separately before activity access:

```text
EUR_USD      0.00001
XAU_USD      0.001
NAS100_USD   0.1
SPX500_USD   0.1
source       PROVIDER_PRICE_PRECISION_POLICY
```

This is a provider price quantum for the v0.1 stop-buffer interface, not a claim about exchange tick size.

## 10. Trusted dataset gate

An instrument may receive a detector-facing `P6B_CANONICAL_PRICE_DATASET_V2` identity with `quality_status=TRUSTED` only if all of the following hold:

- exact frozen symbol;
- complete sealed primary retrieval;
- deterministic normalized M1 digest;
- page-level provenance complete;
- all 4 independent re-fetch samples exactly match provider values;
- all missing intervals are reconciled to approved historical availability evidence;
- no unexplained/provider-missing gaps remain;
- H1 is deterministically aggregated from actual expected M1 observations;
- New-York-midnight D1 is deterministically aggregated from actual expected M1 observations;
- price quantum is the pre-frozen provider quantum;
- dataset identity/digest is frozen before detector execution.

If any item fails, that instrument is **NOT TRUSTED**. The reason must be preserved; the data rules may not be relaxed because the resulting strategy sample would otherwise be small.

## 11. Cross-instrument gate

The previously frozen activity protocol requires at least two accepted trusted instruments. If fewer than two instruments survive data qualification:

```text
INSUFFICIENT_ELIGIBLE_UNIVERSE
```

and detector counts remain unopened.

If at least two survive, the exact trusted set is frozen before detector activity execution. An instrument may be excluded only for a predeclared data-quality failure—not because of its signal count or profitability.

## 12. Outcome firewall

During this protocol:

```text
CRT detector execution                PROHIBITED
TradePlan counts                      PROHIBITED
reason distributions                  PROHIBITED
backtester                            PROHIBITED
P&L                                   PROHIBITED
win rate                              PROHIBITED
expectancy                            PROHIBITED
profit factor                         PROHIBITED
drawdown                              PROHIBITED
v0.1 OOS / CONFIRM                    UNOPENED
paper / shadow / live                 NOT AUTHORIZED
```

Only provider/data-quality metadata may be inspected.

## 13. Implementation identities frozen at protocol time

The protocol relies on these code paths, subject only to defect fixes that do not weaken the gates:

```text
src/romeo_crt_engine/market_data/providers/oanda_history.py
src/romeo_crt_engine/market_data/history_qualification_v2.py
src/romeo_crt_engine/market_data/session_policy_v2.py
src/romeo_crt_engine/market_data/aggregate_v2.py
src/romeo_crt_engine/market_data/price_data_v2.py
src/romeo_crt_engine/market_data/oanda_price_quantum.py
```

Any substantive policy change requires a new protocol version and must occur before the affected data-quality outcome is used for promotion decisions.
