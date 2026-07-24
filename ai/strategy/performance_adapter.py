"""
AI Layer — Strategy Performance Adapter (Phase 66.6: AI Strategy
Intelligence Foundation, TASK 4).

`performance_record_to_strategy_input()` is a pure mapping -- TASK 4's
own instruction: "Type-only. Runtime import emas." (type-only; no
Runtime import). It reads an existing
`ai.performance.models.PerformanceRecord` (Phase 66.5, LOCKed) type-only
and produces the plain keyword arguments
`ai.strategy.strategy_runtime.StrategyRuntime.create()` accepts -- it
never calls `StrategyRuntime.create()` itself, and never imports
`ai.performance.performance_runtime` (confirmed by
`tests/ai/strategy/test_ai_strategy_isolation.py`'s allowed-import
allowlist).

`strategy_name`/`strategy_type`/`strategy_version` are deliberately
absent from the returned mapping -- `PerformanceRecord` carries no
field shaped for any of the three (see `docs/PHASE66_6_AUDIT.md`'s
"Question 4"), and choosing one here would require real inference,
forbidden by Rule 5 every sibling `66.x` adapter already follows.
Mirrors `ai.performance.journal_adapter.journal_entry_to_performance_input()`'s
own "field deliberately omitted" precedent exactly.

This is the one file in `ai/strategy/` permitted to import
`ai.performance.models` -- `models.py`, `access.py`,
`strategy_runtime.py`, `journal_adapter.py`, and `memory_adapter.py`
never do.
"""

from typing import Any, Dict

from ai.performance.models import PerformanceRecord


def performance_record_to_strategy_input(record: PerformanceRecord) -> Dict[str, Any]:
    """
    TASK 4's own "Performance -> Strategy" transform. Never raises:
    every value is relayed directly from `record`, never derived or
    inferred.
    """
    return {
        "confidence": record.confidence_score,
        "notes": record.notes,
    }
