from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import NoReturn

from romeo_crt_engine.alpha_lab.backtest_v4 import run_v4_backtest
from romeo_crt_engine.alpha_lab.data import load_binance_h1
from romeo_crt_engine.alpha_lab.models import CostModel, Metrics
from romeo_crt_engine.alpha_lab.models_v4 import V4Config
from romeo_crt_engine.alpha_lab.optimize_v4 import (
    search_v4_dev,
    v4_holdout_a_gate,
    v4_holdout_b_gate,
)

SCHEMA_VERSION = "ALPHA_LAB_CANDIDATE_V4"
BTC_SYMBOL = "BTCUSDT"
ETH_SYMBOL = "ETHUSDT"
BNB_SYMBOL = "BNBUSDT"
BTC_DEV_START = datetime(2019, 1, 1, tzinfo=UTC)
BTC_DEV_END = datetime(2023, 1, 1, tzinfo=UTC)
ETH_HOLDOUT_START = datetime(2019, 1, 1, tzinfo=UTC)
ETH_HOLDOUT_END = datetime(2025, 1, 1, tzinfo=UTC)
BNB_CONFIRM_START = datetime(2025, 1, 1, tzinfo=UTC)
BNB_CONFIRM_END = datetime(2026, 8, 1, tzinfo=UTC)


def _metrics_dict(metrics: Metrics) -> dict[str, object]:
    return {
        "closed_trades": metrics.closed_trades,
        "wins": metrics.wins,
        "losses": metrics.losses,
        "win_rate": metrics.win_rate,
        "expectancy_r": metrics.expectancy_r,
        "profit_factor": metrics.profit_factor,
        "net_pnl": metrics.net_pnl,
        "return_pct": metrics.return_pct,
        "max_drawdown_pct": metrics.max_drawdown_pct,
        "final_equity": metrics.final_equity,
    }


