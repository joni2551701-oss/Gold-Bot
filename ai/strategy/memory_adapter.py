"""
AI Layer — Strategy Memory Reference (Phase 66.6: AI Strategy
Intelligence Foundation, TASK 6).

TASK 6's own instruction: "Faqat key generator... ai.memory import
qilish taqiqlanadi" (a key generator only; importing `ai.memory` is
forbidden). This module deliberately never imports `ai.memory` at all
-- `ai/memory/models.py`'s `MemoryScope` enum has no member shaped for
a strategy record, and adding one is out of this phase's own scope.
Mirrors `ai/performance/memory_adapter.py`'s (Phase 66.5, TASK 9) own
precedent exactly.
"""

from ai.strategy.models import StrategyRecord


def strategy_reference_key(record: StrategyRecord) -> str:
    """Never raises: a pure string format over already-primitive fields, no Memory call of any kind."""
    return f"strategy:{record.strategy_id}"
