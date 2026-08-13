from __future__ import annotations

import argparse
import gzip
import io
import json
import os
import time
from datetime import UTC, datetime
from hashlib import sha256
from pathlib import Path
from urllib.error import HTTPError, URLError

from romeo_crt_engine.market_data.history_qualification_v2 import (
    DEV_END_UTC,
    DEV_START_UTC,
    HISTORY_QUALIFICATION_SCHEMA_VERSION,
    REFETCH_WINDOWS_UTC,
    MissingInterval,
    assert_refetch_equal,
    candle_value_record,
    gap_digest,
    missing_interval_record,
    normalized_m1_sha256,
)
from romeo_crt_engine.market_data.oanda_qualification import (
    build_instrument_discovery_manifest,
)
from romeo_crt_engine.market_data.providers.oanda_account import (
    fetch_account_summary,
    fetch_authorized_account_ids,
)
from romeo_crt_engine.market_data.providers.oanda_history import (
    DEFAULT_PAGE_MINUTES,
    OandaHistoryPage,
    OandaHistoryRequestWindow,
    build_m1_request_windows,
    fetch_m1_history_page,
)
from romeo_crt_engine.market_data.providers.oanda_v20 import (
    LIVE_BASE_URL,
    PRACTICE_BASE_URL,
    OandaPriceCandle,
    fetch_account_instruments,
)

FROZEN_PHASE6B_INSTRUMENTS = (
    "EUR_USD",
    "XAU_USD",
    "NAS100_USD",
    "SPX500_USD",
)
HISTORY_SMOKE_START = datetime(2019, 3, 12, 14, 0, tzinfo=UTC)
HISTORY_SMOKE_END = datetime(2019, 3, 12, 15, 0, tzinfo=UTC)
HISTORY_PRICE_COMPONENT = "M"
MIN_FULL_HISTORY_REQUEST_DELAY_SECONDS = 1.05
MAX_HISTORY_FETCH_ATTEMPTS = 5
RETRYABLE_HTTP_STATUS = frozenset({429, 500, 502, 503, 504})


def _environment(value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in {"practice", "live"}:
        raise argparse.ArgumentTypeError("environment must be practice or live")
    return normalized


def _frozen_instrument(value: str) -> str:
    if value not in FROZEN_PHASE6B_INSTRUMENTS:
        raise argparse.ArgumentTypeError("instrument is not in the frozen Phase-6B universe")
    return value


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Discover runtime OANDA account/instrument metadata and optionally perform "
            "credential-free Phase-6B historical-data qualification. This command never "
            "invokes the CRT detector or backtester."
        )
    )
    parser.add_argument(
        "--environment",
        type=_environment,
        default=os.environ.get("OANDA_ENV", "practice"),
        help="OANDA environment; defaults to OANDA_ENV or practice",
    )
    parser.add_argument(
        "--allow-live-read",
        action="store_true",
        help="Explicitly allow read-only metadata qualification against the live API endpoint",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path for the credential-free discovery manifest",
    )
    parser.add_argument(
        "--history-smoke-output",
        type=Path,
        help=(
            "Optional credential-free output for the fixed Phase-6B one-hour 2019 MID/M1 "
            "historical-access smoke check; no strategy code is invoked"
        ),
    )
    parser.add_argument(
        "--full-history-instrument",
        type=_frozen_instrument,
        help=(
            "Collect the frozen 2019-2022 MID/M1 DEV interval for exactly one frozen "
            "instrument. Practice environment only; detector/backtester remain disabled."
        ),
    )
    parser.add_argument(
        "--full-history-output-dir",
        type=Path,
        help="Output directory for the credential-free full-history qualification artifacts",
    )
    parser.add_argument(
        "--full-history-request-delay-seconds",
        type=float,
        default=MIN_FULL_HISTORY_REQUEST_DELAY_SECONDS,
        help="Delay between new OANDA history connections; must be at least 1.05 seconds",
    )
    return parser


