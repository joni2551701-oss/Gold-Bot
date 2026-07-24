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

from ai.journal.trade_journal import (
    TradeOutcome,
    DecisionType,
    TradeJournalEntry,
    create_journal_entry,
)

__all__ = ["TradeOutcome", "DecisionType", "TradeJournalEntry", "create_journal_entry"]
