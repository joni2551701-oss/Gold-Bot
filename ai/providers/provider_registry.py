"""
AI Layer — Provider Registry (Phase 61.0: AI Infrastructure
Foundation, TASK 3; Gemini entry replaced with a real implementation
Phase 61.2: AI Runtime Foundation, TASK 3).

Static catalog of every provider this codebase knows the *shape* of,
same "descriptor + build function" pattern
`ai/capabilities/capability_registry.py` and
`configuration/feature_registry.py` both use. Registering a provider
here does not mean it is selected for use -- `provider_manager.py`
owns the live Preferred/Fallback/Disabled selection state.

`gemini` now points at `ai.providers.gemini_provider.GeminiProvider`
(a real implementation) instead of the placeholder stub -- the
placeholder `GeminiProvider` class was removed from
`placeholder_providers.py` rather than kept alongside the real one, to
avoid two classes with the same name/conceptual identity coexisting
(CLAUDE.md's "No duplicate logic"). `openai`/`claude`/`grok`/
`local_llm` stay placeholder this phase, per Phase 61.2's own
"Boshlanish: Gemini Provider" scoping.
"""

from dataclasses import dataclass

from ai.providers.base_provider import BaseAIProvider
from ai.providers.gemini_provider import GeminiProvider
from ai.providers.placeholder_providers import (
    ClaudeProvider,
    GrokProvider,
    LocalLLMProvider,
    OpenAIProvider,
)


@dataclass(frozen=True)
class ProviderDescriptor:
    name: str
    provider: BaseAIProvider
    description: str = ""


def build_provider_registry() -> list:
    """Never raises: every placeholder provider is a plain, dependency-free stub constructed in-process."""
    return [
        ProviderDescriptor(
            name="openai", provider=OpenAIProvider(),
            description="Placeholder -- no real OpenAI API call (Phase 61.0 foundation).",
        ),
        ProviderDescriptor(
            name="gemini", provider=GeminiProvider(),
            description="Real implementation (Phase 61.2) -- calls the Gemini REST API when GEMINI_API_KEY is configured; health_check() reports False otherwise.",
        ),
        ProviderDescriptor(
            name="claude", provider=ClaudeProvider(),
            description="Placeholder -- no real Claude API call (Phase 61.0 foundation).",
        ),
        ProviderDescriptor(
            name="grok", provider=GrokProvider(),
            description="Placeholder -- no real Grok API call (Phase 61.0 foundation).",
        ),
        ProviderDescriptor(
            name="local_llm", provider=LocalLLMProvider(),
            description="Placeholder -- no local inference wired yet (Phase 61.0 foundation).",
        ),
    ]
