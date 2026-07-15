"""
Phase 60.3, TASK 6 -- execution/simulator/simulator_engine.py tests.
Real lifecycle.paper_trade/risk.risk_manager objects -- no mocks.
"""

from datetime import datetime, timedelta, timezone

import pytest

from execution.simulator.simulator_engine import ExecutionSimulator
from execution.simulator.slippage import SlippageConfig
from execution.simulator.spread import SpreadConfig
from lifecycle.paper_trade import create_paper_trade, open_paper_trade
from risk.risk_manager import RiskResult
from signals.schema import SignalSchema


def _approved_signal(**overrides) -> SignalSchema:
    base = dict(
        signal_id="sig-1",
        created_at=datetime.now(timezone.utc),
        symbol="XAUUSD",
        timeframe="M15",
        direction="BUY",
        entry_price=2350.0,
        stop_loss=2340.0,
        take_profit=2370.0,
        decision="APPROVED",
    )
    base.update(overrides)
    return SignalSchema(**base)


def _open_trade(**overrides):
    signal = _approved_signal(**overrides)
    trade = create_paper_trade(signal)
    return open_paper_trade(trade).trade


def _risk_result(lot_size=0.1):
    return RiskResult(approved=True, lot_size=lot_size, risk_amount=100.0, risk_reward=2.0, reason="ok")


def test_simulate_fills_a_buy_order_with_slippage():
    trade = _open_trade()
    simulator = ExecutionSimulator(slippage_config=SlippageConfig(points=0.15), spread_config=SpreadConfig(default_points=0.0))

    result = simulator.simulate(trade, _risk_result())

    assert result.filled is True
    assert result.fill.fill_price == pytest.approx(2350.15)


def test_simulate_fills_a_sell_order_with_slippage():
    trade = _open_trade(direction="SELL", entry_price=2350.0, stop_loss=2360.0, take_profit=2330.0)
    simulator = ExecutionSimulator(slippage_config=SlippageConfig(points=0.15), spread_config=SpreadConfig(default_points=0.0))

    result = simulator.simulate(trade, _risk_result())

    assert result.fill.fill_price == pytest.approx(2349.85)


def test_simulate_rejects_when_spread_too_wide():
    trade = _open_trade()
    simulator = ExecutionSimulator(spread_config=SpreadConfig(max_points=0.5, session_spreads={"NY_NEWS": 0.80}))

    result = simulator.simulate(trade, _risk_result(), session="NY_NEWS")

    assert result.filled is False
    assert result.fill is None
    assert "too wide" in result.rejection_reason


def test_simulate_never_mutates_the_paper_trade():
    trade = _open_trade()
    original_entry = trade.entry
    simulator = ExecutionSimulator()

    simulator.simulate(trade, _risk_result())

    assert trade.entry == original_entry


def test_simulate_uses_session_spread_in_fill_price():
    trade = _open_trade()
    simulator = ExecutionSimulator(
        slippage_config=SlippageConfig(points=0.0),
        spread_config=SpreadConfig(session_spreads={"LONDON": 0.15}, max_points=1.0),
    )

    result = simulator.simulate(trade, _risk_result(), session="LONDON")

    assert result.fill.spread_points == 0.15
    assert result.fill.fill_price == pytest.approx(2350.15)


def test_simulate_order_carries_lot_size_from_risk_result():
    trade = _open_trade()
    simulator = ExecutionSimulator()

    result = simulator.simulate(trade, _risk_result(lot_size=0.25))

    assert result.order.lot_size == 0.25


def test_simulate_respects_signal_time_for_latency():
    trade = _open_trade()
    simulator = ExecutionSimulator()
    signal_time = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)

    result = simulator.simulate(trade, _risk_result(), signal_time=signal_time)

    assert result.order.requested_at == signal_time
    assert result.fill.filled_at == signal_time + timedelta(milliseconds=result.fill.latency_ms)
