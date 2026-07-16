"""
AI Layer — AI Context Snapshot (Phase 61.0: AI Infrastructure
Foundation, TASK 5).

`AIContext` is the one bundled input shape a future AI provider call
receives -- composed from the five sources the brief names (Market
Context, Signal Schema, User Profile, Trade History, Learning
Context), never raw market data (`data/` types are never imported
here). Pure data, no behavior.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from ai.interfaces import MarketContext
from ai.journal.trade_journal import TradeJournalEntry
from ai.learning_context import LearningContext
from ai.profiles.user_profile import AIUserProfile
from signals.schema import SignalSchema


@dataclass(frozen=True)
class AIContext:
    """
    Every field is optional except `built_at` -- a caller may build a
    partial context (e.g. market analysis with no user personalization)
    the same way `ai/interfaces.py`'s `AIAnalyzerInterface.evaluate()`
    already treats `user_context` as optional.
    """
    market_context: Optional[MarketContext] = None
    signal: Optional[SignalSchema] = None
    user_profile: Optional[AIUserProfile] = None
    trade_history: List[TradeJournalEntry] = field(default_factory=list)
    learning_context: Optional[LearningContext] = None
    built_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """JSON-safe dict for logging/inspection -- not itself a prompt or an API payload (that is a future phase's job, e.g. ai/prompts/)."""
        return {
            "market_context": {
                "symbol": self.market_context.symbol,
                "timeframe": self.market_context.timeframe,
                "summary": self.market_context.summary,
            } if self.market_context else None,
            "signal": self.signal.to_dict() if self.signal else None,
            "user_profile": {
                "telegram_id": self.user_profile.telegram_id,
                "experience_level": self.user_profile.experience_level,
                "preferred_strategy": self.user_profile.preferred_strategy,
                "risk_style": self.user_profile.risk_style,
                "language": self.user_profile.language,
            } if self.user_profile else None,
            "trade_history_count": len(self.trade_history),
            "learning_context": self.learning_context.to_dict() if self.learning_context else None,
            "built_at": self.built_at.isoformat() if self.built_at else None,
        }
