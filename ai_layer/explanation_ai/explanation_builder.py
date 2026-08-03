"""
AI Layer — AI Explanation Intelligence Layer (Phase 63.1, TASK 2;
renamed from "AI Explanation Engine" per the Director's own Phase 63.1
Decision — this module explains an already-made decision, it never
makes one).

`ExplanationBuilder` is deterministic and template-based -- it never
calls `AIService`/`BaseAIProvider`, never makes a network call, and
never imports `decision/` or `risk/` (Constitution Article 3, no
exceptions for those two packages). Its input is `ExplanationInput`
(Phase 63.1's own primitive-values contract) -- plain floats/strings
a caller such as `core/pipeline.py` extracts from its own
`DecisionResult`/`RiskResult` before calling in; this module never
sees those objects. This is the Director's own approved resolution to
the Phase 63.1 TASK 0 audit finding (`docs/PHASE63_1_AUDIT.md`).

This phase does not wire `core/pipeline.py` to call this builder --
foundation only, same "built and tested, not yet live-integrated"
posture every Phase 61.x/63.0 module has used.
"""

from typing import Optional

from ai_layer.explanation_ai.explanation_input import ExplanationInput, ExplanationMode
from ai_layer.explanation_ai.explanation_output import ExplanationOutput
from ai_layer.explanation_ai.explanation_templates import (
    build_education_explanation,
    build_no_trade_explanation,
    build_trade_explanation,
)
from ai_layer.personal_ai.persona_manager.persona import Persona
from ai_layer.personal_ai.persona_manager.persona_manager import PersonaManager

_DEFAULT_RISK_NOTE = (
    "Educational content only, not financial advice. Markets can move "
    "against any analysis; this is not a guarantee."
)


def _confidence_to_unit_scale(confidence: Optional[float]) -> float:
    """0-100 (ExplanationInput's own scale) -> 0.0-1.0 (ExplanationOutput's own scale). Never raises: a missing/out-of-range value clamps to [0.0, 1.0]."""
    if confidence is None:
        return 0.0
    return max(0.0, min(1.0, confidence / 100.0))


def _title_for(data: ExplanationInput) -> str:
    if data.mode is ExplanationMode.TRADE:
        return f"{data.symbol} Trade Explanation"
    if data.mode is ExplanationMode.NO_TRADE:
        return f"{data.symbol} — No Trade"
    return f"Education: {data.concept or data.symbol}"


def _summary_for(data: ExplanationInput) -> str:
    if data.mode is ExplanationMode.TRADE:
        return f"{data.market_bias or 'Unspecified'} bias on {data.symbol}."
    if data.mode is ExplanationMode.NO_TRADE:
        return f"No trade on {data.symbol}: {data.market_condition or 'condition not specified'}."
    return data.concept or f"Education note for {data.symbol}."


class ExplanationBuilder:
    """Every dependency is injectable, same convention as every other Phase 61.x/62.x/63.x manager."""

    def __init__(self, persona_manager: Optional[PersonaManager] = None) -> None:
        self._persona_manager = persona_manager or PersonaManager()

    def _resolve_persona(self, persona_name: Optional[str]) -> Optional[Persona]:
        if persona_name is not None:
            return self._persona_manager.get(persona_name)
        return self._persona_manager.get_active_persona()

    def build(self, data: ExplanationInput) -> ExplanationOutput:
        """Never raises: every field either comes from `data` or falls back to an honest default -- no AI call, no fabricated reasoning."""
        persona = self._resolve_persona(data.persona_name)

        if data.mode is ExplanationMode.TRADE:
            body = build_trade_explanation(data)
        elif data.mode is ExplanationMode.NO_TRADE:
            body = build_no_trade_explanation(data)
        else:
            body = build_education_explanation(data)

        return ExplanationOutput(
            title=_title_for(data),
            summary=_summary_for(data),
            body=body,
            risk_note=persona.disclaimer if persona else _DEFAULT_RISK_NOTE,
            invalidation=data.invalidation or "not specified",
            confidence=_confidence_to_unit_scale(data.confidence),
            language=data.language,
            market_context=data.market_bias,
            technical_reasoning=data.technical_reason,
            fundamental_reasoning=data.fundamental_reason,
            risk_reasoning=data.risk_reason,
            educational_note=data.lesson if data.mode is ExplanationMode.EDUCATION else None,
            persona=persona.name if persona else None,
        )
