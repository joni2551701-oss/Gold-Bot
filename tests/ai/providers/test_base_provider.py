"""Phase 61.0 TASK 3 — Provider interface tests. No real API call anywhere."""

import pytest

from ai_layer.ai_engine.providers.base_provider import BaseAIProvider, ProviderResult


def test_base_provider_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        BaseAIProvider()


def test_base_provider_requires_every_method_implemented():
    class Incomplete(BaseAIProvider):
        @property
        def name(self):
            return "incomplete"

    with pytest.raises(TypeError):
        Incomplete()


def test_provider_result_is_immutable():
    result = ProviderResult(content="x")
    with pytest.raises(Exception):
        result.content = "y"
