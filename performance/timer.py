"""
Performance Metrics — timer utility (Phase A19).

PerformanceTimer measures a code block's wall-clock duration; it does
not decide, retry, or alter what runs inside it. See
docs/PERFORMANCE_METRICS.md for the full contract.

Usage (context manager):
    with PerformanceTimer("context_build", module="ContextEngine") as timer:
        build_context()
    print(timer.duration_ms)

Usage (with a collector -- a PerformanceMetric is recorded automatically):
    collector = PerformanceCollector()
    with PerformanceTimer("context_build", module="ContextEngine", collector=collector):
        build_context()

Usage (decorator):
    @measure_performance("strategy_execution", module="StrategyEngine", collector=collector)
    def run_strategy():
        ...
"""

import functools
import time
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Optional

from core.errors.base import GoldBotError
from core.logger import setup_logger
from performance.collector import PerformanceCollector
from performance.metrics import PerformanceMetric, generate_metric_id

logger = setup_logger("PerformanceMetrics")


class PerformanceTimer:
    """
    A context manager measuring wall-clock time via
    time.perf_counter() (monotonic, not affected by system clock
    changes -- the same primitive core/pipeline.py's own _log_stage()
    timing already uses).

    Never swallows an exception raised inside the `with` block --
    __exit__ always returns False, so the original exception still
    propagates after this timer records status="failed". If that
    exception is a core.errors.base.GoldBotError, its `.code` is
    captured as the metric's error_code (Phase A18 integration) --
    isinstance-checked, never guessed for any other exception type.
    """

    def __init__(
        self,
        name: str,
        module: str = "Unknown",
        collector: Optional[PerformanceCollector] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.name = name
        self.module = module
        self.collector = collector
        self.metadata = metadata or {}
        self.duration_ms: Optional[float] = None
        self.status = "success"
        self.error_code: Optional[str] = None
        self._start: Optional[float] = None

    def __enter__(self) -> "PerformanceTimer":
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        elapsed_seconds = time.perf_counter() - self._start
        self.duration_ms = round(elapsed_seconds * 1000, 3)

        if exc_type is not None:
            self.status = "failed"
            if isinstance(exc_val, GoldBotError):
                self.error_code = exc_val.code

        metric = PerformanceMetric(
            name=self.name,
            module=self.module,
            duration_ms=self.duration_ms,
            metric_id=generate_metric_id(),
            timestamp=datetime.now(timezone.utc),
            status=self.status,
            metadata=self.metadata,
            error_code=self.error_code,
        )

        logger.info(
            f"PERFORMANCE module={self.module} name={self.name} "
            f"duration_ms={self.duration_ms} status={self.status.upper()}"
        )

        if self.collector is not None:
            self.collector.record(metric)

        return False  # never swallow the exception


def measure_performance(
    name: str,
    module: str = "Unknown",
    collector: Optional[PerformanceCollector] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Callable:
    """
    Decorator form of PerformanceTimer -- wraps a function so every
    call automatically measures start time, end time, and duration,
    recording a PerformanceMetric (if `collector` is given) exactly
    as the context-manager form does. The wrapped function's return
    value and any raised exception both pass through unchanged.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with PerformanceTimer(name, module=module, collector=collector, metadata=metadata):
                return func(*args, **kwargs)
        return wrapper
    return decorator
