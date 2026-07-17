"""Phase 61.0 TASK 3 — every placeholder provider stubs every method, no real API call. Gemini moved to tests/ai/providers/test_gemini_provider.py (Phase 61.2, real implementation, no longer a placeholder). OpenAI/Claude/Grok moved to their own real-implementation test files (Phase 61.5 TASK 1) -- LocalLLM is the one placeholder remaining."""

import pytest

from ai.providers.placeholder_providers import LocalLLMProvider

ALL_PROVIDERS = [LocalLLMProvider]


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
