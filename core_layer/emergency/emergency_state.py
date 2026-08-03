"""
Core Layer — Emergency State Model (Phase 59.9: Emergency Safety Layer
Foundation, TASK 1).

A finer-grained, dedicated vocabulary for the emergency layer --
deliberately separate from core_layer.system_state.system_state.SystemState (Phase 59.6),
same "two parallel hierarchies for two different granularities"
precedent already established by telegram.owner.owner_roles.OwnerRole
vs telegram.permissions.PermissionLevel. SystemState's own docstring
reserved PANIC/MAINTENANCE "for a future Phase 59.9" -- this phase
does not reuse those two values because SystemState has no equivalent
of WARNING/PAUSED (a circuit-breaker-driven, less-severe posture, distinct
from a full KILLED stop), which this phase's circuit_breaker.py (TASK 4)
needs. Reconciling the two enums (or having one wrap the other) is left
to a future, separately-approved wiring phase -- this phase does not
touch core_layer/system_state/system_state.py.

Foundation only: nothing in core/pipeline.py, decision/, risk/, or
execution/ reads this module. Constructing an EmergencyStateRecord
changes no runtime behavior anywhere.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class EmergencyState(Enum):
    """
    NORMAL: default operating state -- no emergency condition active.
    WARNING: a circuit-breaker condition was observed (see
        circuit_breaker.py's CircuitDecision.WARNING) but nothing has
        been paused or killed yet -- an advisory state only.
    PAUSED: signal generation should be treated as temporarily
        suspended by whoever wires this layer in later -- reversible,
        typically owner- or circuit-breaker-initiated.
    KILLED: the most severe state -- execution should be treated as
        fully blocked by whoever wires this layer in later. Reversible
        only via restore_normal().
    MAINTENANCE: an owner-initiated maintenance window -- distinct from
        PAUSED/KILLED in intent (planned, not a safety trip), see
        maintenance.py (TASK 5) for the finer-grained detail record.
    """
    NORMAL = "NORMAL"
    WARNING = "WARNING"
    PAUSED = "PAUSED"
    KILLED = "KILLED"
    MAINTENANCE = "MAINTENANCE"


@dataclass(frozen=True)
class EmergencyStateRecord:
    """
    An immutable record of one state transition -- not a mutable
    "current state" holder (emergency_manager.py's EmergencyManager,
    backed by database.emergency_repository.EmergencyRepository, is the
    holder). `source` distinguishes who/what caused the transition
    ("system" for an automatic/circuit-breaker-driven change, "owner"
    for a manual one), same convention as
    configuration.runtime_state.FeatureRuntimeState's own `source`
    field. `expires_at` is optional, reserved for a future
    time-boxed PAUSED/MAINTENANCE window -- this phase never sets or
    reads it beyond storing/round-tripping the value.
    """
    state: EmergencyState
    reason: Optional[str] = None
    activated_by: Optional[str] = None
    source: str = "system"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


def create_emergency_state_record(
    state: EmergencyState,
    reason: Optional[str] = None,
    activated_by: Optional[str] = None,
    source: str = "system",
    expires_at: Optional[datetime] = None,
) -> EmergencyStateRecord:
    """Pure, deterministic factory -- stamps created_at/updated_at to the same 'now', same convention as database.runtime_feature_models.create_runtime_feature_record()."""
    now = datetime.now(timezone.utc)
    return EmergencyStateRecord(
        state=state,
        reason=reason,
        activated_by=activated_by,
        source=source,
        created_at=now,
        updated_at=now,
        expires_at=expires_at,
    )