def _run_history_smoke(
    *,
    base_url: str,
    account_id: str,
    token: str,
    output: Path,
) -> None:
    window = OandaHistoryRequestWindow(start=HISTORY_SMOKE_START, end=HISTORY_SMOKE_END)
    records: list[dict[str, object]] = []
    for instrument in FROZEN_PHASE6B_INSTRUMENTS:
        try:
            page = fetch_m1_history_page(
                base_url=base_url,
                account_id=account_id,
                token=token,
                instrument=instrument,
                window=window,
                price_component=HISTORY_PRICE_COMPONENT,
                timeout_seconds=45.0,
            )
        except HTTPError as error:
            raise SystemExit(
                f"OANDA historical smoke failed for {instrument} with HTTP {error.code}"
            ) from None

        if len(page.candles) != 60:
            raise SystemExit(
                f"OANDA historical smoke expected 60 complete M1 candles for {instrument}; "
                f"observed {len(page.candles)}"
            )
        if page.candles[0].open_time != HISTORY_SMOKE_START:
            raise SystemExit(f"OANDA historical smoke start mismatch for {instrument}")
        if page.candles[-1].close_time != HISTORY_SMOKE_END:
            raise SystemExit(f"OANDA historical smoke end mismatch for {instrument}")

        records.append(
            {
                "instrument": instrument,
                "price_component": "MID",
                "granularity": "M1",
                "start_utc": HISTORY_SMOKE_START.isoformat(),
                "end_utc": HISTORY_SMOKE_END.isoformat(),
                "complete_candle_count": len(page.candles),
                "request_sha256": page.request_sha256,
                "raw_response_sha256": page.raw_response_sha256,
                "normalized_provider_values_sha256": normalized_m1_sha256(page.candles),
                "status": "EXACT_60_MINUTE_INTERVAL_AVAILABLE",
            }
        )

    smoke_manifest = {
        "schema_version": "P6B_OANDA_HISTORY_SMOKE_V1",
        "provider": "OANDA_V20",
        "environment": "practice",
        "account_scope": "REDACTED_RUNTIME_ACCOUNT",
        "window_selected_before_provider_access": True,
        "instrument_count": len(records),
        "instruments": records,
        "status": "HISTORICAL_M1_ACCESS_CONFIRMED",
        "detector_activity_counts_authorized": False,
        "strategy_outcome_access_authorized": False,
        "pnl_outcome_access_authorized": False,
        "backtester_authorized": False,
        "paper_trading_authorized": False,
        "live_trading_authorized": False,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(smoke_manifest, sort_keys=True, indent=2) + "\n")

    print("history_smoke=HISTORICAL_M1_ACCESS_CONFIRMED")
    print(f"history_smoke_instruments={len(records)}/{len(FROZEN_PHASE6B_INSTRUMENTS)}")
    print("history_smoke_detector_activity_counts_authorized=false")
    print("history_smoke_pnl_outcome_access_authorized=false")


def _fetch_history_page_with_retry(
    *,
    base_url: str,
    account_id: str,
    token: str,
    instrument: str,
    window: OandaHistoryRequestWindow,
) -> OandaHistoryPage:
    for attempt in range(1, MAX_HISTORY_FETCH_ATTEMPTS + 1):
        try:
            return fetch_m1_history_page(
                base_url=base_url,
                account_id=account_id,
                token=token,
                instrument=instrument,
                window=window,
                price_component=HISTORY_PRICE_COMPONENT,
                timeout_seconds=45.0,
            )
        except HTTPError as error:
            if error.code not in RETRYABLE_HTTP_STATUS or attempt == MAX_HISTORY_FETCH_ATTEMPTS:
                raise SystemExit(
                    f"OANDA history request failed for {instrument} with HTTP {error.code}"
                ) from None
        except URLError:
            if attempt == MAX_HISTORY_FETCH_ATTEMPTS:
                raise SystemExit(
                    f"OANDA history request failed for {instrument} after network retries"
                ) from None
        time.sleep(min(2 ** (attempt - 1), 8))
    raise AssertionError("unreachable OANDA history retry state")


def _page_provenance_record(index: int, page: OandaHistoryPage) -> dict[str, object]:
    return {
        "page_index": index,
        "start_utc": page.window.start.astimezone(UTC).isoformat(),
        "end_utc": page.window.end.astimezone(UTC).isoformat(),
        "retrieved_at_utc": page.retrieved_at.astimezone(UTC).isoformat(),
        "request_sha256": page.request_sha256,
        "raw_response_sha256": page.raw_response_sha256,
        "complete_candle_count": len(page.candles),
    }


