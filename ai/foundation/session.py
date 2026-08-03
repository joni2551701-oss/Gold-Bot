"""
AI Foundation — AI Session (TASK-AI-001: AI Foundation Activation).

An in-memory session registry that carries a `FoundationContext` per
session and supports the Director's three operations:
create_session / close_session / restore_session. In-memory only, no
persistence, no background thread -- the same "foundation, not a
service" posture the existing `ai.session.SessionManager` uses. This is
reuse-by-pattern of that manager (create/get/close), extended with the
`restore_session` operation the Foundation contract adds; it is not an
import of `ai.session` (that package transitively pulls `core_layer.logger.logger`,
which the Foundation->Core prohibition forbids).

Depends only on stdlib and `ai.foundation.context`.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

from ai.foundation.context import FoundationContext


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class FoundationSession:
    """
    A single session. `active` flips to False on close and back to True
    on restore -- a closed session is retained (not deleted) so it can
    be restored, until `purge` drops it.
    """
    session_id: str
    context: FoundationContext
    created_at: datetime = field(default_factory=_now)
    last_activity: datetime = field(default_factory=_now)
    active: bool = True


class FoundationSessionManager:
    """One in-memory session table. Never raises on unknown ids -- close/restore report via return value/None."""

    def __init__(self) -> None:
        self._sessions: Dict[str, FoundationSession] = {}

    def create_session(
        self,
        session_id: Optional[str] = None,
        user_id: Optional[str] = None,
        language: str = "en",
        persona_id: Optional[str] = None,
        metadata: Optional[Dict[str, object]] = None,
    ) -> FoundationSession:
        """Mint a new active session. A `session_id` is generated if not supplied; a duplicate id raises."""
        sid = session_id or uuid4().hex
        if sid in self._sessions:
            raise ValueError(f"session already exists: {sid}")
        context = FoundationContext(
            session_id=sid,
            user_id=user_id,
            language=language,
            persona_id=persona_id,
            metadata=dict(metadata or {}),
        )
        session = FoundationSession(session_id=sid, context=context)
        self._sessions[sid] = session
        return session

    def get_session(self, session_id: str) -> Optional[FoundationSession]:
        return self._sessions.get(session_id)

    def close_session(self, session_id: str) -> bool:
        """Deactivate a session (kept for restore). Returns False if unknown or already closed."""
        session = self._sessions.get(session_id)
        if session is None or not session.active:
            return False
        session.active = False
        session.last_activity = _now()
        return True

    def restore_session(self, session_id: str) -> Optional[FoundationSession]:
        """Reactivate a previously-closed session. Returns None if unknown."""
        session = self._sessions.get(session_id)
        if session is None:
            return None
        session.active = True
        session.last_activity = _now()
        return session

    def purge(self, session_id: str) -> bool:
        """Permanently drop a session (cannot be restored afterwards)."""
        return self._sessions.pop(session_id, None) is not None

    def list_sessions(self) -> List[str]:
        return list(self._sessions.keys())

    def active_sessions(self) -> List[str]:
        return [sid for sid, s in self._sessions.items() if s.active]

    def clear(self) -> None:
        self._sessions.clear()
