"""
Voice Layer — Voice Session Manager (Phase 65.2, TASK 7/8).

In-memory session lifecycle: create/get/end, mirroring
`ai/session/session_manager.py`'s `SessionManager` shape (no
persistence, no background expiry job) for a genuinely different
resource -- `VoiceSession`, not `ConversationState`. See
`docs/PHASE65_2_AUDIT.md`'s own "genuinely different session concept"
resolution for why this is not a duplicate Manager.

`set_voice_profile()` (TASK 8 — Senior/Seniorita "configuration, not a
new Persona") validates the chosen name against the injected
`VoiceProfileRegistry` (Phase 65.0, unmodified) rather than
introducing any Persona-linkage concept -- a user "choosing Senior or
Seniorita" is choosing an existing `VoiceProfile` by name, nothing
about `ai.persona.Persona` is read or referenced anywhere in this
file.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Optional

from core_layer.logger.logger import setup_logger
from voice.registry import VoiceProfileRegistry
from voice.session.models import VoiceSession

logger = setup_logger("VoiceSessionManager")


class VoiceSessionManager:
    """Every dependency is injectable, same convention as every other Phase 61.x-65.x manager."""

    def __init__(self, profile_registry: Optional[VoiceProfileRegistry] = None) -> None:
        self._profiles = profile_registry or VoiceProfileRegistry()
        self._sessions: Dict[str, VoiceSession] = {}

    def create_session(self, user_id: str, voice_profile_name: str, language: str = "en") -> Optional[VoiceSession]:
        """Never raises: an unknown voice_profile_name returns None rather than creating a session with a profile that doesn't exist."""
        if not self._profiles.exists(voice_profile_name):
            logger.warning(f"create_session called with an unknown voice profile: {voice_profile_name}")
            return None

        session_id = str(uuid.uuid4())
        session = VoiceSession(
            session_id=session_id, user_id=user_id, voice_profile_name=voice_profile_name,
            language=language, created_at=datetime.now(timezone.utc),
        )
        self._sessions[session_id] = session
        logger.info(f"Voice session created: session_id={session_id}, user_id={user_id}, profile={voice_profile_name}")
        return session

    def get_session(self, session_id: str) -> Optional[VoiceSession]:
        return self._sessions.get(session_id)

    def end_session(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)
        logger.info(f"Voice session ended: session_id={session_id}")

    def set_voice_profile(self, session_id: str, voice_profile_name: str) -> bool:
        """Never raises: an unknown session_id or voice_profile_name returns False, leaving the session's own profile unchanged."""
        session = self._sessions.get(session_id)
        if session is None:
            return False
        if not self._profiles.exists(voice_profile_name):
            logger.warning(f"set_voice_profile called with an unknown voice profile: {voice_profile_name}")
            return False
        session.voice_profile_name = voice_profile_name
        return True

    def link_conversation_session(self, session_id: str, conversation_session_id: str) -> bool:
        """Sets the pointer into ai.session.SessionManager's own store. Never raises: an unknown session_id returns False."""
        session = self._sessions.get(session_id)
        if session is None:
            return False
        session.conversation_session_id = conversation_session_id
        return True
