"""
AI Layer — AI Context Builder (Phase 61.0: AI Infrastructure
Foundation, TASK 5).

Pure composition: `build_ai_context()` bundles five already-computed
inputs into one `AIContext`. It never fetches, computes, or derives
any of them itself -- `ai/learning_context.py`'s own docstring
precedent ("reuses... directly", "does NOT itself generate") is
followed here for every input, not just learning data.
"""

from datetime import datetime, timezone
from typing import List, Optional

from ai.context.context_adapter import sanitize_market_context
from ai.context.context_snapshot import AIContext
from ai.interfaces import MarketContext
from ai.journal.trade_journal import TradeJournalEntry
from ai.learning_context import LearningContext
from ai.profiles.user_profile import AIUserProfile
from signals.schema import SignalSchema


def build_ai_context(
    market_context: Optional[MarketContext] = None,
    signal: Optional[SignalSchema] = None,
    user_profile: Optional[AIUserProfile] = None,
    trade_history: Optional[List[TradeJournalEntry]] = None,
    learning_context: Optional[LearningContext] = None,
) -> AIContext:
    """Never raises: every input is optional, an all-None call returns an AIContext with every field empty/None except built_at."""
    return AIContext(
        market_context=sanitize_market_context(market_context),
        signal=signal,
        user_profile=user_profile,
        trade_history=list(trade_history) if trade_history is not None else [],
        learning_context=learning_context,
        built_at=datetime.now(timezone.utc),
    )