def _write_json(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _as_mapping(value: object, *, field: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError(f"{field} must be an object")
    result: dict[str, object] = {}
    for key, item in value.items():
        if not isinstance(key, str):
            raise TypeError(f"{field} keys must be strings")
        result[key] = item
    return result


def _required(mapping: dict[str, object], key: str) -> object:
    if key not in mapping:
        raise ValueError(f"missing required field: {key}")
    return mapping[key]


def _as_int(value: object, *, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{field} must be integer")
    return value


def _as_float(value: object, *, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{field} must be numeric")
    return float(value)


def _as_bool(value: object, *, field: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{field} must be boolean")
    return value


def _as_str(value: object, *, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be string")
    return value


def _load_json(path: Path) -> dict[str, object]:
    raw: object = json.loads(path.read_text(encoding="utf-8"))
    return _as_mapping(raw, field=str(path))


def _read_candidate(path: Path) -> tuple[V4Config, CostModel, str, bool]:
    payload = _load_json(path)
    if _as_str(_required(payload, "schema_version"), field="schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported V4 candidate schema")
    config_map = _as_mapping(_required(payload, "config"), field="config")
    costs_map = _as_mapping(_required(payload, "costs"), field="costs")
    config = V4Config(
        entry_lookback=_as_int(_required(config_map, "entry_lookback"), field="entry_lookback"),
        breakout_buffer_bps=_as_float(
            _required(config_map, "breakout_buffer_bps"), field="breakout_buffer_bps"
        ),
        use_rising_ema200_regime=_as_bool(
            _required(config_map, "use_rising_ema200_regime"),
            field="use_rising_ema200_regime",
        ),
        atr_period=_as_int(_required(config_map, "atr_period"), field="atr_period"),
        initial_stop_atr=_as_float(
            _required(config_map, "initial_stop_atr"), field="initial_stop_atr"
        ),
        trail_atr=_as_float(_required(config_map, "trail_atr"), field="trail_atr"),
        max_hold_bars=_as_int(_required(config_map, "max_hold_bars"), field="max_hold_bars"),
        risk_fraction=_as_float(_required(config_map, "risk_fraction"), field="risk_fraction"),
    )
    costs = CostModel(
        fee_bps_per_side=_as_float(
            _required(costs_map, "fee_bps_per_side"), field="fee_bps_per_side"
        ),
        slippage_bps_per_side=_as_float(
            _required(costs_map, "slippage_bps_per_side"), field="slippage_bps_per_side"
        ),
        max_leverage=_as_float(_required(costs_map, "max_leverage"), field="max_leverage"),
    )
    candidate_id = _as_str(_required(payload, "candidate_id"), field="candidate_id")
    if candidate_id != config.config_id:
        raise ValueError("candidate_id does not match frozen V4 configuration")
    dev_gate_pass = _as_bool(_required(payload, "dev_gate_pass"), field="dev_gate_pass")
    return config, costs, candidate_id, dev_gate_pass


def _read_holdout_a_pass(path: Path, *, candidate_id: str) -> None:
    payload = _load_json(path)
    observed_id = _as_str(_required(payload, "candidate_id"), field="candidate_id")
    if observed_id != candidate_id:
        raise ValueError("holdout-A candidate identity mismatch")
    if not _as_bool(_required(payload, "holdout_a_gate_pass"), field="holdout_a_gate_pass"):
        raise ValueError("holdout-B access denied because holdout A did not pass")


def _dev_search(cache_dir: Path, candidate_out: Path, metrics_out: Path) -> int:
    dataset = load_binance_h1(
        symbol=BTC_SYMBOL,
        start=BTC_DEV_START,
        end=BTC_DEV_END,
        cache_dir=cache_dir / "btc-dev",
    )
    costs = CostModel()
    search = search_v4_dev(dataset.bars, costs=costs)
    candidate: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "candidate_id": search.result.config.config_id,
        "development_market": BTC_SYMBOL,
        "dev_window": {
            "start": BTC_DEV_START.isoformat(),
            "end_exclusive": BTC_DEV_END.isoformat(),
        },
        "fresh_holdout_a": {
            "symbol": ETH_SYMBOL,
            "start": ETH_HOLDOUT_START.isoformat(),
            "end_exclusive": ETH_HOLDOUT_END.isoformat(),
        },
        "fresh_holdout_b": {
            "symbol": BNB_SYMBOL,
            "start": BNB_CONFIRM_START.isoformat(),
            "end_exclusive": BNB_CONFIRM_END.isoformat(),
        },
        "dev_dataset_sha256": dataset.dataset_sha256,
        "config": asdict(search.result.config),
        "costs": asdict(costs),
        "dev_metrics": _metrics_dict(search.result.metrics),
        "search_score": search.score,
        "searched_configs": search.searched_configs,
        "dev_gate_pass": search.gate_pass,
        "holdout_a_access_authorized": search.gate_pass,
        "btc_2023_plus_accessed_by_v4": False,
    }
    _write_json(candidate_out, candidate)
    _write_json(
        metrics_out,
        {
            "candidate_id": search.result.config.config_id,
            "dataset_sha256": dataset.dataset_sha256,
            "metrics": _metrics_dict(search.result.metrics),
            "searched_configs": search.searched_configs,
            "dev_gate_pass": search.gate_pass,
        },
    )
    print("ALPHA_LAB_V4_DEV_RESULT=" + json.dumps(candidate, sort_keys=True))
    return 0


def _holdout_a(cache_dir: Path, candidate_path: Path, result_out: Path) -> int:
    config, costs, candidate_id, dev_gate_pass = _read_candidate(candidate_path)
    if not dev_gate_pass:
        raise ValueError("ETH holdout access denied because V4 DEV did not pass")
    dataset = load_binance_h1(
        symbol=ETH_SYMBOL,
        start=ETH_HOLDOUT_START,
        end=ETH_HOLDOUT_END,
        cache_dir=cache_dir / "eth-holdout-a",
    )
    result = run_v4_backtest(dataset.bars, config, costs=costs)
    passed = v4_holdout_a_gate(result)
    payload: dict[str, object] = {
        "schema_version": "ALPHA_LAB_HOLDOUT_A_RESULT_V4",
        "candidate_id": candidate_id,
        "symbol": ETH_SYMBOL,
        "window": {
            "start": ETH_HOLDOUT_START.isoformat(),
            "end_exclusive": ETH_HOLDOUT_END.isoformat(),
        },
        "dataset_sha256": dataset.dataset_sha256,
        "metrics": _metrics_dict(result.metrics),
        "holdout_a_gate_pass": passed,
        "holdout_b_access_authorized": passed,
    }
    _write_json(result_out, payload)
    print("ALPHA_LAB_V4_HOLDOUT_A_RESULT=" + json.dumps(payload, sort_keys=True))
    return 0


def _holdout_b(
    cache_dir: Path,
    candidate_path: Path,
    holdout_a_path: Path,
    result_out: Path,
) -> int:
    config, costs, candidate_id, dev_gate_pass = _read_candidate(candidate_path)
    if not dev_gate_pass:
        raise ValueError("BNB holdout access denied because V4 DEV did not pass")
    _read_holdout_a_pass(holdout_a_path, candidate_id=candidate_id)
    dataset = load_binance_h1(
        symbol=BNB_SYMBOL,
        start=BNB_CONFIRM_START,
        end=BNB_CONFIRM_END,
        cache_dir=cache_dir / "bnb-holdout-b",
    )
    result = run_v4_backtest(dataset.bars, config, costs=costs)
    passed = v4_holdout_b_gate(result)
    payload: dict[str, object] = {
        "schema_version": "ALPHA_LAB_HOLDOUT_B_RESULT_V4",
        "candidate_id": candidate_id,
        "symbol": BNB_SYMBOL,
        "window": {
            "start": BNB_CONFIRM_START.isoformat(),
            "end_exclusive": BNB_CONFIRM_END.isoformat(),
        },
        "dataset_sha256": dataset.dataset_sha256,
        "metrics": _metrics_dict(result.metrics),
        "holdout_b_gate_pass": passed,
        "disposition": "MULTI_MARKET_HISTORICAL_PASS" if passed else "HOLDOUT_B_FAIL_REJECT_V4",
        "paper_trading_authorized": False,
        "live_trading_authorized": False,
    }
    _write_json(result_out, payload)
    print("ALPHA_LAB_V4_HOLDOUT_B_RESULT=" + json.dumps(payload, sort_keys=True))
    return 0


def _die(message: str) -> NoReturn:
    raise SystemExit(message)


def main() -> int:
    parser = argparse.ArgumentParser(description="Alpha Lab V4 fresh-holdout research cycle")
    subparsers = parser.add_subparsers(dest="command", required=True)

    dev = subparsers.add_parser("dev-search")
    dev.add_argument("--cache-dir", type=Path, default=Path(".alpha-cache-v4"))
    dev.add_argument("--candidate-out", type=Path, default=Path("alpha-v4-candidate.json"))
    dev.add_argument("--metrics-out", type=Path, default=Path("alpha-v4-dev-metrics.json"))

    holdout_a = subparsers.add_parser("holdout-a")
    holdout_a.add_argument("--cache-dir", type=Path, default=Path(".alpha-cache-v4"))
    holdout_a.add_argument("--candidate", type=Path, required=True)
    holdout_a.add_argument("--result-out", type=Path, default=Path("alpha-v4-holdout-a.json"))

    holdout_b = subparsers.add_parser("holdout-b")
    holdout_b.add_argument("--cache-dir", type=Path, default=Path(".alpha-cache-v4"))
    holdout_b.add_argument("--candidate", type=Path, required=True)
    holdout_b.add_argument("--holdout-a-result", type=Path, required=True)
    holdout_b.add_argument("--result-out", type=Path, default=Path("alpha-v4-holdout-b.json"))

    args = parser.parse_args()
    if args.command == "dev-search":
        return _dev_search(args.cache_dir, args.candidate_out, args.metrics_out)
    if args.command == "holdout-a":
        return _holdout_a(args.cache_dir, args.candidate, args.result_out)
    if args.command == "holdout-b":
        return _holdout_b(
            args.cache_dir,
            args.candidate,
            args.holdout_a_result,
            args.result_out,
        )
    _die("unsupported command")


if __name__ == "__main__":
    raise SystemExit(main())
