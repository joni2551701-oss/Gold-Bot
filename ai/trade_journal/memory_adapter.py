"""
AI Layer — Trade Journal Memory Reference (Phase 66.2: AI Trade
Journal Intelligence Foundation, TASK 6).

TASK 6's own instruction: "Memory o'zgarmaydi. Kelajak uchun reference
tayyorlansin" (Memory does not change; a reference is prepared for the
future). This module deliberately never imports `ai.memory` at all --
`ai/memory/models.py`'s `MemoryScope` enum has no member shaped for a
trade journal entry, and adding one would violate Rule 6. Instead this
is a plain string-key generator a future, separately-approved phase
would use as `ai.memory.models.MemoryEntry.key` when it decides to
wire real Memory storage -- confirmed zero-import by
`tests/ai/trade_journal/test_trade_journal_isolation.py`.
"""

from ai.trade_journal.models import TradeJournalEntry


def memory_reference_key(entry: TradeJournalEntry) -> str:
    """Never raises: a pure string format over already-primitive fields, no Memory call of any kind."""
    return f"trade_journal:{entry.journal_id}"
