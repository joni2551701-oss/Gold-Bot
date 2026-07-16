"""
AI Layer — AI Context Snapshot (Phase 61.0: AI Infrastructure
Foundation, TASK 5; extended Phase 61.1: AI Provider Reliability
Foundation, TASK 7).

`AIContext` is the one bundled input shape a future AI provider call
receives -- composed from the five sources the brief names (Market
Context, Signal Schema, User Profile, Trade History, Learning
Context), never raw market data (`data/` types are never imported
here). Pure data, no behavior.

Phase 61.1 TASK 7 adds `schema_version`/`context_version`, both
additive with safe defaults so every Phase 61.0 caller of
`build_ai_context()` keeps working unchanged. `built_at` already
serves the brief's own "created_at" purpose (Phase 61.0) -- not
duplicated under a second field name, per the Module Reuse Principle
applied within this dataclass itself.
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

    schema_version: the `AIContext` dataclass shape itself -- bump this
        when a field is added/removed/retyped, so a stored or logged
        `AIContext.to_dict()` can be told apart from a later shape.
    context_version: which *version of this context's own inputs* was
        used to build it (e.g. a future caller building against a
        newer `LearningContext` shape) -- distinct from
        `schema_version`, which never changes just because the inputs
        did. Both default to "1.0", the shape/inputs Phase 61.0
        shipped.
    """
    market_context: Optional[MarketContext] = None
    signal: Optional[SignalSchema] = None
    user_profile: Optional[AIUserProfile] = None
    trade_history: List[TradeJournalEntry] = field(default_factory=list)
    learning_context: Optional[LearningContext] = None
    built_at: Optional[datetime] = None
    schema_version: str = "1.0"
    context_version: str = "1.0"

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
            "schema_version": self.schema_version,
            "context_version": self.context_version,
        }
