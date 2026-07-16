"""Phase 61.0 TASK 3 — every placeholder provider stubs every method, no real API call."""

import pytest

from ai.providers.placeholder_providers import (
    ClaudeProvider, GeminiProvider, GrokProvider, LocalLLMProvider, OpenAIProvider,
)

ALL_PROVIDERS = [OpenAIProvider, GeminiProvider, ClaudeProvider, GrokProvider, LocalLLMProvider]


@pytest.mark.parametrize("provider_cls", ALL_PROVIDERS)
def test_provider_has_a_stable_name(provider_cls):
    provider = provider_cls()
    assert isinstance(provider.name, str) and provider.name


@pytest.mark.parametrize("provider_cls", ALL_PROVIDERS)
@pytest.mark.parametrize("method", ["analyze", "chat", "explain", "image", "voice"])
def test_provider_method_returns_placeholder_result(provider_cls, method):
    provider = provider_cls()
    result = getattr(provider, method)("prompt")
    assert result.metadata["placeholder"] is True
    assert provider.name in result.content


@pytest.mark.parametrize("provider_cls", ALL_PROVIDERS)
def test_provider_vision_accepts_optional_image_ref(provider_cls):
    provider = provider_cls()
    result = provider.vision("prompt")
    assert result.metadata["placeholder"] is True
    result_with_ref = provider.vision("prompt", image_ref="ref")
    assert result_with_ref.metadata["placeholder"] is True
