"""
Phase 60.3, TASK 8 -- analytics/execution_report.py tests.
"""

from datetime import datetime, timezone

from analytics.execution_report import (
    build_execution_record,
    format_execution_record,
    summarize_execution_records,
)
from execution_layer.execution_engine.simulator.models import ExecutionSimulationResult, SimulatedFill, SimulatedOrder


def _order(order_id="o1"):
    return SimulatedOrder(
        order_id=order_id, trade_id="t1", symbol="XAUUSD", direction="BUY",
        requested_price=2350.0, lot_size=0.1, requested_at=datetime.now(timezone.utc),
    )


def _filled_result(order_id="o1"):
    fill = SimulatedFill(
        fill_price=2350.15, spread_points=0.15, slippage_points=0.10,
        latency_ms=2000, filled_at=datetime.now(timezone.utc),
    )
    return ExecutionSimulationResult(filled=True, order=_order(order_id), fill=fill)


def _rejected_result(order_id="o2"):
    return ExecutionSimulationResult(filled=False, order=_order(order_id), rejection_reason="spread too wide")


def test_build_execution_record_from_filled_result():
    record = build_execution_record(_filled_result())

    assert record.filled is True
    assert record.fill_price == 2350.15
    assert record.slippage_points == 0.10
    assert record.rejection_reason is None


def test_build_execution_record_from_rejected_result():
    record = build_execution_record(_rejected_result())

    assert record.filled is False
    assert record.fill_price is None
    assert record.rejection_reason == "spread too wide"


def test_summarize_execution_records_computes_fill_rate():
    records = [build_execution_record(_filled_result("o1")), build_execution_record(_rejected_result("o2"))]

    summary = summarize_execution_records(records)

    assert summary.total_orders == 2
    assert summary.filled_count == 1
    assert summary.rejected_count == 1
    assert summary.fill_rate == 0.5


def test_summarize_execution_records_averages_slippage_and_latency():
    records = [build_execution_record(_filled_result("o1")), build_execution_record(_filled_result("o2"))]

    summary = summarize_execution_records(records)

    assert summary.average_slippage_points == 0.10
    assert summary.average_latency_ms == 2000


def test_summarize_execution_records_empty_list_is_all_zero():
    summary = summarize_execution_records([])
    assert summary.total_orders == 0
    assert summary.fill_rate == 0.0
    assert summary.average_slippage_points is None


def test_format_execution_record_filled():
    text = format_execution_record(build_execution_record(_filled_result()))
    assert "fill=2350.15" in text
    assert "slippage=0.1" in text


def test_format_execution_record_rejected():
    text = format_execution_record(build_execution_record(_rejected_result()))
    assert "REJECTED" in text
    assert "spread too wide" in text
