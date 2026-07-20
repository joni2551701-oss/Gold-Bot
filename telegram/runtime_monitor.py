"""
Telegram Layer — Runtime Monitor (GoldBot Core Telegram Runtime
Activation Alpha, TASK 4).

Tracks the aiogram Bot/Dispatcher connection's own operational state
(connected / last heartbeat / error count / uptime) -- a different
concern from `monitoring.system_monitor.SystemMonitor`'s trading-
pipeline uptime/last_scan (Core Owner Monitoring Alpha, previous
phase). `record_error()` relays into
`monitoring.system_monitor.record_error()` as a cross-module sink
(the same pattern `monitoring.error_monitor.ErrorMonitor.capture()`
already established), so a Telegram-runtime error also surfaces in
`/owner_status`'s `last_error` field without duplicating storage.

In-memory only, module-level singleton (`DEFAULT_RUNTIME_MONITOR`),
mirroring `SystemMonitor`'s own convention -- `telegram/polling.py` is
itself the long-running process this tracks, so a fresh process
restart is a legitimate "runtime reset," no persistence needed. Tests
construct their own `TelegramRuntimeMonitor()` instance for isolation,
same as `monitoring.system_monitor`'s own test suite does.
"""

import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from core.logger import setup_logger
from monitoring.system_monitor import record_error as _record_core_error

logger = setup_logger("TelegramRuntimeMonitor")


@dataclass(frozen=True)
class TelegramRuntimeStatus:
    status: str
    last_ping: Optional[str]
    errors: int
    uptime_seconds: float


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class TelegramRuntimeMonitor:
    def __init__(self):
        self._started_at = time.monotonic()
        self._connected = False
        self._last_ping: Optional[str] = None
        self._error_count = 0

    def record_connected(self) -> None:
        self._connected = True

    def record_heartbeat(self, timestamp: Optional[str] = None) -> None:
        self._last_ping = timestamp or _now_iso()

    def record_error(self, message: str) -> None:
        """Never raises: the relay into monitoring.system_monitor is best-effort."""
        self._error_count += 1
        try:
            _record_core_error(message)
        except Exception as e:
            logger.warning(f"record_error: relay to monitoring.system_monitor failed: {e}")

    def uptime_seconds(self) -> float:
        return time.monotonic() - self._started_at

    def get_status(self) -> TelegramRuntimeStatus:
        return TelegramRuntimeStatus(
            status="CONNECTED" if self._connected else "DISCONNECTED",
            last_ping=self._last_ping,
            errors=self._error_count,
            uptime_seconds=self.uptime_seconds(),
        )


DEFAULT_RUNTIME_MONITOR = TelegramRuntimeMonitor()


def record_connected() -> None:
    DEFAULT_RUNTIME_MONITOR.record_connected()


def record_heartbeat(timestamp: Optional[str] = None) -> None:
    DEFAULT_RUNTIME_MONITOR.record_heartbeat(timestamp)


def record_error(message: str) -> None:
    DEFAULT_RUNTIME_MONITOR.record_error(message)


def get_status() -> TelegramRuntimeStatus:
    return DEFAULT_RUNTIME_MONITOR.get_status()
