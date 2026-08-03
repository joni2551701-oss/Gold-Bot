"""
Phase 60.3, TASK 2 -- execution_layer/execution_engine/simulator/models.py tests.
"""

from datetime import datetime, timezone

import pytest

from execution_layer.execution_engine.simulator.models import ExecutionSimulationResult, SimulatedFill, SimulatedOrder


def test_simulated_order_is_frozen():
    order = SimulatedOrder(
        order_id="o1", trade_id="t1", symbol="XAUUSD", direction="BUY",
        requested_price=2350.0, lot_size=0.1, requested_at=datetime.now(timezone.utc),
    )
    with pytest.raises(AttributeError):
        order.requested_price = 9999.0


def test_simulated_fill_is_frozen():
    fill = SimulatedFill(
        fill_price=2350.15, spread_points=0.15, slippage_points=0.10,
        latency_ms=2000, filled_at=datetime.now(timezone.utc),
    )
    with pytest.raises(AttributeError):
        fill.fill_price = 9999.0


def test_execution_simulation_result_rejected_has_no_fill():
    order = SimulatedOrder(
        order_id="o1", trade_id="t1", symbol="XAUUSD", direction="BUY",
        requested_price=2350.0, lot_size=0.1, requested_at=datetime.now(timezone.utc),
    )
    result = ExecutionSimulationResult(filled=False, order=order, rejection_reason="spread too wide")
    assert result.fill is None
    assert result.rejection_reason == "spread too wide"


def test_execution_simulation_result_filled_has_fill():
    order = SimulatedOrder(
        order_id="o1", trade_id="t1", symbol="XAUUSD", direction="BUY",
        requested_price=2350.0, lot_size=0.1, requested_at=datetime.now(timezone.utc),
    )
    fill = SimulatedFill(
        fill_price=2350.15, spread_points=0.15, slippage_points=0.10,
        latency_ms=2000, filled_at=datetime.now(timezone.utc),
    )
    result = ExecutionSimulationResult(filled=True, order=order, fill=fill)
    assert result.fill is fill
    assert result.rejection_reason is None
