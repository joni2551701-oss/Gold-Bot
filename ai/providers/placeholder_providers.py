"""
AI Layer — Placeholder Providers (Phase 61.0: AI Infrastructure
Foundation, TASK 3; Gemini placeholder removed Phase 61.2: AI Runtime
Foundation, TASK 3; OpenAI/Claude/Grok placeholders removed Phase
61.5: AI Production Integration Foundation, TASK 1).

One remaining stub `BaseAIProvider` implementation (Local LLM). It
makes no real network call -- its methods return a fixed
`ProviderResult` whose `content` says so explicitly.

OpenAI/Claude/Grok's placeholders were removed from this file (Phase
61.5) once `ai/providers/openai_provider.py`/`claude_provider.py`/
`grok_provider.py`'s real implementations replaced them in
`provider_registry.py` -- keeping both would have meant two classes
with the same conceptual identity, one live one dead (CLAUDE.md's "No
duplicate logic"), same precedent as Gemini's Phase 61.2 removal.
`core/secrets.py` still carries `LOCAL_LLM_CONFIG` (Phase 61.2 TASK 2)
-- this placeholder deliberately still does not read it; a future
phase replaces it with a real implementation the same way the other
four were.
"""

from ai.providers.base_provider import BaseAIProvider, ProviderResult


class _StubProviderMixin:
    """Shared stub behavior: every method returns the same "not implemented" shape, tagged with this provider's own name."""

    _NAME = "stub"

    @property
    def name(self) -> str:
        return self._NAME

    def _stub(self, method: str) -> ProviderResult:
        return ProviderResult(
            content=f"[{self._NAME}] placeholder response -- {method}() has no real API call yet.",
            metadata={"provider": self._NAME, "placeholder": True},
        )

    def analyze(self, prompt: str) -> ProviderResult:
        return self._stub("analyze")

    def chat(self, prompt: str) -> ProviderResult:
        return self._stub("chat")

    def explain(self, prompt: str) -> ProviderResult:
        return self._stub("explain")

    def vision(self, prompt: str, image_ref=None) -> ProviderResult:
        return self._stub("vision")

    def image(self, prompt: str) -> ProviderResult:
        return self._stub("image")

    def voice(self, prompt: str) -> ProviderResult:
        return self._stub("voice")


class LocalLLMProvider(_StubProviderMixin, BaseAIProvider):
    _NAME = "local_llm"
