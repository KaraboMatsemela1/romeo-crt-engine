# Phase 6B OANDA Local Historical Collection Runbook v1

**Runbook ID:** `P6B-OANDA-LOCAL-COLLECTION-RUNBOOK-V1`  
**Parent execution:** `P6B-OANDA-HISTORY-SHARD-EXECUTION-V1`  
**Environment:** OANDA practice only  
**Detector / TradePlan / P&L access:** PROHIBITED

## Purpose

Execute the already-frozen 2019-2022 OANDA MID/M1 historical collection locally without placing credentials in GitHub, repository files, logs, manifests, or issue comments.

Collector:

```text
scripts/collect_oanda_history_shard.py
```

The collector does not import or invoke detector, backtest, order, paper, shadow, or live-trading code.

## 1. Checkout the Phase 6B branch

```bash
git fetch origin
git checkout agent/phase-6b-candidate-revision
git pull --ff-only
```

## 2. Prepare the Python environment

Use Python 3.12+ and the repository development dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

## 3. Provide runtime credentials securely

The collector reads only these environment variables:

```text
OANDA_ENV=practice
OANDA_ACCOUNT_ID=<runtime practice REST-v20 account>
OANDA_API_TOKEN=<runtime personal access token>
```

Do not write the real values into this repository, markdown files, issues, PRs, shell scripts, screenshots, or chat.

Example shell pattern:

```bash
export OANDA_ENV=practice
export OANDA_ACCOUNT_ID='...'
export OANDA_API_TOKEN='...'
```

Clear the sensitive values after collection:

```bash
unset OANDA_ACCOUNT_ID OANDA_API_TOKEN
```

## 4. First admissible execution — EUR_USD / 2019

Run exactly:

```bash
python scripts/collect_oanda_history_shard.py \
  --instrument EUR_USD \
  --year 2019
```

Expected output artifacts:

```text
artifacts/phase6b/oanda_raw/EUR_USD_2019_MID_M1.jsonl.gz
artifacts/phase6b/oanda_raw/EUR_USD_2019_MID_M1.manifest.json
```

Expected terminal state includes:

```text
history_shard=EUR_USD/2019
refetch=EXACT_PROVIDER_VALUE_MATCH
detector_execution_authorized=false
pnl_outcome_access_authorized=false
```

The manifest is still a **raw-data artifact**. `gap_reconciliation_status` must remain `UNRECONCILED`; successful collection does not make the shard detector-facing `TRUSTED`.

## 5. Inspect only data-quality metadata

Permitted inspection after each shard:

- instrument/year identity;
- page count;
- complete candle count;
- request/raw-response/retrieval/value hashes;
- missing interval count/minutes/timestamps;
- independent re-fetch status;
- credential-redaction and authorization flags.

Prohibited inspection during this gate:

- detector execution;
- TradePlan counts;
- reason distributions;
- backtester results;
- P&L, win rate, expectancy, profit factor, drawdown;
- v0.1 OOS or CONFIRM outcomes.

## 6. Complete all 16 frozen shards

Only after the first shard completes with the expected artifact structure, run the complete frozen matrix:

```bash
for instrument in EUR_USD XAU_USD NAS100_USD SPX500_USD; do
  for year in 2019 2020 2021 2022; do
    python scripts/collect_oanda_history_shard.py \
      --instrument "$instrument" \
      --year "$year" || exit 1
  done
done
```

Do not change instruments, years, price component, page width, request-delay rule, or re-fetch windows in response to observed data.

A failed transport/job may be rerun for the exact same frozen shard.

## 7. Artifact handling

Raw local artifacts under `artifacts/phase6b/oanda_raw/` are not automatically authorized for Git commit.

Before sharing or committing any manifest, verify that it contains no:

```text
account ID
API token
Authorization header
Bearer token
balance
NAV
```

The collector is designed to persist account scope only as:

```text
REDACTED_RUNTIME_ACCOUNT
```

Do not commit raw M1 price files unless a later project decision explicitly defines the storage/repository policy.

## 8. Gate after 16 shards

After all 16 collection units exist:

1. confirm all 16 mapped independent re-fetches passed;
2. union the four yearly raw missing-interval inventories per instrument;
3. reconcile every missing minute exactly to date-valid OANDA closure/session/holiday evidence;
4. leave any unexplained/provider-missing minute fail-closed;
5. consolidate four years into one provider-value stream per instrument;
6. build deterministic H1 and New-York-midnight D1;
7. freeze one `P6B_CANONICAL_PRICE_DATASET_V2` identity per trusted instrument;
8. only then authorize the detector-only 2/2/30 activity gate.

## Authorization

```text
FULL_RAW_HISTORY_COLLECTION_AUTHORIZED = true
DETECTOR_EXECUTION_AUTHORIZED          = false
TRADEPLAN_COUNT_ACCESS_AUTHORIZED      = false
BACKTESTER_AUTHORIZED                  = false
PNL_OUTCOME_ACCESS_AUTHORIZED          = false
V0_1_OOS_ACCESS_AUTHORIZED             = false
V0_1_CONFIRM_ACCESS_AUTHORIZED         = false
PAPER_TRADING_AUTHORIZED               = false
SHADOW_TRADING_AUTHORIZED              = false
LIVE_TRADING_AUTHORIZED                = false
```
