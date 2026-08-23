from __future__ import annotations

from collections.abc import Sequence

from romeo_crt_engine.alpha_lab.models import (
    BacktestResult,
    Bar,
    CostModel,
    Direction,
    ExitReason,
    Metrics,
    Signal,
    StrategyConfig,
    Trade,
)
from romeo_crt_engine.alpha_lab.strategy import generate_signals


def _adverse_entry(price: float, direction: Direction, costs: CostModel) -> float:
    rate = costs.slippage_bps_per_side / 10_000.0
    return price * (1.0 + rate) if direction == "long" else price * (1.0 - rate)


def _adverse_exit(price: float, direction: Direction, costs: CostModel) -> float:
    rate = costs.slippage_bps_per_side / 10_000.0
    return price * (1.0 - rate) if direction == "long" else price * (1.0 + rate)


def _gross_pnl(direction: Direction, entry: float, exit_price: float, quantity: float) -> float:
    if direction == "long":
        return (exit_price - entry) * quantity
    return (entry - exit_price) * quantity


def _exit_for_bar(
    bar: Bar,
    *,
    direction: Direction,
    stop: float,
    target: float,
) -> tuple[ExitReason, float] | None:
    if direction == "long":
        if bar.open <= stop:
            return "stop", bar.open
        if bar.open >= target:
            return "target", target
        stop_hit = bar.low <= stop
        target_hit = bar.high >= target
    else:
        if bar.open >= stop:
            return "stop", bar.open
        if bar.open <= target:
            return "target", target
        stop_hit = bar.high >= stop
        target_hit = bar.low <= target

    if stop_hit and target_hit:
        return "stop_same_bar", stop
    if stop_hit:
        return "stop", stop
    if target_hit:
        return "target", target
    return None


def _validate_bars(bars: Sequence[Bar]) -> None:
    previous = None
    for bar in bars:
        if previous is not None and bar.open_time <= previous:
            raise ValueError("bars must be strictly ordered and unique")
        previous = bar.open_time


def _trade_from_signal(
    bars: Sequence[Bar],
    signal: Signal,
    *,
    config: StrategyConfig,
    costs: CostModel,
    equity: float,
) -> tuple[Trade, int] | None:
    entry_index = signal.signal_index + 1
    final_index = entry_index + config.max_hold_bars - 1
    if final_index >= len(bars):
        return None

    entry_bar = bars[entry_index]
    entry_reference = entry_bar.open
    if signal.direction == "long":
        stop = signal.signal_low - (config.stop_buffer_atr * signal.atr)
        if stop <= 0 or stop >= entry_reference:
            return None
        target = entry_reference + ((entry_reference - stop) * config.target_r)
    else:
        stop = signal.signal_high + (config.stop_buffer_atr * signal.atr)
        if stop <= entry_reference:
            return None
        target = entry_reference - ((stop - entry_reference) * config.target_r)
        if target <= 0:
            return None

    entry_fill = _adverse_entry(entry_reference, signal.direction, costs)
    stop_fill = _adverse_exit(stop, signal.direction, costs)
    fee_rate = costs.fee_bps_per_side / 10_000.0
    stop_loss_per_unit = abs(entry_fill - stop_fill) + fee_rate * (entry_fill + stop_fill)
    if stop_loss_per_unit <= 0:
        return None

    risk_budget = equity * config.risk_fraction
    risk_quantity = risk_budget / stop_loss_per_unit
    leverage_quantity = (equity * costs.max_leverage) / entry_fill
    quantity = min(risk_quantity, leverage_quantity)
    if quantity <= 0:
        return None

    exit_reason: ExitReason = "max_hold"
    exit_reference = bars[final_index].close
    exit_index = final_index
    for index in range(entry_index, final_index + 1):
        decision = _exit_for_bar(
            bars[index],
            direction=signal.direction,
            stop=stop,
            target=target,
        )
        if decision is None:
            continue
        exit_reason, exit_reference = decision
        exit_index = index
        break

    exit_fill = _adverse_exit(exit_reference, signal.direction, costs)
    gross = _gross_pnl(signal.direction, entry_fill, exit_fill, quantity)
    fees = fee_rate * quantity * (entry_fill + exit_fill)
    net = gross - fees
    r_multiple = net / risk_budget if risk_budget > 0 else 0.0

    trade = Trade(
        direction=signal.direction,
        signal_time=bars[signal.signal_index].open_time,
        entry_time=entry_bar.open_time,
        exit_time=bars[exit_index].open_time,
        entry_price=entry_fill,
        exit_price=exit_fill,
        stop_price=stop,
        target_price=target,
        quantity=quantity,
        risk_budget=risk_budget,
        gross_pnl=gross,
        fees=fees,
        net_pnl=net,
        r_multiple=r_multiple,
        exit_reason=exit_reason,
    )
    return trade, exit_index


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
            drawdown_pct = ((peak - equity) / peak) * 100.0
            max_drawdown_pct = max(max_drawdown_pct, drawdown_pct)

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


def run_backtest(
    bars: Sequence[Bar],
    config: StrategyConfig,
    *,
    costs: CostModel | None = None,
    initial_equity: float = 100_000.0,
) -> BacktestResult:
    if initial_equity <= 0:
        raise ValueError("initial_equity must be positive")
    _validate_bars(bars)
    if costs is None:
        costs = CostModel()

    signals = generate_signals(bars, config)
    trades: list[Trade] = []
    equity = initial_equity
    next_signal_index = 0

    for signal in signals:
        if signal.signal_index < next_signal_index:
            continue
        outcome = _trade_from_signal(
            bars,
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

    return BacktestResult(
        config=config,
        costs=costs,
        metrics=_metrics(initial_equity, trades),
        trades=tuple(trades),
    )
