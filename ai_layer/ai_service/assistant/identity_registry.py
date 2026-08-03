"""
Assistant Layer — Identity Registry (Phase 65.3: Personal AI Assistant
Foundation, TASK 1/3).

Static catalog, same "module-level constant + build function" pattern
`ai/persona/persona_registry.py` and `ai_layer/voice_ai/profiles.py` already
established (Article 7's Reuse Principle -- reuse the pattern). Two
entries only, per the brief's own Rule 4 ("Faqat: Senior, Seniorita" --
Narrator/Mentor/Coach are named as possible future additions, not
built this phase).
"""

from typing import List

from ai_layer.ai_service.assistant.identity import AssistantIdentity

SENIOR_IDENTITY = AssistantIdentity(
    name="Senior",
    display_name="Senior Trading AI",
    description="Professional analyst identity -- calm, data-driven market conversation.",
    default_voice="Senior",
    default_avatar="senior_avatar_v1",
    supported_languages=("en",),
)

SENIORITA_IDENTITY = AssistantIdentity(
    name="Seniorita",
    display_name="Seniorita",
    description="Mentor identity -- education, training, beginner-friendly conversation.",
    default_voice="Seniorita",
    default_avatar="seniorita_avatar_v1",
    supported_languages=("en",),
)


def build_identity_registry() -> List[AssistantIdentity]:
    """Never raises. Two entries this phase -- a future phase may register more (Narrator/Mentor/Coach) without changing this function's shape."""
    return [SENIOR_IDENTITY, SENIORITA_IDENTITY]
