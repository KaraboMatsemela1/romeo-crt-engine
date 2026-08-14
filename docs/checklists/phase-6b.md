# Phase 6B — Candidate Revision Checklist

**Status:** **COMPLETE — `INSUFFICIENT_MULTI_MARKET_SAMPLE`**  
**Research target:** `CRT-C3-D1-H1-M1-BEAR-v0.2-MULTI-MARKET-RESEARCH`  
**Underlying frozen alpha:** `CRT-C3-D1-H1-M1-BEAR-v0.1`  
**Preserved failed research path:** `CRT-C3-D1-H1-M1-BULL-v0.2-RESEARCH` -> `EVIDENCE_INSUFFICIENT`  
**Phase 7:** **BLOCKED**

## A. Historical integrity

- [x] Preserve v0.1 strategy, detector, simulator, and Phase-6 evidence unchanged.
- [x] Preserve v0.1 `INSUFFICIENT_EVIDENCE` result.
- [x] Keep v0.1 OOS unopened.
- [x] Keep v0.1 CONFIRM unopened.
- [x] Keep v0.1 parameter optimization prohibited.
- [x] Keep paper, shadow, and live trading unauthorized.

## B. Prior bullish successor route

- [x] Close the bullish successor route as **`EVIDENCE_INSUFFICIENT`** without opening outcomes.

## C. Multi-market candidate freeze

- [x] Preserve frozen bearish v0.1 alpha rules without relaxation.
- [x] Freeze MID as the signal price component.
- [x] Freeze the source-supported OANDA universe before detector activity:
  - [x] `EUR_USD`
  - [x] `XAU_USD`
  - [x] `NAS100_USD`
  - [x] `SPX500_USD`
- [x] Prohibit post-count or post-P&L instrument cherry-picking.

## D. Historical provider qualification

Protocol baseline: `P6B-OANDA-HISTORY-QUALIFICATION-V1`.  
Observation/reconciliation policy: `P6B_OANDA_OBSERVATION_POLICY_V2`.

- [x] Freeze OANDA practice MID/M1 unsmoothed retrieval.
- [x] Freeze 2019-2022 yearly raw retrieval shards.
- [x] Freeze deterministic paging and provider-value independent refetch.
- [x] Keep credentials runtime-only and repository evidence credential-free.
- [x] Collect and independently validate all 16 frozen instrument/year shards.
- [x] Achieve 4/4 independent re-fetch comparisons per instrument.
- [x] Enumerate every missing M1 interval exactly.
- [x] Freeze omission states `EXPECTED_MARKET_CLOSURE`, `NO_PRICE_OBSERVATION`, and fail-closed `UNRESOLVED_PROVIDER_GAP`.
- [x] Prohibit synthetic prices, forward fill, and timestamp-shape-only classification.
- [x] Persist exact V2 reconciliation evidence for all 16 shards.
- [x] Validate the all-gap MID/S5 method with the controlled XAU_USD/2022 pilot.
- [x] Expand all-gap S5 classification across the complete frozen universe.
- [x] Classify exactly 122,626 / 122,626 missing intervals.
- [x] Classify exactly 2,885,967 / 2,885,967 missing minutes.
- [x] End with 0 `UNRESOLVED_PROVIDER_GAP` intervals and 0 unresolved minutes.
- [x] Mark all four instruments `RAW_GAP_QUALIFIED`.
- [x] Preserve the XAU_USD/2019 technical retry on the same frozen evidence/workflow semantics.

Sealed raw qualification:

```text
complete M1 candles                    5,529,393
raw missing intervals                    122,626
raw missing minutes                    2,885,967
all-gap evidence shards                    16/16 PASS
NO_PRICE_OBSERVATION intervals           122,626
NO_PRICE_OBSERVATION minutes           2,885,967
UNRESOLVED_PROVIDER_GAP intervals              0
UNRESOLVED_PROVIDER_GAP minutes                0
raw-gap-qualified instruments               4/4
```

Canonical evidence: `experiments/phase6b/P6B_ALL_GAP_S5_UNIVERSE_001.md`.

## E. Canonical New-York DEV coverage

- [x] Recognize that the frozen New-York DEV window maps to `2019-01-01T05:00:00Z .. 2023-01-01T05:00:00Z` exclusive.
- [x] Keep the raw yearly provider qualification boundary at `2023-01-01T00:00:00Z` unchanged.
- [x] Separately qualify only the five-hour canonical tail `2023-01-01T00:00:00Z .. 2023-01-01T05:00:00Z`.
- [x] Qualify the canonical tail 4/4 with exact independent empty refetch and MID/S5 evidence.
- [x] Confirm zero unresolved tail gaps/minutes.
- [x] Do not widen DEV beyond the frozen New-York boundary.

## F. Trusted canonical dataset construction

