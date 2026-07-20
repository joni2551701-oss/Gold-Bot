"""
AI Layer — Learning Journal Adapter (Phase 66.3: AI Learning
Intelligence Foundation, TASK 4).

`journal_entry_to_learning_input()` is a pure mapping — TASK 4's own
instruction: "Hech qanday AI yo'q. Faqat mapping" (no AI, mapping
only). It reads an existing `TradeJournalEntry` (`ai/trade_journal/`,
Phase 66.2) type-only and produces the plain keyword arguments
`LearningRuntime.create()` accepts — it never calls
`LearningRuntime.create()` itself (that decision belongs to the
caller), never infers a `topic`/`level` from the journal entry's own
`mistakes`/`lesson` text (that would be real AI inference, forbidden
by Rule 10), and never mutates `TradeJournalEntry`.

This is the one file in `ai/learning/` permitted to import
`ai.trade_journal.models` -- `models.py`, `access.py`,
`learning_runtime.py`, and `memory_adapter.py` never do.
"""

from typing import Any, Dict

from ai.learning.models import LearningSource
from ai.trade_journal.models import TradeJournalEntry


def journal_entry_to_learning_input(entry: TradeJournalEntry) -> Dict[str, Any]:
    """
    TASK 4's own "TradeJournal -> LearningRecord transform" pipeline
    leg. Never raises: every value is relayed directly from `entry`,
    never derived or inferred. `topic`/`level` are deliberately absent
    from the returned mapping -- this adapter cannot know which
    `LearningTopic`/`LearningLevel` a journal entry maps to without
    performing real inference (Rule 10); a caller supplies those
    explicitly when it calls `LearningRuntime.create()`.
    """
    return {
        "user_id": entry.trade_id,
        "confidence": entry.confidence,
        "notes": entry.lesson or entry.reason,
        "source": LearningSource.JOURNAL,
    }
