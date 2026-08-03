"""
Phase A19 -- Performance Metrics tests: timer and decorator
(performance/timer.py).
"""

import time

import pytest

from performance.collector import PerformanceCollector
from performance.timer import PerformanceTimer, measure_performance
from core_layer.errors.exceptions import StrategyError, DataError
from core_layer.errors import codes


def test_timer_measures_a_positive_duration():
    with PerformanceTimer("context_build", module="ContextEngine") as timer:
        time.sleep(0.005)

    assert timer.duration_ms is not None
    assert timer.duration_ms > 0
    assert timer.status == "success"


def test_timer_without_collector_does_not_raise():
    """A collector is optional -- the timer must work standalone."""
    with PerformanceTimer("x", module="M") as timer:
        pass
    assert timer.duration_ms is not None


def test_timer_records_a_metric_when_collector_supplied():
    collector = PerformanceCollector()

    with PerformanceTimer("context_build", module="ContextEngine", collector=collector):
        time.sleep(0.001)

    metrics = collector.get_metrics()
    assert len(metrics) == 1
    assert metrics[0].name == "context_build"
    assert metrics[0].module == "ContextEngine"
    assert metrics[0].status == "success"
    assert metrics[0].duration_ms > 0


def test_timer_never_swallows_an_exception():
    collector = PerformanceCollector()

    with pytest.raises(ValueError):
        with PerformanceTimer("x", module="M", collector=collector):
            raise ValueError("boom")

    # the metric is still recorded, status=failed, even though the exception propagated
    metrics = collector.get_metrics()
    assert len(metrics) == 1
    assert metrics[0].status == "failed"


def test_timer_captures_error_code_from_a_goldbot_error():
    """Phase A18 integration: a GoldBotError's .code becomes the metric's error_code."""
    collector = PerformanceCollector()

    with pytest.raises(StrategyError):
        with PerformanceTimer("strategy_execution", module="StrategyEngine", collector=collector):
            raise StrategyError(code=codes.STRATEGY_001, message="setup invalid", module="StrategyEngine")

    metric = collector.get_metrics()[0]
    assert metric.status == "failed"
    assert metric.error_code == codes.STRATEGY_001


def test_timer_leaves_error_code_none_for_a_non_goldbot_exception():
    collector = PerformanceCollector()

    with pytest.raises(ValueError):
        with PerformanceTimer("x", module="M", collector=collector):
            raise ValueError("not a GoldBotError")

    assert collector.get_metrics()[0].error_code is None


def test_timer_metadata_is_passed_through():
    collector = PerformanceCollector()

    with PerformanceTimer("x", module="M", collector=collector, metadata={"candles": 200}):
        pass

    assert collector.get_metrics()[0].metadata == {"candles": 200}


def test_different_goldbot_error_subclasses_all_capture_their_code():
    collector = PerformanceCollector()

    with pytest.raises(DataError):
        with PerformanceTimer("market_data_fetch_time", module="MarketDataLayer", collector=collector):
            raise DataError(code=codes.DATA_001, message="missing candle", module="MarketDataLayer")

    assert collector.get_metrics()[0].error_code == codes.DATA_001


# --- Decorator ---

def test_measure_performance_decorator_returns_the_function_result():
    @measure_performance("decision_time", module="DecisionEngine")
    def compute():
        return 42

    assert compute() == 42


def test_measure_performance_decorator_records_a_metric():
    collector = PerformanceCollector()

    @measure_performance("decision_time", module="DecisionEngine", collector=collector)
    def compute():
        time.sleep(0.001)
        return "ok"

    result = compute()

    assert result == "ok"
    metrics = collector.get_metrics()
    assert len(metrics) == 1
    assert metrics[0].name == "decision_time"
    assert metrics[0].module == "DecisionEngine"
    assert metrics[0].status == "success"


def test_measure_performance_decorator_propagates_exceptions_and_records_failure():
    collector = PerformanceCollector()

    @measure_performance("decision_time", module="DecisionEngine", collector=collector)
    def compute():
        raise RuntimeError("bad")

    with pytest.raises(RuntimeError):
        compute()

    assert collector.get_metrics()[0].status == "failed"


def test_measure_performance_decorator_preserves_function_metadata():
    @measure_performance("x", module="M")
    def my_function():
        """docstring"""
        return None

    assert my_function.__name__ == "my_function"
    assert my_function.__doc__ == "docstring"


def test_measure_performance_decorator_passes_through_arguments():
    @measure_performance("x", module="M")
    def add(a, b, c=0):
        return a + b + c

    assert add(1, 2, c=3) == 6
