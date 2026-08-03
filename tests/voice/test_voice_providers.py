"""Phase 65.0 TASK 6 — ai_layer/voice_ai/providers.py: static provider catalog."""

from ai_layer.voice_ai.providers import build_voice_provider_registry
from ai_layer.voice_ai.models import VoiceProviderType


def test_build_voice_provider_registry_returns_four_providers():
    providers = build_voice_provider_registry()
    assert len(providers) == 4
    assert {p.provider_type for p in providers} == {
        VoiceProviderType.OPENAI, VoiceProviderType.ELEVENLABS,
        VoiceProviderType.LOCAL, VoiceProviderType.CUSTOM,
    }


def test_openai_descriptor_supports_stream_and_ssml_only():
    providers = {p.provider_type: p for p in build_voice_provider_registry()}
    openai = providers[VoiceProviderType.OPENAI]
    assert openai.supports_stream is True
    assert openai.supports_ssml is True
    assert openai.supports_clone is False
    assert openai.supports_emotion is False


def test_elevenlabs_descriptor_supports_everything():
    providers = {p.provider_type: p for p in build_voice_provider_registry()}
    elevenlabs = providers[VoiceProviderType.ELEVENLABS]
    assert elevenlabs.supports_stream is True
    assert elevenlabs.supports_clone is True
    assert elevenlabs.supports_emotion is True
    assert elevenlabs.supports_ssml is True


def test_local_and_custom_descriptors_support_nothing():
    providers = {p.provider_type: p for p in build_voice_provider_registry()}
    for provider_type in (VoiceProviderType.LOCAL, VoiceProviderType.CUSTOM):
        descriptor = providers[provider_type]
        assert descriptor.supports_stream is False
        assert descriptor.supports_clone is False
        assert descriptor.supports_emotion is False
        assert descriptor.supports_ssml is False
