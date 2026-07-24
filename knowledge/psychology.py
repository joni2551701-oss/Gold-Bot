"""
Knowledge Foundation — Trading Psychology entries (Phase 61.3, TASK 3).

General, widely-established trading-discipline concepts (not proprietary
GoldBot theory, and not derived from any single `docs/*.md` file the way
SMC/Wyckoff/Risk are). Framed as educational content a future
Explanation/Conversation consumer can offer a user -- GoldBot itself
detects none of these states; there is no psychology-scoring code
anywhere in this codebase, and none is implied here.
"""

from knowledge.models import KnowledgeCategory, KnowledgeEntry

PSYCHOLOGY_ENTRIES = (
    KnowledgeEntry(
        key="psychology.fomo",
        category=KnowledgeCategory.PSYCHOLOGY,
        title="FOMO (Fear of Missing Out)",
        summary=(
            "Entering a trade late, after a move has already extended, out "
            "of fear of missing further gains rather than because a valid "
            "setup is present. A signal's own quality grade and reasons "
            "(see the Explainability entries) exist independent of how "
            "far price has already moved -- they are not a defense against "
            "FOMO, only a separate, structured account of why a signal "
            "fired."
        ),
        tags=("fomo", "discipline", "entry timing"),
    ),
    KnowledgeEntry(
        key="psychology.revenge_trading",
        category=KnowledgeCategory.PSYCHOLOGY,
        title="Revenge trading",
        summary=(
            "Taking an unplanned trade immediately after a loss, driven by "
            "an urge to 'win back' the loss rather than by a fresh, valid "
            "setup. Widely regarded as one of the fastest ways to compound "
            "a single loss into a much larger one."
        ),
        tags=("revenge trading", "discipline", "loss"),
    ),
    KnowledgeEntry(
        key="psychology.overtrading",
        category=KnowledgeCategory.PSYCHOLOGY,
        title="Overtrading",
        summary=(
            "Taking a high volume of trades beyond what a trader's own "
            "strategy or risk plan calls for, often driven by boredom or a "
            "need for constant action rather than the presence of "
            "genuinely qualifying setups."
        ),
        tags=("overtrading", "discipline", "frequency"),
    ),
    KnowledgeEntry(
        key="psychology.patience_for_quality_setups",
        category=KnowledgeCategory.PSYCHOLOGY,
        title="Patience for higher-quality setups",
        summary=(
            "Waiting for a setup with more confirming factors (structure, "
            "liquidity, session, regime alignment) rather than acting on "
            "the first plausible-looking one. GoldBot's own Signal Quality "
            "Score grades (A+ through C) are one structured way this "
            "difference is already made visible in the signal itself."
        ),
        tags=("patience", "signal quality", "discipline"),
    ),
)