def _append_missing_interval(
    gaps: list[MissingInterval],
    *,
    start: datetime,
    end: datetime,
) -> None:
    if end > start:
        gaps.append(MissingInterval(start=start, end=end))


def _is_refetch_sample(candle: OandaPriceCandle) -> bool:
    return any(start <= candle.open_time < end for start, end in REFETCH_WINDOWS_UTC)


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n")


def _run_full_history_collection(
    *,
    base_url: str,
    account_id: str,
    token: str,
    instrument: str,
    output_dir: Path,
    request_delay_seconds: float,
) -> None:
    if request_delay_seconds < MIN_FULL_HISTORY_REQUEST_DELAY_SECONDS:
        raise SystemExit(
            "full-history request delay must be at least "
            f"{MIN_FULL_HISTORY_REQUEST_DELAY_SECONDS:.2f} seconds"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    windows = build_m1_request_windows(
        DEV_START_UTC,
        DEV_END_UTC,
        page_minutes=DEFAULT_PAGE_MINUTES,
    )

    m1_path = output_dir / "m1.jsonl.gz"
    pages_path = output_dir / "pages.json"
    gaps_path = output_dir / "missing_intervals.json"
    manifest_path = output_dir / "manifest.json"

    normalized_digest = sha256()
    normalized_digest.update(b"P6B_OANDA_M1_VALUE_STREAM_V1\n")
    page_records: list[dict[str, object]] = []
    gaps: list[MissingInterval] = []
    refetch_primary: list[OandaPriceCandle] = []
    cursor = DEV_START_UTC
    previous: OandaPriceCandle | None = None
    candle_count = 0
    empty_page_count = 0

    with m1_path.open("wb") as raw_file:
        with gzip.GzipFile(fileobj=raw_file, mode="wb", mtime=0) as compressed_file:
            with io.TextIOWrapper(compressed_file, encoding="utf-8", newline="\n") as text_file:
                for page_index, window in enumerate(windows):
                    page = _fetch_history_page_with_retry(
                        base_url=base_url,
                        account_id=account_id,
                        token=token,
                        instrument=instrument,
                        window=window,
                    )
                    page_records.append(_page_provenance_record(page_index, page))
                    if not page.candles:
                        empty_page_count += 1

                    for candle in page.candles:
                        if not (DEV_START_UTC <= candle.open_time < DEV_END_UTC):
                            continue

                        if previous is not None and candle.open_time == previous.open_time:
                            if candle_value_record(candle) != candle_value_record(previous):
                                raise SystemExit(
                                    f"conflicting duplicate OANDA candle for {instrument}"
                                )
                            continue
                        if previous is not None and candle.open_time < previous.open_time:
                            raise SystemExit(f"out-of-order OANDA history for {instrument}")
                        if candle.open_time > cursor:
                            _append_missing_interval(gaps, start=cursor, end=candle.open_time)
                        if candle.open_time < cursor:
                            raise SystemExit(f"overlapping OANDA history for {instrument}")

                        record = candle_value_record(candle)
                        line = json.dumps(record, sort_keys=True, separators=(",", ":"))
                        text_file.write(line)
                        text_file.write("\n")
                        normalized_digest.update(line.encode())
                        normalized_digest.update(b"\n")
                        candle_count += 1
                        cursor = candle.close_time
                        previous = candle
                        if _is_refetch_sample(candle):
                            refetch_primary.append(candle)

                    if (page_index + 1) % 25 == 0 or page_index + 1 == len(windows):
                        print(
                            f"history_progress instrument={instrument} "
                            f"pages={page_index + 1}/{len(windows)} candles={candle_count} "
                            f"empty_pages={empty_page_count}"
                        )
                    if page_index + 1 < len(windows):
                        time.sleep(request_delay_seconds)

    _append_missing_interval(gaps, start=cursor, end=DEV_END_UTC)

    refetch_results: list[dict[str, object]] = []
    for sample_index, (sample_start, sample_end) in enumerate(REFETCH_WINDOWS_UTC):
        page = _fetch_history_page_with_retry(
            base_url=base_url,
            account_id=account_id,
            token=token,
            instrument=instrument,
            window=OandaHistoryRequestWindow(start=sample_start, end=sample_end),
        )
        primary_window = tuple(
            candle
            for candle in refetch_primary
            if sample_start <= candle.open_time < sample_end
        )
        comparison_sha256 = assert_refetch_equal(
            primary_window,
            page.candles,
            start=sample_start,
            end=sample_end,
        )
        refetch_results.append(
            {
                "sample_index": sample_index,
                "start_utc": sample_start.isoformat(),
                "end_utc": sample_end.isoformat(),
                "complete_candle_count": len(primary_window),
                "comparison_sha256": comparison_sha256,
                "raw_refetch_response_sha256": page.raw_response_sha256,
                "status": "EXACT_PROVIDER_VALUE_MATCH",
            }
        )
        if sample_index + 1 < len(REFETCH_WINDOWS_UTC):
            time.sleep(request_delay_seconds)

    gap_sha = gap_digest(gaps)
    _write_json(
        pages_path,
        {
            "schema_version": "P6B_OANDA_HISTORY_PAGE_PROVENANCE_V1",
            "instrument": instrument,
            "page_count": len(page_records),
            "pages": page_records,
        },
    )
    _write_json(
        gaps_path,
        {
            "schema_version": "P6B_OANDA_MISSING_INTERVALS_V1",
            "instrument": instrument,
            "requested_start_utc": DEV_START_UTC.isoformat(),
            "requested_end_utc": DEV_END_UTC.isoformat(),
            "classification_state": "UNRECONCILED",
            "interval_count": len(gaps),
            "missing_minutes": sum(gap.missing_minutes for gap in gaps),
            "gap_sha256": gap_sha,
            "intervals": [missing_interval_record(gap) for gap in gaps],
        },
    )
    _write_json(
        manifest_path,
        {
            "schema_version": HISTORY_QUALIFICATION_SCHEMA_VERSION,
            "protocol_id": "P6B-OANDA-HISTORY-QUALIFICATION-V1",
            "provider": "OANDA_V20",
            "venue": "OANDA_FXTRADE",
            "environment": "practice",
            "account_scope": "REDACTED_RUNTIME_ACCOUNT",
            "instrument": instrument,
            "price_component": "MID",
            "granularity": "M1",
            "smooth": False,
            "requested_start_utc": DEV_START_UTC.isoformat(),
            "requested_end_utc": DEV_END_UTC.isoformat(),
            "page_minutes": DEFAULT_PAGE_MINUTES,
            "page_count": len(page_records),
            "empty_page_count": empty_page_count,
            "complete_candle_count": candle_count,
            "normalized_m1_sha256": normalized_digest.hexdigest(),
            "missing_interval_count": len(gaps),
            "missing_minutes": sum(gap.missing_minutes for gap in gaps),
            "missing_intervals_sha256": gap_sha,
            "refetch_samples": refetch_results,
            "status": "RETRIEVED_UNRECONCILED_GAPS",
            "detector_activity_counts_authorized": False,
            "strategy_outcome_access_authorized": False,
            "pnl_outcome_access_authorized": False,
            "backtester_authorized": False,
            "paper_trading_authorized": False,
            "shadow_trading_authorized": False,
            "live_trading_authorized": False,
        },
    )

    print(f"full_history_instrument={instrument}")
    print(f"full_history_pages={len(page_records)}")
    print(f"full_history_complete_candles={candle_count}")
    print(f"full_history_missing_intervals={len(gaps)}")
    print(f"full_history_missing_minutes={sum(gap.missing_minutes for gap in gaps)}")
    print("full_history_refetch=4/4_EXACT_PROVIDER_VALUE_MATCH")
    print("full_history_status=RETRIEVED_UNRECONCILED_GAPS")
    print("full_history_detector_activity_counts_authorized=false")
    print("full_history_pnl_outcome_access_authorized=false")


def main() -> int:
    args = _parser().parse_args()
    environment = str(args.environment)
    if environment == "live" and not args.allow_live_read:
        raise SystemExit("live OANDA reads require --allow-live-read; practice is the default")

    account_id = os.environ.get("OANDA_ACCOUNT_ID", "")
    token = os.environ.get("OANDA_API_TOKEN", "")
    if not account_id or not token:
        raise SystemExit(
            "OANDA_ACCOUNT_ID and OANDA_API_TOKEN must be provided via the runtime environment"
        )

    observed_at = datetime.now(UTC)
    base_url = PRACTICE_BASE_URL if environment == "practice" else LIVE_BASE_URL

    try:
        authorized_account_ids = fetch_authorized_account_ids(
            base_url=base_url,
            token=token,
        )
    except HTTPError as error:
        raise SystemExit(
            f"OANDA authorization preflight failed with HTTP {error.code} in {environment}; "
            "verify the personal access token and selected API environment"
        ) from None

    print(f"authorized_account_count={len(authorized_account_ids)}")
    configured_account_authorized = account_id in authorized_account_ids
    print(f"configured_account_authorized={str(configured_account_authorized).lower()}")
    if not configured_account_authorized:
        raise SystemExit(
            "configured OANDA_ACCOUNT_ID is not authorized by this token in the selected "
            f"{environment} environment"
        )

    try:
        instruments = fetch_account_instruments(
            base_url=base_url,
            account_id=account_id,
            token=token,
            observed_at=observed_at,
        )
    except HTTPError as error:
        raise SystemExit(
            f"OANDA instrument discovery failed with HTTP {error.code} after authorization "
            "preflight; the configured account is not usable for the v20 instrument endpoint"
        ) from None

    account = None
    account_summary_available = True
    try:
        account = fetch_account_summary(
            base_url=base_url,
            account_id=account_id,
            token=token,
            observed_at=observed_at,
        )
    except HTTPError as error:
        if error.code != 403:
            raise SystemExit(
                f"OANDA account-summary qualification failed with HTTP {error.code}"
            ) from None
        account_summary_available = False

    manifest = build_instrument_discovery_manifest(
        instruments,
        environment=environment,
        observed_at=observed_at,
        account=account,
    )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(manifest, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )

    matches = manifest["source_family_matches"]
    if not isinstance(matches, list):
        raise TypeError("qualification manifest source_family_matches is invalid")
    matched_count = sum(
        1
        for item in matches
        if isinstance(item, dict) and item.get("status") == "MATCHED"
    )

    account_profile = manifest["account_profile"]
    if account_profile is not None and not isinstance(account_profile, dict):
        raise TypeError("qualification manifest account_profile is invalid")

    print(f"provider={manifest['provider']}")
    print(f"environment={environment}")
    print(f"account_summary_available={str(account_summary_available).lower()}")
    if isinstance(account_profile, dict):
        print(f"account_home_currency={account_profile['home_currency']}")
    else:
        print("account_home_currency=UNAVAILABLE")
    print(f"available_instrument_count={manifest['available_instrument_count']}")
    print(f"source_family_matches={matched_count}/{len(matches)}")
    print(f"manifest={output}")

    history_smoke_output = args.history_smoke_output
    if history_smoke_output is not None:
        if environment != "practice":
            raise SystemExit("Phase-6B historical smoke is authorized only against practice")
        _run_history_smoke(
            base_url=base_url,
            account_id=account_id,
            token=token,
            output=Path(history_smoke_output),
        )

    full_history_instrument = args.full_history_instrument
    full_history_output_dir = args.full_history_output_dir
    if (full_history_instrument is None) != (full_history_output_dir is None):
        raise SystemExit(
            "--full-history-instrument and --full-history-output-dir must be supplied together"
        )
    if full_history_instrument is not None and full_history_output_dir is not None:
        if environment != "practice":
            raise SystemExit("Phase-6B full history collection is authorized only against practice")
        available_names = {instrument.name for instrument in instruments}
        if full_history_instrument not in available_names:
            raise SystemExit("frozen full-history instrument is not available on this account")
        _run_full_history_collection(
            base_url=base_url,
            account_id=account_id,
            token=token,
            instrument=full_history_instrument,
            output_dir=Path(full_history_output_dir),
            request_delay_seconds=float(args.full_history_request_delay_seconds),
        )

    print("strategy_outcome_access_authorized=false")
    print("live_trading_authorized=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
