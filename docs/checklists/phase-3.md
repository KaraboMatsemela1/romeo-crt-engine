# Phase 3 Checklist — Trusted Market-Data Layer

Canonical phase definition: [PROJECT_BIBLE.md](../../PROJECT_BIBLE.md).

**Entry status:** READY TO START after the pre-Phase-3 gate review.

## Entry gate

- [x] Phase 0 engineering foundation complete
- [x] Phase 1 research/reconciliation complete
- [x] Phase 2 frozen candidate exists
- [x] Strategy/code calendar semantics re-reviewed
- [x] CI green on the pre-Phase-3 gate branch before merge
- [x] Paper/live trading remains unauthorized

## Provider and instrument contract

- [ ] Select first provider/instrument/venue route
- [ ] Record provider terms/limitations relevant to historical storage and replay
- [ ] Define canonical instrument ID and provider-symbol mapping
- [ ] Record asset class, venue, timezone/session metadata, currency, price precision and tick size
- [ ] Define provider capability matrix: raw granularity, bid/ask, volume, corrections, pagination, rate limits

## Raw layer

- [ ] Define immutable raw-observation schema
- [ ] Preserve provider timestamps and ingestion timestamps
- [ ] Preserve provider identifiers/revision metadata where available
- [ ] Implement content/integrity hashing
- [ ] Implement storage adapter behind Phase-0 `ArtifactStore`
- [ ] Never silently rewrite historical raw payloads

## Normalized layer

- [ ] Normalize timestamps to UTC
- [ ] Normalize symbol/instrument metadata without losing provider provenance
- [ ] Validate finite prices and legal OHLC relationships
- [ ] Define bid/ask/spread representation when available
- [ ] Preserve source/provider and quality flags
- [ ] Make normalization deterministic and versioned

## Calendar / resampling

- [ ] Construct canonical H1 candles from trusted observations
- [ ] Construct canonical D1 candles using `00:00 America/New_York` wall clock
- [ ] Test EST and EDT dates
- [ ] Test spring-forward 23-hour D1 window
- [ ] Test fall-back 25-hour D1 window
- [ ] Validate H1 repeated/skipped local hours around DST
- [ ] Do not fabricate prices during market closures
- [ ] Compare provider-native bars against canonical bars before treating them as equivalent

## Data-quality gates

- [ ] Duplicate timestamp detection
- [ ] Out-of-order event detection
- [ ] Missing/gap classification
- [ ] Stale-data detection
- [ ] Impossible OHLC rejection
- [ ] Future timestamp rejection
- [ ] Symbol/venue metadata mismatch detection
- [ ] Provider correction/revision handling
- [ ] Market closure/halt/maintenance handling
- [ ] Deterministic quarantine/rejection reason codes

## Dataset versioning

- [ ] Generate dataset manifest
- [ ] Include provider/instrument/time range/schema/calendar/normalizer versions
- [ ] Include raw artifact references and hashes
- [ ] Include row counts and quality summary
- [ ] Produce manifest SHA-256
- [ ] Create immutable `DatasetRef`
- [ ] A correction produces a new dataset version

## Reproducibility

- [ ] Same raw artifacts + code/config produce byte/logically equivalent normalized data
- [ ] Same dataset version reproduces identical D1/H1 bars
- [ ] No strategy result is used to repair or selectively clean data
- [ ] Dataset generation command/workflow is documented
- [ ] Representative fixture dataset is small enough for CI where practical

## Exit gate

- [ ] Historical window reproduced deterministically from a trusted dataset
- [ ] D1/H1 calendar tests pass
- [ ] Data-quality regression suite passes
- [ ] Manifest/integrity verification passes
- [ ] Provider metadata and limitations documented
- [ ] Dataset version frozen for Phase 4
- [ ] Independent Phase-3 review complete
- [ ] Status/documentation updated

Phase 3 may build infrastructure around the frozen strategy, but it must not modify `CRT-C3-D1-H1-M1-BEAR-v0.1` semantics to make data look convenient.
