"""
AI Layer — Performance Memory Reference (Phase 66.5: AI Performance
Intelligence Foundation, TASK 9).

TASK 9's own instruction: "Faqat key yasaydi. `ai_layer.knowledge_ai.memory_manager` import
qilinmaydi" (only builds a key; `ai_layer.knowledge_ai.memory_manager` is never imported). This
module deliberately never imports `ai_layer.knowledge_ai.memory_manager` at all -- `ai/memory/models.py`'s
`MemoryScope` enum has no member shaped for a performance record, and
adding one would be out of this phase's own scope. Mirrors
`ai/learning/memory_adapter.py`'s (Phase 66.3, TASK 5) and
`ai/trade_journal/memory_adapter.py`'s (Phase 66.2, TASK 6) own
precedent exactly.
"""

from ai_layer.ai_engine.performance.models import PerformanceRecord


def performance_memory_key(record: PerformanceRecord) -> str:
    """Never raises: a pure string format over already-primitive fields, no Memory call of any kind."""
    return f"performance:{record.user_id}:{record.id}"
