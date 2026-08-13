from __future__ import annotations

import argparse
import json
import os
import time
from datetime import UTC, datetime, timedelta
from hashlib import sha256
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from romeo_crt_engine.market_data.history_qualification_v2 import (
    REFETCH_WINDOWS_UTC,
    assert_refetch_equal,
    enumerate_missing_intervals,
    gap_digest,
    missing_interval_record,
    normalized_m1_sha256,
    write_m1_jsonl_gz,
)
from romeo_crt_engine.market_data.providers.oanda_history import (
    DEFAULT_PAGE_MINUTES,
    OandaHistoryRequestWindow,
    fetch_m1_history_page,
    retrieve_m1_history,
)
from romeo_crt_engine.market_data.providers.oanda_v20 import (
    PRACTICE_BASE_URL,
    request_fingerprint,
)

FROZEN_INSTRUMENTS = ("EUR_USD", "XAU_USD", "NAS100_USD", "SPX500_USD")
FROZEN_YEARS = (2019, 2020, 2021, 2022)
REQUEST_DELAY_SECONDS = 0.55
RECONCILIATION_SCHEMA_VERSION = "P6B_OANDA_RECONCILIATION_EVIDENCE_V2"
OBSERVATION_POLICY_VERSION = "P6B_OANDA_OBSERVATION_POLICY_V2"
S5_EVIDENCE_SCHEMA_VERSION = "P6B_OANDA_S5_GAP_EVIDENCE_V1"
MAX_SHORT_GAP_MINUTES = 60
S5_BUCKET_HOURS = 6
REDACTED_ACCOUNT_PATH_TOKEN = "{ACCOUNT}"


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Collect one frozen Phase-6B OANDA practice MID/M1 yearly shard locally. "
            "This command performs data qualification only and never invokes detector, "
            "backtest, order, paper, shadow, or live-trading code."
        )
    )
    parser.add_argument("--instrument", required=True, choices=FROZEN_INSTRUMENTS)
    parser.add_argument("--year", required=True, type=int, choices=FROZEN_YEARS)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("artifacts/phase6b/oanda_raw"),
    )
    parser.add_argument(
        "--probe-s5-short-gaps",
        action="store_true",
        help="Probe M1 gaps <=60 minutes with read-only S5 evidence and persist counts/hashes only.",
    )
    return parser


def _sha256_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _page_record(page: object) -> dict[str, object]:
    from romeo_crt_engine.market_data.providers.oanda_history import OandaHistoryPage

    if not isinstance(page, OandaHistoryPage):
        raise TypeError("unexpected OANDA history page type")
    return {
        "start_utc": page.window.start.astimezone(UTC).isoformat(),
        "end_utc": page.window.end.astimezone(UTC).isoformat(),
        "retrieved_at_utc": page.retrieved_at.astimezone(UTC).isoformat(),
        "request_sha256": page.request_sha256,
        "raw_response_sha256": page.raw_response_sha256,
        "complete_candle_count": len(page.candles),
    }


def _assert_false_flags(document: dict[str, object]) -> None:
    false_flags = (
        "trusted_dataset_authorized",
        "detector_execution_authorized",
        "tradeplan_count_access_authorized",
        "backtester_authorized",
        "pnl_outcome_access_authorized",
        "paper_trading_authorized",
        "shadow_trading_authorized",
        "live_trading_authorized",
    )
    for flag in false_flags:
        if document.get(flag) is not False:
            raise ValueError(f"{flag} must remain false")


def _assert_manifest_safe(manifest: dict[str, object]) -> None:
    if manifest.get("schema_version") != "P6B_OANDA_HISTORY_SHARD_V1":
        raise ValueError("unexpected shard manifest schema")
    if manifest.get("account_scope") != "REDACTED_RUNTIME_ACCOUNT":
        raise ValueError("runtime account scope must remain redacted")
    if manifest.get("gap_reconciliation_status") != "UNRECONCILED":
        raise ValueError("raw shard must remain UNRECONCILED")

    refetch = manifest.get("refetch")
    if not isinstance(refetch, dict) or refetch.get("status") != "EXACT_PROVIDER_VALUE_MATCH":
        raise ValueError("independent re-fetch must exactly match provider values")

    _assert_false_flags(manifest)

    serialized = json.dumps(manifest, sort_keys=True)
    forbidden = (
        "Authorization",
        "Bearer ",
        "OANDA_API_TOKEN",
        "OANDA_ACCOUNT_ID",
        '"balance"',
        '"NAV"',
    )
    for marker in forbidden:
        if marker in serialized:
            raise ValueError(f"forbidden persisted marker found: {marker}")


