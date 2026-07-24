"""
AI Layer — Research Strategy Adapter (Phase 66.8: AI Research
Intelligence Foundation, TASK 5).

`strategy_record_to_research_input()` is a pure, type-only mapping --
TASK 5's own instruction: "Reuse: ai/strategy. Type-only mapping." It
reads an existing `ai.strategy.models.StrategyRecord` (Phase 66.6,
LOCKed) type-only and produces the plain keyword arguments
`ai.research.research_runtime.ResearchRuntime.create()` accepts -- it
never calls `ResearchRuntime.create()` itself, and never imports
`ai.strategy.strategy_runtime`.

`category=ResearchCategory.STRATEGY` is a **structural constant of
this adapter**, not content-based inference -- see
`docs/PHASE66_8_AUDIT.md`'s "Question 6", the same reasoning
`ai.research.performance_adapter.py`'s own docstring already applies.

`title`/`priority`/`status`/`summary`/`source_count` are deliberately
absent -- `StrategyRecord` carries no field shaped for any of the
five.

This is the one file in `ai/research/` permitted to import
`ai.strategy.models` -- `models.py`, `access.py`, `research_runtime.py`,
`performance_adapter.py`, `portfolio_adapter.py`, and `memory_adapter.py`
never do.
"""

from typing import Any, Dict

from ai.research.models import ResearchCategory
from ai.strategy.models import StrategyRecord


def strategy_record_to_research_input(record: StrategyRecord) -> Dict[str, Any]:
    """
    TASK 5's own "Strategy -> Research" transform. Never raises:
    `notes` is relayed directly from `record`, `category` is this
    adapter's own fixed constant -- neither is derived or inferred
    from content.
    """
    return {
        "category": ResearchCategory.STRATEGY,
        "notes": record.notes,
    }
