"""
AI Layer — Learning Memory Reference (Phase 66.3: AI Learning
Intelligence Foundation, TASK 5).

TASK 5's own instruction: "Faqat key yasaydi. Memory Runtime
chaqirilmaydi" (only builds a key; Memory Runtime is never called).
This module deliberately never imports `ai.memory` at all --
`ai/memory/models.py`'s `MemoryScope` enum has no member shaped for a
learning-topic record, and adding one would be out of this phase's own
scope. Mirrors `ai/trade_journal/memory_adapter.py`'s own precedent
exactly (Phase 66.2, TASK 6).
"""

from ai.learning.models import LearningRecord


def memory_reference_key(record: LearningRecord) -> str:
    """Never raises: a pure string format over already-primitive fields, no Memory call of any kind."""
    return f"learning:{record.id}"
