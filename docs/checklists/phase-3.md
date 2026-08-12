# Phase 3 Checklist — Trusted Market-Data Layer

Canonical phase definition: [PROJECT_BIBLE.md](../../PROJECT_BIBLE.md).

**Status:** **COMPLETE**  
**Frozen Phase-4 reproduction dataset:** `ee1300f0da50e4debcbbc3b7`

## Entry gate

- [x] Phase 0 engineering foundation complete
- [x] Phase 1 research/reconciliation complete
- [x] Phase 2 frozen candidate exists
- [x] Strategy/code calendar semantics re-reviewed
- [x] CI green on the pre-Phase-3 gate before entry
- [x] Paper/live trading remains unauthorized

## Provider and instrument contract

- [x] Select first provider/instrument/venue route — Binance Public Data / Binance Spot / BTCUSDT
- [x] Record provider limitations relevant to historical storage/replay — ADR-005 + `MARKET_DATA.md`
- [x] Define canonical instrument ID and provider-symbol mapping
- [x] Record asset class, venue, analytical timezone, tick size and quantity step
- [x] Define provider capability matrix — raw M1/OHLC/volume/quote-volume/trade-count available; bid/ask/spread unavailable in this route
- [x] Record metadata temporal limitation — exchange filters are snapshot-at-ingestion, not historical reconstruction

## Raw layer

- [x] Define immutable raw-observation/provider-artifact contract
- [x] Preserve original provider bytes and provider timestamps
- [x] Preserve retrieval timestamp and Git revision separately in ingestion receipt
- [x] Preserve provider source/checksum URLs and source SHA-256
- [x] Implement content/integrity hashing
- [x] Implement concrete `LocalArtifactStore` behind Phase-0 `ArtifactStore`
- [x] Never silently rewrite historical raw payloads
- [x] Provider corrections create new raw hashes/dataset versions

## Normalized layer

- [x] Normalize timestamps to UTC
- [x] Preserve provider/venue/symbol provenance
- [x] Validate finite prices and legal OHLC relationships
- [x] Document bid/ask/spread as unavailable rather than fabricate values
- [x] Preserve source hashes and verification evidence
- [x] Make normalization deterministic and versioned
- [x] Separate canonical dataset identity from ingestion-event identity

## Calendar / resampling

- [x] Construct canonical H1 candles from trusted M1 observations
- [x] Construct canonical D1 using `00:00 America/New_York` wall clock
- [x] Test EST and EDT behavior
- [x] Test spring-forward 23-hour D1
- [x] Test fall-back 25-hour D1
- [x] Validate H1 chronology through skipped/repeated local hours
- [x] Do not fabricate prices during missing/maintenance observations
- [x] Provider-native H1/D1 are explicitly untrusted unless separately proven equivalent; v1 always derives from M1

## Data-quality gates

- [x] Duplicate timestamp detection
- [x] Out-of-order event detection
- [x] Missing/gap rejection
- [x] Historical stale/future boundary validation via exact day coverage and ingestion `as_of`
- [x] Impossible/non-finite OHLC rejection
- [x] Future timestamp rejection
- [x] Symbol/venue/provider metadata mismatch detection
- [x] Provider correction/revision policy
- [x] 24/7 route maintenance gap policy — reject missing minute, never fill
- [x] Deterministic rejection reason codes
- [x] Published provider checksum validation
- [x] REST cross-check evidence required per raw artifact

## Dataset versioning

- [x] Generate deterministic dataset manifest
- [x] Include provider/instrument/schema/calendar/normalizer identity
- [x] Include market-data code SHA-256 and dependency-lock SHA-256
- [x] Include raw artifact references and SHA-256 values
- [x] Include provider verification evidence digests
- [x] Include row counts and quality state
- [x] Produce canonical manifest SHA-256
- [x] Create acquisition receipt and `DatasetRef`
- [x] A correction produces a new dataset version
- [x] Commit machine-readable Phase-4 manifest/evidence records

## Reproducibility

- [x] Same canonical raw artifacts + metadata/code/lock/config produce identical normalized data and manifest
- [x] Same dataset version reproduces identical D1/H1 bars
- [x] Retrieval timestamp changes receipt but not canonical dataset identity
- [x] Market-data implementation change changes dataset identity
- [x] No strategy result is used to repair/select data
- [x] Dataset generation command documented
- [x] Exact Python 3.12 dependency lock adopted
- [x] Deterministic CI runs without external market-data dependency
- [x] Real-provider smoke separately proves external route

## Exit gate

- [x] Historical window reproduced deterministically from a trusted provider-backed dataset
- [x] D1/H1 calendar and DST tests pass
- [x] Data-quality regression suite passes
- [x] Manifest/integrity verification passes
- [x] Provider metadata/capabilities/limitations documented
- [x] Dataset version frozen for Phase 4 — `ee1300f0da50e4debcbbc3b7`
- [x] Independent Phase-3 review complete — `docs/reviews/PHASE_3_GATE_REVIEW.md`
- [x] Completion report recorded — `docs/PHASE_3_COMPLETION_REPORT.md`
- [x] Status/documentation updated before merge

## Accepted limitations

- Phase-3 v1 covers BTCUSDT Spot only.
- This archive route has no bid/ask/spread history.
- Current `exchangeInfo` is an ingestion-time snapshot, not historical exchange-rule data.
- The frozen dataset is a small Phase-4 reproduction fixture, not a full validation/OOS dataset.
- Non-24/7 markets require venue-aware closure/session handling in future data routes.

Phase 3 infrastructure does not modify `CRT-C3-D1-H1-M1-BEAR-v0.1` semantics.
