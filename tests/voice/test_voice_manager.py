"""Phase 65.0 TASK 4 — voice/manager.py: VoiceManager."""

from voice.manager import VoiceManager
from voice.models import VoiceProvider, VoiceProviderStatus, VoiceProviderType, VoiceRequest, VoiceSettings
from voice.profiles import SENIORITA_VOICE
from voice.registry import VoiceProfileRegistry


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
