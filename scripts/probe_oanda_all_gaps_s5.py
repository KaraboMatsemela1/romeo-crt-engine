from __future__ import annotations

import sys

import collect_oanda_history_shard as collector

# A single yearly shard can contain at most one leap-year-sized missing interval.
# The underlying collector still splits each gap into provider-safe six-hour S5
# request buckets, so this sentinel only removes the previous <=60 minute filter.
ALL_GAP_MAX_MINUTES = 60 * 24 * 366


def main() -> int:
    collector.MAX_SHORT_GAP_MINUTES = ALL_GAP_MAX_MINUTES
    if "--probe-s5-short-gaps" not in sys.argv:
        sys.argv.append("--probe-s5-short-gaps")
    return collector.main()


if __name__ == "__main__":
    raise SystemExit(main())
