"""
AI Layer — Portfolio Performance Adapter (Phase 66.7: AI Portfolio
Intelligence Foundation, TASK 4).

`performance_record_to_portfolio_input()` is a pure mapping -- TASK
4's own instruction: "Type-only. Performance -> Portfolio mapping.
Inference YO'Q." It reads an existing
`ai.performance.models.PerformanceRecord` (Phase 66.5, LOCKed) type-only
and produces the plain keyword arguments
`ai.portfolio.portfolio_runtime.PortfolioRuntime.create()`/`update()`
accept -- it never calls either method itself, and never imports
`ai.performance.performance_runtime` (confirmed by
`tests/ai/portfolio/test_ai_portfolio_isolation.py`'s allowed-import
allowlist).

`portfolio_name`/`status`/`risk_level`/`health`/`strategy_count`/
`active_strategy_count` are deliberately absent from the returned
mapping -- `PerformanceRecord` carries no field shaped for any of the
six (see `docs/PHASE66_7_AUDIT.md`'s "Question 5"), and choosing one
here would require real inference, forbidden by Rule 5 every sibling
`66.x` adapter already follows. Mirrors
`ai.strategy.performance_adapter.performance_record_to_strategy_input()`'s
own "field deliberately omitted" precedent exactly.

This is the one file in `ai/portfolio/` permitted to import
`ai.performance.models` -- `models.py`, `access.py`,
`portfolio_runtime.py`, `strategy_adapter.py`, and `memory_adapter.py`
never do.
"""

from typing import Any, Dict

from ai.performance.models import PerformanceRecord


def performance_record_to_portfolio_input(record: PerformanceRecord) -> Dict[str, Any]:
    """
    TASK 4's own "Performance -> Portfolio" transform. Never raises:
    every value is relayed directly from `record`, never derived or
    inferred.
    """
    return {
        "notes": record.notes,
    }
