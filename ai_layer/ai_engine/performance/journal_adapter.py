"""
AI Layer — Performance Journal Adapter (Phase 66.5: AI Performance
Intelligence Foundation, TASK 4).

`journal_entry_to_performance_input()` is a pure mapping -- TASK 4's
own instruction: "win/loss o'zi hisoblamaydi, sabab topmaydi" (does
not compute win/loss itself, does not find a cause). It reads an
existing `TradeJournalEntry` (`ai/trade_journal/`, Phase 66.2)
type-only and produces the plain keyword arguments
`PerformanceRuntime.create()` accepts -- it never calls
`PerformanceRuntime.create()` itself, and never mutates
`TradeJournalEntry`.

`entry_quality`/`exit_quality`/`discipline_score`/`risk_score` are
deliberately absent from the returned mapping -- `TradeJournalEntry`
carries no field shaped for any of the four, and inferring one from
`mistakes`/`lesson` text would be real scoring/inference, forbidden by
TASK 3's own rule. Mirrors `ai_layer.personal_ai.senior.journal_adapter.journal_entry_to_coaching_input()`'s
own "field deliberately omitted" precedent exactly.

This is the one file in `ai/performance/` permitted to import
`ai_layer.knowledge_ai.knowledge_base.trade_journal.models` -- `models.py`, `access.py`,
`performance_runtime.py`, `coaching_adapter.py`, `analytics_adapter.py`,
and `memory_adapter.py` never do.
"""

from typing import Any, Dict

from ai_layer.knowledge_ai.knowledge_base.trade_journal.models import TradeJournalEntry


def journal_entry_to_performance_input(entry: TradeJournalEntry) -> Dict[str, Any]:
    """
    TASK 4's own "TradeJournalEntry -> PerformanceRecord" transform.
    Never raises: every value is relayed directly from `entry`, never
    derived or inferred.
    """
    return {
        # TradeJournalEntry carries no user_id field -- trade_id is the
        # closest available identity, same stand-in
        # ai.coaching.journal_adapter.journal_entry_to_coaching_input()
        # already uses for the same reason.
        "user_id": entry.trade_id,
        "trade_id": entry.trade_id,
        "journal_id": entry.journal_id,
        "result": entry.result,
        "direction": entry.direction,
        "confidence_score": entry.confidence,
        "notes": entry.lesson or entry.reason,
    }
