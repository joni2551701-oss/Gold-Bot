"""Phase 65.1 TASK 2-5 — voice/provider_adapters/: openai.py, elevenlabs.py, local.py, custom.py."""

from voice.models import VoiceProviderType, VoiceRequest, VoiceResultStatus
from voice.provider_adapters.custom import CustomVoiceProvider
from voice.provider_adapters.elevenlabs import ElevenLabsVoiceProvider
from voice.provider_adapters.local import LocalVoiceProvider
from voice.provider_adapters.openai import OpenAIVoiceProvider
from voice.provider_contract import (
    VoiceProviderInvalidResponseError,
    VoiceProviderTimeoutError,
    VoiceProviderUnavailableError,
)


class _FakeSecretsNoKeys:
    OPENAI_API_KEY = None
    ELEVENLABS_API_KEY = None


class _FakeSecretsWithKeys:
    OPENAI_API_KEY = "sk-test"
    ELEVENLABS_API_KEY = "el-test"


class _FakeResponse:
    def __init__(self, status_code=200, content=b"AUDIO", headers=None):
        self.status_code = status_code
        self.content = content
        self.headers = headers or {"Content-Type": "audio/mpeg"}


class _FakeSessionOK:
    def post(self, *args, **kwargs):
        return _FakeResponse()


class _FakeSessionEmptyBody:
    def post(self, *args, **kwargs):
        return _FakeResponse(content=b"")


class _FakeSessionServerError:
    def post(self, *args, **kwargs):
        return _FakeResponse(status_code=500, content=b"")


class _RaisingTimeoutSession:
    def post(self, *args, **kwargs):
        import requests
        raise requests.exceptions.Timeout("timed out")


class _RaisingNetworkErrorSession:
    def post(self, *args, **kwargs):
        import requests
        raise requests.exceptions.ConnectionError("network down")


def _request(**overrides):
    defaults = dict(id="r1", profile_name="Senior", provider_type=VoiceProviderType.OPENAI, text="hello world")
    defaults.update(overrides)
    return VoiceRequest(**defaults)


# --- OpenAI ---

def test_openai_provider_name():
    assert OpenAIVoiceProvider(secrets=_FakeSecretsNoKeys()).provider_name == "openai"


def test_openai_validate_false_without_key():
    assert OpenAIVoiceProvider(secrets=_FakeSecretsNoKeys()).validate() is False


def test_openai_validate_true_with_key():
    assert OpenAIVoiceProvider(secrets=_FakeSecretsWithKeys()).validate() is True


def test_openai_generate_audio_raises_unavailable_without_key():
    provider = OpenAIVoiceProvider(secrets=_FakeSecretsNoKeys())
    try:
        provider.generate_audio(_request())
        assert False
    except VoiceProviderUnavailableError:
        pass


def test_openai_generate_audio_returns_ready_result_on_success():
    provider = OpenAIVoiceProvider(session=_FakeSessionOK(), secrets=_FakeSecretsWithKeys())
    result = provider.generate_audio(_request())
    assert result.status == VoiceResultStatus.READY
    assert result.metadata["provider"] == "openai"
    assert result.metadata["byte_length"] == 5


def test_openai_generate_audio_raises_unavailable_on_http_error():
    provider = OpenAIVoiceProvider(session=_FakeSessionServerError(), secrets=_FakeSecretsWithKeys())
    try:
        provider.generate_audio(_request())
        assert False
    except VoiceProviderUnavailableError:
        pass


def test_openai_generate_audio_raises_invalid_response_on_empty_body():
    provider = OpenAIVoiceProvider(session=_FakeSessionEmptyBody(), secrets=_FakeSecretsWithKeys())
    try:
        provider.generate_audio(_request())
        assert False
    except VoiceProviderInvalidResponseError:
        pass


def test_openai_generate_audio_raises_timeout_error():
    provider = OpenAIVoiceProvider(session=_RaisingTimeoutSession(), secrets=_FakeSecretsWithKeys())
    try:
        provider.generate_audio(_request())
        assert False
    except VoiceProviderTimeoutError:
        pass


def test_openai_generate_audio_raises_unavailable_on_network_error():
    provider = OpenAIVoiceProvider(session=_RaisingNetworkErrorSession(), secrets=_FakeSecretsWithKeys())
    try:
        provider.generate_audio(_request())
        assert False
    except VoiceProviderUnavailableError:
        pass


def test_openai_never_leaks_api_key_in_exception_message():
    provider = OpenAIVoiceProvider(session=_FakeSessionServerError(), secrets=_FakeSecretsWithKeys())
    try:
        provider.generate_audio(_request())
    except VoiceProviderUnavailableError as e:
        assert "sk-test" not in str(e)


# --- ElevenLabs ---

def test_elevenlabs_provider_name():
    assert ElevenLabsVoiceProvider(secrets=_FakeSecretsNoKeys()).provider_name == "elevenlabs"


def test_elevenlabs_validate_false_without_key():
    assert ElevenLabsVoiceProvider(secrets=_FakeSecretsNoKeys()).validate() is False


def test_elevenlabs_validate_true_with_key():
    assert ElevenLabsVoiceProvider(secrets=_FakeSecretsWithKeys()).validate() is True


def test_elevenlabs_generate_audio_raises_unavailable_without_key():
    provider = ElevenLabsVoiceProvider(secrets=_FakeSecretsNoKeys())
    try:
        provider.generate_audio(_request(provider_type=VoiceProviderType.ELEVENLABS))
        assert False
    except VoiceProviderUnavailableError:
        pass


def test_elevenlabs_generate_audio_returns_ready_result_on_success():
    provider = ElevenLabsVoiceProvider(session=_FakeSessionOK(), secrets=_FakeSecretsWithKeys())
    result = provider.generate_audio(_request(provider_type=VoiceProviderType.ELEVENLABS))
    assert result.status == VoiceResultStatus.READY
    assert result.metadata["provider"] == "elevenlabs"
    assert "voice_id" in result.metadata


def test_elevenlabs_generate_audio_raises_invalid_response_on_empty_body():
    provider = ElevenLabsVoiceProvider(session=_FakeSessionEmptyBody(), secrets=_FakeSecretsWithKeys())
    try:
        provider.generate_audio(_request(provider_type=VoiceProviderType.ELEVENLABS))
        assert False
    except VoiceProviderInvalidResponseError:
        pass


def test_elevenlabs_accepts_a_custom_voice_id():
    provider = ElevenLabsVoiceProvider(session=_FakeSessionOK(), secrets=_FakeSecretsWithKeys(), voice_id="custom-voice-id")
    result = provider.generate_audio(_request(provider_type=VoiceProviderType.ELEVENLABS))
    assert result.metadata["voice_id"] == "custom-voice-id"


# --- Local / Custom skeletons ---

def test_local_provider_name_and_validate_false():
    provider = LocalVoiceProvider()
    assert provider.provider_name == "local"
    assert provider.validate() is False


def test_local_generate_audio_raises_unavailable():
    provider = LocalVoiceProvider()
    try:
        provider.generate_audio(_request(provider_type=VoiceProviderType.LOCAL))
        assert False
    except VoiceProviderUnavailableError:
        pass


def test_custom_provider_name_and_validate_false():
    provider = CustomVoiceProvider()
    assert provider.provider_name == "custom"
    assert provider.validate() is False


def test_custom_generate_audio_raises_unavailable():
    provider = CustomVoiceProvider()
    try:
        provider.generate_audio(_request(provider_type=VoiceProviderType.CUSTOM))
        assert False
    except VoiceProviderUnavailableError:
        pass
