"""
AI Layer — Chart Intelligence Runtime (Phase 66.1: AI Chart
Intelligence Foundation, TASK 4/5/6/7).

`ChartRuntime` never calls a Vision API, an LLM, or any real image
recognition model (Rule 4) -- `analyze()` is a pure, deterministic
relay/transform over caller-supplied `ChartAnalysisInput` fields, the
same "READ ONLY, never inferred" posture `ai/trading_analyst/analyst_runtime.py`
already established for trade fields. `explain()` composes the
existing, unmodified `ExplanationBuilder` (Phase 63.0/63.1) in
`EDUCATION` mode -- Chart Intelligence narrates an observation, it
never produces a TRADE-mode BUY/SELL/NO_TRADE verdict (Rule 2).

`ChartRuntime` never imports `decision/`, `risk/`, `execution/`,
`strategies/`, `signals/`, `context/`, or `monitoring/` (Constitution
Article 3). Owner-gated: both `analyze()` and `explain()` re-check
`ai.chart_intelligence.access.is_chart_intelligence_enabled_for()`
themselves.
"""

from datetime import datetime, timezone
from typing import Optional

from ai.access.permissions import AIRole
from ai.chart_intelligence.access import is_chart_intelligence_enabled_for
from ai.chart_intelligence.models import ChartAnalysis, ChartAnalysisInput
from ai.explanation.explanation_builder import ExplanationBuilder
from ai.explanation.explanation_input import ExplanationInput, ExplanationMode
from ai.explanation.explanation_output import ExplanationOutput
from configuration.feature_flags import DEFAULT_FLAGS, FeatureFlags


def _confidence_to_unit_scale(confidence: float) -> float:
    """0-100 (ChartAnalysisInput's own scale) -> 0.0-1.0. Never raises: an out-of-range value clamps to [0.0, 1.0]."""
    return max(0.0, min(1.0, confidence / 100.0))


class ChartRuntime:
    """Every dependency is injectable, same convention as every other Phase 61.x-66.0 runtime/manager."""

    def __init__(
        self,
        explanation_builder: Optional[ExplanationBuilder] = None,
        flags: FeatureFlags = DEFAULT_FLAGS,
    ) -> None:
        self._explanation_builder = explanation_builder or ExplanationBuilder()
        self._flags = flags

    def analyze(self, data: ChartAnalysisInput, role: AIRole) -> Optional[ChartAnalysis]:
        """
        TASK 2/4 -- a pure relay/transform, never calls a Vision API.
        Never raises: a denied role returns None before any field is
        even read.
        """
        if not is_chart_intelligence_enabled_for(role, self._flags):
            return None

        return ChartAnalysis(
            symbol=data.symbol,
            timeframe=data.timeframe,
            image_type=data.image_type,
            analysis_type=data.analysis_type,
            market_structure=data.market_structure,
            trend=data.trend,
            liquidity=data.liquidity,
            order_blocks=tuple(data.order_blocks),
            fvg=tuple(data.fvg),
            support=tuple(data.support),
            resistance=tuple(data.resistance),
            confidence=_confidence_to_unit_scale(data.confidence),
            notes=data.notes,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

    def explain(self, chart: ChartAnalysis, role: AIRole, language: str = "en") -> Optional[ExplanationOutput]:
        """
        TASK 5/6 -- the "ChartAnalysis -> Explanation" pipeline leg,
        composing the existing, unmodified `ExplanationBuilder`
        (EDUCATION mode -- Chart Intelligence never produces a TRADE
        verdict, Rule 2). No new Explanation engine.
        """
        if not is_chart_intelligence_enabled_for(role, self._flags):
            return None

        explanation_input = ExplanationInput(
            mode=ExplanationMode.EDUCATION,
            symbol=chart.symbol,
            language=language,
            concept=f"{chart.analysis_type.value} on {chart.symbol} ({chart.timeframe})",
            example=chart.market_structure or chart.trend or chart.liquidity or "chart observation",
            lesson=chart.notes,
        )
        return self._explanation_builder.build(explanation_input)
