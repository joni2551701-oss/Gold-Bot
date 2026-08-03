"""
Monitoring Layer — Health Monitor (Phase B.0 TASK 6's own genuine gap,
see `docs/PHASE_B0_AUDIT.md`). A pure, deterministic OK/WARNING/CRITICAL
classifier over already-known facts -- `core_layer.health_monitor.models.SystemHealth`
(TASK 1) and `core_layer.health_monitor.error_monitor.ErrorMonitor`'s recent error
counts (TASK 6). Never fabricates a grade: every branch is a direct
read of an already-observed field, no scoring, no weighting.
"""

from typing import Mapping, Optional

from core_layer.health_monitor.models import HealthStatus, SystemHealth


def classify_health(system_health: SystemHealth, error_counts: Optional[Mapping[str, int]] = None) -> HealthStatus:
    """
    Never raises: pure function over already-constructed values.

    CRITICAL: database unreachable, or zero data providers online.
    WARNING: some (but not all) providers offline/degraded, or any
        error captured in the observed window, or a captured
        `last_error` present.
    OK: database reachable, providers healthy, no errors observed.
    """
    database_ok = system_health.database_status.upper() in ("OK", "CONNECTED", "RUNNING")
    if not database_ok:
        return HealthStatus.CRITICAL

    online, total = _parse_data_connection(system_health.data_connection)
    if total is not None and total > 0 and online == 0:
        return HealthStatus.CRITICAL

    if total is not None and online is not None and online < total:
        return HealthStatus.WARNING

    if system_health.last_error:
        return HealthStatus.WARNING

    total_errors = sum(error_counts.values()) if error_counts else 0
    if total_errors > 0:
        return HealthStatus.WARNING

    return HealthStatus.OK


def _parse_data_connection(data_connection: str):
    """Parses the existing 'N/M ONLINE' label (system_monitor.py's own format) into (online, total). Never raises: an unparseable label returns (None, None)."""
    try:
        counts = data_connection.split()[0]
        online_str, total_str = counts.split("/")
        return int(online_str), int(total_str)
    except (ValueError, IndexError):
        return None, None
