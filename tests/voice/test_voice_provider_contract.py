"""Phase 65.1 TASK 1 — ai_layer/voice_ai/provider_contract.py: VoiceProviderContract + VoiceProviderError hierarchy."""

from ai_layer.voice_ai.models import VoiceRequest, VoiceResult, VoiceResultStatus, VoiceProviderType
from ai_layer.voice_ai.provider_contract import (
    VoiceProviderContract,
    VoiceProviderError,
    VoiceProviderInvalidResponseError,
    VoiceProviderTimeoutError,
    VoiceProviderUnavailableError,
)


class _FakeProvider(VoiceProviderContract):
    @property
    def provider_name(self) -> str:
        return "fake"

    def generate_audio(self, request: VoiceRequest) -> VoiceResult:
        return VoiceResult(request_id=request.id, status=VoiceResultStatus.READY)


def test_contract_default_validate_is_true():
    provider = _FakeProvider()
    assert provider.validate() is True


def test_contract_default_health_check_delegates_to_validate():
    provider = _FakeProvider()
    assert provider.health_check() == provider.validate()


def test_contract_generate_audio_must_be_implemented():
    provider = _FakeProvider()
    request = VoiceRequest(id="r1", profile_name="Senior", provider_type=VoiceProviderType.OPENAI, text="hi")
    result = provider.generate_audio(request)
    assert result.status == VoiceResultStatus.READY


def test_voice_provider_contract_cannot_be_instantiated_directly():
    try:
        VoiceProviderContract()
        assert False, "VoiceProviderContract is abstract and must not be instantiable"
    except TypeError:
        pass


def test_voice_provider_error_carries_provider_name_and_reason():
    error = VoiceProviderError("openai", "boom")
    assert error.provider_name == "openai"
    assert error.reason == "boom"
    assert "openai" in str(error)
    assert "boom" in str(error)


def test_voice_provider_error_subclasses_are_voice_provider_errors():
    for cls in (VoiceProviderTimeoutError, VoiceProviderUnavailableError, VoiceProviderInvalidResponseError):
        error = cls("openai", "reason")
        assert isinstance(error, VoiceProviderError)
