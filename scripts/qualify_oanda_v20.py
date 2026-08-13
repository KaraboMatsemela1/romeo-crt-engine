from __future__ import annotations

import argparse
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from urllib.error import HTTPError

from romeo_crt_engine.market_data.oanda_qualification import (
    build_instrument_discovery_manifest,
)
from romeo_crt_engine.market_data.providers.oanda_account import (
    fetch_account_summary,
    fetch_authorized_account_ids,
)
from romeo_crt_engine.market_data.providers.oanda_v20 import (
    LIVE_BASE_URL,
    PRACTICE_BASE_URL,
    fetch_account_instruments,
)


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
    return parser


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
        account = fetch_account_summary(
            base_url=base_url,
            account_id=account_id,
            token=token,
            observed_at=observed_at,
        )
        instruments = fetch_account_instruments(
            base_url=base_url,
            account_id=account_id,
            token=token,
            observed_at=observed_at,
        )
    except HTTPError as error:
        raise SystemExit(
            f"OANDA account qualification failed with HTTP {error.code} after authorization "
            "preflight; verify account API eligibility and provider account type"
        ) from None

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
    if not isinstance(account_profile, dict):
        raise TypeError("qualification manifest account_profile is invalid")

    print(f"provider={manifest['provider']}")
    print(f"environment={environment}")
    print(f"account_home_currency={account_profile['home_currency']}")
    print(f"available_instrument_count={manifest['available_instrument_count']}")
    print(f"source_family_matches={matched_count}/{len(matches)}")
    print(f"manifest={output}")
    print("strategy_outcome_access_authorized=false")
    print("live_trading_authorized=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
