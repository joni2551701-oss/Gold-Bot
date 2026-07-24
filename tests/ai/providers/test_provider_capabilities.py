"""Phase 61.1 TASK 3 — Provider Capability Matrix."""

from ai.capabilities.capability import Capability
from ai.providers.provider_capabilities import PROVIDER_CAPABILITIES, capabilities_of, supports


def test_gemini_supports_chat_vision_document_per_worked_example():
    assert supports("gemini", Capability.CHAT)
    assert supports("gemini", Capability.VISION)
    assert supports("gemini", Capability.DOCUMENT)


def test_openai_supports_chat_image_voice_per_worked_example():
    assert supports("openai", Capability.CHAT)
    assert supports("openai", Capability.IMAGE)
    assert supports("openai", Capability.VOICE)


def test_grok_supports_only_chat():
    assert capabilities_of("grok") == frozenset({Capability.CHAT})


def test_unregistered_provider_supports_nothing():
    assert supports("unknown_provider", Capability.CHAT) is False
    assert capabilities_of("unknown_provider") == frozenset()


def test_every_declared_provider_supports_chat():
    for provider_name in PROVIDER_CAPABILITIES:
        assert supports(provider_name, Capability.CHAT)


def test_matrix_covers_the_five_known_providers():
    assert set(PROVIDER_CAPABILITIES.keys()) == {"openai", "gemini", "claude", "grok", "local_llm"}