def _build_reconciliation_evidence(manifest: dict[str, object]) -> dict[str, object]:
    missing = manifest.get("missing_intervals")
    refetch = manifest.get("refetch")
    if not isinstance(missing, list):
        raise TypeError("raw shard manifest lacks exact missing-interval inventory")
    if not isinstance(refetch, dict):
        raise TypeError("raw shard manifest lacks refetch evidence")

    evidence: dict[str, object] = {
        "schema_version": RECONCILIATION_SCHEMA_VERSION,
        "observation_policy_version": OBSERVATION_POLICY_VERSION,
        "parent_protocol": "P6B-OANDA-HISTORY-QUALIFICATION-V1",
        "provider": manifest.get("provider"),
        "environment": "practice",
        "account_scope": "REDACTED_RUNTIME_ACCOUNT",
        "instrument": manifest.get("instrument"),
        "year": manifest.get("year"),
        "price_component": "MID",
        "granularity": "M1",
        "requested_start_utc": manifest.get("requested_start_utc"),
        "requested_end_utc": manifest.get("requested_end_utc"),
        "complete_candle_count": manifest.get("complete_candle_count"),
        "normalized_provider_values_sha256": manifest.get(
            "normalized_provider_values_sha256"
        ),
        "missing_interval_count": manifest.get("missing_interval_count"),
        "missing_minutes": manifest.get("missing_minutes"),
        "missing_intervals_sha256": manifest.get("missing_intervals_sha256"),
        "missing_intervals": missing,
        "refetch": {
            "start_utc": refetch.get("start_utc"),
            "end_utc": refetch.get("end_utc"),
            "provider_value_sha256": refetch.get("provider_value_sha256"),
            "status": refetch.get("status"),
        },
        "classification_contract": {
            "allowed_terminal_states": [
                "EXPECTED_MARKET_CLOSURE",
                "NO_PRICE_OBSERVATION",
            ],
            "fail_closed_state": "UNRESOLVED_PROVIDER_GAP",
            "synthetic_prices_authorized": False,
            "forward_fill_authorized": False,
            "timestamp_shape_only_classification_authorized": False,
        },
        "reconciliation_status": "PENDING_CLASSIFICATION",
        "trusted_dataset_authorized": False,
        "detector_execution_authorized": False,
        "tradeplan_count_access_authorized": False,
        "backtester_authorized": False,
        "pnl_outcome_access_authorized": False,
        "paper_trading_authorized": False,
        "shadow_trading_authorized": False,
        "live_trading_authorized": False,
    }
    _assert_false_flags(evidence)
    serialized = json.dumps(evidence, sort_keys=True).lower()
    for marker in (
        "authorization",
        "bearer ",
        "oanda_api_token",
        "oanda_account_id",
        '"balance"',
        '"nav"',
        ".jsonl.gz",
    ):
        if marker in serialized:
            raise ValueError(f"forbidden reconciliation evidence marker found: {marker}")
    return evidence


def _parse_utc(value: object) -> datetime:
    if not isinstance(value, str):
        raise TypeError("timestamp must be a string")
    parsed = datetime.fromisoformat(value)
    if parsed.utcoffset() is None:
        raise ValueError("timestamp must be timezone-aware")
    return parsed.astimezone(UTC)


