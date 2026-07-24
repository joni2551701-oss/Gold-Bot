"""Phase 65.0 TASK 5 — voice/profiles.py: static profile catalog."""

from voice.profiles import NARRATOR_VOICE, SENIOR_VOICE, SENIORITA_VOICE, build_voice_profile_registry
from voice.models import VoiceProviderType


def test_build_voice_profile_registry_returns_three_profiles():
    profiles = build_voice_profile_registry()
    assert len(profiles) == 3
    assert {p.name for p in profiles} == {"Senior", "Seniorita", "Narrator"}


def test_senior_voice_shape():
    assert SENIOR_VOICE.name == "Senior"
    assert SENIOR_VOICE.default_provider == VoiceProviderType.OPENAI
    assert "en" in SENIOR_VOICE.supported_languages


def test_seniorita_voice_shape():
    assert SENIORITA_VOICE.name == "Seniorita"
    assert SENIORITA_VOICE.display_name == "Seniorita"
    assert SENIORITA_VOICE.default_provider == VoiceProviderType.OPENAI


def test_narrator_voice_shape():
    assert NARRATOR_VOICE.name == "Narrator"
    assert NARRATOR_VOICE.default_provider == VoiceProviderType.LOCAL


def test_seniorita_voice_profile_is_not_an_ai_persona():
    """Phase 63.8 established only SENIOR_TRADING_AI is a registered Persona; VoiceProfile('Seniorita', ...) must not reference or create one."""
    from ai.persona.persona_manager import PersonaManager

    manager = PersonaManager()
    assert manager.get("Seniorita") is None
