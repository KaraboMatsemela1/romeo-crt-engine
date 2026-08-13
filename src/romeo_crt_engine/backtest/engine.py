from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import Sequence
from datetime import datetime
from decimal import ROUND_FLOOR, Decimal
from hashlib import sha256

from romeo_crt_engine.backtest.models import (
    SIMULATOR_VERSION,
    BacktestConfig,
    BacktestMetrics,
    BacktestResult,
    CompletedTrade,
    ExitReason,
    JournalEvent,
    JournalEventType,
    OpenAtEnd,
    OpenPosition,
    PlanRejection,
    RejectionReason,
    SimulatedFill,
    trade_plan_decimal_prices,
)
from romeo_crt_engine.crt.detector import DetectorCandidate, DetectorDataset, DetectorRun
from romeo_crt_engine.crt.v0_1 import Direction
from romeo_crt_engine.market_data.models import BarTimeframe, CanonicalBar


def _require_quantity_step(quantity_step: Decimal) -> None:
    if not quantity_step.is_finite() or quantity_step <= 0:
        raise ValueError("quantity_step must be positive and finite")


def _floor_to_step(value: Decimal, step: Decimal) -> Decimal:
    if value <= 0:
        return Decimal(0)
    units = (value / step).to_integral_value(rounding=ROUND_FLOOR)
    return units * step


def _short_entry_fill_price(reference: Decimal, config: BacktestConfig) -> Decimal:
    return reference * (Decimal(1) - config.cost_model.adverse_price_rate)


def _short_exit_fill_price(reference: Decimal, config: BacktestConfig) -> Decimal:
    return reference * (Decimal(1) + config.cost_model.adverse_price_rate)


def _fee(fill_price: Decimal, quantity: Decimal, config: BacktestConfig) -> Decimal:
    return fill_price * quantity * config.cost_model.fee_rate


def _validate_binding(run: DetectorRun, dataset: DetectorDataset) -> None:
    if run.dataset.dataset_version != dataset.identity.dataset_version:
        raise ValueError("detector run and canonical dataset version do not match")
    if run.dataset.manifest_sha256 != dataset.identity.manifest_sha256:
        raise ValueError("detector run and canonical dataset manifest do not match")
    if run.dataset.normalized_sha256 != dataset.identity.normalized_sha256:
        raise ValueError("detector run and canonical dataset content digest do not match")
    if (run.dataset.provider, run.dataset.venue, run.dataset.symbol) != (
        dataset.identity.provider,
        dataset.identity.venue,
        dataset.identity.symbol,
    ):
        raise ValueError("detector run and canonical dataset instrument identity do not match")


def _validate_h1(bars: Sequence[CanonicalBar], run: DetectorRun) -> None:
    previous_close: float | None = None
    for bar in bars:
        if bar.timeframe is not BarTimeframe.H1:
            raise ValueError("backtester consumes canonical H1 bars only")
        if (bar.provider, bar.venue, bar.symbol) != (
            run.dataset.provider,
            run.dataset.venue,
            run.dataset.symbol,
        ):
            raise ValueError("H1 identity does not match detector run")
        open_timestamp = bar.open_time.timestamp()
        if previous_close is not None and open_timestamp != previous_close:
            raise ValueError("H1 event clock must be gapless and ordered")
        previous_close = bar.close_time.timestamp()


def _size_short(
    candidate: DetectorCandidate,
    *,
    equity: Decimal,
    quantity_step: Decimal,
    config: BacktestConfig,
) -> tuple[Decimal, Decimal, Decimal]:
    plan = candidate.trade_plan
    if plan is None:
        raise ValueError("cannot size candidate without TradePlan")
    if plan.direction is not Direction.BEARISH:
        return Decimal(0), Decimal(0), Decimal(0)

    entry_reference, stop_reference, _ = trade_plan_decimal_prices(plan)
    entry_fill = _short_entry_fill_price(entry_reference, config)
    estimated_stop_fill = _short_exit_fill_price(stop_reference, config)
    loss_per_unit = (
        (estimated_stop_fill - entry_fill)
        + (entry_fill * config.cost_model.fee_rate)
        + (estimated_stop_fill * config.cost_model.fee_rate)
    )
    if loss_per_unit <= 0:
        raise ValueError("estimated short stop loss per unit must be positive")

    risk_budget = equity * config.risk_fraction
    raw_quantity = risk_budget / loss_per_unit
    quantity = _floor_to_step(raw_quantity, quantity_step)
    estimated_loss = quantity * loss_per_unit
    return quantity, risk_budget, estimated_loss


