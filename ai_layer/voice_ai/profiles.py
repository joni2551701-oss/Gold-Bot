"""
Voice Layer — Voice Profiles (Phase 65.0, TASK 5).

Static catalog, same "module-level constant + build function" pattern
`ai/persona/persona_registry.py` already established (Rule 8 — reuse
the pattern). No audio, no synthesis, no client of any kind (Rule 3)
-- every profile below is metadata only. Consolidated into one file
rather than the brief's literal `profiles/senior.py`/`seniorita.py`/
`narrator.py` layout -- see `docs/PHASE65_0_AUDIT.md`'s own file-layout
resolution.

`SENIORITA_VOICE.name == "Seniorita"` is a free-text voice-profile
identifier only -- it does not create, and is not, an
`ai_layer.personal_ai.persona_manager.persona.Persona`. No such `Persona` exists in this
codebase (only `SENIOR_TRADING_AI` is registered), and creating one is
explicitly out of this phase's scope.
"""

from typing import List

from ai_layer.voice_ai.models import VoiceProfile, VoiceProviderType

SENIOR_VOICE = VoiceProfile(
    name="Senior",
    display_name="Senior Trading AI",
    description="Professional analyst voice -- market updates, weekly reports, trade replays.",
    supported_languages=("en",),
    supported_modes=("MARKET_UPDATE", "WEEKLY_REPORT", "TRADE_REPLAY"),
    default_provider=VoiceProviderType.OPENAI,
)

SENIORITA_VOICE = VoiceProfile(
    name="Seniorita",
    display_name="Seniorita",
    description="Mentor voice -- education, training, beginner guides.",
    supported_languages=("en",),
    supported_modes=("EDUCATION", "TRAINING", "BEGINNER_GUIDE"),
    default_provider=VoiceProviderType.OPENAI,
)

NARRATOR_VOICE = VoiceProfile(
    name="Narrator",
    display_name="Narrator",
    description="Neutral narration voice -- generic content with no persona attached.",
    supported_languages=("en",),
    supported_modes=("GENERAL",),
    default_provider=VoiceProviderType.LOCAL,
)


def build_voice_profile_registry() -> List[VoiceProfile]:
    """Never raises. Three entries this phase (Senior/Seniorita/Narrator) -- a future phase may register more without changing this function's shape."""
    return [SENIOR_VOICE, SENIORITA_VOICE, NARRATOR_VOICE]
