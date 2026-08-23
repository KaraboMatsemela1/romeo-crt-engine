from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import NoReturn, cast

from romeo_crt_engine.alpha_lab.backtest import run_backtest
from romeo_crt_engine.alpha_lab.data import load_binance_h1
from romeo_crt_engine.alpha_lab.models import (
    CostModel,
    DirectionMode,
    Metrics,
    StrategyConfig,
)
from romeo_crt_engine.alpha_lab.optimize import oos_gate, search_dev

DEV_START = datetime(2019, 1, 1, tzinfo=UTC)
DEV_END = datetime(2023, 1, 1, tzinfo=UTC)
OOS_START = datetime(2023, 1, 1, tzinfo=UTC)
OOS_END = datetime(2025, 1, 1, tzinfo=UTC)
CONFIRM_START = datetime(2025, 1, 1, tzinfo=UTC)
SYMBOL = "BTCUSDT"
SCHEMA_VERSION = "ALPHA_LAB_CANDIDATE_V1"


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


def _as_object_mapping(value: object, *, field: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError(f"{field} must be an object")
    result: dict[str, object] = {}
    for key, item in value.items():
        if not isinstance(key, str):
            raise ValueError(f"{field} keys must be strings")
        result[key] = item
    return result


def _required(mapping: dict[str, object], key: str) -> object:
    if key not in mapping:
        raise ValueError(f"missing required field: {key}")
    return mapping[key]


def _read_config(candidate_path: Path) -> tuple[StrategyConfig, CostModel, str, bool]:
    raw: object = json.loads(candidate_path.read_text(encoding="utf-8"))
    payload = _as_object_mapping(raw, field="candidate")
    if _required(payload, "schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported candidate schema")
    config_map = _as_object_mapping(_required(payload, "config"), field="config")
    costs_map = _as_object_mapping(_required(payload, "costs"), field="costs")
    direction_raw = str(_required(config_map, "direction_mode"))
    if direction_raw not in {"both", "long_only", "short_only"}:
        raise ValueError("invalid direction_mode")

    config = StrategyConfig(
        lookback_hours=int(_required(config_map, "lookback_hours")),
        min_sweep_bps=float(_required(config_map, "min_sweep_bps")),
        reclaim_fraction=float(_required(config_map, "reclaim_fraction")),
        ema_fast=int(_required(config_map, "ema_fast")),
        ema_slow=int(_required(config_map, "ema_slow")),
        direction_mode=cast(DirectionMode, direction_raw),
        atr_period=int(_required(config_map, "atr_period")),
        stop_buffer_atr=float(_required(config_map, "stop_buffer_atr")),
        target_r=float(_required(config_map, "target_r")),
        max_hold_bars=int(_required(config_map, "max_hold_bars")),
        risk_fraction=float(_required(config_map, "risk_fraction")),
    )
    costs = CostModel(
        fee_bps_per_side=float(_required(costs_map, "fee_bps_per_side")),
        slippage_bps_per_side=float(_required(costs_map, "slippage_bps_per_side")),
        max_leverage=float(_required(costs_map, "max_leverage")),
    )
    candidate_id = str(_required(payload, "candidate_id"))
    if candidate_id != config.config_id:
        raise ValueError("candidate_id does not match frozen configuration")
    gate_raw = _required(payload, "dev_gate_pass")
    if not isinstance(gate_raw, bool):
        raise ValueError("dev_gate_pass must be boolean")
    return config, costs, candidate_id, gate_raw


def _dev_search(cache_dir: Path, candidate_out: Path, metrics_out: Path) -> int:
    dataset = load_binance_h1(
        symbol=SYMBOL,
        start=DEV_START,
        end=DEV_END,
        cache_dir=cache_dir / "dev",
    )
    costs = CostModel()
    search = search_dev(dataset.bars, costs=costs)
    metrics = search.result.metrics
    candidate: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "candidate_id": search.result.config.config_id,
        "symbol": SYMBOL,
        "dev_window": {"start": DEV_START.isoformat(), "end_exclusive": DEV_END.isoformat()},
        "oos_window": {"start": OOS_START.isoformat(), "end_exclusive": OOS_END.isoformat()},
        "confirm_boundary": CONFIRM_START.isoformat(),
        "dev_dataset_sha256": dataset.dataset_sha256,
        "config": asdict(search.result.config),
        "costs": asdict(costs),
        "dev_metrics": _metrics_dict(metrics),
        "search_score": search.score,
        "searched_configs": search.searched_configs,
        "dev_gate_pass": search.gate_pass,
        "oos_access_authorized": search.gate_pass,
        "confirm_access_authorized": False,
    }
    _write_json(candidate_out, candidate)
    _write_json(
        metrics_out,
        {
            "candidate_id": search.result.config.config_id,
            "dataset_sha256": dataset.dataset_sha256,
            "metrics": _metrics_dict(metrics),
            "searched_configs": search.searched_configs,
            "dev_gate_pass": search.gate_pass,
        },
    )
    print("ALPHA_LAB_DEV_RESULT=" + json.dumps(candidate, sort_keys=True))
    return 0


def _oos_eval(cache_dir: Path, candidate_path: Path, result_out: Path) -> int:
    config, costs, candidate_id, dev_gate_pass = _read_config(candidate_path)
    if not dev_gate_pass:
        raise ValueError("OOS access denied because the frozen DEV candidate did not pass")
    dataset = load_binance_h1(
        symbol=SYMBOL,
        start=OOS_START,
        end=OOS_END,
        cache_dir=cache_dir / "oos",
    )
    result = run_backtest(dataset.bars, config, costs=costs)
    passed = oos_gate(result)
    payload: dict[str, object] = {
        "schema_version": "ALPHA_LAB_OOS_RESULT_V1",
        "candidate_id": candidate_id,
        "symbol": SYMBOL,
        "oos_window": {"start": OOS_START.isoformat(), "end_exclusive": OOS_END.isoformat()},
        "oos_dataset_sha256": dataset.dataset_sha256,
        "metrics": _metrics_dict(result.metrics),
        "oos_gate_pass": passed,
        "confirm_access_authorized": passed,
        "confirm_data_accessed": False,
    }
    _write_json(result_out, payload)
    print("ALPHA_LAB_OOS_RESULT=" + json.dumps(payload, sort_keys=True))
    return 0


def _die(message: str) -> NoReturn:
    raise SystemExit(message)


def main() -> int:
    parser = argparse.ArgumentParser(description="Alpha Lab guarded DEV/OOS research cycle")
    subparsers = parser.add_subparsers(dest="command", required=True)

    dev = subparsers.add_parser("dev-search")
    dev.add_argument("--cache-dir", type=Path, default=Path(".alpha-cache"))
    dev.add_argument("--candidate-out", type=Path, default=Path("alpha-dev-candidate.json"))
    dev.add_argument("--metrics-out", type=Path, default=Path("alpha-dev-metrics.json"))

    oos = subparsers.add_parser("oos-eval")
    oos.add_argument("--cache-dir", type=Path, default=Path(".alpha-cache"))
    oos.add_argument("--candidate", type=Path, required=True)
    oos.add_argument("--result-out", type=Path, default=Path("alpha-oos-result.json"))

    args = parser.parse_args()
    if args.command == "dev-search":
        return _dev_search(args.cache_dir, args.candidate_out, args.metrics_out)
    if args.command == "oos-eval":
        return _oos_eval(args.cache_dir, args.candidate, args.result_out)
    _die("unsupported command")


if __name__ == "__main__":
    raise SystemExit(main())
