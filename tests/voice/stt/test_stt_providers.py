"""Phase 65.2 TASK 2 — voice/stt/providers/: openai.py, local.py, custom.py."""

from ai_layer.voice_ai.stt.contract import (
    STTProviderInvalidResponseError,
    STTProviderTimeoutError,
    STTProviderUnavailableError,
)
from ai_layer.voice_ai.stt.models import STTRequest, STTResultStatus
from ai_layer.voice_ai.stt.providers.custom import CustomSTTProvider
from ai_layer.voice_ai.stt.providers.local import LocalSTTProvider
from ai_layer.voice_ai.stt.providers.openai import OpenAISTTProvider


class _FakeSecretsNoKey:
    OPENAI_API_KEY = None


class _FakeSecretsWithKey:
    OPENAI_API_KEY = "sk-test"


class _FakeResponse:
    def __init__(self, status_code=200, json_data=None):
        self.status_code = status_code
        self._json = json_data

    def json(self):
        if self._json is None:
            raise ValueError("no json")
        return self._json


class _FakeSessionOK:
    def post(self, *args, **kwargs):
        return _FakeResponse(json_data={"text": "why did you enter this trade"})


class _FakeSessionEmptyText:
    def post(self, *args, **kwargs):
        return _FakeResponse(json_data={"text": ""})


class _FakeSessionBadShape:
    def post(self, *args, **kwargs):
        return _FakeResponse(json_data={"unexpected": "shape"})


class _FakeSessionServerError:
    def post(self, *args, **kwargs):
        return _FakeResponse(status_code=500)


class _RaisingTimeoutSession:
    def post(self, *args, **kwargs):
        import requests
        raise requests.exceptions.Timeout("timed out")


class _RaisingNetworkErrorSession:
    def post(self, *args, **kwargs):
        import requests
        raise requests.exceptions.ConnectionError("network down")


def _request(**overrides):
    defaults = dict(id="r1", audio=b"AUDIODATA", language="en")
    defaults.update(overrides)
    return STTRequest(**defaults)


# --- OpenAI ---

def test_openai_provider_name():
    assert OpenAISTTProvider(secrets=_FakeSecretsNoKey()).provider_name == "openai"


def test_openai_validate_false_without_key():
    assert OpenAISTTProvider(secrets=_FakeSecretsNoKey()).validate() is False


def test_openai_validate_true_with_key():
    assert OpenAISTTProvider(secrets=_FakeSecretsWithKey()).validate() is True


def test_openai_transcribe_raises_unavailable_without_key():
    provider = OpenAISTTProvider(secrets=_FakeSecretsNoKey())
    try:
        provider.transcribe(_request())
        assert False
    except STTProviderUnavailableError:
        pass


def test_openai_transcribe_returns_ready_result_on_success():
    provider = OpenAISTTProvider(session=_FakeSessionOK(), secrets=_FakeSecretsWithKey())
    result = provider.transcribe(_request())
    assert result.status == STTResultStatus.READY
    assert result.text == "why did you enter this trade"
    assert result.metadata["provider"] == "openai"


def test_openai_transcribe_raises_unavailable_on_http_error():
    provider = OpenAISTTProvider(session=_FakeSessionServerError(), secrets=_FakeSecretsWithKey())
    try:
        provider.transcribe(_request())
        assert False
    except STTProviderUnavailableError:
        pass


def test_openai_transcribe_raises_invalid_response_on_empty_text():
    provider = OpenAISTTProvider(session=_FakeSessionEmptyText(), secrets=_FakeSecretsWithKey())
    try:
        provider.transcribe(_request())
        assert False
    except STTProviderInvalidResponseError:
        pass


def test_openai_transcribe_raises_invalid_response_on_bad_shape():
    provider = OpenAISTTProvider(session=_FakeSessionBadShape(), secrets=_FakeSecretsWithKey())
    try:
        provider.transcribe(_request())
        assert False
    except STTProviderInvalidResponseError:
        pass


def test_openai_transcribe_raises_timeout_error():
    provider = OpenAISTTProvider(session=_RaisingTimeoutSession(), secrets=_FakeSecretsWithKey())
    try:
        provider.transcribe(_request())
        assert False
    except STTProviderTimeoutError:
        pass


def test_openai_transcribe_raises_unavailable_on_network_error():
    provider = OpenAISTTProvider(session=_RaisingNetworkErrorSession(), secrets=_FakeSecretsWithKey())
    try:
        provider.transcribe(_request())
        assert False
    except STTProviderUnavailableError:
        pass


def test_openai_stt_never_leaks_api_key_in_exception_message():
    provider = OpenAISTTProvider(session=_FakeSessionServerError(), secrets=_FakeSecretsWithKey())
    try:
        provider.transcribe(_request())
    except STTProviderUnavailableError as e:
        assert "sk-test" not in str(e)


# --- Local / Custom skeletons ---

def test_local_provider_name_and_validate_false():
    provider = LocalSTTProvider()
    assert provider.provider_name == "local"
    assert provider.validate() is False


def test_local_transcribe_raises_unavailable():
    provider = LocalSTTProvider()
    try:
        provider.transcribe(_request())
        assert False
    except STTProviderUnavailableError:
        pass


def test_custom_provider_name_and_validate_false():
    provider = CustomSTTProvider()
    assert provider.provider_name == "custom"
    assert provider.validate() is False


def test_custom_transcribe_raises_unavailable():
    provider = CustomSTTProvider()
    try:
        provider.transcribe(_request())
        assert False
    except STTProviderUnavailableError:
        pass
