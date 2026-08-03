"""
AI Layer — Portfolio Strategy Adapter (Phase 66.7: AI Portfolio
Intelligence Foundation, TASK 5).

`strategy_records_to_portfolio_input()` is a pure mapping -- TASK 5's
own instruction: "Type-only. Strategy -> Portfolio mapping. Inference
YO'Q." Unlike every prior `66.x` adapter (which map exactly one source
record), this one operates over a `Sequence[ai.strategy.models.StrategyRecord]`
(Phase 66.6, LOCKed), because `PortfolioRecord.strategy_count`/
`.active_strategy_count` are aggregate counts that no single
`StrategyRecord` could ever supply -- see `docs/PHASE66_7_AUDIT.md`'s
"Question 5" for the full reasoning. `strategy_count = len(records)`
and `active_strategy_count` counts records whose `status ==
StrategyStatus.ACTIVE` -- both are **deterministic counting, not
inference**: no judgment, scoring, or classification is applied to any
record's content, mirroring the same class of operation
`ai_layer.ai_engine.performance.analytics_adapter.performance_records_to_win_rate_metric()`
(Phase 66.5) already performed (counting `WIN`/`LOSS` results over a
sequence).

`notes` is deliberately absent from the returned mapping -- with
multiple source records, there is no single canonical note to relay
without arbitrarily picking one, which would itself be a judgment call
forbidden by Rule 5.

This is the one file in `ai/portfolio/` permitted to import
`ai_layer.ai_engine.strategy.models` -- `models.py`, `access.py`, `portfolio_runtime.py`,
`performance_adapter.py`, and `memory_adapter.py` never do.
"""

from typing import Any, Dict, Sequence

from ai_layer.ai_engine.strategy.models import StrategyRecord, StrategyStatus


def strategy_records_to_portfolio_input(records: Sequence[StrategyRecord]) -> Dict[str, Any]:
    """
    TASK 5's own "Strategy -> Portfolio" transform. Never raises: an
    empty `records` sequence produces `strategy_count=0`/
    `active_strategy_count=0`, not an exception.
    """
    active_count = sum(1 for record in records if record.status == StrategyStatus.ACTIVE)
    return {
        "strategy_count": len(records),
        "active_strategy_count": active_count,
    }
