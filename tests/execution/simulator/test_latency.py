"""
Phase 60.3, TASK 5 -- execution_layer/execution_engine/simulator/latency.py tests.
"""

from datetime import datetime, timezone

from execution_layer.execution_engine.simulator.latency import LatencyConfig, apply_latency, compute_latency


def test_compute_latency_returns_configured_value():
    assert compute_latency(LatencyConfig(execution_latency_ms=2000)) == 2000


def test_compute_latency_uses_default_when_no_config():
    assert compute_latency() == LatencyConfig().execution_latency_ms


def test_apply_latency_shifts_forward_by_milliseconds():
    """Director's own worked example: signal at 10:00:00, order at 10:00:02."""
    signal_time = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    result = apply_latency(signal_time, 2000)
    assert result == datetime(2026, 1, 1, 10, 0, 2, tzinfo=timezone.utc)


def test_apply_latency_zero_is_a_no_op():
    signal_time = datetime(2026, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    assert apply_latency(signal_time, 0) == signal_time
