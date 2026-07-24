"""
AI Layer — Provider Registry (Phase 61.0: AI Infrastructure
Foundation, TASK 3; Gemini entry replaced with a real implementation
Phase 61.2: AI Runtime Foundation, TASK 3; OpenAI/Claude/Grok entries
replaced with real implementations Phase 61.5: AI Production
Integration Foundation, TASK 1).

Static catalog of every provider this codebase knows the *shape* of,
same "descriptor + build function" pattern
`ai/capabilities/capability_registry.py` and
`configuration/feature_registry.py` both use. Registering a provider
here does not mean it is selected for use -- `provider_manager.py`
owns the live Preferred/Fallback/Disabled selection state.

`gemini`/`openai`/`claude`/`grok` now point at their real
implementations (`ai.providers.gemini_provider.GeminiProvider`,
`ai.providers.openai_provider.OpenAIProvider`,
`ai.providers.claude_provider.ClaudeProvider`,
`ai.providers.grok_provider.GrokProvider`) instead of placeholder
stubs -- each placeholder class was removed from
`placeholder_providers.py` rather than kept alongside the real one, to
avoid two classes with the same name/conceptual identity coexisting
(CLAUDE.md's "No duplicate logic"). `local_llm` stays placeholder this
phase -- no brief item names it.
"""

from dataclasses import dataclass

from ai.providers.base_provider import BaseAIProvider
from ai.providers.claude_provider import ClaudeProvider
from ai.providers.gemini_provider import GeminiProvider
from ai.providers.grok_provider import GrokProvider
from ai.providers.openai_provider import OpenAIProvider
from ai.providers.placeholder_providers import LocalLLMProvider


@dataclass(frozen=True)
class ProviderDescriptor:
    name: str
    provider: BaseAIProvider
    description: str = ""


def build_provider_registry() -> list:
    """Never raises: every real provider fails closed (health_check() False, no key configured) rather than raising at construction time; the one remaining placeholder is a plain, dependency-free stub."""
    return [
        ProviderDescriptor(
            name="openai", provider=OpenAIProvider(),
            description="Real implementation (Phase 61.5) -- calls the OpenAI chat-completions REST API when OPENAI_API_KEY is configured; health_check() reports False otherwise.",
        ),
        ProviderDescriptor(
            name="gemini", provider=GeminiProvider(),
            description="Real implementation (Phase 61.2) -- calls the Gemini REST API when GEMINI_API_KEY is configured; health_check() reports False otherwise.",
        ),
        ProviderDescriptor(
            name="claude", provider=ClaudeProvider(),
            description="Real implementation (Phase 61.5) -- calls the Anthropic Messages REST API when CLAUDE_API_KEY is configured; health_check() reports False otherwise.",
        ),
        ProviderDescriptor(
            name="grok", provider=GrokProvider(),
            description="Real implementation (Phase 61.5) -- calls the xAI chat-completions REST API when GROK_API_KEY is configured; health_check() reports False otherwise.",
        ),
        ProviderDescriptor(
            name="local_llm", provider=LocalLLMProvider(),
            description="Placeholder -- no local inference wired yet (Phase 61.0 foundation).",
        ),
    ]
