"""
AI Layer — Provider Interface Foundation (Phase 61.0: AI Infrastructure
Foundation, TASK 3).

Defines the *shape* every future AI vendor integration must satisfy,
across every capability `ai/capabilities/capability.py` names an AI
call for (not just `evaluate()`/analysis, unlike `ai/interfaces.py`'s
narrower `AIAnalyzerInterface`). No method here calls a real API --
`docs/PHASE61_AI_FOUNDATION_AUDIT.md` TASK 1 confirms no existing
`ai/` module already provides a multi-vendor provider abstraction, so
this is a genuinely new package, not a duplicate of `ai/ai_analyzer.py`
(the live, single-purpose production analyzer) or `ai/ai_prompt.py`
(a Gemini-specific prompt builder).

Same advisory-only boundary as `ai/interfaces.py`'s
`AIAnalyzerInterface`: a `BaseAIProvider` implementation must never
approve/reject a trade, call `risk.risk_manager.RiskManager`, or
trigger execution/Telegram delivery. It answers a question; it never
acts on the answer.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class ProviderResult:
    """
    The one output shape every provider method returns, regardless of
    capability or vendor. `content` is free text (a chat reply, an
    explanation, a summary...); `metadata` carries anything
    capability-specific (e.g. a vision provider's detected labels) so
    this shape never has to grow new fields per capability.
    """
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAIProvider(ABC):
    """
    Contract every provider (placeholder today, real in a future
    phase) implements. Every method is capability-shaped, matching
    `ai/capabilities/capability.py`'s vocabulary
    (chat->CHAT, analyze->ANALYSIS, explain->EXPLANATION,
    vision->VISION, image->IMAGE, voice->VOICE). A provider that
    cannot serve a given capability raises `NotImplementedError`
    rather than silently returning a fabricated answer -- the caller
    (TASK 4's router) is responsible for only routing to a provider
    that declares support for the requested capability.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Stable provider identity, e.g. "gemini" -- used by the registry/router, never by Capability itself."""
        raise NotImplementedError

    @abstractmethod
    def analyze(self, prompt: str) -> ProviderResult:
        raise NotImplementedError

    @abstractmethod
    def chat(self, prompt: str) -> ProviderResult:
        raise NotImplementedError

    @abstractmethod
    def explain(self, prompt: str) -> ProviderResult:
        raise NotImplementedError

    @abstractmethod
    def vision(self, prompt: str, image_ref: Optional[str] = None) -> ProviderResult:
        raise NotImplementedError

    @abstractmethod
    def image(self, prompt: str) -> ProviderResult:
        raise NotImplementedError

    @abstractmethod
    def voice(self, prompt: str) -> ProviderResult:
        raise NotImplementedError
