"""Phase 65.2 TASK 1/2 — voice/stt/manager.py: STTManager (adapter registry + single active provider)."""

from ai_layer.voice_ai.stt.manager import STTManager
from ai_layer.voice_ai.stt.models import STTRequest, STTResultStatus
from ai_layer.voice_ai.stt.providers.local import LocalSTTProvider
from ai_layer.voice_ai.stt.providers.openai import OpenAISTTProvider


def _request(**overrides):
    defaults = dict(id="r1", audio=b"AUDIO", language="en")
    defaults.update(overrides)
    return STTRequest(**defaults)


def test_no_adapters_registered_by_default():
    manager = STTManager()
    assert manager.list_adapters() == []
    assert manager.active_provider() is None


def test_register_adapter_then_get_adapter_returns_it():
    manager = STTManager()
    adapter = OpenAISTTProvider()
    manager.register_adapter(adapter)
    assert manager.get_adapter("openai") is adapter
    assert manager.list_adapters() == ["openai"]


def test_get_adapter_unknown_returns_none():
    manager = STTManager()
    assert manager.get_adapter("unknown") is None


def test_set_active_provider_unknown_returns_false():
    manager = STTManager()
    assert manager.set_active_provider("openai") is False
    assert manager.active_provider() is None


def test_set_active_provider_known_returns_true():
    manager = STTManager()
    manager.register_adapter(OpenAISTTProvider())
    assert manager.set_active_provider("openai") is True
    assert manager.active_provider().provider_name == "openai"


def test_transcribe_rejected_when_no_active_provider():
    manager = STTManager()
    result = manager.transcribe(_request())
    assert result.status == STTResultStatus.REJECTED
    assert "no active STT provider" in result.reason


def test_transcribe_delegates_to_active_provider_and_catches_error():
    manager = STTManager()
    manager.register_adapter(LocalSTTProvider())
    manager.set_active_provider("local")
    result = manager.transcribe(_request())
    assert result.status == STTResultStatus.REJECTED
    assert "local" in result.reason


class _FakeResponse:
    status_code = 200

    def json(self):
        return {"text": "gold price today"}


class _FakeSession:
    def post(self, *args, **kwargs):
        return _FakeResponse()


class _FakeSecretsWithKey:
    OPENAI_API_KEY = "sk-test"


def test_transcribe_succeeds_via_registered_adapter():
    manager = STTManager()
    manager.register_adapter(OpenAISTTProvider(session=_FakeSession(), secrets=_FakeSecretsWithKey()))
    manager.set_active_provider("openai")
    result = manager.transcribe(_request())
    assert result.status == STTResultStatus.READY
    assert result.text == "gold price today"
