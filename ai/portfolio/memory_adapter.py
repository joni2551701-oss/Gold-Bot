"""
AI Layer — Portfolio Memory Reference (Phase 66.7: AI Portfolio
Intelligence Foundation, TASK 6).

TASK 6's own instruction: "Faqat key generator... ai.memory import
qilish TAQIQLANADI" (a key generator only; importing `ai.memory` is
forbidden). This module deliberately never imports `ai.memory` at all
-- `ai/memory/models.py`'s `MemoryScope` enum has no member shaped for
a portfolio record, and adding one is out of this phase's own scope.
Mirrors `ai/strategy/memory_adapter.py`'s (Phase 66.6, TASK 6) own
precedent exactly.
"""

from ai.portfolio.models import PortfolioRecord


def portfolio_reference_key(record: PortfolioRecord) -> str:
    """Never raises: a pure string format over already-primitive fields, no Memory call of any kind."""
    return f"portfolio:{record.portfolio_id}"
