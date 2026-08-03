"""Phase B.0 TASK 7 -- core_layer/health_monitor/performance_collector.py tests."""

from core_layer.health_monitor.models import PerformanceCounters
from core_layer.health_monitor.performance_collector import PerformanceCollector


def test_get_counts_returns_performance_counters():
    collector = PerformanceCollector()
    assert isinstance(collector.get_counts(), PerformanceCounters)


def test_new_collector_starts_at_zero():
    counts = PerformanceCollector().get_counts()
    assert counts.signal_count == 0
    assert counts.decision_count == 0
    assert counts.trade_count == 0
    assert counts.reject_count == 0
    assert counts.error_count == 0
    assert counts.reconnect_count == 0


def test_record_signal_increments_signal_count():
    collector = PerformanceCollector()
    collector.record_signal()
    assert collector.get_counts().signal_count == 1


def test_record_signal_twice_increments_to_two():
    collector = PerformanceCollector()
    collector.record_signal()
    collector.record_signal()
    assert collector.get_counts().signal_count == 2


def test_record_decision_increments_decision_count():
    collector = PerformanceCollector()
    collector.record_decision()
    assert collector.get_counts().decision_count == 1


def test_record_trade_increments_trade_count():
    collector = PerformanceCollector()
    collector.record_trade()
    assert collector.get_counts().trade_count == 1


def test_record_reject_increments_reject_count():
    collector = PerformanceCollector()
    collector.record_reject()
    assert collector.get_counts().reject_count == 1


def test_record_error_increments_error_count():
    collector = PerformanceCollector()
    collector.record_error()
    assert collector.get_counts().error_count == 1


def test_record_reconnect_increments_reconnect_count():
    collector = PerformanceCollector()
    collector.record_reconnect()
    assert collector.get_counts().reconnect_count == 1


def test_counters_are_independent_of_each_other():
    collector = PerformanceCollector()
    collector.record_signal()
    counts = collector.get_counts()
    assert counts.decision_count == 0
    assert counts.trade_count == 0


def test_runtime_seconds_is_non_negative():
    counts = PerformanceCollector().get_counts()
    assert counts.runtime_seconds >= 0.0


def test_two_collectors_do_not_share_state():
    a = PerformanceCollector()
    b = PerformanceCollector()
    a.record_signal()
    assert b.get_counts().signal_count == 0


def test_module_level_default_collector_functions_never_raise():
    import core_layer.health_monitor.performance_collector as module

    module.record_signal()
    module.record_decision()
    module.record_trade()
    module.record_reject()
    module.record_error()
    module.record_reconnect()
    counts = module.get_counts()
    assert isinstance(counts, PerformanceCounters)


def test_performance_collector_never_computes_a_win_rate():
    """Belt-and-suspenders: no method here resembles a computed metric -- PerformanceCounters carries no rate/average field."""
    import dataclasses

    field_names = {f.name for f in dataclasses.fields(PerformanceCounters)}
    forbidden = {"win_rate", "average_confidence", "success_rate", "score"}
    assert field_names.isdisjoint(forbidden)


def test_performance_counters_field_names_match_the_brief():
    import dataclasses

    field_names = {f.name for f in dataclasses.fields(PerformanceCounters)}
    assert field_names == {
        "signal_count", "decision_count", "trade_count", "reject_count",
        "error_count", "reconnect_count", "runtime_seconds",
    }