- [x] Implement fail-closed S5 evidence-to-`MarketGapV2` policy conversion.
- [x] Reject partial, unresolved, coordinate-mismatched, or digest-unbound evidence.
- [x] Re-fetch/reconstruct full canonical MID/M1 history for each raw-gap-qualified instrument.
- [x] Require fresh normalized provider values and fresh gap coordinates to match sealed evidence exactly.
- [x] Derive deterministic H1 data through the approved gap-policy boundary.
- [x] Derive deterministic New-York-midnight D1 data through the approved gap-policy boundary.
- [x] Freeze provider/instrument/session/price-representation precision identity.
- [x] Freeze normalized H1/D1 digest and row counts.
- [x] Emit `P6B_CANONICAL_PRICE_DATASET_V2` with `quality_status = TRUSTED` for all four instruments.
- [x] Reproduce each normalized H1/D1 digest in an independent provider reconstruction before accepting the authoritative build.
- [x] Keep raw M1 provider artifacts unpersisted in the trusted output.

Authoritative trusted build: OANDA Trusted Dataset Build run #3 (`31799895592`).

```text
EUR_USD      H1 24,902 | NY-D1 1,249 | TRUSTED
XAU_USD      H1 23,660 | NY-D1 1,244 | TRUSTED
NAS100_USD   H1 23,604 | NY-D1 1,245 | TRUSTED
SPX500_USD   H1 23,605 | NY-D1 1,245 | TRUSTED
```

- [x] Freeze the exact trusted set before detector counts at commit `8214c31e09d53cffadce453727604e0847a4d22e`.
- [x] Freeze exact artifact IDs, artifact ZIP hashes, H1/D1 hashes, dataset identities, metadata hashes, and price-quantum sources.
- [x] Confirm accepted trusted instruments = 4 >= required 2.

Canonical freeze:

- `experiments/phase6b/P6B_TRUSTED_DATASET_FREEZE_001.json`
- `experiments/phase6b/P6B_TRUSTED_DATASET_FREEZE_001.md`

## G. Detector-only activity gate

Frozen thresholds:

```text
accepted instruments      >= 2
contributing instruments  >= 2
pooled TradePlans         >= 30
backtester                PROHIBITED
P&L                       PROHIBITED
```

- [x] Commit the exact trusted-universe freeze before opening counts.
- [x] Implement counts-only activity runner without importing/invoking the backtester.
- [x] Restrict output to D1 count, candidate count, NO_SIGNAL count, TradePlan count, ReasonCode counts, and audit hashes.
- [x] Persist no routine candidate timestamps or trade geometry.
- [x] Run the activity gate only against exact frozen artifact IDs/hashes.
- [x] Revalidate trusted artifact ZIP SHA, H1/D1 file SHA, identities, row counts, and normalized digest before detector invocation.
- [x] Execute Phase 6B Detector Activity Gate run #1 (`31802738559`).
- [x] Confirm accepted instruments = 4 / required 2.
- [x] Confirm contributing instruments = 3 / required 2.
- [x] Confirm pooled detector candidates = 4,975.
- [x] Confirm pooled TradePlans = 7 / required 30.
- [x] Confirm backtester was not invoked.
- [x] Confirm P&L was not accessed.
- [x] Close gate as **`INSUFFICIENT_MULTI_MARKET_SAMPLE`**.

Per instrument:

```text
EUR_USD      D1 1,249 | candidates 1,247 | NO_SIGNAL 1,244 | TradePlans 3
NAS100_USD   D1 1,245 | candidates 1,243 | NO_SIGNAL 1,241 | TradePlans 2
SPX500_USD   D1 1,245 | candidates 1,243 | NO_SIGNAL 1,241 | TradePlans 2
XAU_USD      D1 1,244 | candidates 1,242 | NO_SIGNAL 1,242 | TradePlans 0
POOLED                   candidates 4,975 | NO_SIGNAL 4,968 | TradePlans 7
```

Canonical decision:

- `experiments/phase6b/P6B_MULTI_MARKET_ACTIVITY_RESULT_001.json`
- `experiments/phase6b/P6B_MULTI_MARKET_ACTIVITY_RESULT_001.md`

## H. Terminal governance

- [x] Do not lower the 30-TradePlan threshold after seeing the result.
- [x] Do not drop XAU_USD or any low-activity instrument because of observed counts.
- [x] Do not mutate v0.1 alpha rules to increase activity.
- [x] Do not optimize parameters against the opened activity counts.
- [x] Do not open multi-market P&L.
- [x] Do not invoke the Phase-6B backtester.
- [x] Do not open v0.1 OOS or CONFIRM.
- [x] Keep paper, shadow, and live trading unauthorized.
- [x] Keep Phase 7 blocked.
- [x] Require any future research route to be separately justified and preregistered.

## Final handoff

```text
Phase 6B                         COMPLETE — INSUFFICIENT_MULTI_MARKET_SAMPLE
Alpha changes                    NONE
Provider all-gap qualification   PASS 16/16; 0 UNRESOLVED
Canonical NY boundary            PASS 4/4; 0 UNRESOLVED
Trusted canonical datasets       PASS 4/4
Exact trusted universe freeze    SEALED PRE-COUNT
Accepted instruments             4 / required 2
Contributing instruments         3 / required 2
Pooled detector candidates       4,975
Pooled TradePlans                7 / required 30
Performance protocol             NOT AUTHORIZED
Backtester / P&L                 NOT AUTHORIZED
v0.1 OOS / CONFIRM               UNOPENED
Phase 7                          BLOCKED
Paper / shadow / live            NOT AUTHORIZED
```
