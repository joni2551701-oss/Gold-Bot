"""
Voice Layer — Voice Session Model (Phase 65.2, TASK 7).

A genuinely different session concept from `ai/session/`'s
`ConversationState` -- see `docs/PHASE65_2_AUDIT.md`'s own resolution.
`VoiceSession` carries voice-specific state (`voice_profile_name`,
`language`) plus a `conversation_session_id` *pointer* into
`ai.session.SessionManager`'s own store -- never an embedded
`ConversationState` object, the same "never carry another package's
object graph" posture `media_layer/content_manager/models.py`'s `MediaAsset.content_id`
already established. Mutable (unlike most `voice/` dataclasses)
because a session's `conversation_session_id`/`voice_profile_name` are
each set after construction -- same "genuinely accumulates state"
reasoning `ai/session/conversation_state.py`'s own `ConversationState`
already uses for being mutable.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class VoiceSession:
    session_id: str
    user_id: str
    voice_profile_name: str
    language: str = "en"
    conversation_session_id: Optional[str] = None
    created_at: Optional[datetime] = None
