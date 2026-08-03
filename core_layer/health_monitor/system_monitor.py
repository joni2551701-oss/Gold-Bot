"""
Monitoring Layer — System Monitor (GoldBot Core Owner Monitoring
Alpha, TASK 2).

Composes two already-existing, already-tested sources rather than
writing new health-check logic (per
`docs/PHASE_CORE_MONITORING_AUDIT.md`):
`platform_layer.telegram.admin_service.AdminService.get_system_status()` (database
reachability) and `core_layer.health_monitor.provider_health.check_registry_health()`
(per-provider ONLINE/DEGRADED/OFFLINE). `uptime_seconds`/`last_scan`/
`last_error` are this module's own genuine addition -- no existing
process-uptime or scan-timestamp concept exists anywhere in the
codebase (`core_layer/system_state/system_state.py` has no live holder, per the audit).

Never modifies `core/pipeline.py` -- `record_scan()` is a passive
sink a caller reports activity to; this module never infers "last
scan" from the Trading Core itself (Strict Rule: `core/` is
read-only for this phase).
"""

import time
from datetime import datetime, timezone
from typing import Optional

from core_layer.logger.logger import setup_logger
from data_layer.providers.registry import ProviderRegistry, build_default_registry
from core_layer.health_monitor.models import SystemHealth
from core_layer.health_monitor.provider_health import ProviderHealthStatus, check_registry_health
from platform_layer.telegram.admin_service import AdminService

logger = setup_logger("SystemMonitor")


class SystemMonitor:
    """
    Read-only, in-memory observation state -- no database of any
    kind. `DEFAULT_MONITOR` (module-level below) is the shared
    instance every Owner Telegram command reads/writes through in a
    running bot process, so `record_scan()`/`record_error()` calls
    from one command stay visible to a later `/status` call in the
    same process. Tests construct their own `SystemMonitor()` instead
    of touching the shared default.
    """

    def __init__(self) -> None:
        self._started_at = time.monotonic()
        self._last_scan: Optional[str] = None
        self._last_error: Optional[str] = None

    def record_scan(self, timestamp: Optional[str] = None) -> None:
        """Never raises. A caller reports pipeline activity -- this module never infers it."""
        self._last_scan = timestamp or datetime.now(timezone.utc).isoformat()

    def record_error(self, message: Optional[str]) -> None:
        """Never raises. Called by `core_layer.health_monitor.error_monitor.ErrorMonitor.capture()`, or any other caller."""
        self._last_error = message

    def uptime_seconds(self) -> float:
        return time.monotonic() - self._started_at

    def get_health(
        self,
        admin_service: Optional[AdminService] = None,
        registry: Optional[ProviderRegistry] = None,
    ) -> SystemHealth:
        """
        Never raises: every sub-check is already independently
        "never raises" (`AdminService.get_system_status()`,
        `check_registry_health()`) -- this method only composes their
        output plus this instance's own in-memory state, wrapped
        defensively in case a future change to either breaks that
        contract.
        """
        try:
            status = (admin_service or AdminService()).get_system_status()
            database_status = status.database
        except Exception as e:
            logger.warning(f"get_health: AdminService failed: {e}")
            database_status = "N/A"

        try:
            reports = check_registry_health(registry or build_default_registry())
            online = sum(1 for r in reports if r.status == ProviderHealthStatus.ONLINE)
            data_connection = f"{online}/{len(reports)} ONLINE"
        except Exception as e:
            logger.warning(f"get_health: provider registry check failed: {e}")
            data_connection = "N/A"

        return SystemHealth(
            status="RUNNING",
            uptime_seconds=self.uptime_seconds(),
            data_connection=data_connection,
            database_status=database_status,
            last_scan=self._last_scan,
            last_error=self._last_error,
        )


DEFAULT_MONITOR = SystemMonitor()


def get_health(
    admin_service: Optional[AdminService] = None,
    registry: Optional[ProviderRegistry] = None,
) -> SystemHealth:
    return DEFAULT_MONITOR.get_health(admin_service=admin_service, registry=registry)


def record_scan(timestamp: Optional[str] = None) -> None:
    DEFAULT_MONITOR.record_scan(timestamp)


def record_error(message: Optional[str]) -> None:
    DEFAULT_MONITOR.record_error(message)
