"""Run the manual OANDA practice read-only connectivity smoke check."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from romeo_crt_engine.oanda_readonly_smoke import (
    SmokeGuardError,
    SmokeReadError,
    SmokeRuntimeConfig,
    failure_report,
    json_report,
    run_read_only_smoke,
    safe_error_message,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="Non-secret JSON report path")
    return parser


def main() -> int:
    output = _parser().parse_args().output
    try:
        report = run_read_only_smoke(SmokeRuntimeConfig.from_environment(os.environ))
    except (SmokeGuardError, SmokeReadError) as error:
        report = failure_report(error)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json_report(report), encoding="utf-8")
        print(safe_error_message(error))
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json_report(report), encoding="utf-8")
    print("oanda_read_only_smoke=PASS")
    print(f"instrument_metadata_count={report['instrument_count']}")
    print("execution_enabled=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
