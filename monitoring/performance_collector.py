"""
Monitoring Layer — Performance Collector (Phase B.0 TASK 7's own
genuine gap, see `docs/PHASE_B0_AUDIT.md`). "Hozircha faqat yig'adi.
Hisoblamaydi" -- for now, only collects, never computes. Plain,
in-memory tallies only -- no win-rate, no average, no derived metric
of any kind (that is `monitoring.performance.PerformanceTracker`'s
own, separate, already-existing concern, computed from closed trades).

Same "shared module-level instance, tests construct their own" posture
`monitoring.system_monitor.SystemMonitor`/`DEFAULT_MONITOR` already
established -- counts reset on process restart by design (a
count-since-this-process-started concern, not a persisted history;
`monitoring.resource_monitor.get_resource_snapshot()`'s own
`restart_count` is the persisted, cross-restart fact).
"""

import time

from monitoring.models import PerformanceCounters


class PerformanceCollector:
    """Passive tally only (Rule 3: observe/collect/report) -- no method here ever reads, computes, or influences a signal/decision/trade of its own."""

    def __init__(self) -> None:
        self._started_at = time.monotonic()
        self._signal_count = 0
        self._decision_count = 0
        self._trade_count = 0
        self._reject_count = 0
        self._error_count = 0
        self._reconnect_count = 0

    def record_signal(self) -> None:
        self._signal_count += 1

    def record_decision(self) -> None:
        self._decision_count += 1

    def record_trade(self) -> None:
        self._trade_count += 1

    def record_reject(self) -> None:
        self._reject_count += 1

    def record_error(self) -> None:
        self._error_count += 1

    def record_reconnect(self) -> None:
        self._reconnect_count += 1

    def get_counts(self) -> PerformanceCounters:
        return PerformanceCounters(
            signal_count=self._signal_count,
            decision_count=self._decision_count,
            trade_count=self._trade_count,
            reject_count=self._reject_count,
            error_count=self._error_count,
            reconnect_count=self._reconnect_count,
            runtime_seconds=time.monotonic() - self._started_at,
        )


DEFAULT_COLLECTOR = PerformanceCollector()


def get_counts() -> PerformanceCounters:
    return DEFAULT_COLLECTOR.get_counts()


def record_signal() -> None:
    DEFAULT_COLLECTOR.record_signal()


def record_decision() -> None:
    DEFAULT_COLLECTOR.record_decision()


def record_trade() -> None:
    DEFAULT_COLLECTOR.record_trade()


def record_reject() -> None:
    DEFAULT_COLLECTOR.record_reject()


def record_error() -> None:
    DEFAULT_COLLECTOR.record_error()


def record_reconnect() -> None:
    DEFAULT_COLLECTOR.record_reconnect()
