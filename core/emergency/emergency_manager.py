"""
Core Layer — Emergency Manager (Phase 59.9: Emergency Safety Layer
Foundation, TASK 3/6).

The runtime controller for core.emergency.emergency_state.EmergencyState
-- an owner (once a future, separately-approved phase wires a command
to it) can pause/kill/maintenance/restore the bot's emergency posture,
with every transition persisted (append-only history, never lost) and
audited. Same "foundation, not full wiring" posture as
configuration/runtime_feature_manager.py (Phase 59.7): this module is
only ever constructed and called directly (a test, or a future owner
service function) -- nothing in core/pipeline.py, decision/, risk/, or
execution/ constructs or reads an EmergencyManager in this phase, and
this phase does not block any real order or signal.

Composes, rather than reimplements:
    database.emergency_repository.EmergencyRepository -- persistence (TASK 2)
    database.audit_log_repository.AuditLogRepository   -- audit trail (TASK 6)

This is core/ importing database/ -- the same one-directional
foundation-service dependency configuration/runtime_feature_manager.py
already established for configuration/ -> database/ (Phase 59.7,
documented in docs/ARCHITECTURE.md). Never reversed: database/ does not
import core/emergency/.
"""

from typing import Optional

from core.emergency.emergency_state import EmergencyState, EmergencyStateRecord, create_emergency_state_record
from database.audit_log_repository import AuditLogRepository
from database.emergency_repository import EmergencyRepository
from core.logger import setup_logger

logger = setup_logger("EmergencyManager")

_ACTION_FOR_STATE = {
    EmergencyState.PAUSED: "PAUSE_ACTIVATED",
    EmergencyState.KILLED: "KILL_ACTIVATED",
    EmergencyState.MAINTENANCE: "MAINTENANCE_ENABLED",
    EmergencyState.NORMAL: "SYSTEM_RESTORED",
}


class EmergencyManager:
    """
    One process-local manager -- own repository instances (each
    injectable, same optional-dependency convention as
    RuntimeFeatureManager's own constructor). Auto-loads the current
    state on construction: a fresh EmergencyManager backed by the same
    EmergencyRepository (e.g. after a restart) reads the same state
    back, defaulting to NORMAL if nothing has ever been recorded.
    """

    def __init__(
        self,
        emergency_repository: Optional[EmergencyRepository] = None,
        audit_log_repository: Optional[AuditLogRepository] = None,
    ):
        self.repository = emergency_repository or EmergencyRepository()
        self.audit_log_repository = audit_log_repository or AuditLogRepository()

    def get_status(self) -> EmergencyStateRecord:
        """The current state, derived from the repository's most recent history row -- NORMAL (source="system", no reason) if none has ever been recorded."""
        entry = self.repository.get_current_state()
        if entry is None:
            return create_emergency_state_record(EmergencyState.NORMAL, source="system")
        return EmergencyStateRecord(
            state=EmergencyState(entry.state),
            reason=entry.reason,
            activated_by=entry.changed_by,
            source=entry.source,
            created_at=entry.created_at,
            updated_at=entry.updated_at,
        )

    def _transition(
        self, state: EmergencyState, reason: Optional[str], activated_by: Optional[str], source: str
    ) -> EmergencyStateRecord:
        entry = self.repository.record_transition(
            state.value, reason=reason, source=source, changed_by=activated_by
        )
        action = _ACTION_FOR_STATE[state]
        self.audit_log_repository.log_action(
            actor=activated_by or source, action=action, target=state.value,
            result="SUCCESS", details=reason,
        )
        logger.info(f"Emergency state transition: {state.value} (reason={reason}, source={source})")
        return EmergencyStateRecord(
            state=state, reason=reason, activated_by=activated_by, source=source,
            created_at=entry.created_at, updated_at=entry.updated_at,
        )

    def activate_pause(
        self, reason: Optional[str] = None, activated_by: Optional[str] = None, source: str = "system"
    ) -> EmergencyStateRecord:
        return self._transition(EmergencyState.PAUSED, reason, activated_by, source)

    def activate_kill(
        self, reason: Optional[str] = None, activated_by: Optional[str] = None, source: str = "system"
    ) -> EmergencyStateRecord:
        return self._transition(EmergencyState.KILLED, reason, activated_by, source)

    def activate_maintenance(
        self, reason: Optional[str] = None, activated_by: Optional[str] = None, source: str = "system"
    ) -> EmergencyStateRecord:
        return self._transition(EmergencyState.MAINTENANCE, reason, activated_by, source)

    def restore_normal(
        self, reason: Optional[str] = None, activated_by: Optional[str] = None, source: str = "system"
    ) -> EmergencyStateRecord:
        return self._transition(EmergencyState.NORMAL, reason, activated_by, source)
