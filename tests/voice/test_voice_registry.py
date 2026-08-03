"""Phase 65.0 TASK 3 — ai_layer/voice_ai/registry.py: VoiceProfileRegistry."""

from ai_layer.voice_ai.models import VoiceProfile
from ai_layer.voice_ai.profiles import NARRATOR_VOICE, SENIOR_VOICE, SENIORITA_VOICE
from ai_layer.voice_ai.registry import VoiceProfileRegistry


def test_registry_defaults_seeded_with_three_profiles():
    registry = VoiceProfileRegistry()
    assert len(registry.list_all()) == 3
    assert registry.exists("Senior") is True
    assert registry.exists("Seniorita") is True
    assert registry.exists("Narrator") is True


def test_registry_default_profile_is_senior():
    registry = VoiceProfileRegistry()
    assert registry.default() == SENIOR_VOICE


def test_registry_get_returns_the_matching_profile():
    registry = VoiceProfileRegistry()
    assert registry.get("Narrator") == NARRATOR_VOICE


def test_registry_get_unknown_name_returns_none():
    registry = VoiceProfileRegistry()
    assert registry.get("Unknown") is None


def test_registry_exists_false_for_unknown_name():
    registry = VoiceProfileRegistry()
    assert registry.exists("Unknown") is False


def test_registry_register_adds_a_new_profile():
    registry = VoiceProfileRegistry(profiles=[SENIOR_VOICE])
    assert registry.exists("Seniorita") is False

    registry.register(SENIORITA_VOICE)

    assert registry.exists("Seniorita") is True
    assert registry.get("Seniorita") == SENIORITA_VOICE


def test_registry_register_overwrites_existing_name():
    registry = VoiceProfileRegistry()
    replacement = VoiceProfile(name="Senior", display_name="Replaced Senior")

    registry.register(replacement)

    assert registry.get("Senior") == replacement


def test_registry_custom_default_name():
    registry = VoiceProfileRegistry(default_name="Narrator")
    assert registry.default() == NARRATOR_VOICE


def test_registry_default_returns_none_when_configured_default_missing():
    registry = VoiceProfileRegistry(profiles=[SENIOR_VOICE], default_name="Missing")
    assert registry.default() is None
