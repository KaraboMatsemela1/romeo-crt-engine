from __future__ import annotations

import argparse
import gc
import json
import os
from bisect import bisect_left, bisect_right
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from hashlib import sha256
from pathlib import Path
from zoneinfo import ZoneInfo

from romeo_crt_engine.market_data.aggregate_v2 import (
    build_h1_price_bars_v2,
    build_new_york_d1_price_bars_v2,
)
from romeo_crt_engine.market_data.canonical_coverage_v2 import (
    CANONICAL_COVERAGE_END_UTC,
    CANONICAL_COVERAGE_POLICY_VERSION,
    CANONICAL_COVERAGE_START_UTC,
    CANONICAL_TAIL_END_UTC,
    CANONICAL_TAIL_START_UTC,
)
from romeo_crt_engine.market_data.history_qualification_v2 import normalized_m1_sha256
from romeo_crt_engine.market_data.oanda_qualification import canonicalize_oanda_m1
from romeo_crt_engine.market_data.price_data_v2 import (
    CanonicalPriceBarV2,
    encode_canonical_price_bars_jsonl,
    normalized_price_digest_v2,
)
from romeo_crt_engine.market_data.providers.oanda_history import (
    DEFAULT_PAGE_MINUTES,
    OandaHistoryRequestWindow,
    fetch_m1_history_page,
    retrieve_m1_history,
)
from romeo_crt_engine.market_data.providers.oanda_v20 import (
    PRACTICE_BASE_URL,
    OandaInstrumentRecord,
    fetch_account_instruments,
)
from romeo_crt_engine.market_data.s5_gap_policy_v2 import OBSERVATION_POLICY_VERSION
from romeo_crt_engine.market_data.session_policy_v2 import MarketGapV2, minute_is_expected
from romeo_crt_engine.market_data.trusted_oanda_dataset_v2 import (
    TRUSTED_BUILD_SCHEMA_VERSION,
    market_gaps_from_canonical_tail_evidence,
    oanda_instrument_metadata_record,
    price_dataset_identity_record,
    trusted_dataset_identity,
    validate_yearly_reconstruction,
)

FROZEN_INSTRUMENTS = ("EUR_USD", "XAU_USD", "NAS100_USD", "SPX500_USD")
FROZEN_YEARS = (2019, 2020, 2021, 2022)
NEW_YORK = ZoneInfo("America/New_York")
REQUEST_DELAY_SECONDS = 0.55
H1_CHUNK_HOURS = 6


