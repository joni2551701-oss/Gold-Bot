"""
Knowledge Foundation — Wyckoff entries (Phase 61.3, TASK 3).

Restates `docs/WYCKOFF.md` and `context/wyckoff.py`'s own detection
rule -- GoldBot's Spring/Upthrust detector, not full Wyckoff phase
theory (Phase A/B/C/D/E boundaries are explicitly out of scope, per
`docs/WYCKOFF.md`'s own "What this does NOT do" section, and are not
claimed here either).
"""

from knowledge.models import KnowledgeCategory, KnowledgeEntry

WYCKOFF_ENTRIES = (
    KnowledgeEntry(
        key="wyckoff.spring",
        category=KnowledgeCategory.WYCKOFF,
        title="Wyckoff Spring",
        summary=(
            "A test of support: Sell-Side Liquidity (SSL) is swept, "
            "followed by the nearest subsequent bullish BOS or CHoCH. "
            "GoldBot labels this an Accumulation-phase event. The swept "
            "liquidity zone itself is the Manipulation leg of the cycle -- "
            "it is not a separate, third event type."
        ),
        tags=("spring", "wyckoff", "accumulation", "support test"),
    ),
    KnowledgeEntry(
        key="wyckoff.upthrust",
        category=KnowledgeCategory.WYCKOFF,
        title="Wyckoff Upthrust",
        summary=(
            "A test of resistance: Buy-Side Liquidity (BSL) is swept, "
            "followed by the nearest subsequent bearish BOS or CHoCH. "
            "GoldBot labels this a Distribution-phase event -- the mirror "
            "case of a Spring."
        ),
        tags=("upthrust", "wyckoff", "distribution", "resistance test"),
    ),
    KnowledgeEntry(
        key="wyckoff.confirming_break",
        category=KnowledgeCategory.WYCKOFF,
        title="Why Wyckoff needs a confirming break",
        summary=(
            "A liquidity sweep alone does not make a Spring or Upthrust -- "
            "GoldBot only emits the event once the nearest same-direction "
            "structural break (BOS or CHoCH) after the sweep is found. A "
            "sweep with no subsequent break of any distance produces no "
            "Wyckoff event at all."
        ),
        tags=("wyckoff", "confirmation", "bos", "choch"),
    ),
    KnowledgeEntry(
        key="wyckoff.volume_not_available",
        category=KnowledgeCategory.WYCKOFF,
        title="Volume confirmation is not available",
        summary=(
            "Classic Wyckoff analysis also looks at volume behavior around "
            "a Spring or Upthrust. GoldBot's candle data is OHLC-only -- "
            "there is no volume source -- so `volume_confirmed` on every "
            "Wyckoff event is always `None` ('not checked'), never a "
            "fabricated true/false."
        ),
        tags=("wyckoff", "volume", "limitation"),
    ),
)
