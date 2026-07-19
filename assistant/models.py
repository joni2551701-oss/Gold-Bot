"""
Assistant Layer — Assistant Profile Model (Phase 65.3: Personal AI
Assistant Foundation, TASK 2).

`AssistantProfile` is a genuinely new resource type -- not a third
session class alongside `ai.session.conversation_state.ConversationState`
and `voice.session.models.VoiceSession` (see `docs/PHASE65_3_AUDIT.md`
Question 4). It is durable per-user settings, not per-conversation or
per-voice-call state: no TTL, no turn history, no audio bytes. Mutable
(unlike most frozen `ai/`-adjacent dataclasses) because `selected_identity`/
`selected_voice`/`selected_language`/`timezone` each change after
construction, the same "genuinely accumulates state over its lifetime"
reasoning `ai/session/conversation_state.py`'s `ConversationState` and
`voice/session/models.py`'s `VoiceSession` both already use for being
mutable.

`user_id` (never `assistant_id`) is the field any future Memory
integration must key by -- see TASK 6's "Assistant Memory egasi emas.
Memory Userniki." (Assistant is not the memory owner; memory belongs
to the user) and `assistant/conversation_adapter.py`'s
`assistant_memory_scope_key()`.

Deliberately has no `provider` field -- TASK 8's "Provider: Hidden"
requirement is satisfied by this field never existing here at all, not
by hiding it in a UI layer.

`AssistantRuntime` (Phase 65.4, TASK 8) is a genuinely different
resource from `AssistantProfile` above: a live, ephemeral session
record (`session_id`/`started_at`/`updated_at`/`active`/
`conversation_id`) versus durable per-user settings. Not a third
session class alongside `ai.session.conversation_state.ConversationState`
and `voice.session.models.VoiceSession` either -- see
`docs/PHASE65_4_AUDIT.md` Question 1 for why extending
`AssistantManager` with runtime-lifecycle methods (rather than a new
`AssistantRuntimeManager`) is the correct move. `conversation_id` is a
pointer into `ai.session.SessionManager`'s own store, never an
embedded `ConversationState` object -- the same "never carry another
package's object graph" posture `VoiceSession.conversation_session_id`
already established in Phase 65.2.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AssistantProfile:
    assistant_id: str
    user_id: str
    selected_identity: str
    selected_voice: Optional[str] = None
    selected_language: str = "en"
    timezone: str = "UTC"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class AssistantRuntime:
    session_id: str
    assistant_id: str
    started_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    active: bool = True
    conversation_id: Optional[str] = None
