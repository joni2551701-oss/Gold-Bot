"""
Assistant Layer — Conversation/Voice/Memory Integration Adapters
(Phase 65.3: Personal AI Assistant Foundation, TASK 5/6).

Three pure functions. None of them import `voice/`,
`ai.conversation/`, or `ai.memory/` -- see `docs/PHASE65_3_AUDIT.md`'s
"core architectural resolution" section for why: the brief's own
diagram places Assistant *before* Conversation, so applying the
Intelligence Dependency Principle literally, `assistant/` may depend
on nothing downstream of it. Integration here is structural, not a
Python import: each function returns a plain `dict`/`str` shaped to
exactly match an existing, already-LOCKed public API's parameters. A
future, separately-approved live-wiring phase is the one that actually
calls `voice.session.manager.VoiceSessionManager.create_session(**...)`
or `ai.conversation.conversation_engine.ConversationEngine.start_session(**...)`
with this function's output.
"""

from typing import Dict, Optional

from assistant.identity import AssistantIdentity
from assistant.models import AssistantProfile


def assistant_to_voice_session_params(profile: AssistantProfile, identity: AssistantIdentity) -> Dict[str, str]:
    """
    Shaped to match `voice.session.manager.VoiceSessionManager.create_session()`'s
    existing `(user_id, voice_profile_name, language)` parameters.
    `selected_voice` wins when set; otherwise falls back to the
    identity's own `default_voice` -- TASK 8's "Voice: Auto".
    """
    return {
        "user_id": profile.user_id,
        "voice_profile_name": profile.selected_voice or identity.default_voice,
        "language": profile.selected_language,
    }


def assistant_to_conversation_params(profile: AssistantProfile) -> Dict[str, str]:
    """Shaped to match `ai.conversation.conversation_engine.ConversationEngine.start_session()`'s existing `(telegram_id)` parameter -- `user_id` is reused as the telegram_id pointer, never a new identifier scheme."""
    return {"telegram_id": profile.user_id}


def assistant_memory_scope_key(profile: AssistantProfile, sub_key: Optional[str] = None) -> str:
    """
    Returns a `"USER_PREFERENCE:{user_id}"`-shaped string, matching the
    exact `"scope:key"` convention
    `ai.conversation.conversation_adapters.memory_key_from_entry()`
    already establishes -- without importing
    `ai.memory.models.MemoryScope` (the literal `"USER_PREFERENCE"`
    mirrors that enum's existing value by convention only, the same
    coincidental-name-not-code-link pattern already used for
    `SENIORITA_VOICE.name`). Always keyed by `profile.user_id`, never
    `profile.assistant_id` -- TASK 6's "Assistant Memory egasi emas.
    Memory Userniki." (Assistant is not the memory owner; memory
    belongs to the user), enforced by construction.
    """
    base = f"USER_PREFERENCE:{profile.user_id}"
    return f"{base}:{sub_key}" if sub_key else base
