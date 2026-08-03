"""Phase 65.2 TASK 1 — voice/stt/contract.py: STTProviderContract + STTProviderError hierarchy."""

from ai_layer.voice_ai.stt.contract import (
    STTProviderContract,
    STTProviderError,
    STTProviderInvalidResponseError,
    STTProviderTimeoutError,
    STTProviderUnavailableError,
)
from ai_layer.voice_ai.stt.models import STTRequest, STTResult, STTResultStatus


class _FakeSTTProvider(STTProviderContract):
    @property
    def provider_name(self) -> str:
        return "fake"

    def transcribe(self, request: STTRequest) -> STTResult:
        return STTResult(request_id=request.id, status=STTResultStatus.READY, text="ok")


def test_contract_default_validate_is_true():
    provider = _FakeSTTProvider()
    assert provider.validate() is True


def test_contract_default_health_check_delegates_to_validate():
    provider = _FakeSTTProvider()
    assert provider.health_check() == provider.validate()


def test_contract_transcribe_must_be_implemented():
    provider = _FakeSTTProvider()
    request = STTRequest(id="r1", audio=b"AUDIO")
    result = provider.transcribe(request)
    assert result.status == STTResultStatus.READY


def test_stt_provider_contract_cannot_be_instantiated_directly():
    try:
        STTProviderContract()
        assert False, "STTProviderContract is abstract and must not be instantiable"
    except TypeError:
        pass


def test_stt_provider_error_carries_provider_name_and_reason():
    error = STTProviderError("openai", "boom")
    assert error.provider_name == "openai"
    assert error.reason == "boom"
    assert "openai" in str(error)
    assert "boom" in str(error)


def test_stt_provider_error_subclasses_are_stt_provider_errors():
    for cls in (STTProviderTimeoutError, STTProviderUnavailableError, STTProviderInvalidResponseError):
        error = cls("openai", "reason")
        assert isinstance(error, STTProviderError)
