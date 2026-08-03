"""
Knowledge Foundation — Smart Money Concepts entries (Phase 61.3, TASK 3).

Restates `context_layer/market_structure/bos.py`, `context_layer/market_structure/choch.py`, `context_layer/liquidity/liquidity.py`,
`context_layer/order_block/order_block.py`, `context_layer/fair_value_gap/fvg.py`, and `context_layer/amd/amd.py`'s own
docstrings and detection rules -- the exact concepts GoldBot's Context
Engine already detects, not a second, independently-invented SMC theory.
"""

from ai_layer.knowledge_ai.knowledge_base.models import KnowledgeCategory, KnowledgeEntry

SMC_ENTRIES = (
    KnowledgeEntry(
        key="smc.bos",
        category=KnowledgeCategory.SMC,
        title="Break of Structure (BOS)",
        summary=(
            "A confirmed continuation of the current trend: price closes "
            "beyond a trend-aligned structural pivot (a Higher High for a "
            "bullish trend, a Lower Low for a bearish trend). GoldBot only "
            "confirms a BOS on a closed candle beyond that pivot, never on "
            "an intrabar touch."
        ),
        tags=("bos", "break of structure", "structure", "trend"),
    ),
    KnowledgeEntry(
        key="smc.choch",
        category=KnowledgeCategory.SMC,
        title="Change of Character (CHoCH)",
        summary=(
            "The first structural break against the prevailing trend -- the "
            "earliest signal that the trend may be reversing, distinct from "
            "a BOS, which confirms the existing trend is continuing."
        ),
        tags=("choch", "change of character", "reversal", "structure"),
    ),
    KnowledgeEntry(
        key="smc.liquidity_sweep",
        category=KnowledgeCategory.SMC,
        title="Liquidity Sweep (BSL / SSL)",
        summary=(
            "Price briefly trades through a zone where resting orders are "
            "likely clustered -- Buy-Side Liquidity (BSL, above equal highs "
            "or resistance) or Sell-Side Liquidity (SSL, below equal lows or "
            "support) -- before reversing. GoldBot detects the sweep event "
            "itself; whether it is followed by a confirming break is a "
            "separate, later check (see the Wyckoff Spring/Upthrust entry)."
        ),
        tags=("liquidity", "sweep", "bsl", "ssl", "equal highs", "equal lows"),
    ),
    KnowledgeEntry(
        key="smc.order_block",
        category=KnowledgeCategory.SMC,
        title="Order Block",
        summary=(
            "The last opposing candle before a decisive structural move -- "
            "a bullish order block precedes a bullish break, a bearish "
            "order block precedes a bearish break. Treated as a zone price "
            "may return to and react from, not a signal on its own."
        ),
        tags=("order block", "ob", "zone"),
    ),
    KnowledgeEntry(
        key="smc.fair_value_gap",
        category=KnowledgeCategory.SMC,
        title="Fair Value Gap (FVG)",
        summary=(
            "A three-candle imbalance where the first and third candles' "
            "wicks do not overlap, leaving a gap the market often revisits "
            "before continuing. Confirmed on the third candle, same "
            "closed-candle-only convention every GoldBot structural "
            "detector uses."
        ),
        tags=("fvg", "fair value gap", "imbalance", "gap"),
    ),
    KnowledgeEntry(
        key="smc.amd_cycle",
        category=KnowledgeCategory.SMC,
        title="AMD Cycle (Accumulation - Manipulation - Distribution)",
        summary=(
            "GoldBot's `context_layer/amd/amd.py` correlates a liquidity sweep (the "
            "Manipulation leg) with a subsequent structural break (the "
            "Distribution leg) into one cycle. This is a general "
            "correlation; Wyckoff Spring/Upthrust (see the Wyckoff category) "
            "is a narrower, more specific version of the same underlying "
            "idea, detected independently rather than reusing this logic."
        ),
        tags=("amd", "accumulation", "manipulation", "distribution"),
    ),
)
