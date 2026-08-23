from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from romeo_crt_engine.alpha_lab import confirm_v3
from romeo_crt_engine.alpha_lab.models import Dataset, Metrics
from romeo_crt_engine.alpha_lab.models_v3 import V3BacktestResult


def test_confirm_protocol_is_frozen_before_data_access() -> None:
    config, costs = confirm_v3._verify_frozen_lineage()
    assert config == confirm_v3.EXPECTED_CONFIG
    assert config.config_id == "v3-47f727727bbd433e5b22"
    assert costs == confirm_v3.EXPECTED_COSTS
    assert confirm_v3.CONFIRM_START == datetime(2025, 1, 1, tzinfo=UTC)
    assert confirm_v3.CONFIRM_END == datetime(2026, 8, 1, tzinfo=UTC)


def test_confirm_run_uses_exact_window_and_no_search(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    observed: dict[str, object] = {}

    def fake_loader(**kwargs: object) -> Dataset:
        observed.update(kwargs)
        return Dataset(
            symbol="BTCUSDT",
            start=confirm_v3.CONFIRM_START,
            end=confirm_v3.CONFIRM_END,
            bars=(),
            dataset_sha256="f" * 64,
            source_hashes=(),
        )

    metrics = Metrics(
        closed_trades=120,
        wins=55,
        losses=65,
        win_rate=55 / 120,
        expectancy_r=0.10,
        profit_factor=1.20,
        net_pnl=1000.0,
        return_pct=1.0,
        max_drawdown_pct=9.0,
        final_equity=101_000.0,
    )

    def fake_backtest(*args: object, **kwargs: object) -> V3BacktestResult:
        return V3BacktestResult(
            config=confirm_v3.EXPECTED_CONFIG,
            costs=confirm_v3.EXPECTED_COSTS,
            metrics=metrics,
            trades=(),
        )

    monkeypatch.setattr(confirm_v3, "load_binance_h1", fake_loader)
    monkeypatch.setattr(confirm_v3, "run_v3_backtest", fake_backtest)
    output = tmp_path / "confirm.json"
    assert confirm_v3.run_confirm(cache_dir=tmp_path, result_out=output) == 0
    assert observed["start"] == confirm_v3.CONFIRM_START
    assert observed["end"] == confirm_v3.CONFIRM_END
    assert observed["symbol"] == "BTCUSDT"
    assert output.exists()


def test_confirm_gate_rejects_insufficient_activity() -> None:
    metrics = Metrics(
        closed_trades=99,
        wins=50,
        losses=49,
        win_rate=50 / 99,
        expectancy_r=0.20,
        profit_factor=1.50,
        net_pnl=1000.0,
        return_pct=1.0,
        max_drawdown_pct=5.0,
        final_equity=101_000.0,
    )
    assert confirm_v3._confirm_gate(metrics) is False
