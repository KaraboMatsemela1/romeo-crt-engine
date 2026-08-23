from __future__ import annotations

from collections.abc import Sequence

from romeo_crt_engine.alpha_lab.models import Bar, CostModel, Metrics, Trade
from romeo_crt_engine.alpha_lab.models_v4 import V4BacktestResult, V4Config, V4Signal
from romeo_crt_engine.alpha_lab.strategy_v4 import atr_series, generate_v4_signals


def _adverse_entry(price: float, costs: CostModel) -> float:
    return price * (1.0 + (costs.slippage_bps_per_side / 10_000.0))


def _adverse_exit(price: float, costs: CostModel) -> float:
    return price * (1.0 - (costs.slippage_bps_per_side / 10_000.0))


def _validate_bars(bars: Sequence[Bar]) -> None:
    previous = None
    for bar in bars:
        if previous is not None and bar.open_time <= previous:
            raise ValueError("bars must be strictly ordered and unique")
        previous = bar.open_time


def _trade_from_signal(
    bars: Sequence[Bar],
    atr_values: Sequence[float | None],
    signal: V4Signal,
    *,
    config: V4Config,
    costs: CostModel,
    equity: float,
) -> tuple[Trade, int] | None:
    entry_index = signal.signal_index + 1
    final_index = min(entry_index + config.max_hold_bars - 1, len(bars) - 1)
    if entry_index >= len(bars) or final_index <= entry_index:
        return None

    entry_bar = bars[entry_index]
    entry_reference = entry_bar.open
    initial_distance = signal.atr * config.initial_stop_atr
    if initial_distance <= 0 or initial_distance >= entry_reference:
        return None
    initial_stop = entry_reference - initial_distance

    entry_fill = _adverse_entry(entry_reference, costs)
    estimated_stop_fill = _adverse_exit(initial_stop, costs)
    fee_rate = costs.fee_bps_per_side / 10_000.0
    stop_loss_per_unit = (
        (entry_fill - estimated_stop_fill) + fee_rate * (entry_fill + estimated_stop_fill)
    )
    if stop_loss_per_unit <= 0:
        return None

    risk_budget = equity * config.risk_fraction
    risk_quantity = risk_budget / stop_loss_per_unit
    leverage_quantity = (equity * costs.max_leverage) / entry_fill
    quantity = min(risk_quantity, leverage_quantity)
    if quantity <= 0:
        return None

    active_stop = initial_stop
    highest_high = entry_bar.high
    exit_reference = bars[final_index].close
    exit_index = final_index
    exit_reason = "max_hold"
    stop_at_exit = active_stop

    for index in range(entry_index, final_index + 1):
        bar = bars[index]
        if bar.open <= active_stop:
            exit_reference = bar.open
            exit_index = index
            exit_reason = "stop"
            stop_at_exit = active_stop
            break
        if bar.low <= active_stop:
            exit_reference = active_stop
            exit_index = index
            exit_reason = "stop"
            stop_at_exit = active_stop
            break
        if index == final_index:
            stop_at_exit = active_stop
            break

        highest_high = max(highest_high, bar.high)
        atr_value = atr_values[index]
        if atr_value is None:
            continue
        candidate_stop = highest_high - (config.trail_atr * atr_value)
        active_stop = max(active_stop, candidate_stop)

    exit_fill = _adverse_exit(exit_reference, costs)
    gross = (exit_fill - entry_fill) * quantity
    fees = fee_rate * quantity * (entry_fill + exit_fill)
    net = gross - fees
    r_multiple = net / risk_budget if risk_budget > 0 else 0.0
    return (
        Trade(
            direction="long",
            signal_time=bars[signal.signal_index].open_time,
            entry_time=entry_bar.open_time,
            exit_time=bars[exit_index].open_time,
            entry_price=entry_fill,
            exit_price=exit_fill,
            stop_price=stop_at_exit,
            target_price=0.0,
            quantity=quantity,
            risk_budget=risk_budget,
            gross_pnl=gross,
            fees=fees,
            net_pnl=net,
            r_multiple=r_multiple,
            exit_reason=exit_reason,
        ),
        exit_index,
    )


def _metrics(initial_equity: float, trades: Sequence[Trade]) -> Metrics:
    wins = sum(trade.net_pnl > 0 for trade in trades)
    losses = sum(trade.net_pnl < 0 for trade in trades)
    closed = len(trades)
    win_rate = wins / closed if closed else 0.0
    expectancy = sum(trade.r_multiple for trade in trades) / closed if closed else 0.0
    gross_profit = sum(trade.net_pnl for trade in trades if trade.net_pnl > 0)
    gross_loss = -sum(trade.net_pnl for trade in trades if trade.net_pnl < 0)
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else None
    net_pnl = sum(trade.net_pnl for trade in trades)
    equity = initial_equity
    peak = initial_equity
    max_drawdown_pct = 0.0
    for trade in trades:
        equity += trade.net_pnl
        peak = max(peak, equity)
        if peak > 0:
            max_drawdown_pct = max(max_drawdown_pct, ((peak - equity) / peak) * 100.0)
    return Metrics(
        closed_trades=closed,
        wins=wins,
        losses=losses,
        win_rate=win_rate,
        expectancy_r=expectancy,
        profit_factor=profit_factor,
        net_pnl=net_pnl,
        return_pct=((equity - initial_equity) / initial_equity) * 100.0,
        max_drawdown_pct=max_drawdown_pct,
        final_equity=equity,
    )


def run_v4_backtest(
    bars: Sequence[Bar],
    config: V4Config,
    *,
    costs: CostModel | None = None,
    initial_equity: float = 100_000.0,
) -> V4BacktestResult:
    if initial_equity <= 0:
        raise ValueError("initial_equity must be positive")
    _validate_bars(bars)
    if costs is None:
        costs = CostModel()
    atr_values = atr_series(bars, config.atr_period)
    signals = generate_v4_signals(bars, config)
    trades: list[Trade] = []
    equity = initial_equity
    next_signal_index = 0
    for signal in signals:
        if signal.signal_index < next_signal_index:
            continue
        outcome = _trade_from_signal(
            bars,
            atr_values,
            signal,
            config=config,
            costs=costs,
            equity=equity,
        )
        if outcome is None:
            continue
        trade, exit_index = outcome
        trades.append(trade)
        equity += trade.net_pnl
        if equity <= 0:
            break
        next_signal_index = exit_index + 1
    return V4BacktestResult(
        config=config,
        costs=costs,
        metrics=_metrics(initial_equity, trades),
        trades=tuple(trades),
    )
