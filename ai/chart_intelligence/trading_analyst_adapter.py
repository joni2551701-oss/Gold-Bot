"""
AI Layer — Chart Intelligence Trading Analyst Integration (Phase 66.1:
AI Chart Intelligence Foundation, TASK 5).

Composes an existing `TradingAnalysis` (`ai/trading_analyst/`, Phase
66.0) alongside this phase's own `ChartAnalysis` into a single combined
`ExplanationOutput` -- the pipeline's own "Trading Analyst -> Chart
Intelligence -> Explanation" order (see the Position diagram in
`docs/ai/AI_CHART_INTELLIGENCE.md`). Zero new business logic: both
objects are read type-only (never mutated, never re-computed) and
their already-primitive fields are passed into the existing,
unmodified `ExplanationBuilder` -- the same "compose the shared class a
second time with a different, appropriately-scoped input" pattern
`ai/trading_analyst/analyst_runtime.py` itself already uses relative to
`ai/intelligence_runtime.py`.

This is the one file in `ai/chart_intelligence/` permitted to import
`ai.trading_analyst.models` -- `models.py`, `access.py`,
`chart_runtime.py`, `content_adapter.py`, and
`vision_provider_types.py` never do.
"""

from ai.chart_intelligence.models import ChartAnalysis
from ai.explanation.explanation_builder import ExplanationBuilder
from ai.explanation.explanation_input import ExplanationInput, ExplanationMode
from ai.explanation.explanation_output import ExplanationOutput
from ai.trading_analyst.models import TradingAnalysis


def combined_explanation(
    trading: TradingAnalysis,
    chart: ChartAnalysis,
    explanation_builder: ExplanationBuilder,
) -> ExplanationOutput:
    """
    TASK 5's "TradingAnalysis -> ChartAnalysis -> Explanation" pipeline
    leg. Never raises: builds a TRADE-mode `ExplanationInput` from both
    objects' own already-primitive fields. `direction`/`market_bias`
    are relayed from `trading` unchanged -- Chart Intelligence never
    produces its own BUY/SELL/NO_TRADE verdict (Rule 2); this function
    does not either.
    """
    technical_reason = "; ".join(
        part for part in (trading.summary, chart.market_structure, chart.trend) if part
    )
    explanation_input = ExplanationInput(
        mode=ExplanationMode.TRADE,
        symbol=trading.symbol,
        market_bias=trading.market_bias,
        confidence=chart.confidence * 100.0,
        risk_reward=trading.rr,
        technical_reason=technical_reason or None,
        invalidation=chart.notes,
    )
    return explanation_builder.build(explanation_input)
