"""Phase B.0 -- core_layer/health_monitor/models.py additions (HealthStatus, ResourceSnapshot, PerformanceCounters, DecisionPipelineEntry.stage_durations_ms) tests."""

import dataclasses

from core_layer.health_monitor.models import (
    DecisionPipelineEntry,
    HealthStatus,
    PerformanceCounters,
    ResourceSnapshot,
)


def test_health_status_has_exactly_three_members():
    assert {member.value for member in HealthStatus} == {"OK", "WARNING", "CRITICAL"}


def test_decision_pipeline_entry_stage_durations_ms_defaults_to_empty_tuple():
    entry = DecisionPipelineEntry(
        timestamp="2026-01-01T00:00:00Z", symbol="XAUUSD", timeframe="M15",
        criteria_met=(), criteria_total=5, decision="NO TRADE",
    )
    assert entry.stage_durations_ms == ()


def test_decision_pipeline_entry_accepts_stage_durations_ms():
    entry = DecisionPipelineEntry(
        timestamp="2026-01-01T00:00:00Z", symbol="XAUUSD", timeframe="M15",
        criteria_met=(), criteria_total=5, decision="NO TRADE",
        stage_durations_ms=(("context", 4.2), ("signal", 1.1)),
    )
    assert entry.stage_durations_ms == (("context", 4.2), ("signal", 1.1))


def test_decision_pipeline_entry_is_frozen():
    entry = DecisionPipelineEntry(
        timestamp="t", symbol="XAUUSD", timeframe="M15", criteria_met=(), criteria_total=5, decision="NO TRADE",
    )
    try:
        entry.decision = "BUY"
        assert False, "should have raised"
    except dataclasses.FrozenInstanceError:
        pass


def test_resource_snapshot_accepts_all_fields():
    snapshot = ResourceSnapshot(
        cpu_time_seconds=1.5, max_rss_kb=2048, thread_count=4,
        restart_count=2, uptime_seconds=90.0, heartbeat_at="2026-01-01T00:00:00Z",
    )
    assert snapshot.cpu_time_seconds == 1.5
    assert snapshot.max_rss_kb == 2048
    assert snapshot.thread_count == 4
    assert snapshot.restart_count == 2


def test_resource_snapshot_allows_none_cpu_and_memory():
    snapshot = ResourceSnapshot(
        cpu_time_seconds=None, max_rss_kb=None, thread_count=1,
        restart_count=0, uptime_seconds=0.0, heartbeat_at="t",
    )
    assert snapshot.cpu_time_seconds is None
    assert snapshot.max_rss_kb is None


def test_resource_snapshot_is_frozen():
    snapshot = ResourceSnapshot(
        cpu_time_seconds=None, max_rss_kb=None, thread_count=1,
        restart_count=0, uptime_seconds=0.0, heartbeat_at="t",
    )
    try:
        snapshot.thread_count = 99
        assert False, "should have raised"
    except dataclasses.FrozenInstanceError:
        pass


def test_performance_counters_defaults_all_zero():
    counters = PerformanceCounters()
    assert counters.signal_count == 0
    assert counters.decision_count == 0
    assert counters.trade_count == 0
    assert counters.reject_count == 0
    assert counters.error_count == 0
    assert counters.reconnect_count == 0
    assert counters.runtime_seconds == 0.0


def test_performance_counters_accepts_explicit_values():
    counters = PerformanceCounters(signal_count=3, decision_count=2, trade_count=1, reject_count=1, error_count=0, reconnect_count=0, runtime_seconds=10.0)
    assert counters.signal_count == 3


def test_performance_counters_is_frozen():
    counters = PerformanceCounters()
    try:
        counters.signal_count = 99
        assert False, "should have raised"
    except dataclasses.FrozenInstanceError:
        pass


def test_no_field_on_new_models_is_a_trading_core_object_type():
    """Belt-and-suspenders: every field on HealthStatus/ResourceSnapshot/PerformanceCounters is a primitive, str, int, float, or Optional."""
    allowed_fragments = ("str", "int", "float", "Optional", "Tuple", "Sequence")
    for f in dataclasses.fields(ResourceSnapshot):
        assert any(fragment in str(f.type) for fragment in allowed_fragments), f"ResourceSnapshot.{f.name}: {f.type}"
    for f in dataclasses.fields(PerformanceCounters):
        assert any(fragment in str(f.type) for fragment in allowed_fragments), f"PerformanceCounters.{f.name}: {f.type}"
