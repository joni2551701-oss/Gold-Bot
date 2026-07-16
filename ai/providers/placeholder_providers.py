"""
AI Layer — Placeholder Providers (Phase 61.0: AI Infrastructure
Foundation, TASK 3; Gemini placeholder removed Phase 61.2: AI Runtime
Foundation, TASK 3).

Four stub `BaseAIProvider` implementations (OpenAI/Claude/Grok/Local
LLM). None make a real network call -- every method returns a fixed
`ProviderResult` whose `content` says so explicitly. Grouped in one
file rather than separate top-level modules since each class here is a
handful of identical-shaped lines -- near-empty files would not add
clarity.

Gemini's placeholder was removed from this file (Phase 61.2) once
`ai/providers/gemini_provider.py`'s real implementation replaced it in
`provider_registry.py` -- keeping both would have meant two classes
with the same conceptual identity, one live one dead
(CLAUDE.md's "No duplicate logic"). `core/secrets.py` also now carries
`OPENAI_API_KEY`/`CLAUDE_API_KEY`/`GROK_API_KEY`/`LOCAL_LLM_CONFIG`
(Phase 61.2 TASK 2) -- these four placeholders deliberately still do
not read them; a future phase replaces one or more of these classes
with a real implementation the same way Gemini's was.
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


class OpenAIProvider(_StubProviderMixin, BaseAIProvider):
    _NAME = "openai"


class ClaudeProvider(_StubProviderMixin, BaseAIProvider):
    _NAME = "claude"


class GrokProvider(_StubProviderMixin, BaseAIProvider):
    _NAME = "grok"


class LocalLLMProvider(_StubProviderMixin, BaseAIProvider):
    _NAME = "local_llm"