def _s5_bucket_start(timestamp: datetime) -> datetime:
    return timestamp.replace(
        hour=(timestamp.hour // S5_BUCKET_HOURS) * S5_BUCKET_HOURS,
        minute=0,
        second=0,
        microsecond=0,
    )


def _s5_buckets(start: datetime, end: datetime) -> tuple[tuple[datetime, datetime], ...]:
    cursor = _s5_bucket_start(start)
    buckets: list[tuple[datetime, datetime]] = []
    while cursor < end:
        buckets.append((cursor, cursor + timedelta(hours=S5_BUCKET_HOURS)))
        cursor += timedelta(hours=S5_BUCKET_HOURS)
    return tuple(buckets)


def _fetch_s5_bucket(
    *,
    account_id: str,
    token: str,
    instrument: str,
    start: datetime,
    end: datetime,
) -> dict[str, object]:
    parameters = {
        "price": "M",
        "granularity": "S5",
        "from": start.isoformat().replace("+00:00", "Z"),
        "to": end.isoformat().replace("+00:00", "Z"),
        "smooth": "false",
        "includeFirst": "true",
    }
    real_path = f"/v3/accounts/{account_id}/instruments/{instrument}/candles"
    redacted_path = (
        f"/v3/accounts/{REDACTED_ACCOUNT_PATH_TOKEN}/instruments/{instrument}/candles"
    )
    request = Request(
        f"{PRACTICE_BASE_URL}{real_path}?{urlencode(parameters)}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept-Datetime-Format": "RFC3339",
        },
        method="GET",
    )
    with urlopen(request, timeout=45.0) as response:
        payload = cast(bytes, response.read())
    document = cast(dict[str, Any], json.loads(payload))
    if document.get("instrument") != instrument or document.get("granularity") != "S5":
        raise ValueError("unexpected OANDA S5 response identity")
    raw_candles = document.get("candles")
    if not isinstance(raw_candles, list):
        raise TypeError("OANDA S5 response candles must be a list")
    timestamps: list[str] = []
    for raw in raw_candles:
        if not isinstance(raw, dict) or raw.get("complete") is not True:
            continue
        timestamp = raw.get("time")
        if not isinstance(timestamp, str):
            raise TypeError("OANDA S5 candle time must be a string")
        timestamps.append(_parse_utc(timestamp).isoformat())
    return {
        "start_utc": start.isoformat(),
        "end_utc": end.isoformat(),
        "request_sha256": request_fingerprint(redacted_path, parameters),
        "raw_response_sha256": sha256(payload).hexdigest(),
        "complete_s5_count": len(timestamps),
        "timestamps": timestamps,
    }


