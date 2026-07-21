"""
AI Layer — Research Performance Adapter (Phase 66.8: AI Research
Intelligence Foundation, TASK 4).

`performance_record_to_research_input()` is a pure, type-only mapping
-- TASK 4's own instruction: "Reuse: ai/performance. Type-only
mapping. Inference YO'Q." It reads an existing
`ai.performance.models.PerformanceRecord` (Phase 66.5, LOCKed) type-only
and produces the plain keyword arguments
`ai.research.research_runtime.ResearchRuntime.create()` accepts -- it
never calls `ResearchRuntime.create()` itself, and never imports
`ai.performance.performance_runtime`.

`category=ResearchCategory.PERFORMANCE` is a **structural constant of
this adapter**, not content-based inference -- see
`docs/PHASE66_8_AUDIT.md`'s "Question 6": every record this specific
adapter ever produces originates from a `PerformanceRecord`, so its
category is fixed by construction, never derived by reading `notes`
or any other field's content.

`title`/`priority`/`status`/`summary`/`source_count` are deliberately
absent from the returned mapping -- `PerformanceRecord` carries no
field shaped for any of the five, and choosing one here would require
real content-based inference, forbidden by Rule 5 every sibling
adapter already follows.

This is the one file in `ai/research/` permitted to import
`ai.performance.models` -- `models.py`, `access.py`,
`research_runtime.py`, `strategy_adapter.py`, `portfolio_adapter.py`,
and `memory_adapter.py` never do.
"""

from typing import Any, Dict

from ai.performance.models import PerformanceRecord
from ai.research.models import ResearchCategory


def performance_record_to_research_input(record: PerformanceRecord) -> Dict[str, Any]:
    """
    TASK 4's own "Performance -> Research" transform. Never raises:
    `notes` is relayed directly from `record`, `category` is this
    adapter's own fixed constant -- neither is derived or inferred
    from content.
    """
    return {
        "category": ResearchCategory.PERFORMANCE,
        "notes": record.notes,
    }
