"""Phase 61.5 TASK 1 — Real OpenAI Provider. No real network call anywhere -- every test injects a fake session."""

import requests
import pytest

from ai.capabilities.capability import Capability
from ai.providers.openai_provider import OpenAIProvider
from ai.providers.runtime_errors import (
    ProviderInvalidResponseError,
    ProviderRateLimitError,
    ProviderTimeoutError,
    ProviderUnavailableError,
)


class _FakeSecrets:
    def __init__(self, api_key=None):
        self._api_key = api_key

    @property
    def OPENAI_API_KEY(self):
        if self._api_key is None:
            return None
        return self._api_key


class _FakeResponse:
    def __init__(self, status_code=200, payload=None):
        self.status_code = status_code
        self._payload = payload or {}

    def json(self):
        return self._payload


class _FakeSession:
    """Records every post() call so a test can assert what was sent (and, crucially, what was NOT sent -- the key never in the URL)."""

    def __init__(self, response=None, exception=None):
        self._response = response
        self._exception = exception
        self.calls = []

    def post(self, url, headers=None, json=None, timeout=None):
        self.calls.append({"url": url, "headers": headers, "json": json, "timeout": timeout})
        if self._exception is not None:
            raise self._exception
        return self._response


def _openai_success_payload(text="Gold is in an uptrend."):
    return {"choices": [{"message": {"content": text}}]}


def test_health_check_false_without_api_key():
    provider = OpenAIProvider(secrets=_FakeSecrets(api_key=None))
    assert provider.health_check() is False


def test_health_check_true_with_api_key():
    provider = OpenAIProvider(secrets=_FakeSecrets(api_key="fake-key-123"))
    assert provider.health_check() is True


def test_name_is_openai():
    provider = OpenAIProvider(secrets=_FakeSecrets(api_key="fake-key"))
    assert provider.name == "openai"


def test_capabilities_inherited_from_provider_capabilities_matrix():
    provider = OpenAIProvider(secrets=_FakeSecrets(api_key="fake-key"))
    caps = provider.capabilities()
    assert Capability.CHAT in caps
    assert Capability.ANALYSIS in caps


def test_analyze_returns_provider_result_on_success():
    session = _FakeSession(response=_FakeResponse(200, _openai_success_payload("uptrend")))
    provider = OpenAIProvider(session=session, secrets=_FakeSecrets(api_key="fake-key"))

    result = provider.analyze("what is the gold trend?")

    assert result.content == "uptrend"
    assert result.metadata["provider"] == "openai"
    assert len(session.calls) == 1


def test_chat_and_explain_also_use_the_real_call_path():
    session = _FakeSession(response=_FakeResponse(200, _openai_success_payload("hello")))
    provider = OpenAIProvider(session=session, secrets=_FakeSecrets(api_key="fake-key"))

    provider.chat("hi")
    provider.explain("why?")

    assert len(session.calls) == 2


def test_api_key_travels_only_in_the_header_never_in_the_url():
    session = _FakeSession(response=_FakeResponse(200, _openai_success_payload()))
    provider = OpenAIProvider(session=session, secrets=_FakeSecrets(api_key="super-secret-key"))

    provider.analyze("prompt")

    call = session.calls[0]
    assert "super-secret-key" not in call["url"]
    assert call["headers"]["Authorization"] == "Bearer super-secret-key"


def test_missing_api_key_raises_provider_unavailable_error():
    provider = OpenAIProvider(secrets=_FakeSecrets(api_key=None))
    with pytest.raises(ProviderUnavailableError):
        provider.analyze("prompt")


def test_missing_api_key_error_message_does_not_leak_a_key():
    provider = OpenAIProvider(secrets=_FakeSecrets(api_key=None))
    try:
        provider.analyze("prompt")
    except ProviderUnavailableError as e:
        assert "OPENAI_API_KEY not configured" in str(e)


def test_timeout_raises_provider_timeout_error():
    session = _FakeSession(exception=requests.exceptions.Timeout())
    provider = OpenAIProvider(session=session, secrets=_FakeSecrets(api_key="fake-key"))
    with pytest.raises(ProviderTimeoutError):
        provider.analyze("prompt")


def test_connection_error_raises_provider_unavailable_error():
    session = _FakeSession(exception=requests.exceptions.ConnectionError())
    provider = OpenAIProvider(session=session, secrets=_FakeSecrets(api_key="fake-key"))
    with pytest.raises(ProviderUnavailableError):
        provider.analyze("prompt")


def test_http_429_raises_provider_rate_limit_error():
    session = _FakeSession(response=_FakeResponse(429, {}))
    provider = OpenAIProvider(session=session, secrets=_FakeSecrets(api_key="fake-key"))
    with pytest.raises(ProviderRateLimitError):
        provider.analyze("prompt")


def test_http_500_raises_provider_unavailable_error():
    session = _FakeSession(response=_FakeResponse(500, {}))
    provider = OpenAIProvider(session=session, secrets=_FakeSecrets(api_key="fake-key"))
    with pytest.raises(ProviderUnavailableError):
        provider.analyze("prompt")


def test_malformed_response_raises_provider_invalid_response_error():
    session = _FakeSession(response=_FakeResponse(200, {"unexpected": "shape"}))
    provider = OpenAIProvider(session=session, secrets=_FakeSecrets(api_key="fake-key"))
    with pytest.raises(ProviderInvalidResponseError):
        provider.analyze("prompt")


def test_vision_raises_not_implemented_error():
    provider = OpenAIProvider(secrets=_FakeSecrets(api_key="fake-key"))
    with pytest.raises(NotImplementedError):
        provider.vision("prompt")


def test_image_raises_not_implemented_error():
    provider = OpenAIProvider(secrets=_FakeSecrets(api_key="fake-key"))
    with pytest.raises(NotImplementedError):
        provider.image("prompt")


def test_voice_raises_not_implemented_error():
    provider = OpenAIProvider(secrets=_FakeSecrets(api_key="fake-key"))
    with pytest.raises(NotImplementedError):
        provider.voice("prompt")


def test_constructed_without_secrets_never_crashes_even_if_env_var_unset(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    provider = OpenAIProvider()
    assert provider.health_check() is False