def _build_s5_gap_evidence(
    *,
    reconciliation: dict[str, object],
    account_id: str,
    token: str,
) -> dict[str, object]:
    instrument = str(reconciliation["instrument"])
    missing = reconciliation.get("missing_intervals")
    if not isinstance(missing, list):
        raise TypeError("reconciliation evidence lacks missing intervals")

    eligible: list[tuple[int, datetime, datetime, int]] = []
    needed: set[tuple[datetime, datetime]] = set()
    for index, raw_gap in enumerate(missing):
        if not isinstance(raw_gap, dict):
            raise TypeError("missing interval record must be an object")
        minutes = int(raw_gap["missing_minutes"])
        if minutes > MAX_SHORT_GAP_MINUTES:
            continue
        start = _parse_utc(raw_gap["start_utc"])
        end = _parse_utc(raw_gap["end_utc"])
        eligible.append((index, start, end, minutes))
        needed.update(_s5_buckets(start, end))

    bucket_results: dict[tuple[datetime, datetime], dict[str, object]] = {}
    for position, bucket in enumerate(sorted(needed)):
        start, end = bucket
        bucket_results[bucket] = _fetch_s5_bucket(
            account_id=account_id,
            token=token,
            instrument=instrument,
            start=start,
            end=end,
        )
        if position < len(needed) - 1:
            time.sleep(REQUEST_DELAY_SECONDS)

    classifications: list[dict[str, object]] = []
    no_price_gap_count = 0
    no_price_minutes = 0
    unresolved_gap_count = 0
    unresolved_minutes = 0
    for gap_index, start, end, minutes in eligible:
        observations = 0
        refs: list[dict[str, object]] = []
        for bucket in _s5_buckets(start, end):
            result = bucket_results[bucket]
            timestamps = result["timestamps"]
            if not isinstance(timestamps, list):
                raise TypeError("internal S5 bucket timestamps must be a list")
            count_inside = sum(
                1
                for raw_timestamp in timestamps
                if start <= _parse_utc(raw_timestamp) < end
            )
            observations += count_inside
            refs.append(
                {
                    "start_utc": result["start_utc"],
                    "end_utc": result["end_utc"],
                    "request_sha256": result["request_sha256"],
                    "raw_response_sha256": result["raw_response_sha256"],
                    "complete_s5_count_in_gap": count_inside,
                }
            )
        classification = (
            "NO_PRICE_OBSERVATION" if observations == 0 else "UNRESOLVED_PROVIDER_GAP"
        )
        if observations == 0:
            no_price_gap_count += 1
            no_price_minutes += minutes
        else:
            unresolved_gap_count += 1
            unresolved_minutes += minutes
        classifications.append(
            {
                "gap_index": gap_index,
                "start_utc": start.isoformat(),
                "end_utc": end.isoformat(),
                "missing_minutes": minutes,
                "classification": classification,
                "s5_complete_observations_inside_gap": observations,
                "evidence": refs,
            }
        )

    result: dict[str, object] = {
        "schema_version": S5_EVIDENCE_SCHEMA_VERSION,
        "observation_policy_version": OBSERVATION_POLICY_VERSION,
        "provider": "OANDA_V20",
        "environment": "practice",
        "account_scope": "REDACTED_RUNTIME_ACCOUNT",
        "instrument": instrument,
        "year": reconciliation["year"],
        "source_missing_intervals_sha256": reconciliation["missing_intervals_sha256"],
        "max_probed_gap_minutes": MAX_SHORT_GAP_MINUTES,
        "s5_bucket_hours": S5_BUCKET_HOURS,
        "eligible_gap_count": len(eligible),
        "queried_bucket_count": len(needed),
        "no_price_observation_gap_count": no_price_gap_count,
        "no_price_observation_minutes": no_price_minutes,
        "unresolved_provider_gap_count": unresolved_gap_count,
        "unresolved_provider_gap_minutes": unresolved_minutes,
        "classifications": classifications,
        "trusted_dataset_authorized": False,
        "detector_execution_authorized": False,
        "tradeplan_count_access_authorized": False,
        "backtester_authorized": False,
        "pnl_outcome_access_authorized": False,
        "paper_trading_authorized": False,
        "shadow_trading_authorized": False,
        "live_trading_authorized": False,
    }
    _assert_false_flags(result)
    serialized = json.dumps(result, sort_keys=True).lower()
    for marker in (
        "authorization",
        "bearer ",
        "oanda_api_token",
        "oanda_account_id",
        '"balance"',
        '"nav"',
    ):
        if marker in serialized:
            raise ValueError(f"forbidden S5 evidence marker found: {marker}")
    return result