@dataclass(frozen=True, slots=True)
class GapWindowIndex:
    gaps: tuple[MarketGapV2, ...]
    starts: tuple[datetime, ...]
    ends: tuple[datetime, ...]

    @classmethod
    def build(cls, gaps: tuple[MarketGapV2, ...]) -> GapWindowIndex:
        ordered = tuple(sorted(gaps, key=lambda item: item.start_time))
        previous_end: datetime | None = None
        for gap in ordered:
            if previous_end is not None and gap.start_time < previous_end:
                raise ValueError("trusted dataset gap evidence must not overlap")
            previous_end = gap.end_time
        return cls(
            gaps=ordered,
            starts=tuple(item.start_time for item in ordered),
            ends=tuple(item.end_time for item in ordered),
        )

    def overlapping(self, start: datetime, end: datetime) -> tuple[MarketGapV2, ...]:
        if end <= start:
            raise ValueError("gap lookup end must be after start")
        left = bisect_right(self.ends, start)
        right = bisect_left(self.starts, end)
        return self.gaps[left:right]


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Reconstruct one frozen Phase-6B OANDA MID/M1 instrument from the provider, "
            "bind it to sealed all-gap evidence, derive H1 and New-York D1 bars, and emit "
            "a detector-facing TRUSTED identity. No detector, backtester, P&L, paper, "
            "shadow, or live-trading code is invoked."
        )
    )
    parser.add_argument("--instrument", required=True, choices=FROZEN_INSTRUMENTS)
    parser.add_argument("--evidence-dir", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    return parser


def _load_json(path: Path) -> dict[str, object]:
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise TypeError(f"expected JSON object: {path}")
    return document


def _find_exact(root: Path, filename: str) -> Path:
    matches = tuple(root.rglob(filename))
    if len(matches) != 1:
        raise ValueError(f"expected exactly one {filename} under {root}; found {len(matches)}")
    return matches[0]


def _sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _select_instrument(
    records: tuple[OandaInstrumentRecord, ...],
    instrument: str,
) -> OandaInstrumentRecord:
    matches = tuple(item for item in records if item.name == instrument)
    if len(matches) != 1:
        raise ValueError(f"exact OANDA instrument metadata unavailable: {instrument}")
    return matches[0]


def _assert_fully_omitted(
    start: datetime,
    end: datetime,
    gaps: tuple[MarketGapV2, ...],
) -> None:
    cursor = start
    while cursor < end:
        if minute_is_expected(cursor, gaps):
            raise ValueError(
                "provider reconstruction omitted an expected minute without evidence: "
                f"{cursor.isoformat()}"
            )
        cursor += timedelta(minutes=1)


def _build_h1_chunked(
    m1: tuple[CanonicalPriceBarV2, ...],
    gaps: tuple[MarketGapV2, ...],
    *,
    coverage_start: datetime,
    coverage_end: datetime,
) -> tuple[CanonicalPriceBarV2, ...]:
    if coverage_end <= coverage_start:
        return ()
    index = GapWindowIndex.build(gaps)
    output: list[CanonicalPriceBarV2] = []
    bar_index = 0
    cursor = coverage_start
    step = timedelta(hours=H1_CHUNK_HOURS)

    while cursor < coverage_end:
        chunk_end = min(cursor + step, coverage_end)
        while bar_index < len(m1) and m1[bar_index].open_time < cursor:
            bar_index += 1
        end_index = bar_index
        while end_index < len(m1) and m1[end_index].open_time < chunk_end:
            end_index += 1
        chunk_bars = m1[bar_index:end_index]
        chunk_gaps = index.overlapping(cursor, chunk_end)
        if chunk_bars:
            output.extend(
                build_h1_price_bars_v2(
                    chunk_bars,
                    coverage_start=cursor,
                    coverage_end=chunk_end,
                    gaps=chunk_gaps,
                )
            )
        else:
            _assert_fully_omitted(cursor, chunk_end, chunk_gaps)
        bar_index = end_index
        cursor = chunk_end
    return tuple(output)


def _ny_window(local_date: date) -> tuple[datetime, datetime]:
    start = datetime.combine(local_date, time.min, tzinfo=NEW_YORK).astimezone(UTC)
    end = datetime.combine(local_date + timedelta(days=1), time.min, tzinfo=NEW_YORK).astimezone(UTC)
    return start, end


def _group_by_new_york_date(
    m1: tuple[CanonicalPriceBarV2, ...],
) -> dict[date, tuple[CanonicalPriceBarV2, ...]]:
    groups: dict[date, list[CanonicalPriceBarV2]] = {}
    for bar in m1:
        local_date = bar.open_time.astimezone(NEW_YORK).date()
        groups.setdefault(local_date, []).append(bar)
    return {key: tuple(value) for key, value in groups.items()}


def _build_one_d1(
    local_date: date,
    bars: tuple[CanonicalPriceBarV2, ...],
    gaps: tuple[MarketGapV2, ...],
) -> CanonicalPriceBarV2 | None:
    start, end = _ny_window(local_date)
    index = GapWindowIndex.build(gaps)
    window_gaps = index.overlapping(start, end)
    if not bars:
        _assert_fully_omitted(start, end, window_gaps)
        return None
    result = build_new_york_d1_price_bars_v2(
        bars,
        eligible_local_dates=(local_date,),
        gaps=window_gaps,
    )
    if len(result) != 1:
        raise ValueError("one eligible New-York date must produce exactly one D1 bar")
    return result[0]


def _safe_manifest(document: Mapping[str, object]) -> None:
    serialized = json.dumps(document, sort_keys=True).lower()
    for marker in (
        "authorization",
        "bearer ",
        "oanda_api_token",
        "oanda_account_id",
        '"balance"',
        '"nav"',
    ):
        if marker in serialized:
            raise ValueError(f"forbidden persisted marker found: {marker}")
    for flag in (
        "detector_execution_authorized",
        "tradeplan_count_access_authorized",
        "backtester_authorized",
        "pnl_outcome_access_authorized",
        "paper_trading_authorized",
        "shadow_trading_authorized",
        "live_trading_authorized",
    ):
        if document.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")


def main() -> int:
    args = _parser().parse_args()
    instrument = str(args.instrument)
    evidence_dir = Path(args.evidence_dir)
    output_dir = Path(args.output_dir)

    if os.environ.get("OANDA_ENV", "practice").strip().lower() != "practice":
        raise SystemExit("trusted Phase-6B reconstruction is authorized only for OANDA practice")
    account_id = os.environ.get("OANDA_ACCOUNT_ID", "")
    token = os.environ.get("OANDA_API_TOKEN", "")
    if not account_id or not token:
        raise SystemExit("OANDA_ACCOUNT_ID and OANDA_API_TOKEN are required at runtime")

    observed_at = datetime.now(UTC)
    provider_instruments = fetch_account_instruments(
        base_url=PRACTICE_BASE_URL,
        account_id=account_id,
        token=token,
        observed_at=observed_at,
        timeout_seconds=45.0,
    )
    metadata = _select_instrument(provider_instruments, instrument)

    h1_all: list[CanonicalPriceBarV2] = []
    d1_all: list[CanonicalPriceBarV2] = []
    reconstruction_records: list[dict[str, object]] = []
    evidence_records: list[dict[str, object]] = []
    pending_dec31_date: date | None = None
    pending_dec31_bars: tuple[CanonicalPriceBarV2, ...] = ()
    pending_dec31_gaps: tuple[MarketGapV2, ...] = ()

    for year in FROZEN_YEARS:
        reconciliation_path = _find_exact(
            evidence_dir,
            f"{instrument}_{year}_MID_M1.reconciliation-v2.json",
        )
        s5_path = _find_exact(
            evidence_dir,
            f"{instrument}_{year}_MID_M1.s5-gap-evidence-v1.json",
        )
        reconciliation = _load_json(reconciliation_path)
        s5_evidence = _load_json(s5_path)

        start = datetime(year, 1, 1, tzinfo=UTC)
        end = datetime(year + 1, 1, 1, tzinfo=UTC)
        retrieval = retrieve_m1_history(
            base_url=PRACTICE_BASE_URL,
            account_id=account_id,
            token=token,
            instrument=instrument,
            start=start,
            end=end,
            price_component="M",
            page_minutes=DEFAULT_PAGE_MINUTES,
            timeout_seconds=45.0,
            request_delay_seconds=REQUEST_DELAY_SECONDS,
        )
        gaps = validate_yearly_reconstruction(
            retrieval.candles,
            reconciliation,
            s5_evidence,
        )
        reconstruction_records.append(
            {
                "year": year,
                "complete_m1": len(retrieval.candles),
                "normalized_provider_values_sha256": normalized_m1_sha256(retrieval.candles),
                "sealed_missing_intervals_sha256": reconciliation["missing_intervals_sha256"],
                "sealed_gap_count": len(gaps),
                "sealed_unresolved_gap_count": s5_evidence["unresolved_provider_gap_count"],
                "sealed_refetch_status": reconciliation["refetch"],
            }
        )
        evidence_records.append(
            {
                "year": year,
                "reconciliation_file_sha256": _sha256_file(reconciliation_path),
                "s5_evidence_file_sha256": _sha256_file(s5_path),
            }
        )

        canonical = canonicalize_oanda_m1(
            retrieval.candles,
            session_policy_version=OBSERVATION_POLICY_VERSION,
        )
        canonical = tuple(
            bar
            for bar in canonical
            if CANONICAL_COVERAGE_START_UTC <= bar.open_time < CANONICAL_COVERAGE_END_UTC
        )
        gap_index = GapWindowIndex.build(gaps)

        h1_start = max(start, CANONICAL_COVERAGE_START_UTC)
        h1_end = min(end, CANONICAL_COVERAGE_END_UTC)
        h1_all.extend(
            _build_h1_chunked(
                canonical,
                gaps,
                coverage_start=h1_start,
                coverage_end=h1_end,
            )
        )

        by_date = _group_by_new_york_date(canonical)
        if pending_dec31_date is not None:
            current_prefix = by_date.get(pending_dec31_date, ())
            pending_start, pending_end = _ny_window(pending_dec31_date)
            current_gaps = gap_index.overlapping(pending_start, pending_end)
            completed = _build_one_d1(
                pending_dec31_date,
                pending_dec31_bars + current_prefix,
                tuple(sorted(pending_dec31_gaps + current_gaps, key=lambda item: item.start_time)),
            )
            if completed is not None:
                d1_all.append(completed)

        for local_date in sorted(by_date):
            if local_date.year != year or (local_date.month, local_date.day) == (12, 31):
                continue
            local_start, local_end = _ny_window(local_date)
            completed = _build_one_d1(
                local_date,
                by_date[local_date],
                gap_index.overlapping(local_start, local_end),
            )
            if completed is not None:
                d1_all.append(completed)

        pending_dec31_date = date(year, 12, 31)
        pending_dec31_bars = by_date.get(pending_dec31_date, ())
        pending_start, pending_end = _ny_window(pending_dec31_date)
        pending_dec31_gaps = gap_index.overlapping(pending_start, pending_end)

        del retrieval
        del canonical
        del by_date
        gc.collect()

    tail_path = _find_exact(evidence_dir, f"{instrument}.json")
    tail_evidence = _load_json(tail_path)
    tail_gaps = market_gaps_from_canonical_tail_evidence(tail_evidence)

    tail_page = fetch_m1_history_page(
        base_url=PRACTICE_BASE_URL,
        account_id=account_id,
        token=token,
        instrument=instrument,
        window=OandaHistoryRequestWindow(
            start=CANONICAL_TAIL_START_UTC,
            end=CANONICAL_TAIL_END_UTC,
        ),
        price_component="M",
        timeout_seconds=45.0,
    )
    if tail_page.candles:
        raise ValueError("fresh canonical-tail reconstruction contradicts sealed empty evidence")

    _assert_fully_omitted(CANONICAL_TAIL_START_UTC, CANONICAL_TAIL_END_UTC, tail_gaps)
    if pending_dec31_date != date(2022, 12, 31):
        raise ValueError("final pending D1 date is not the frozen 2022-12-31 boundary")
    final_gaps = tuple(
        sorted(pending_dec31_gaps + tail_gaps, key=lambda item: item.start_time)
    )
    final_d1 = _build_one_d1(
        pending_dec31_date,
        pending_dec31_bars,
        final_gaps,
    )
    if final_d1 is not None:
        d1_all.append(final_d1)

    h1 = tuple(h1_all)
    d1 = tuple(d1_all)
    if not h1 or not d1:
        raise ValueError("trusted detector-facing H1/D1 output must not be empty")
    if any(h1[index].open_time >= h1[index + 1].open_time for index in range(len(h1) - 1)):
        raise ValueError("trusted H1 output is not strictly ordered")
    if any(d1[index].open_time >= d1[index + 1].open_time for index in range(len(d1) - 1)):
        raise ValueError("trusted D1 output is not strictly ordered")

    normalized_sha = normalized_price_digest_v2(h1, d1)
    identity = trusted_dataset_identity(
        instrument=metadata,
        normalized_sha256=normalized_sha,
        h1_rows=len(h1),
        d1_rows=len(d1),
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    h1_path = output_dir / f"{instrument}.H1.jsonl"
    d1_path = output_dir / f"{instrument}.D1_NY.jsonl"
    identity_path = output_dir / f"{instrument}.identity.json"
    manifest_path = output_dir / f"{instrument}.trusted-build.json"
    h1_path.write_bytes(encode_canonical_price_bars_jsonl(h1))
    d1_path.write_bytes(encode_canonical_price_bars_jsonl(d1))
    identity_path.write_text(
        json.dumps(price_dataset_identity_record(identity), sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )

    manifest: dict[str, object] = {
        "schema_version": TRUSTED_BUILD_SCHEMA_VERSION,
        "canonical_coverage_policy_version": CANONICAL_COVERAGE_POLICY_VERSION,
        "observation_policy_version": OBSERVATION_POLICY_VERSION,
        "provider": "OANDA_V20",
        "venue": "OANDA_FXTRADE",
        "environment": "practice",
        "account_scope": "REDACTED_RUNTIME_ACCOUNT",
        "instrument": instrument,
        "price_component": "MID",
        "canonical_coverage_start_utc": CANONICAL_COVERAGE_START_UTC.isoformat(),
        "canonical_coverage_end_utc": CANONICAL_COVERAGE_END_UTC.isoformat(),
        "instrument_metadata": oanda_instrument_metadata_record(metadata),
        "dataset_identity": price_dataset_identity_record(identity),
        "yearly_reconstruction": reconstruction_records,
        "sealed_evidence_files": evidence_records,
        "canonical_tail_evidence_file_sha256": _sha256_file(tail_path),
        "fresh_canonical_tail_complete_m1": len(tail_page.candles),
        "fresh_canonical_tail_request_sha256": tail_page.request_sha256,
        "fresh_canonical_tail_raw_response_sha256": tail_page.raw_response_sha256,
        "h1_file_sha256": _sha256_file(h1_path),
        "d1_file_sha256": _sha256_file(d1_path),
        "h1_rows": len(h1),
        "d1_rows": len(d1),
        "normalized_h1_d1_sha256": normalized_sha,
        "m1_persisted": False,
        "raw_provider_price_artifacts_persisted": False,
        "quality_status": "TRUSTED",
        "detector_execution_authorized": False,
        "tradeplan_count_access_authorized": False,
        "backtester_authorized": False,
        "pnl_outcome_access_authorized": False,
        "paper_trading_authorized": False,
        "shadow_trading_authorized": False,
        "live_trading_authorized": False,
    }
    _safe_manifest(manifest)
    manifest_path.write_text(
        json.dumps(manifest, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"trusted_dataset={instrument}")
    print("quality_status=TRUSTED")
    print(f"h1_rows={len(h1)}")
    print(f"d1_rows={len(d1)}")
    print(f"normalized_h1_d1_sha256={normalized_sha}")
    print(f"price_quantum={identity.price_quantum}")
    print(f"price_quantum_source={identity.price_quantum_source.value}")
    print(f"identity={identity_path}")
    print(f"manifest={manifest_path}")
    print("detector_execution_authorized=false")
    print("pnl_outcome_access_authorized=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
