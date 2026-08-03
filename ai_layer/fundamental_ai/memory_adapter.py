"""
AI Layer — Research Memory Reference (Phase 66.8: AI Research
Intelligence Foundation, TASK 7).

TASK 7's own instruction: "Faqat key generator... ai.memory import
qilish TAQIQLANADI" (a key generator only; importing `ai_layer.knowledge_ai.memory_manager` is
forbidden). This module deliberately never imports `ai_layer.knowledge_ai.memory_manager` at all
-- `ai/memory/models.py`'s `MemoryScope` enum has no member shaped for
a research record, and adding one is out of this phase's own scope.
Mirrors `ai/portfolio/memory_adapter.py`'s (Phase 66.7, TASK 6) own
precedent exactly.
"""

from ai_layer.fundamental_ai.models import ResearchRecord


def research_reference_key(record: ResearchRecord) -> str:
    """Never raises: a pure string format over already-primitive fields, no Memory call of any kind."""
    return f"research:{record.research_id}"
