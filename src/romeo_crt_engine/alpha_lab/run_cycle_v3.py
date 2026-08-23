from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import NoReturn

from romeo_crt_engine.alpha_lab.backtest_v3 import run_v3_backtest
from romeo_crt_engine.alpha_lab.data import load_binance_h1
from romeo_crt_engine.alpha_lab.models import CostModel, Metrics
from romeo_crt_engine.alpha_lab.models_v3 import V3Config
from romeo_crt_engine.alpha_lab.optimize_v3 import search_v3_dev, v3_oos_gate
from romeo_crt_engine.alpha_lab.run_cycle import (
    CONFIRM_START,
    DEV_END,
    DEV_START,
    OOS_END,
    OOS_START,
    SYMBOL,
)

SCHEMA_VERSION = "ALPHA_LAB_CANDIDATE_V3"


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


def _as_str(value: object, *, field: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{field} must be string")
    return value


def _as_bool(value: object, *, field: str) -> bool:
    if not isinstance(value, bool):
        raise TypeError(f"{field} must be boolean")
    return value


def _read_candidate(path: Path) -> tuple[V3Config, CostModel, str, bool]:
    raw: object = json.loads(path.read_text(encoding="utf-8"))
    payload = _as_mapping(raw, field="candidate")
    if _as_str(_required(payload, "schema_version"), field="schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported candidate schema")
    config_map = _as_mapping(_required(payload, "config"), field="config")
    costs_map = _as_mapping(_required(payload, "costs"), field="costs")
    config = V3Config(
        lookback_hours=_as_int(_required(config_map, "lookback_hours"), field="lookback_hours"),
        breakout_buffer_bps=_as_float(
            _required(config_map, "breakout_buffer_bps"), field="breakout_buffer_bps"
        ),
        use_ema200_regime=_as_bool(
            _required(config_map, "use_ema200_regime"), field="use_ema200_regime"
        ),
        volatility_ratio_min=_as_float(
            _required(config_map, "volatility_ratio_min"), field="volatility_ratio_min"
        ),
        close_location_min=_as_float(
            _required(config_map, "close_location_min"), field="close_location_min"
        ),
        atr_period=_as_int(_required(config_map, "atr_period"), field="atr_period"),
        volatility_lookback=_as_int(
            _required(config_map, "volatility_lookback"), field="volatility_lookback"
        ),
        stop_atr=_as_float(_required(config_map, "stop_atr"), field="stop_atr"),
        target_r=_as_float(_required(config_map, "target_r"), field="target_r"),
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
        raise ValueError("candidate_id does not match frozen V3 configuration")
    return config, costs, candidate_id, _as_bool(
        _required(payload, "dev_gate_pass"), field="dev_gate_pass"
    )


def _dev_search(cache_dir: Path, candidate_out: Path, metrics_out: Path) -> int:
    dataset = load_binance_h1(
        symbol=SYMBOL,
        start=DEV_START,
        end=DEV_END,
        cache_dir=cache_dir / "dev",
    )
    costs = CostModel()
    search = search_v3_dev(dataset.bars, costs=costs)
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
        "dev_metrics": _metrics_dict(search.result.metrics),
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
            "metrics": _metrics_dict(search.result.metrics),
            "searched_configs": search.searched_configs,
            "dev_gate_pass": search.gate_pass,
        },
    )
    print("ALPHA_LAB_V3_DEV_RESULT=" + json.dumps(candidate, sort_keys=True))
    return 0


def _oos_eval(cache_dir: Path, candidate_path: Path, result_out: Path) -> int:
    config, costs, candidate_id, dev_gate_pass = _read_candidate(candidate_path)
    if not dev_gate_pass:
        raise ValueError("V3 OOS access denied because DEV did not pass")
    dataset = load_binance_h1(
        symbol=SYMBOL,
        start=OOS_START,
        end=OOS_END,
        cache_dir=cache_dir / "oos",
    )
    result = run_v3_backtest(dataset.bars, config, costs=costs)
    passed = v3_oos_gate(result)
    payload: dict[str, object] = {
        "schema_version": "ALPHA_LAB_OOS_RESULT_V3",
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
    print("ALPHA_LAB_V3_OOS_RESULT=" + json.dumps(payload, sort_keys=True))
    return 0


def _die(message: str) -> NoReturn:
    raise SystemExit(message)


def main() -> int:
    parser = argparse.ArgumentParser(description="Alpha Lab V3 guarded DEV/OOS research cycle")
    subparsers = parser.add_subparsers(dest="command", required=True)
    dev = subparsers.add_parser("dev-search")
    dev.add_argument("--cache-dir", type=Path, default=Path(".alpha-cache-v3"))
    dev.add_argument("--candidate-out", type=Path, default=Path("alpha-v3-dev-candidate.json"))
    dev.add_argument("--metrics-out", type=Path, default=Path("alpha-v3-dev-metrics.json"))
    oos = subparsers.add_parser("oos-eval")
    oos.add_argument("--cache-dir", type=Path, default=Path(".alpha-cache-v3"))
    oos.add_argument("--candidate", type=Path, required=True)
    oos.add_argument("--result-out", type=Path, default=Path("alpha-v3-oos-result.json"))
    args = parser.parse_args()
    if args.command == "dev-search":
        return _dev_search(args.cache_dir, args.candidate_out, args.metrics_out)
    if args.command == "oos-eval":
        return _oos_eval(args.cache_dir, args.candidate, args.result_out)
    _die("unsupported command")


if __name__ == "__main__":
    raise SystemExit(main())
