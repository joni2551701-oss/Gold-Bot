"""
AI Layer — Strategy Journal Adapter (Phase 66.6: AI Strategy
Intelligence Foundation, TASK 5).

`journal_entry_to_strategy_input()` is a pure mapping -- TASK 5's own
instruction: "Hech qanday inference yo'q" (no inference of any kind).
It reads an existing `ai_layer.knowledge_ai.knowledge_base.trade_journal.models.TradeJournalEntry`
(Phase 66.2) type-only and produces the plain keyword arguments
`ai_layer.ai_engine.strategy.strategy_runtime.StrategyRuntime.create()` accepts -- it
never calls `StrategyRuntime.create()` itself, and never mutates
`TradeJournalEntry`.

`strategy_name`/`strategy_type`/`strategy_version` are deliberately
absent from the returned mapping -- `TradeJournalEntry` carries no
field shaped for any of the three (see `docs/PHASE66_6_AUDIT.md`'s
"Question 3"). Mirrors
`ai_layer.ai_engine.performance.journal_adapter.journal_entry_to_performance_input()`'s
own "field deliberately omitted" precedent exactly. `confidence` is
also deliberately absent -- `TradeJournalEntry.confidence` is a
per-trade value, not a per-strategy one, and relaying it here would
conflate the two, which is inference, forbidden by Rule 5.

This is the one file in `ai/strategy/` permitted to import
`ai_layer.knowledge_ai.knowledge_base.trade_journal.models` -- `models.py`, `access.py`,
`strategy_runtime.py`, `performance_adapter.py`, and `memory_adapter.py`
never do.
"""

from typing import Any, Dict

from ai_layer.knowledge_ai.knowledge_base.trade_journal.models import TradeJournalEntry


def journal_entry_to_strategy_input(entry: TradeJournalEntry) -> Dict[str, Any]:
    """
    TASK 5's own "TradeJournalEntry -> Strategy" transform. Never
    raises: every value is relayed directly from `entry`, never derived
    or inferred.
    """
    return {
        "notes": entry.lesson or entry.reason,
    }
