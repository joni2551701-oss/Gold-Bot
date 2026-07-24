"""
Phase A19 -- Performance Metrics tests: collector
(performance/collector.py).
"""

from performance.collector import PerformanceCollector
from performance.metrics import PerformanceMetric


def _metric(name="x", module="M", duration_ms=1):
    return PerformanceMetric(name=name, module=module, duration_ms=duration_ms)


def test_collector_starts_empty():
    collector = PerformanceCollector()
    assert collector.get_metrics() == []


def test_record_adds_a_metric():
    collector = PerformanceCollector()
    metric = _metric()

    collector.record(metric)

    assert collector.get_metrics() == [metric]


def test_record_preserves_insertion_order():
    collector = PerformanceCollector()
    m1, m2, m3 = _metric("a"), _metric("b"), _metric("c")

    collector.record(m1)
    collector.record(m2)
    collector.record(m3)

    assert collector.get_metrics() == [m1, m2, m3]


def test_get_metrics_returns_a_copy_not_the_internal_list():
    collector = PerformanceCollector()
    collector.record(_metric())

    result = collector.get_metrics()
    result.append(_metric("intruder"))

    assert len(collector.get_metrics()) == 1  # unaffected by mutating the returned list


def test_get_by_module_filters_correctly():
    collector = PerformanceCollector()
    collector.record(_metric("a", module="ContextEngine"))
    collector.record(_metric("b", module="StrategyEngine"))
    collector.record(_metric("c", module="ContextEngine"))

    context_metrics = collector.get_by_module("ContextEngine")

    assert len(context_metrics) == 2
    assert {m.name for m in context_metrics} == {"a", "c"}


def test_get_by_module_returns_empty_list_for_unknown_module():
    collector = PerformanceCollector()
    collector.record(_metric(module="ContextEngine"))

    assert collector.get_by_module("DoesNotExist") == []


def test_clear_removes_every_metric():
    collector = PerformanceCollector()
    collector.record(_metric())
    collector.record(_metric())

    collector.clear()

    assert collector.get_metrics() == []


def test_each_collector_instance_is_independent():
    """Not a singleton -- one collector's state must never leak into another's."""
    first = PerformanceCollector()
    second = PerformanceCollector()

    first.record(_metric())

    assert len(first.get_metrics()) == 1
    assert len(second.get_metrics()) == 0
