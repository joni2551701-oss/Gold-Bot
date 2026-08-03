"""Phase 65.0 TASK 2 — ai_layer/voice_ai/models.py: dataclasses + enums."""

from ai_layer.voice_ai.models import (
    VoiceProvider,
    VoiceProviderStatus,
    VoiceProviderType,
    VoiceProfile,
    VoiceRequest,
    VoiceResult,
    VoiceResultStatus,
    VoiceSettings,
)


def test_voice_provider_type_has_four_values():
    assert {t.value for t in VoiceProviderType} == {"OPENAI", "ELEVENLABS", "LOCAL", "CUSTOM"}


def test_voice_provider_status_has_two_values():
    assert {s.value for s in VoiceProviderStatus} == {"ENABLED", "DISABLED"}


def test_voice_result_status_has_three_values():
    assert {s.value for s in VoiceResultStatus} == {"PENDING", "READY", "REJECTED"}


def test_voice_provider_defaults():
    provider = VoiceProvider(provider_type=VoiceProviderType.LOCAL, name="local")
    assert provider.supports_stream is False
    assert provider.supports_clone is False
    assert provider.supports_emotion is False
    assert provider.supports_ssml is False
    assert provider.status == VoiceProviderStatus.DISABLED


def test_voice_provider_is_frozen():
    provider = VoiceProvider(provider_type=VoiceProviderType.LOCAL, name="local")
    try:
        provider.name = "mutated"
        assert False, "VoiceProvider should be frozen"
    except AttributeError:
        pass


def test_voice_profile_defaults():
    profile = VoiceProfile(name="Narrator", display_name="Narrator")
    assert profile.description == ""
    assert profile.supported_languages == ()
    assert profile.supported_modes == ()
    assert profile.default_provider is None


def test_voice_profile_is_frozen():
    profile = VoiceProfile(name="Narrator", display_name="Narrator")
    try:
        profile.name = "mutated"
        assert False, "VoiceProfile should be frozen"
    except AttributeError:
        pass


def test_voice_settings_defaults():
    settings = VoiceSettings()
    assert settings.language == "en"
    assert settings.speed == 1.0
    assert settings.pitch == 1.0


def test_voice_request_defaults():
    request = VoiceRequest(id="r1", profile_name="Senior", provider_type=VoiceProviderType.OPENAI, text="hi")
    assert request.settings == VoiceSettings()
    assert request.requested_at == ""


def test_voice_request_is_frozen():
    request = VoiceRequest(id="r1", profile_name="Senior", provider_type=VoiceProviderType.OPENAI, text="hi")
    try:
        request.text = "mutated"
        assert False, "VoiceRequest should be frozen"
    except AttributeError:
        pass


def test_voice_result_defaults():
    result = VoiceResult(request_id="r1", status=VoiceResultStatus.PENDING)
    assert result.reason == ""
    assert result.generated_at == ""


def test_voice_result_is_frozen():
    result = VoiceResult(request_id="r1", status=VoiceResultStatus.PENDING)
    try:
        result.status = VoiceResultStatus.READY
        assert False, "VoiceResult should be frozen"
    except AttributeError:
        pass
