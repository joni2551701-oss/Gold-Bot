"""
Core Layer — Maintenance Mode model (Phase 59.9: Emergency Safety
Layer Foundation, TASK 5).

MaintenanceMode is a finer-grained detail record for the
EmergencyState.MAINTENANCE state (core.emergency.emergency_state) --
same "enum value vs. detail record" split already established by
configuration.feature_registry.FeatureDescriptor vs
configuration.runtime_state.FeatureRuntimeState. EmergencyManager
(TASK 3) persists the state transition itself (via
EmergencyRepository's append-only history); this module models the
maintenance-specific shape (reason/owner/started_at) a future owner
service could build a `/maintenance on` response from -- pure,
immutable, no persistence of its own in this phase.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class MaintenanceMode:
    enabled: bool
    reason: Optional[str] = None
    started_at: Optional[datetime] = None
    owner: Optional[str] = None


def enable_maintenance(reason: Optional[str] = None, owner: Optional[str] = None) -> MaintenanceMode:
    """Pure factory -- stamps started_at, same convention as every other create_X()/enable_X() factory in this codebase."""
    return MaintenanceMode(enabled=True, reason=reason, started_at=datetime.now(timezone.utc), owner=owner)


def disable_maintenance(owner: Optional[str] = None) -> MaintenanceMode:
    """The NORMAL-equivalent maintenance shape -- enabled=False, no reason/started_at (there is no active window to describe)."""
    return MaintenanceMode(enabled=False, reason=None, started_at=None, owner=owner)
