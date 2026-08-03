"""Phase 65.0 TASK 4 — ai_layer/voice_ai/manager.py: VoiceManager. Extended Phase 65.1 TASK 6/7 — adapter registry + per-profile provider selection."""

from ai_layer.voice_ai.manager import VoiceManager
from ai_layer.voice_ai.models import VoiceProvider, VoiceProviderStatus, VoiceProviderType, VoiceRequest, VoiceSettings
from ai_layer.voice_ai.profiles import SENIOR_VOICE, SENIORITA_VOICE
from ai_layer.voice_ai.provider_adapters.local import LocalVoiceProvider
from ai_layer.voice_ai.provider_adapters.openai import OpenAIVoiceProvider
from ai_layer.voice_ai.registry import VoiceProfileRegistry


def _valid_request(**overrides):
    defaults = dict(
        id="r1", profile_name="Senior", provider_type=VoiceProviderType.OPENAI,
        text="hello", settings=VoiceSettings(),
    )
    defaults.update(overrides)
    return VoiceRequest(**defaults)


def test_all_providers_start_disabled():
    manager = VoiceManager()
    for provider_type in VoiceProviderType:
        assert manager.is_provider_enabled(provider_type) is False


def test_get_profile_delegates_to_injected_registry():
    registry = VoiceProfileRegistry()
    registry.register(SENIORITA_VOICE)
    manager = VoiceManager(profile_registry=registry)
    assert manager.get_profile("Seniorita") == SENIORITA_VOICE


def test_register_profile_delegates_to_registry_not_duplicate_storage():
    manager = VoiceManager()
    assert manager.get_profile("Seniorita") is not None  # pre-seeded via default registry
    manager.register_profile(SENIORITA_VOICE)
    assert manager.get_profile("Seniorita") == SENIORITA_VOICE


def test_get_provider_returns_none_for_unregistered_type():
    manager = VoiceManager()
    manager._providers.pop(VoiceProviderType.CUSTOM)
    assert manager.get_provider(VoiceProviderType.CUSTOM) is None


def test_register_provider_starts_disabled():
    manager = VoiceManager()
    new_provider = VoiceProvider(provider_type=VoiceProviderType.CUSTOM, name="custom2")
    manager.register_provider(new_provider)
    assert manager.is_provider_enabled(VoiceProviderType.CUSTOM) is False


def test_set_provider_status_enables_provider():
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    assert manager.is_provider_enabled(VoiceProviderType.OPENAI) is True


def test_set_provider_status_ignores_unknown_provider_type():
    manager = VoiceManager()
    manager._providers.pop(VoiceProviderType.CUSTOM)
    manager.set_provider_status(VoiceProviderType.CUSTOM, VoiceProviderStatus.ENABLED)
    assert manager.is_provider_enabled(VoiceProviderType.CUSTOM) is False


def test_list_providers_returns_all_four():
    manager = VoiceManager()
    assert len(manager.list_providers()) == 4


def test_validate_true_for_enabled_provider_known_profile_nonempty_text():
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    assert manager.validate(_valid_request()) is True


def test_validate_false_when_provider_disabled():
    manager = VoiceManager()
    assert manager.validate(_valid_request()) is False


def test_validate_false_for_unknown_profile():
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    assert manager.validate(_valid_request(profile_name="Unknown")) is False


def test_validate_false_for_empty_text():
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    assert manager.validate(_valid_request(text="")) is False


def test_prepare_mirrors_validate():
    manager = VoiceManager()
    manager.set_provider_status(VoiceProviderType.OPENAI, VoiceProviderStatus.ENABLED)
    request = _valid_request()
    assert manager.prepare(request) is True
    assert manager.validate(request) is True


# --- Adapter registry (Phase 65.1 TASK 6/7) ---

def test_get_adapter_returns_none_when_unregistered():
    manager = VoiceManager()
    assert manager.get_adapter(VoiceProviderType.OPENAI) is None


def test_register_adapter_then_get_adapter_returns_it():
    manager = VoiceManager()
    adapter = OpenAIVoiceProvider()
    manager.register_adapter(VoiceProviderType.OPENAI, adapter)
    assert manager.get_adapter(VoiceProviderType.OPENAI) is adapter


def test_register_adapter_does_not_change_provider_enabled_status():
    manager = VoiceManager()
    manager.register_adapter(VoiceProviderType.OPENAI, OpenAIVoiceProvider())
    assert manager.is_provider_enabled(VoiceProviderType.OPENAI) is False


def test_list_adapters_reflects_registrations():
    manager = VoiceManager()
    assert manager.list_adapters() == []
    manager.register_adapter(VoiceProviderType.OPENAI, OpenAIVoiceProvider())
    manager.register_adapter(VoiceProviderType.LOCAL, LocalVoiceProvider())
    assert set(manager.list_adapters()) == {VoiceProviderType.OPENAI, VoiceProviderType.LOCAL}


# --- Per-profile provider selection (Phase 65.1 TASK 6) ---

def test_provider_for_profile_defaults_to_profile_default_provider():
    manager = VoiceManager()
    assert manager.provider_for_profile("Senior") == SENIOR_VOICE.default_provider


def test_provider_for_profile_unknown_profile_returns_none():
    manager = VoiceManager()
    assert manager.provider_for_profile("Unknown") is None


def test_set_provider_for_profile_overrides_default():
    manager = VoiceManager()
    assert manager.provider_for_profile("Senior") == VoiceProviderType.OPENAI

    manager.set_provider_for_profile("Senior", VoiceProviderType.ELEVENLABS)

    assert manager.provider_for_profile("Senior") == VoiceProviderType.ELEVENLABS


def test_set_provider_for_profile_never_mutates_the_locked_static_profile():
    manager = VoiceManager()
    manager.set_provider_for_profile("Senior", VoiceProviderType.ELEVENLABS)
    assert SENIOR_VOICE.default_provider == VoiceProviderType.OPENAI