def _entry_fill(candidate: DetectorCandidate, quantity: Decimal, config: BacktestConfig) -> SimulatedFill:
    plan = candidate.trade_plan
    if plan is None:
        raise ValueError("cannot fill candidate without TradePlan")
    reference, _, _ = trade_plan_decimal_prices(plan)
    price = _short_entry_fill_price(reference, config)
    return SimulatedFill(
        timestamp=plan.entry_time,
        reference_price=reference,
        fill_price=price,
        quantity=quantity,
        fee=_fee(price, quantity, config),
    )


def _exit_decision(
    position: OpenPosition,
    bar: CanonicalBar,
) -> tuple[ExitReason, Decimal, datetime] | None:
    _, stop, target = trade_plan_decimal_prices(position.plan)

    if bar.open >= stop:
        return ExitReason.STOP_GAP, bar.open, bar.open_time
    if bar.open <= target:
        return ExitReason.TARGET_GAP, target, bar.open_time

    stop_hit = bar.high >= stop
    target_hit = bar.low <= target
    if stop_hit and target_hit:
        return ExitReason.STOP_SAME_BAR_AMBIGUITY, stop, bar.close_time
    if stop_hit:
        return ExitReason.STOP, stop, bar.close_time
    if target_hit:
        return ExitReason.TARGET, target, bar.close_time
    return None


def _close_position(
    position: OpenPosition,
    *,
    exit_reason: ExitReason,
    exit_reference: Decimal,
    exit_time: datetime,
    equity_before: Decimal,
    config: BacktestConfig,
) -> CompletedTrade:
    exit_price = _short_exit_fill_price(exit_reference, config)
    exit_fill = SimulatedFill(
        timestamp=exit_time,
        reference_price=exit_reference,
        fill_price=exit_price,
        quantity=position.entry_fill.quantity,
        fee=_fee(exit_price, position.entry_fill.quantity, config),
    )
    gross = (position.entry_fill.fill_price - exit_fill.fill_price) * position.entry_fill.quantity
    total_fees = position.entry_fill.fee + exit_fill.fee
    net = gross - total_fees
    r_multiple = net / position.risk_budget
    return CompletedTrade(
        candidate_id=position.candidate_id,
        plan=position.plan,
        entry_fill=position.entry_fill,
        exit_fill=exit_fill,
        exit_reason=exit_reason,
        risk_budget=position.risk_budget,
        gross_pnl=gross,
        total_fees=total_fees,
        net_pnl=net,
        r_multiple=r_multiple,
        equity_after=equity_before + net,
    )


def _metrics(
    initial_equity: Decimal,
    trades: Sequence[CompletedTrade],
) -> BacktestMetrics:
    wins = sum(trade.net_pnl > 0 for trade in trades)
    losses = sum(trade.net_pnl < 0 for trade in trades)
    count = len(trades)
    win_rate = Decimal(wins) / Decimal(count) if count else None
    gross_pnl = sum((trade.gross_pnl for trade in trades), Decimal(0))
    net_pnl = sum((trade.net_pnl for trade in trades), Decimal(0))
    total_fees = sum((trade.total_fees for trade in trades), Decimal(0))
    average_r = (
        sum((trade.r_multiple for trade in trades), Decimal(0)) / Decimal(count)
        if count
        else None
    )
    gross_profit = sum((trade.net_pnl for trade in trades if trade.net_pnl > 0), Decimal(0))
    gross_loss = -sum((trade.net_pnl for trade in trades if trade.net_pnl < 0), Decimal(0))
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else None

    peak = initial_equity
    max_drawdown = Decimal(0)
    for trade in trades:
        peak = max(peak, trade.equity_after)
        drawdown = peak - trade.equity_after
        max_drawdown = max(max_drawdown, drawdown)

    return BacktestMetrics(
        closed_trades=count,
        wins=wins,
        losses=losses,
        win_rate=win_rate,
        gross_pnl=gross_pnl,
        net_pnl=net_pnl,
        total_fees=total_fees,
        average_r=average_r,
        expectancy_r=average_r,
        profit_factor=profit_factor,
        max_realized_drawdown=max_drawdown,
    )


