"""
AI Layer — Provider Health Tracker (Phase 61.1: AI Provider
Reliability Foundation, TASK 2).

In-memory, per-provider `HealthStatus` record -- no real health check
runs anywhere in this phase; a caller (a future real-integration phase,
or a test) reports an observed status via `record()`. Seeded from
`provider_registry.py`'s same five names `ProviderManager` already
uses, so `ai/router/router.py` (TASK 4) can consult both without a
name mismatch.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Optional

from ai.providers.provider_registry import build_provider_registry
from ai.providers.provider_status import AVAILABLE_STATUSES, HealthStatus
from core.logger import setup_logger

logger = setup_logger("ProviderHealth")


@dataclass(frozen=True)
class ProviderHealthRecord:
    provider_name: str
    status: HealthStatus
    reason: Optional[str]
    checked_at: datetime


class ProviderHealthTracker:
    """Every registered provider starts ONLINE -- optimistic default, matching `ProviderManager`'s own "no provider disabled until a caller says so" posture."""

    def __init__(self) -> None:
        self._records: Dict[str, ProviderHealthRecord] = {
            name: ProviderHealthRecord(
                provider_name=name, status=HealthStatus.ONLINE, reason=None,
                checked_at=datetime.now(timezone.utc),
            )
            for name in (d.name for d in build_provider_registry())
        }

    def record(self, provider_name: str, status: HealthStatus, reason: Optional[str] = None) -> None:
        """Unregistered provider names are still recorded (not rejected) -- a health tracker should not silently drop an observation just because it predates registry knowledge of that name."""
        self._records[provider_name] = ProviderHealthRecord(
            provider_name=provider_name, status=status, reason=reason,
            checked_at=datetime.now(timezone.utc),
        )
        logger.info(f"Provider health recorded: provider={provider_name} status={status.value} reason={reason}")

    def mark_recovered(self, provider_name: str) -> None:
        self.record(provider_name, HealthStatus.ONLINE, reason="recovered")

    def status_of(self, provider_name: str) -> Optional[HealthStatus]:
        record = self._records.get(provider_name)
        return record.status if record else None

    def is_available(self, provider_name: str) -> bool:
        """An unrecorded/unknown provider is treated as unavailable -- fail-safe, never assume health for a name this tracker has no observation for."""
        status = self.status_of(provider_name)
        return status in AVAILABLE_STATUSES if status is not None else False

    def all_records(self) -> Dict[str, ProviderHealthRecord]:
        return dict(self._records)
