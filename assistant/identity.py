"""
Assistant Layer — Assistant Identity Model (Phase 65.3: Personal AI
Assistant Foundation, TASK 1).

Pure presentation metadata -- no behavior, no prompt, no AI call.
`AssistantIdentity` is deliberately NOT `ai.persona.persona.Persona`:
Persona is "AI qanday fikrlaydi" (how the AI thinks -- tone,
disclaimer, system_identity for a future prompt builder);
AssistantIdentity is "AI qanday ko'rinadi/tanishtiriladi" (how the
assistant presents itself to a user -- display name, description,
default voice/avatar, language support). Rule 3 (Persona Protection)
requires these never be mixed; this module never imports
`ai/persona/` to keep that separation structural, not just
conventional -- the same posture `voice/profiles.py`'s own
`SENIORITA_VOICE` already established for Voice Profiles.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class AssistantIdentity:
    """
    name: the identity's stable key (e.g. "Senior", "Seniorita") --
        coincidentally matches `voice.profiles.SENIOR_VOICE.name`/
        `SENIORITA_VOICE.name` by convention only, never by import.
    display_name: human-facing label.
    description: one-line description of this identity's character.
    default_voice: a `voice.profiles` profile *name* string this
        identity resolves to when no explicit voice override is
        selected ("Voice: Auto" per TASK 8) -- a free-text pointer,
        never a `voice.models.VoiceProfile` object.
    default_avatar: a stable identifier string only (e.g.
        "senior_avatar_v1") -- no image/video/render exists or is
        referenced this phase (Director Note 4).
    supported_languages: language codes this identity is available in.
    """
    name: str
    display_name: str
    description: str
    default_voice: str
    default_avatar: str
    supported_languages: Tuple[str, ...] = ("en",)
