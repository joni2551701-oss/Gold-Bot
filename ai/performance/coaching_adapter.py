"""
AI Layer — Performance Coaching Adapter (Phase 66.5: AI Performance
Intelligence Foundation, TASK 5).

`performance_record_to_coaching_input()` is a pure mapping -- TASK 5's
own instruction: "Faqat structure" (structure only). It reads an
existing `PerformanceRecord` (this package's own `models.py`)
type-only and produces the plain keyword arguments
`ai.coaching.coaching_runtime.CoachingRuntime.create()` accepts -- it
never calls `CoachingRuntime.create()` itself (that decision belongs
to the caller), and never mutates `PerformanceRecord`.

`topic`/`priority`/`type`/`recommendation` are deliberately absent
from the returned mapping -- `PerformanceRecord` has no `topic`-shaped
field (unlike `ai.learning.models.LearningRecord.topic`, which
`ai.coaching.learning_adapter.py` can relay directly), so choosing one
here would require real inference over the four quality scores,
forbidden by this same rule every sibling `66.x` adapter already
follows. Mirrors `ai.coaching.journal_adapter.journal_entry_to_coaching_input()`'s
own "topic deliberately omitted" precedent exactly.

Mirrors `ai.coaching.journal_adapter.py`'s own shape exactly: it reads
its *source* package's model (`ai.performance.models.PerformanceRecord`,
already local to this package) and returns a plain, untyped `Dict` of
`CoachingRuntime.create()` kwargs -- it never imports `ai.coaching.models`
or `ai.coaching.coaching_runtime` at all (no import is needed to
return a dict), and never calls into the Coaching package itself
(Rule: "Faqat structure").
"""

from typing import Any, Dict

from ai.performance.models import PerformanceRecord


def performance_record_to_coaching_input(record: PerformanceRecord) -> Dict[str, Any]:
    """
    TASK 5's own "Performance Issue -> Coaching Recommendation"
    transform. Never raises: every value is relayed directly from
    `record`, never derived or inferred.
    """
    return {
        "user_id": record.user_id,
        "message": record.notes or "",
        "journal_id": record.journal_id,
        "metadata": {
            "trade_id": record.trade_id,
            "direction": record.direction or "",
            "result": record.result or "",
        },
    }
