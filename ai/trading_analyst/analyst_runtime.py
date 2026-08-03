"""
AI Layer — Trading Analyst Runtime (Phase 66.0: AI Trading Analyst
Foundation, TASK 3/4/5/6/7).

Composes two real, unmodified public methods — zero new business
logic of its own, the same "the composed systems do the work" posture
`ai/intelligence_runtime.py` and `voice/conversation_bridge.py` both
already established:

    IntelligenceRuntime.run()      (TASK 3 — Knowledge/Memory/
                                     Reasoning/Conversation grounding,
                                     reused exactly as-is, Phase 64.0)
    ExplanationBuilder.build()     (TASK 6/7 — the existing, real
                                     TRADE-mode explanation builder,
                                     Phase 63.0/63.1; no new
                                     Explanation engine)

`TradingAnalystRuntime` never imports `decision/`, `risk/`,
`execution/`, `strategies/`, `signals/`, `context/`, or `monitoring/`
(Rule 4, Constitution Article 3) — every field it reads comes from the
caller-supplied `TradingAnalysisInput`, never a Trading Core object.
Owner-gated: `analyze()` re-checks
`ai.trading_analyst.access.is_trading_analyst_enabled_for()` itself.
"""

from datetime import datetime, timezone
from typing import Optional

from ai.access.permissions import AIRole
from ai.explanation.explanation_builder import ExplanationBuilder
from ai.explanation.explanation_input import ExplanationInput, ExplanationMode
from ai.intelligence_runtime import IntelligenceRuntime
from ai.trading_analyst.access import is_trading_analyst_enabled_for
from ai.trading_analyst.models import TradingAnalysis, TradingAnalysisInput
from goldbot.core_layer.configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


def _confidence_to_unit_scale(confidence: float) -> float:
    """0-100 (TradingAnalysisInput's own scale) -> 0.0-1.0. Never raises: an out-of-range value clamps to [0.0, 1.0]."""
    return max(0.0, min(1.0, confidence / 100.0))


def _recommendation_for(data: TradingAnalysisInput) -> str:
    """
    TASK 5 — a narrative "WHY {direction}" string built entirely from
    already-supplied fields, never a new BUY/SELL/NO_TRADE verdict
    (Director Note 1). Falls back to `technical_reason` when no
    `strengths` entry is available.
    """
    reason = data.strengths[0] if data.strengths else (data.technical_reason or "no additional detail")
    return f"WHY {data.direction}: {reason}"


class TradingAnalystRuntime:
    """Every dependency is injectable, same convention as every other Phase 61.x-66.0 runtime/manager."""

    def __init__(
        self,
        intelligence_runtime: Optional[IntelligenceRuntime] = None,
        explanation_builder: Optional[ExplanationBuilder] = None,
        flags: FeatureFlags = DEFAULT_FLAGS,
    ) -> None:
        self._intelligence_runtime = intelligence_runtime or IntelligenceRuntime()
        self._explanation_builder = explanation_builder or ExplanationBuilder()
        self._flags = flags

    def analyze(self, data: TradingAnalysisInput, role: AIRole) -> Optional[TradingAnalysis]:
        """
        Never raises: a denied role returns None before either
        composed system is ever touched. TASK 3's own pipeline order
        (Knowledge -> Memory -> Reasoning -> Conversation ->
        Explanation) is walked by `IntelligenceRuntime.run()`
        (unmodified); the resulting grounding is informational only —
        it never blocks or alters this method's own output, matching
        `IntelligenceRuntime.run()`'s own never-raises, always-returns
        posture.
        """
        if not is_trading_analyst_enabled_for(role, self._flags):
            return None

        self._intelligence_runtime.run(topic=data.symbol)

        explanation_input = ExplanationInput(
            mode=ExplanationMode.TRADE,
            symbol=data.symbol,
            language=data.language,
            market_bias=data.market_bias,
            entry=data.entry,
            stop_loss=data.stop_loss,
            take_profit=data.take_profit,
            confidence=data.confidence,
            risk_reward=data.risk_reward,
            technical_reason=data.technical_reason,
            risk_reason=data.risk_reason,
            invalidation=data.invalidation,
        )
        explanation_output = self._explanation_builder.build(explanation_input)

        return TradingAnalysis(
            symbol=data.symbol,
            direction=data.direction,
            confidence=_confidence_to_unit_scale(data.confidence),
            market_bias=data.market_bias,
            risk_level=data.risk_level,
            rr=data.risk_reward,
            summary=explanation_output.summary,
            strengths=tuple(data.strengths),
            weaknesses=tuple(data.weaknesses),
            recommendation=_recommendation_for(data),
            educational_note=explanation_output.educational_note,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )
