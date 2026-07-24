"""
AI Layer — Research Portfolio Adapter (Phase 66.8: AI Research
Intelligence Foundation, TASK 6).

`portfolio_record_to_research_input()` is a pure, type-only mapping --
TASK 6's own instruction: "Reuse: ai/portfolio. Type-only mapping." It
reads an existing `ai.portfolio.models.PortfolioRecord` (Phase 66.7,
LOCKed) type-only and produces the plain keyword arguments
`ai.research.research_runtime.ResearchRuntime.create()` accepts -- it
never calls `ResearchRuntime.create()` itself, and never imports
`ai.portfolio.portfolio_runtime`.

`category=ResearchCategory.PORTFOLIO` is a **structural constant of
this adapter**, not content-based inference -- see
`docs/PHASE66_8_AUDIT.md`'s "Question 6", the same reasoning
`ai.research.performance_adapter.py`'s own docstring already applies.

`title`/`priority`/`status`/`summary`/`source_count` are deliberately
absent -- `PortfolioRecord` carries no field shaped for any of the
five.

This is the one file in `ai/research/` permitted to import
`ai.portfolio.models` -- `models.py`, `access.py`, `research_runtime.py`,
`performance_adapter.py`, `strategy_adapter.py`, and `memory_adapter.py`
never do.
"""

from typing import Any, Dict

from ai.portfolio.models import PortfolioRecord
from ai.research.models import ResearchCategory


def portfolio_record_to_research_input(record: PortfolioRecord) -> Dict[str, Any]:
    """
    TASK 6's own "Portfolio -> Research" transform. Never raises:
    `notes` is relayed directly from `record`, `category` is this
    adapter's own fixed constant -- neither is derived or inferred
    from content.
    """
    return {
        "category": ResearchCategory.PORTFOLIO,
        "notes": record.notes,
    }