def _run_hash(
    run: DetectorRun,
    config: BacktestConfig,
    trades: Sequence[CompletedTrade],
    rejections: Sequence[PlanRejection],
    open_at_end: Sequence[OpenAtEnd],
    final_equity: Decimal,
) -> str:
    payload = {
        "simulator_version": SIMULATOR_VERSION,
        "detector_run_sha256": run.run_sha256,
        "config_sha256": config.config_sha256,
        "trades": [
            {
                "candidate_id": trade.candidate_id,
                "entry_time": trade.entry_fill.timestamp.isoformat(),
                "entry_fill": str(trade.entry_fill.fill_price),
                "quantity": str(trade.entry_fill.quantity),
                "exit_time": trade.exit_fill.timestamp.isoformat(),
                "exit_fill": str(trade.exit_fill.fill_price),
                "exit_reason": trade.exit_reason.value,
                "net_pnl": str(trade.net_pnl),
                "r_multiple": str(trade.r_multiple),
            }
            for trade in trades
        ],
        "rejections": [
            {
                "candidate_id": rejection.candidate_id,
                "timestamp": rejection.timestamp.isoformat(),
                "reason": rejection.reason.value,
            }
            for rejection in rejections
        ],
        "open_at_end": [
            {
                "candidate_id": item.candidate_id,
                "entry_time": item.entry_fill.timestamp.isoformat(),
                "mark_time": item.final_mark_time.isoformat(),
                "mark_price": str(item.final_mark_price),
            }
            for item in open_at_end
        ],
        "final_equity": str(final_equity),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256(encoded).hexdigest()


def run_backtest(
    detector_run: DetectorRun,
    dataset: DetectorDataset,
    *,
    quantity_step: Decimal,
    config: BacktestConfig | None = None,
) -> BacktestResult:
    """Simulate frozen TradePlans on a causal H1 event clock.

    BTCUSDT Spot is the observation source in the first route. Short fills here are a synthetic
    linear research assumption, not a claim that Binance Spot itself executes naked shorts.
    """
    if config is None:
        config = BacktestConfig()

    _require_quantity_step(quantity_step)
    _validate_binding(detector_run, dataset)
    _validate_h1(dataset.h1, detector_run)

    plan_candidates = tuple(
        sorted(
            (candidate for candidate in detector_run.candidates if candidate.trade_plan is not None),
            key=lambda candidate: (
                candidate.trade_plan.entry_time.timestamp() if candidate.trade_plan else 0.0,
                candidate.candidate_id,
            ),
        )
    )
    plans_by_close: dict[float, list[DetectorCandidate]] = defaultdict(list)
    for candidate in plan_candidates:
        plan = candidate.trade_plan
        if plan is None:
            continue
        plans_by_close[plan.entry_time.timestamp()].append(candidate)

    available_closes = {bar.close_time.timestamp() for bar in dataset.h1}
    rejections: list[PlanRejection] = []
    journal: list[JournalEvent] = []
    for candidate in plan_candidates:
        plan = candidate.trade_plan
        if plan is None:
            continue
        if plan.direction is not Direction.BEARISH:
            rejection = PlanRejection(
                candidate_id=candidate.candidate_id,
                timestamp=plan.entry_time,
                reason=RejectionReason.UNSUPPORTED_DIRECTION,
            )
            rejections.append(rejection)
            journal.append(
                JournalEvent(
                    timestamp=plan.entry_time,
                    event_type=JournalEventType.PLAN_REJECTED,
                    candidate_id=candidate.candidate_id,
                    detail=rejection.reason.value,
                )
            )
        elif plan.entry_time.timestamp() not in available_closes:
            rejection = PlanRejection(
                candidate_id=candidate.candidate_id,
                timestamp=plan.entry_time,
                reason=RejectionReason.MISSING_ENTRY_CLOCK,
            )
            rejections.append(rejection)
            journal.append(
                JournalEvent(
                    timestamp=plan.entry_time,
                    event_type=JournalEventType.PLAN_REJECTED,
                    candidate_id=candidate.candidate_id,
                    detail=rejection.reason.value,
                )
            )

    rejected_ids = {rejection.candidate_id for rejection in rejections}
    equity = config.initial_equity
    open_positions: list[OpenPosition] = []
    completed: list[CompletedTrade] = []

    for bar in dataset.h1:
        survivors: list[OpenPosition] = []
        for position in open_positions:
            decision = _exit_decision(position, bar)
            if decision is None:
                survivors.append(position)
                continue
            exit_reason, exit_reference, exit_time = decision
            trade = _close_position(
                position,
                exit_reason=exit_reason,
                exit_reference=exit_reference,
                exit_time=exit_time,
                equity_before=equity,
                config=config,
            )
            equity = trade.equity_after
            completed.append(trade)
            journal.append(
                JournalEvent(
                    timestamp=trade.exit_fill.timestamp,
                    event_type=JournalEventType.EXIT_FILLED,
                    candidate_id=trade.candidate_id,
                    detail=f"{trade.exit_reason.value}|net={trade.net_pnl}|r={trade.r_multiple}",
                )
            )
        open_positions = survivors

        closing_candidates = sorted(
            plans_by_close.get(bar.close_time.timestamp(), ()),
            key=lambda candidate: candidate.candidate_id,
        )
        for candidate in closing_candidates:
            if candidate.candidate_id in rejected_ids:
                continue
            plan = candidate.trade_plan
            if plan is None:
                continue
            if len(open_positions) >= config.max_concurrent_positions:
                rejection = PlanRejection(
                    candidate_id=candidate.candidate_id,
                    timestamp=plan.entry_time,
                    reason=RejectionReason.POSITION_LIMIT,
                )
                rejections.append(rejection)
                journal.append(
                    JournalEvent(
                        timestamp=plan.entry_time,
                        event_type=JournalEventType.PLAN_REJECTED,
                        candidate_id=candidate.candidate_id,
                        detail=rejection.reason.value,
                    )
                )
                continue

            quantity, risk_budget, estimated_loss = _size_short(
                candidate,
                equity=equity,
                quantity_step=quantity_step,
                config=config,
            )
            if quantity <= 0:
                rejection = PlanRejection(
                    candidate_id=candidate.candidate_id,
                    timestamp=plan.entry_time,
                    reason=RejectionReason.SIZE_BELOW_MIN_STEP,
                )
                rejections.append(rejection)
                journal.append(
                    JournalEvent(
                        timestamp=plan.entry_time,
                        event_type=JournalEventType.PLAN_REJECTED,
                        candidate_id=candidate.candidate_id,
                        detail=rejection.reason.value,
                    )
                )
                continue

            fill = _entry_fill(candidate, quantity, config)
            position = OpenPosition(
                candidate_id=candidate.candidate_id,
                plan=plan,
                entry_fill=fill,
                risk_budget=risk_budget,
                estimated_stop_loss=estimated_loss,
            )
            open_positions.append(position)
            journal.append(
                JournalEvent(
                    timestamp=fill.timestamp,
                    event_type=JournalEventType.ENTRY_FILLED,
                    candidate_id=candidate.candidate_id,
                    detail=(
                        f"reference={fill.reference_price}|fill={fill.fill_price}|"
                        f"quantity={fill.quantity}|fee={fill.fee}|risk_budget={risk_budget}"
                    ),
                )
            )

    open_at_end: list[OpenAtEnd] = []
    if dataset.h1:
        final_bar = dataset.h1[-1]
        for position in open_positions:
            unrealized = (position.entry_fill.fill_price - final_bar.close) * position.entry_fill.quantity
            item = OpenAtEnd(
                candidate_id=position.candidate_id,
                plan=position.plan,
                entry_fill=position.entry_fill,
                final_mark_time=final_bar.close_time,
                final_mark_price=final_bar.close,
                unrealized_gross_pnl=unrealized,
            )
            open_at_end.append(item)
            journal.append(
                JournalEvent(
                    timestamp=final_bar.close_time,
                    event_type=JournalEventType.POSITION_OPEN_AT_END,
                    candidate_id=position.candidate_id,
                    detail=f"mark={final_bar.close}|unrealized_gross={unrealized}",
                )
            )

    metrics = _metrics(config.initial_equity, completed)
    run_sha = _run_hash(detector_run, config, completed, rejections, open_at_end, equity)
    return BacktestResult(
        simulator_version=SIMULATOR_VERSION,
        strategy_version=detector_run.strategy_version,
        detector_version=detector_run.detector_version,
        dataset_version=detector_run.dataset.dataset_version,
        dataset_manifest_sha256=detector_run.dataset.manifest_sha256,
        symbol=detector_run.dataset.symbol,
        config=config,
        completed_trades=tuple(completed),
        rejections=tuple(rejections),
        open_at_end=tuple(open_at_end),
        journal=tuple(journal),
        metrics=metrics,
        final_realized_equity=equity,
        run_sha256=run_sha,
    )
