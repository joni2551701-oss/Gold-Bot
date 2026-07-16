"""
AI Layer — Placeholder Providers (Phase 61.0: AI Infrastructure
Foundation, TASK 3).

Five stub `BaseAIProvider` implementations, one per named vendor
(OpenAI/Gemini/Claude/Grok) plus a Local LLM placeholder. None make a
real network call -- every method returns a fixed `ProviderResult`
whose `content` says so explicitly. Grouped in one file rather than
five top-level modules since the Phase 61.0 brief names only
`base_provider.py`/`provider_manager.py`/`provider_registry.py` as
required files and each class here is a handful of identical-shaped
lines -- five near-empty files would not add clarity.

`core/secrets.py` already carries `GEMINI_API_KEY` (Phase 55) and is
ready for a real provider to read it -- these placeholders deliberately
do not read it, since TASK 3's brief says "Real API YO'Q. Faqat
interface." A future Phase 61.1+ replaces one or more of these classes
with a real implementation; this phase only fixes the shape.
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


class GeminiProvider(_StubProviderMixin, BaseAIProvider):
    _NAME = "gemini"


class ClaudeProvider(_StubProviderMixin, BaseAIProvider):
    _NAME = "claude"


class GrokProvider(_StubProviderMixin, BaseAIProvider):
    _NAME = "grok"


class LocalLLMProvider(_StubProviderMixin, BaseAIProvider):
    _NAME = "local_llm"