def main() -> int:
    args = _parser().parse_args()
    instrument = str(args.instrument)
    year = int(args.year)
    output_dir = Path(args.output_dir)

    environment = os.environ.get("OANDA_ENV", "practice").strip().lower()
    if environment != "practice":
        raise SystemExit("Phase-6B raw history collection is authorized only for OANDA practice")

    account_id = os.environ.get("OANDA_ACCOUNT_ID", "")
    token = os.environ.get("OANDA_API_TOKEN", "")
    if not account_id or not token:
        raise SystemExit("OANDA_ACCOUNT_ID and OANDA_API_TOKEN are required in the local environment")

    start = datetime(year, 1, 1, tzinfo=UTC)
    end = datetime(year + 1, 1, 1, tzinfo=UTC)
    refetch_start, refetch_end = REFETCH_WINDOWS_UTC[FROZEN_YEARS.index(year)]

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

    output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"{instrument}_{year}_MID_M1"
    values_path = output_dir / f"{stem}.jsonl.gz"
    manifest_path = output_dir / f"{stem}.manifest.json"
    reconciliation_path = output_dir / f"{stem}.reconciliation-v2.json"
    s5_evidence_path = output_dir / f"{stem}.s5-gap-evidence-v1.json"

    normalized_sha = normalized_m1_sha256(retrieval.candles)
    jsonl_content_sha = write_m1_jsonl_gz(values_path, retrieval.candles)
    missing = enumerate_missing_intervals(
        retrieval.candles,
        requested_start=start,
        requested_end=end,
    )

    refetch_page = fetch_m1_history_page(
        base_url=PRACTICE_BASE_URL,
        account_id=account_id,
        token=token,
        instrument=instrument,
        window=OandaHistoryRequestWindow(start=refetch_start, end=refetch_end),
        price_component="M",
        timeout_seconds=45.0,
    )
    refetch_value_sha = assert_refetch_equal(
        retrieval.candles,
        refetch_page.candles,
        start=refetch_start,
        end=refetch_end,
    )

    manifest: dict[str, object] = {
        "schema_version": "P6B_OANDA_HISTORY_SHARD_V1",
        "execution_id": "P6B-OANDA-HISTORY-SHARD-EXECUTION-V1",
        "parent_protocol": "P6B-OANDA-HISTORY-QUALIFICATION-V1",
        "provider": "OANDA_V20",
        "environment": "practice",
        "account_scope": "REDACTED_RUNTIME_ACCOUNT",
        "instrument": instrument,
        "year": year,
        "price_component": "MID",
        "granularity": "M1",
        "smooth": False,
        "requested_start_utc": start.isoformat(),
        "requested_end_utc": end.isoformat(),
        "page_minutes": DEFAULT_PAGE_MINUTES,
        "request_delay_seconds": REQUEST_DELAY_SECONDS,
        "page_count": len(retrieval.pages),
        "complete_candle_count": len(retrieval.candles),
        "retrieval_sha256": retrieval.retrieval_sha256,
        "normalized_provider_values_sha256": normalized_sha,
        "jsonl_content_sha256": jsonl_content_sha,
        "gzip_file_sha256_noncanonical": _sha256_file(values_path),
        "pages": [_page_record(page) for page in retrieval.pages],
        "missing_interval_count": len(missing),
        "missing_minutes": sum(interval.missing_minutes for interval in missing),
        "missing_intervals_sha256": gap_digest(missing),
        "missing_intervals": [missing_interval_record(interval) for interval in missing],
        "refetch": {
            "start_utc": refetch_start.isoformat(),
            "end_utc": refetch_end.isoformat(),
            "request_sha256": refetch_page.request_sha256,
            "raw_response_sha256": refetch_page.raw_response_sha256,
            "complete_candle_count": len(refetch_page.candles),
            "provider_value_sha256": refetch_value_sha,
            "status": "EXACT_PROVIDER_VALUE_MATCH",
        },
        "gap_reconciliation_status": "UNRECONCILED",
        "trusted_dataset_authorized": False,
        "detector_execution_authorized": False,
        "tradeplan_count_access_authorized": False,
        "backtester_authorized": False,
        "pnl_outcome_access_authorized": False,
        "paper_trading_authorized": False,
        "shadow_trading_authorized": False,
        "live_trading_authorized": False,
    }
    _assert_manifest_safe(manifest)
    manifest_path.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    reconciliation = _build_reconciliation_evidence(manifest)
    reconciliation_path.write_text(
        json.dumps(reconciliation, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )

    if args.probe_s5_short_gaps:
        s5_evidence = _build_s5_gap_evidence(
            reconciliation=reconciliation,
            account_id=account_id,
            token=token,
        )
        s5_evidence_path.write_text(
            json.dumps(s5_evidence, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"s5_gap_evidence={s5_evidence_path}")
        print(f"s5_eligible_gaps={s5_evidence['eligible_gap_count']}")
        print(f"s5_no_price_gaps={s5_evidence['no_price_observation_gap_count']}")
        print(f"s5_unresolved_gaps={s5_evidence['unresolved_provider_gap_count']}")

    print(f"history_shard={instrument}/{year}")
    print(f"complete_candles={len(retrieval.candles)}")
    print(f"pages={len(retrieval.pages)}")
    print(f"missing_intervals={len(missing)}")
    print(f"missing_minutes={manifest['missing_minutes']}")
    print("manifest_self_check=PASS")
    print("refetch=EXACT_PROVIDER_VALUE_MATCH")
    print("reconciliation_evidence_safe=true")
    print("reconciliation_status=PENDING_CLASSIFICATION")
    print(f"values={values_path}")
    print(f"manifest={manifest_path}")
    print(f"reconciliation={reconciliation_path}")
    print("detector_execution_authorized=false")
    print("pnl_outcome_access_authorized=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
