"""
AI Layer — Explanation Engine (Phase 61.3: AI Intelligence Layer,
TASK 7).

Wraps `ai/runtime/ai_service.py`'s `AIService.ask()` (unmodified) for
EXPLANATION/SUMMARY/EDUCATION/ANALYSIS-shaped questions only -- no new
provider call, no new capability. Reuses `signals/explainability.py`'s
`SignalExplanation` (already-computed reasons; `ai/` -> `signals/` is
the one sanctioned cross-layer import this session's own boundary
audit established) and `knowledge/registry.py`'s entries as prompt
input -- this module never recomputes signal reasoning, never detects
anything, and never calls a strategy or the pipeline.

`explain_signal()` is the only method with a real end-to-end path
today: `Capability.EXPLANATION` is one of the six capabilities
`ai/runtime/ai_service.py`'s `_CAPABILITY_METHOD` maps to a real
`BaseAIProvider` method. `summarize_report()` (`Capability.SUMMARY`)
and `explain_topic()` (`Capability.EDUCATION`) build a correctly-shaped
request but are always cleanly rejected by `AIService.ask()` itself
("no runtime method mapping yet") until a future phase adds a
provider-side SUMMARY/EDUCATION method -- a pre-existing gap this
module does not attempt to close, per the same "foundation, not yet
wired" posture every other Phase 61.x module has used.
"""

from typing import Optional

from ai.access.permissions import AIRole
from ai.capabilities.capability import Capability
from ai.context.context_snapshot import AIContext
from ai.runtime.ai_service import AIService
from ai.runtime.runtime_request import RuntimeRequest
from ai.runtime.runtime_response import RuntimeResponse
from knowledge.registry import get_entry
from signals.explainability import SignalExplanation


def _format_signal_explanation(explanation: SignalExplanation) -> str:
    reasons_text = "; ".join(explanation.reasons) if explanation.reasons else "no supporting reasons found"
    return (
        f"Explain in plain language why this {explanation.direction} signal fired.\n"
        f"Reasons: {reasons_text}\n"
        f"Quality: {explanation.quality}\n"
        f"Confidence: {explanation.confidence}%"
    )


class ExplanationEngine:
    """Every dependency is injectable, same convention as `AIService`/`ConversationEngine`."""

    def __init__(self, ai_service: Optional[AIService] = None) -> None:
        self._ai_service = ai_service or AIService()

    def explain_signal(
        self,
        explanation: SignalExplanation,
        ai_context: AIContext,
        role: AIRole,
        telegram_id: Optional[str] = None,
    ) -> RuntimeResponse:
        """The only method here with a real BaseAIProvider mapping today (EXPLANATION)."""
        prompt = _format_signal_explanation(explanation)
        request = RuntimeRequest(
            capability=Capability.EXPLANATION, ai_context=ai_context, role=role,
            prompt=prompt, telegram_id=telegram_id,
        )
        return self._ai_service.ask(request)

    def summarize_report(
        self,
        report_text: str,
        ai_context: AIContext,
        role: AIRole,
        telegram_id: Optional[str] = None,
    ) -> RuntimeResponse:
        """Formats an already-built analytics report string (e.g. analytics.strategy_report/analytics.learning_report's own formatted text) into a SUMMARY-capability request. Currently always rejected by AIService.ask() -- see module docstring."""
        prompt = f"Summarize this report for a trader:\n\n{report_text}"
        request = RuntimeRequest(
            capability=Capability.SUMMARY, ai_context=ai_context, role=role,
            prompt=prompt, telegram_id=telegram_id,
        )
        return self._ai_service.ask(request)

    def explain_topic(
        self,
        key: str,
        ai_context: AIContext,
        role: AIRole,
        telegram_id: Optional[str] = None,
    ) -> RuntimeResponse:
        """Looks up a knowledge/ entry by key (Phase 61.3, TASK 3) and asks for a deeper EDUCATION-capability explanation of it. Currently always rejected by AIService.ask() -- see module docstring."""
        entry = get_entry(key)
        if entry is None:
            return RuntimeResponse(
                accepted=False, content=None, provider_name=None,
                reason=f"no knowledge entry found for key {key}",
            )
        prompt = f"Explain this concept in more depth: {entry.title}. {entry.summary}"
        request = RuntimeRequest(
            capability=Capability.EDUCATION, ai_context=ai_context, role=role,
            prompt=prompt, telegram_id=telegram_id,
        )
        return self._ai_service.ask(request)

    def analyze_market(
        self,
        ai_context: AIContext,
        role: AIRole,
        telegram_id: Optional[str] = None,
    ) -> RuntimeResponse:
        """Thin passthrough to AIService.ask() with capability=ANALYSIS -- included for API symmetry with this engine's other three methods; AIService already derives the prompt from ai_context.market_context on its own, so this adds no new prompt-building logic."""
        request = RuntimeRequest(capability=Capability.ANALYSIS, ai_context=ai_context, role=role, telegram_id=telegram_id)
        return self._ai_service.ask(request)
