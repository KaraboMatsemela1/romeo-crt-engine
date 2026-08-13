# CRT Detector Contract

## Purpose

Phase 4 connects the frozen strategy specification to trusted canonical market data without changing either contract.

The first detector route is:

```text
trusted canonical dataset
  -> manifest/content verification
  -> canonical D1/H1 adapter
  -> exhaustive rolling C1/C2/C3 instances
  -> frozen CRT v0.1 evaluator
  -> deterministic candidate/rejection record
  -> immutable TradePlan when eligible
```

The detector is an interpretation/explanation layer around the already-frozen executable strategy in:

```text
src/romeo_crt_engine/crt/v0_1.py
```

It must not duplicate or silently reinterpret those predicates.

## Frozen identities

```text
strategy_version = CRT-C3-D1-H1-M1-BEAR-v0.1
detector_version = CRT-DETECTOR-v0.1
phase4_dataset    = ee1300f0da50e4debcbbc3b7
```

The Phase-4 dataset is a compact trusted integration fixture. It contains one complete New-York D1 candle and therefore cannot form a C1/C2/C3 strategy instance by itself. A detector run against that exact dataset must report:

```text
status          = INSUFFICIENT_D1_HISTORY
candidate_count = 0
trade_plan_count= 0
```

That result is a data-window fact, not `NO_SIGNAL`, not a losing trade and not a profitability conclusion.

## Trusted-data gate

A `DetectorDataset` is accepted only when all of the following hold:

1. manifest schema is `PHASE3_DATASET_MANIFEST_V1`;
2. quality status is `TRUSTED`;
3. provider, venue and symbol are present;
4. price tick is positive and finite;
5. manifest H1/D1 counts equal loaded canonical row counts;
6. every loaded bar matches manifest provider/venue/symbol;
7. H1 and D1 bars are strictly ordered and unique;
8. loaded H1/D1 content reproduces the manifest `normalized_sha256` exactly.

The detector does not accept an arbitrary folder merely because it contains files called `H1.jsonl` and `D1.jsonl`.

## Causal input contract

For one rolling parent candidate, the detector may pass to the frozen strategy:

### C1

A fully completed canonical D1 candle:

```text
open_time
close_time
open
high
low
close
```

### C2

The immediately following fully completed canonical D1 candle with the same fields.

### C3 gate

At C3 eligibility, only:

```text
open_time
close_time  # calendar boundary, not future price
open_price
```

The final C3 D1 high, low and close are deliberately not passed into strategy evaluation.

### H1 observations

Only completed H1 candles whose full interval lies within the C3 window are supplied to `evaluate_bearish_c3`.

The strategy then evaluates those H1 observations causally in chronological order. A later H1 candle cannot retroactively make an earlier entry valid.

## C3 future-information invariant

Changing only the final D1 C3:

```text
high
low
close
```

must not change:

- detector state;
- reason code;
- TradePlan entry time/price;
- stop;
- target;
- causal-input hash.

A regression test explicitly mutates those future D1 values to extreme numbers and requires the same strategy decision.

## Rolling candidate generation

For canonical D1 rows:

```text
D1[0], D1[1], D1[2] -> candidate 0
D1[1], D1[2], D1[3] -> candidate 1
D1[2], D1[3], D1[4] -> candidate 2
...
```

No historical parent is chosen because a later setup worked.

Each candidate gets a stable ID derived from:

```text
strategy version
+ dataset version
+ C1 open time
+ C2 open time
+ C3 open time
```

Overlapping candidates are permitted because that is the frozen parent-enumeration policy.

## Candidate explanation record

Every evaluated candidate contains:

```text
candidate_id
strategy_version
detector_version
dataset_version
manifest_sha256
provider
venue
symbol
c1_open_time
c2_open_time
c3_open_time
h1_observation_count
state
reason
rule_trace
evidence_ids
causal_input_sha256
trade_plan | null
```

This record is designed to be journalable before Phase 5 introduces account/order simulation.

## Reason and rule trace

The detector preserves the frozen strategy reason code and attaches the relevant specification rules.

Examples:

```text
NO_BEARISH_PARENT_SWEEP
  -> CRT-V01-003-BEARISH-C2-SWEEP

PARENT_CLOSE_NOT_RECLAIMED
  -> CRT-V01-004-C2-CLOSE-RECLAIM

TARGET1_CONSUMED_IN_C2
  -> CRT-V01-005-T1-PENDING

NO_MODEL1_CONFIRMATION
  -> CRT-V01-007-MODEL1-CORE
  -> CRT-V01-008-MODEL1-CONFIRMATION
  -> CRT-V01-011-C3-EXPIRY
```

`rule_trace` explains the deterministic contract involved. It does not invent new Romeo rules.

## Evidence trace

The detector preserves source/project evidence IDs already bound to the frozen strategy, such as:

```text
ROMEO-2024-CRT
ROMEO-2024-TS
ROMEO-2025-S1
ROMEO-2025-S7
P0-FIX-002
P2-PARAM-M1-THICK-050
P2-PARAM-STOP-1TICK
```

The detector may not upgrade the confidence of those sources or replace a frozen project parameter with a retrospectively optimized value.

## Causal-input hash

`causal_input_sha256` hashes the exact strategy-observable candidate state:

- C1 completed OHLC and source digest;
- C2 completed OHLC and source digest;
- C3 calendar/open gate;
- completed in-window H1 observations.

It intentionally excludes C3 final D1 high/low/close.

This provides an audit key for answering:

> Were these two detector decisions actually based on identical information available to the strategy?

## Run identity

A detector run produces `run_sha256` over:

```text
strategy_version
detector_version
dataset_version
manifest_sha256
candidate IDs
causal-input hashes
states
reason codes
```

Identical detector/data inputs must therefore produce the same run identity.

## Exact frozen-dataset reconstruction

`scripts/reconstruct_frozen_dataset.py` reconstructs the committed Phase-3 dataset rather than creating a new ingestion-time metadata snapshot.

It:

1. reads the committed frozen manifest;
2. reuses its instrument metadata snapshot;
3. downloads the exact raw archive dates;
4. requires exact provider raw SHA-256 matches;
5. repeats REST cross-checks;
6. rebuilds the canonical H1/D1 content;
7. requires the same dataset version;
8. requires the same canonical manifest SHA-256;
9. writes a new acquisition receipt for the current retrieval event.

Canonical dataset identity and current acquisition receipt identity remain separate.

## Detector CLI

Run against a reconstructed trusted dataset:

```bash
python scripts/run_crt_detector.py \
  --dataset-dir data/normalized/<dataset-version> \
  --require-dataset-version <dataset-version> \
  --require-manifest-sha256 <manifest-sha256>
```

The command emits machine-readable JSON and fails if the required frozen identity does not match.

## Phase-2 fixture parity

Phase 4 does not replace the frozen fixture corpus. It routes the same cases through canonical `CanonicalBar` objects and the new detector entry point.

The detector must reproduce all committed Phase-2 outcomes, including the positive `TradePlan` case and every negative reason code.

This proves integration parity, not historical profitability.

## What Phase 4 does not do

Phase 4 does **not**:

- calculate P&L;
- simulate a fill;
- decide order size;
- model spread/commission/slippage;
- modify entry/stop/target rules;
- choose the best parent after seeing the future;
- rank signals with ML;
- use an LLM in the decision path;
- authorize a trade through the risk engine;
- send broker orders;
- declare the strategy profitable.

Those boundaries are deliberate. Phase 5 may consume `TradePlan` outputs for cost-aware simulation, but it may not change the detector retrospectively to improve results.
