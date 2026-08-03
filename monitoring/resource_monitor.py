"""
Monitoring Layer — Resource Monitor (Phase B.0 TASK 2's own genuine
gap, see `docs/PHASE_B0_AUDIT.md`). CPU/RAM/thread/restart/heartbeat
observation, distinct from `monitoring/system_monitor.py`'s own
database/data-connection/scan-activity concern.

Uses only the standard library (`resource`, `threading`) -- no new
dependency (`psutil` is not installed anywhere in this codebase, per
the audit). `resource` is POSIX-only; every field it would supply is
`Optional` and left `None` on a platform where it raises, never
fabricated. "Loop" (from the brief's own CPU/RAM/Thread/Loop/Restart/
Heartbeat/Latency list) is represented by the already-existing
`monitoring.system_monitor.SystemMonitor.record_scan()`/`last_scan`
mechanism -- not duplicated here. "Latency" is likewise already
covered by `monitoring/provider_health.py` and `MarketHealth.latency_ms`
-- not duplicated here either.
"""

import threading
from datetime import datetime, timezone
from typing import Optional

from core_layer.logger.logger import setup_logger
from database.monitoring_repository import MonitoringRepository
from monitoring.models import ResourceSnapshot
from monitoring.system_monitor import DEFAULT_MONITOR

logger = setup_logger("ResourceMonitor")

try:
    import resource as _resource
except ImportError:  # pragma: no cover -- non-POSIX platform
    _resource = None


def _cpu_and_memory():
    """Never raises: returns (None, None) when the `resource` module is unavailable or fails."""
    if _resource is None:
        return None, None
    try:
        usage = _resource.getrusage(_resource.RUSAGE_SELF)
        cpu_time_seconds = usage.ru_utime + usage.ru_stime
        max_rss_kb = usage.ru_maxrss
        return cpu_time_seconds, max_rss_kb
    except Exception as e:
        logger.warning(f"_cpu_and_memory failed: {e}")
        return None, None


def record_process_start(repository: Optional[MonitoringRepository] = None) -> None:
    """Call once at process startup (e.g. GoldBot.__init__). Never raises: a database failure is logged and swallowed -- a monitoring write must never block startup."""
    try:
        (repository or MonitoringRepository()).record_process_start()
    except Exception as e:
        logger.warning(f"record_process_start failed: {e}")


def get_resource_snapshot(repository: Optional[MonitoringRepository] = None) -> ResourceSnapshot:
    """Never raises: every sub-read is already defensive; a restart-count read failure falls back to 0 rather than propagating."""
    cpu_time_seconds, max_rss_kb = _cpu_and_memory()

    try:
        restart_count = (repository or MonitoringRepository()).get_restart_count()
    except Exception as e:
        logger.warning(f"get_resource_snapshot: get_restart_count failed: {e}")
        restart_count = 0

    return ResourceSnapshot(
        cpu_time_seconds=cpu_time_seconds,
        max_rss_kb=max_rss_kb,
        thread_count=threading.active_count(),
        restart_count=restart_count,
        uptime_seconds=DEFAULT_MONITOR.uptime_seconds(),
        heartbeat_at=datetime.now(timezone.utc).isoformat(),
    )
