"""
AI Layer — Coaching Learning Adapter (Phase 66.4: AI Coaching
Intelligence Foundation, TASK 4).

`learning_record_to_coaching_input()` is a pure mapping -- TASK 4's own
instruction: "Hech qanday yangi AI analiz qilmaydi. Mapping only." It
reads an existing `LearningRecord` (`ai/learning/`, Phase 66.3)
type-only and produces the plain keyword arguments
`CoachingRuntime.create()` accepts -- it never calls
`CoachingRuntime.create()` itself (that decision belongs to the
caller), and never mutates `LearningRecord`.

Unlike `journal_adapter.py` (TASK 5), this adapter *can* relay `topic`
directly -- `LearningRecord.topic` is already an explicit,
caller-supplied classification on the source record, so copying it is
a direct relay, not an inference. `message` is populated from
`LearningRecord.notes` verbatim (relayed, never rewritten or
summarized) -- a caller is free to override it before calling
`CoachingRuntime.create()`.

This is the one file in `ai/coaching/` permitted to import
`ai.learning.models` -- `models.py`, `access.py`,
`coaching_runtime.py`, and `journal_adapter.py` never do.
"""

from typing import Any, Dict

from ai.learning.models import LearningRecord


def learning_record_to_coaching_input(record: LearningRecord) -> Dict[str, Any]:
    """
    TASK 4's own "LearningRecord -> Coaching Input" transform. Never
    raises: every value is relayed directly from `record`, never
    derived or inferred. `priority`/`type`/`recommendation` are
    deliberately absent from the returned mapping -- this adapter has
    no basis to choose those without performing real inference; a
    caller supplies them explicitly when it calls
    `CoachingRuntime.create()`.
    """
    return {
        "user_id": record.user_id,
        "topic": record.topic,
        "message": record.notes or "",
        "learning_id": record.id,
        "metadata": {
            "level": record.level.value,
            "source": record.source.value,
        },
    }
