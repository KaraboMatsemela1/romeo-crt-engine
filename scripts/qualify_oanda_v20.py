from __future__ import annotations

import argparse
import json
import os
from datetime import UTC, datetime
from pathlib import Path

from romeo_crt_engine.market_data.oanda_qualification import (
    build_instrument_discovery_manifest,
)
from romeo_crt_engine.market_data.providers.oanda_account import fetch_account_summary
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
