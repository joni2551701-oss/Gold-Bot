"""
Performance Metrics — collector (Phase A19).

PerformanceCollector stores PerformanceMetric records only -- it does
not generate a signal, does not make a decision, and does not write
to the database. See docs/PERFORMANCE_METRICS.md for the full
contract.
"""

from typing import List

from performance.metrics import PerformanceMetric


class PerformanceCollector:
    """
    A plain, in-memory list of PerformanceMetric records. Not a
    singleton -- each PerformanceCollector() is independent, so
    tests/future callers never leak state into one another (same
    convention as strategy_layer.strategy_manager.lifecycle.strategy_registry.StrategyRegistry/
    assets.asset_registry.AssetRegistry).
    """

    def __init__(self) -> None:
        self._metrics: List[PerformanceMetric] = []

    def record(self, metric: PerformanceMetric) -> None:
        """Appends `metric` -- never validates or rejects it (see performance.metrics.validate_metric() for that, a separate, opt-in step)."""
        self._metrics.append(metric)

    def get_metrics(self) -> List[PerformanceMetric]:
        """Every recorded metric, in the order recorded. Returns a copy -- mutating the result never affects the collector."""
        return list(self._metrics)

    def get_by_module(self, module: str) -> List[PerformanceMetric]:
        """Only metrics whose `.module` equals `module`, in the order recorded."""
        return [metric for metric in self._metrics if metric.module == module]

    def clear(self) -> None:
        """Removes every recorded metric."""
        self._metrics.clear()
