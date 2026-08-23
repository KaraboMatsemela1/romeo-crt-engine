from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

from romeo_crt_engine.alpha_lab.backtest_v3 import run_v3_backtest
from romeo_crt_engine.alpha_lab.data import load_binance_h1
from romeo_crt_engine.alpha_lab.models import CostModel, Metrics
from romeo_crt_engine.alpha_lab.models_v3 import V3Config

SYMBOL = "BTCUSDT"
EXPECTED_CANDIDATE_ID = "v3-47f727727bbd433e5b22"
CONFIRM_START = datetime(2025, 1, 1, tzinfo=UTC)
CONFIRM_END = datetime(2026, 8, 1, tzinfo=UTC)
DEV_RESULT_PATH = Path("experiments/alpha_lab/ALPHA_LAB_DEV_RESULT_V3.json")
OOS_RESULT_PATH = Path("experiments/alpha_lab/ALPHA_LAB_OOS_RESULT_V3.json")
CONFIRM_MIN_TRADES = 100
CONFIRM_MIN_PROFIT_FACTOR = 1.15
CONFIRM_MAX_DRAWDOWN_PCT = 20.0

EXPECTED_CONFIG = V3Config(
    lookback_hours=24,
    breakout_buffer_bps=10.0,
    use_ema200_regime=True,
    volatility_ratio_min=1.0,
    close_location_min=0.5,
    atr_period=14,
    volatility_lookback=48,
    stop_atr=1.5,
    target_r=3.0,
    max_hold_bars=24,
    risk_fraction=0.01,
)
EXPECTED_COSTS = CostModel(
    fee_bps_per_side=4.0,
    slippage_bps_per_side=2.0,
    max_leverage=3.0,
)


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


def _verify_frozen_lineage() -> tuple[V3Config, CostModel]:
    dev = _load_json(DEV_RESULT_PATH)
    oos = _load_json(OOS_RESULT_PATH)

    dev_candidate = _as_str(_required(dev, "candidate_id"), field="DEV candidate_id")
    oos_candidate = _as_str(_required(oos, "candidate_id"), field="OOS candidate_id")
    if dev_candidate != EXPECTED_CANDIDATE_ID or oos_candidate != EXPECTED_CANDIDATE_ID:
        raise ValueError("sealed candidate identity does not match the preregistered V3 candidate")
    if EXPECTED_CONFIG.config_id != EXPECTED_CANDIDATE_ID:
        raise ValueError("hard-coded V3 configuration does not match expected candidate identity")

    if not _as_bool(_required(dev, "dev_gate_pass"), field="dev_gate_pass"):
        raise ValueError("CONFIRM denied because sealed DEV did not pass")
    if not _as_bool(_required(oos, "oos_gate_pass"), field="oos_gate_pass"):
        raise ValueError("CONFIRM denied because sealed OOS did not pass")
    if not _as_bool(
        _required(oos, "confirm_access_authorized"), field="confirm_access_authorized"
    ):
        raise ValueError("CONFIRM denied by sealed OOS authorization state")

    dev_config = _as_mapping(_required(dev, "config"), field="DEV config")
    dev_costs = _as_mapping(_required(dev, "costs"), field="DEV costs")
    if dev_config != asdict(EXPECTED_CONFIG):
        raise ValueError("sealed DEV configuration differs from preregistered V3 configuration")
    if dev_costs != asdict(EXPECTED_COSTS):
        raise ValueError("sealed DEV costs differ from preregistered V3 costs")

    return EXPECTED_CONFIG, EXPECTED_COSTS


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


def _confirm_gate(metrics: Metrics) -> bool:
    return (
        metrics.closed_trades >= CONFIRM_MIN_TRADES
        and metrics.profit_factor is not None
        and metrics.profit_factor >= CONFIRM_MIN_PROFIT_FACTOR
        and metrics.expectancy_r > 0
        and metrics.max_drawdown_pct <= CONFIRM_MAX_DRAWDOWN_PCT
    )


def run_confirm(*, cache_dir: Path, result_out: Path) -> int:
    config, costs = _verify_frozen_lineage()
    dataset = load_binance_h1(
        symbol=SYMBOL,
        start=CONFIRM_START,
        end=CONFIRM_END,
        cache_dir=cache_dir / "confirm",
    )
    result = run_v3_backtest(dataset.bars, config, costs=costs)
    passed = _confirm_gate(result.metrics)
    payload: dict[str, object] = {
        "schema_version": "ALPHA_LAB_CONFIRM_RESULT_V3",
        "candidate_id": EXPECTED_CANDIDATE_ID,
        "symbol": SYMBOL,
        "confirm_window": {
            "start": CONFIRM_START.isoformat(),
            "end_exclusive": CONFIRM_END.isoformat(),
        },
        "confirm_dataset_sha256": dataset.dataset_sha256,
        "config": asdict(config),
        "costs": asdict(costs),
        "metrics": _metrics_dict(result.metrics),
        "confirm_gate": {
            "minimum_closed_trades": CONFIRM_MIN_TRADES,
            "minimum_profit_factor": CONFIRM_MIN_PROFIT_FACTOR,
            "positive_expectancy_required": True,
            "maximum_drawdown_pct": CONFIRM_MAX_DRAWDOWN_PCT,
        },
        "confirm_gate_pass": passed,
        "disposition": "CONFIRM_PASS" if passed else "CONFIRM_FAIL_REJECT_V3",
        "paper_trading_authorized": False,
        "live_trading_authorized": False,
    }
    result_out.parent.mkdir(parents=True, exist_ok=True)
    result_out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("ALPHA_LAB_V3_CONFIRM_RESULT=" + json.dumps(payload, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Frozen Alpha Lab V3 CONFIRM evaluator")
    parser.add_argument("--cache-dir", type=Path, default=Path(".alpha-cache-v3-confirm"))
    parser.add_argument(
        "--result-out", type=Path, default=Path("alpha-v3-confirm-result.json")
    )
    args = parser.parse_args()
    return run_confirm(cache_dir=args.cache_dir, result_out=args.result_out)


if __name__ == "__main__":
    raise SystemExit(main())
