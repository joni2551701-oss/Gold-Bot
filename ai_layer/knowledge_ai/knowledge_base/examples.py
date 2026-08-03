"""
Knowledge Foundation — Worked Examples (Phase 61.3, TASK 3).

Reuses the exact worked examples `docs/MARKET_REGIME.md` and
`docs/EXPLAINABILITY.md` already committed to, restated as queryable
entries rather than invented afresh.
"""

from ai_layer.knowledge_ai.knowledge_base.models import KnowledgeCategory, KnowledgeEntry

EXAMPLES_ENTRIES = (
    KnowledgeEntry(
        key="examples.trending_regime",
        category=KnowledgeCategory.EXAMPLES,
        title="Worked example: a TRENDING regime call",
        summary=(
            "Execution-timeframe structure and HTF Bias agree (both "
            "bullish): regime=TRENDING, direction=BULLISH, "
            "confidence=85.0, reasons=['HTF bullish bias', 'HH/HL "
            "structure']. Confidence drops to 55.0 if HTF Bias is "
            "unavailable or neutral -- same TRENDING label, lower "
            "confidence, because there is no higher-timeframe "
            "confirmation. If structure and HTF Bias actively disagree, "
            "the result is RANGE instead, not a low-confidence TRENDING."
        ),
        tags=("market regime", "trending", "example", "htf bias"),
    ),
    KnowledgeEntry(
        key="examples.signal_explanation",
        category=KnowledgeCategory.EXAMPLES,
        title="Worked example: a signal explanation",
        summary=(
            "A BUY signal with quality A+ and confidence 85% might carry "
            "reasons=['HTF bullish bias', 'HH/HL structure', 'Liquidity "
            "sweep detected', 'FVG reaction', 'London session']. Every "
            "reason traces back to an already-computed criterion (Signal "
            "Quality Score's criteria_met, Wyckoff, Session, Market "
            "Regime) -- none is a new confidence value or new detection, "
            "only a rephrasing of what was already found."
        ),
        tags=("explainability", "signal", "example", "reasons"),
    ),
)
