"""
Compatibility shim (Phase 55 AI folder restructure).

The real module moved to ai/journal/trade_journal.py as part of the
new professional ai/ package layout. trade_journal.py had zero
importers anywhere in the codebase at the time of the move (confirmed
by a repo-wide grep), so this shim exists purely as a defensive,
zero-cost safety net for any future/external caller that still does
`from ai.trade_journal import ...` -- not because anything currently
depends on this path.
"""

from ai_layer.knowledge_ai.knowledge_base.journal.trade_journal import (
    TradeOutcome,
    DecisionType,
    TradeJournalRecord,
    create_journal_entry,
)

# TASK-AI-000A (Stage 2): the completed-trade record class was renamed
# TradeJournalEntry -> TradeJournalRecord to remove the duplicate class
# name it shared with ai.trade_journal.models.TradeJournalEntry.
__all__ = ["TradeOutcome", "DecisionType", "TradeJournalRecord", "create_journal_entry"]
