from __future__ import annotations

import argparse
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import HTTPError

from romeo_crt_engine.market_data.history_qualification_v2 import normalized_m1_sha256
from romeo_crt_engine.market_data.oanda_qualification import (
    build_instrument_discovery_manifest,
)
from romeo_crt_engine.market_data.providers.oanda_account import (
    fetch_account_summary,
    fetch_authorized_account_ids,
)
from romeo_crt_engine.market_data.providers.oanda_history import (
    OandaHistoryRequestWindow,
    fetch_m1_history_page,
)
from romeo_crt_engine.market_data.providers.oanda_v20 import (
    LIVE_BASE_URL,
    PRACTICE_BASE_URL,
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


def _environment(value: str) -> str:
    normalized = value.strip().lower()
    if normalized not in {"practice", "live"}:
        raise argparse.ArgumentTypeError("environment must be practice or live")
    return normalized


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Discover runtime OANDA account/instrument execution metadata and emit a "
            "credential-free Phase-6B qualification manifest. This command does not run "
            "strategy outcomes."
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
        help="Explicitly allow read-only qualification against the live API endpoint",
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
                price_component="M",
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

    print("strategy_outcome_access_authorized=false")
    print("live_trading_authorized=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
