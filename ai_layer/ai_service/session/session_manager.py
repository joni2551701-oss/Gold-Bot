"""
AI Layer — Session Manager (Phase 61.0: AI Infrastructure Foundation,
TASK 7).

In-memory session lifecycle: create/get/end. No persistence, no
background expiry job -- `is_expired()` is a pure function of a
caller-supplied "now", so a test controls time explicitly rather than
this module reaching for a real clock/sleep.
"""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from ai_layer.ai_service.session.conversation_state import ConversationState
from core_layer.logger.logger import setup_logger

logger = setup_logger("AISessionManager")

DEFAULT_SESSION_TTL = timedelta(minutes=30)


class SessionManager:
    def __init__(self, ttl: timedelta = DEFAULT_SESSION_TTL) -> None:
        self._ttl = ttl
        self._sessions: Dict[str, ConversationState] = {}

    def create_session(self, telegram_id: str) -> ConversationState:
        session_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        state = ConversationState(session_id=session_id, telegram_id=telegram_id, created_at=now, last_activity=now)
        self._sessions[session_id] = state
        logger.info(f"AI session created: session_id={session_id}, telegram_id={telegram_id}")
        return state

    def get_session(self, session_id: str) -> Optional[ConversationState]:
        return self._sessions.get(session_id)

    def end_session(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
        logger.info(f"AI session ended: session_id={session_id}")

    def is_expired(self, session_id: str, now: Optional[datetime] = None) -> bool:
        """Never raises: an unknown session_id is treated as expired (there is nothing to keep alive)."""
        state = self._sessions.get(session_id)
        if state is None:
            return True
        check_time = now if now is not None else datetime.now(timezone.utc)
        last_activity = state.last_activity or state.created_at
        return (check_time - last_activity) > self._ttl

    def purge_expired(self, now: Optional[datetime] = None) -> int:
        """Removes every expired session, returns how many were removed. A caller invokes this explicitly -- no background timer runs it."""
        expired_ids = [sid for sid in self._sessions if self.is_expired(sid, now)]
        for sid in expired_ids:
            self.end_session(sid)
        return len(expired_ids)
