"""
Monitoring Layer — Error Monitor (GoldBot Core Owner Monitoring Alpha,
TASK 6).

Genuinely new capture mechanism -- confirmed via
`docs/PHASE_CORE_MONITORING_AUDIT.md`'s own `core/logger.py` section
that no ErrorEvent/error-capture/severity persistence exists anywhere
in this codebase; `core.logger.setup_logger()` is a bare stdout
logger only. Persisted via `database.monitoring_repository.MonitoringRepository`
(TASK 9), so `/errors`' own "Last 24h" window survives a process
restart.

`capture()` also relays the message into
`monitoring.system_monitor.DEFAULT_MONITOR.record_error()`, so
`SystemHealth.last_error` (TASK 1) reflects the most recently captured
error without every caller having to remember to update both.
"""

from collections import Counter
from typing import Dict, Optional, Sequence

from core.logger import setup_logger
from database.monitoring_repository import MonitoringRepository
from monitoring.models import ErrorEvent, ErrorSeverity
from monitoring.system_monitor import record_error as record_system_error

logger = setup_logger("ErrorMonitor")


class ErrorMonitor:
    def __init__(self, repository: Optional[MonitoringRepository] = None):
        self._repository = repository

    def _get_repository(self) -> MonitoringRepository:
        if self._repository is None:
            self._repository = MonitoringRepository()
        return self._repository

    def capture(
        self,
        module: str,
        error_type: str,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
    ) -> Optional[ErrorEvent]:
        """Never raises: a database failure logs a warning and returns None -- capturing an error must never itself raise a second error."""
        try:
            row = self._get_repository().record_error(module, error_type, message, severity.value)
        except Exception as e:
            logger.warning(f"capture failed: {e}")
            return None

        record_system_error(message)

        return ErrorEvent(
            timestamp=row.created_at.isoformat() if row.created_at else "",
            module=row.module,
            error_type=row.error_type,
            message=row.message,
            severity=ErrorSeverity(row.severity),
        )

    def get_recent_errors(self, hours: int = 24, limit: int = 200) -> Sequence[ErrorEvent]:
        """Never raises: a database failure returns an empty tuple."""
        try:
            rows = self._get_repository().get_recent_errors(hours=hours, limit=limit)
        except Exception as e:
            logger.warning(f"get_recent_errors failed: {e}")
            return ()

        return tuple(
            ErrorEvent(
                timestamp=row.created_at.isoformat() if row.created_at else "",
                module=row.module,
                error_type=row.error_type,
                message=row.message,
                severity=ErrorSeverity(row.severity),
            )
            for row in rows
        )

    def get_error_counts(self, hours: int = 24) -> Dict[str, int]:
        """Counts by error_type over the window -- matches this brief's own '/errors' worked example ('API timeout: 2, Data error: 0, Exception: 1')."""
        return dict(Counter(event.error_type for event in self.get_recent_errors(hours=hours)))
