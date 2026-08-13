from __future__ import annotations

import json
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

PRACTICE_BASE_URL = "https://api-fxpractice.oanda.com"
INSTRUMENT = "EUR_USD"
PROBES = (
    ("2019", datetime(2019, 2, 6, 11, 59, tzinfo=UTC)),
    ("2020", datetime(2020, 2, 5, 18, 26, tzinfo=UTC)),
    ("2021", datetime(2021, 8, 16, 16, 27, tzinfo=UTC)),
    ("2022", datetime(2022, 2, 1, 3, 16, tzinfo=UTC)),
)


def _fetch(
    *,
    account_id: str,
    token: str,
    granularity: str,
    start: datetime,
    end: datetime,
) -> list[dict[str, object]]:
    parameters = urlencode(
        {
            "price": "M",
            "granularity": granularity,
            "from": start.isoformat().replace("+00:00", "Z"),
            "to": end.isoformat().replace("+00:00", "Z"),
            "smooth": "false",
            "includeFirst": "true",
        }
    )
    path = f"/v3/accounts/{account_id}/instruments/{INSTRUMENT}/candles"
    request = Request(
        f"{PRACTICE_BASE_URL}{path}?{parameters}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept-Datetime-Format": "RFC3339",
        },
        method="GET",
    )
    with urlopen(request, timeout=30.0) as response:
        document = json.loads(response.read())
    if document.get("instrument") != INSTRUMENT or document.get("granularity") != granularity:
        raise ValueError("unexpected OANDA candle response identity")
    candles = document.get("candles")
    if not isinstance(candles, list):
        raise ValueError("unexpected OANDA candle response schema")
    return candles


def _timestamp(candle: dict[str, object]) -> datetime:
    value = candle.get("time")
    if not isinstance(value, str):
        raise ValueError("OANDA candle is missing a timestamp")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def main() -> int:
    if os.environ.get("OANDA_ENV", "practice").strip().lower() != "practice":
        raise SystemExit("Phase-6B candle absence probe is practice-only")
    account_id = os.environ.get("OANDA_ACCOUNT_ID", "")
    token = os.environ.get("OANDA_API_TOKEN", "")
    if not account_id or not token:
        raise SystemExit("OANDA_ACCOUNT_ID and OANDA_API_TOKEN are required")

    results: list[dict[str, object]] = []
    for year, missing_start in PROBES:
        query_start = missing_start - timedelta(minutes=1)
        query_end = missing_start + timedelta(minutes=2)
        missing_end = missing_start + timedelta(minutes=1)
        m1 = _fetch(
            account_id=account_id,
            token=token,
            granularity="M1",
            start=query_start,
            end=query_end,
        )
        s5 = _fetch(
            account_id=account_id,
            token=token,
            granularity="S5",
            start=query_start,
            end=query_end,
        )

        m1_missing = [item for item in m1 if missing_start <= _timestamp(item) < missing_end]
        s5_missing = [item for item in s5 if missing_start <= _timestamp(item) < missing_end]
        s5_prices = 0
        for item in s5_missing:
            volume = item.get("volume")
            if not isinstance(volume, int):
                raise ValueError("OANDA S5 candle volume is not an integer")
            s5_prices += volume

        results.append(
            {
                "year": year,
                "missing_minute_start_utc": missing_start.isoformat(),
                "query_start_utc": query_start.isoformat(),
                "query_end_utc": query_end.isoformat(),
                "m1_query_candle_count": len(m1),
                "m1_candles_inside_missing_minute": len(m1_missing),
                "m1_query_times_utc": [item["time"] for item in m1],
                "s5_query_candle_count": len(s5),
                "s5_candles_inside_missing_minute": len(s5_missing),
                "s5_prices_created_inside_missing_minute": s5_prices,
                "s5_query_times_utc": [item["time"] for item in s5],
            }
        )

    artifact = {
        "schema_version": "P6B_OANDA_CANDLE_ABSENCE_PROBE_V1",
        "provider": "OANDA_V20",
        "environment": "practice",
        "account_scope": "REDACTED_RUNTIME_ACCOUNT",
        "instrument": INSTRUMENT,
        "price_component": "MID",
        "probes_selected_from_raw_gap_inventory_only": True,
        "results": results,
        "detector_execution_authorized": False,
        "pnl_outcome_access_authorized": False,
        "live_trading_authorized": False,
    }
    serialized = json.dumps(artifact, sort_keys=True).lower()
    for forbidden in ("account_id", "api_token", "authorization", "bearer ", "balance", "nav"):
        if forbidden in serialized:
            raise ValueError("probe artifact contains forbidden credential/account material")

    output = Path("artifacts/phase6b/oanda_raw/EUR_USD_CANDLE_ABSENCE_PROBE_V1.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(artifact, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    print("OANDA_CANDLE_ABSENCE_PROBE_SAFE=true")
    for row in results:
        print(
            "year={year} m1_inside={m1} s5_inside={s5} s5_prices={prices}".format(
                year=row["year"],
                m1=row["m1_candles_inside_missing_minute"],
                s5=row["s5_candles_inside_missing_minute"],
                prices=row["s5_prices_created_inside_missing_minute"],
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
