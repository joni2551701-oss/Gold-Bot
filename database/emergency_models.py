"""
Database Layer — Emergency State persistence model (Phase 59.9:
Emergency Safety Layer Foundation, TASK 2). Mirrors
database/audit_log_models.py's own shape/naming split: the DB-row
model gets its own name (EmergencyStateEntry), distinct from the
domain model (core.emergency.emergency_state.EmergencyStateRecord) --
same "two names for two layers" precedent as
database.runtime_feature_models.RuntimeFeatureRecord vs
configuration.runtime_state.FeatureRuntimeState.

Append-only by design (see database/emergency_repository.py): every
transition is a new row, never an UPDATE, so history is never lost
("Tarix yo'qolmasligi kerak" -- per this task's own brief). `updated_at`
therefore always equals `created_at` for a given row -- kept only for
literal field-parity with the Director's brief (id/state/reason/
source/changed_by/created_at/updated_at), not because a row is ever
actually updated after insert.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class EmergencyStateEntry:
    """
    Mirrors the 'emergency_states' table row shape. `id` is
    intentionally excluded -- repository-internal detail, same
    convention as every other Phase 59.x model in this codebase.
    state: the EmergencyState value name (stored as TEXT, e.g. "KILLED").
    changed_by: who/what caused this transition (a Telegram user_id,
        "owner", or "system" for an automatic one) -- free text, no
        fixed taxonomy, same posture as AuditLogEntry.actor.
    source: "owner" or "system", same distinction as
        core.emergency.emergency_state.EmergencyStateRecord.source.
    """
    state: str
    reason: Optional[str] = None
    source: str = "system"
    changed_by: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


def create_emergency_state_entry(
    state: str,
    reason: Optional[str] = None,
    source: str = "system",
    changed_by: Optional[str] = None,
) -> EmergencyStateEntry:
    """Pure, deterministic factory -- stamps created_at/updated_at to the same 'now' (see module docstring on why both are stamped identically)."""
    now = datetime.now(timezone.utc)
    return EmergencyStateEntry(
        state=state,
        reason=reason,
        source=source,
        changed_by=changed_by,
        created_at=now,
        updated_at=now,
    )
