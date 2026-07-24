"""
AI Layer — Coaching Journal Adapter (Phase 66.4: AI Coaching
Intelligence Foundation, TASK 5).

`journal_entry_to_coaching_input()` is a pure mapping -- TASK 5's own
instruction: "Mapping only. Inference taqiqlanadi." (mapping only,
inference forbidden). It reads an existing `TradeJournalEntry`
(`ai/trade_journal/`, Phase 66.2) type-only and produces the plain
keyword arguments `CoachingRuntime.create()` accepts -- it never calls
`CoachingRuntime.create()` itself, and never mutates
`TradeJournalEntry`.

`topic` is deliberately absent from the returned mapping -- unlike
`LearningRecord` (which already carries an explicit `topic`),
`TradeJournalEntry` has no topic-shaped field, so choosing one here
would require real inference (forbidden). Mirrors
`ai.learning.journal_adapter.journal_entry_to_learning_input()`'s own
"topic/level deliberately omitted" precedent exactly.

This is the one file in `ai/coaching/` permitted to import
`ai.trade_journal.models` -- `models.py`, `access.py`,
`coaching_runtime.py`, and `learning_adapter.py` never do.
"""

from typing import Any, Dict

from ai.trade_journal.models import TradeJournalEntry


def journal_entry_to_coaching_input(entry: TradeJournalEntry) -> Dict[str, Any]:
    """
    TASK 5's own "TradeJournalEntry -> Coaching Input" transform.
    Never raises: every value is relayed directly from `entry`, never
    derived or inferred. `topic`/`priority`/`type`/`recommendation` are
    deliberately absent from the returned mapping -- a caller supplies
    them explicitly when it calls `CoachingRuntime.create()`.
    """
    return {
        "user_id": entry.trade_id,
        "message": entry.lesson or entry.reason or "",
        "journal_id": entry.journal_id,
        "metadata": {
            "symbol": entry.symbol,
            "direction": entry.direction,
        },
    }
