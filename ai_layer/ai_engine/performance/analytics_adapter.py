"""
AI Layer — Performance Analytics Adapter (Phase 66.5: AI Performance
Intelligence Foundation, TASK 6).

TASK 6's own instruction: "Mavjud analytics/ bilan ishlash imkoniyatini
tekshiradi. Agar mos bo'lsa: reuse. Agar mos bo'lmasa: yangi
abstraction." (checks whether the existing analytics/ can be worked
with; reuse if it fits, a new abstraction if it doesn't.)

`docs/PHASE66_5_AUDIT.md`'s own conclusion (question 2): **partial
reuse**. `backtesting_layer.statistics.strategy_report.compute_win_rate()` -- a plain
`(wins, losses) -> float` utility already reused by
`backtesting_layer/statistics/performance_metrics.py` itself -- fits directly over
`PerformanceRecord.result` counts, so this module reuses it rather
than reimplementing a win-rate formula. Full reuse of
`backtesting_layer.statistics.performance_metrics.compute_performance_metrics()` does
**not** fit: it requires `SignalPerformance.r_multiple`, a field
`PerformanceRecord` carries no equivalent of, and synthesizing one
from a quality score would be fabrication (forbidden). That gap is
documented, not worked around, here and in the audit doc.
"""

from datetime import datetime, timezone
from typing import Sequence

from backtesting_layer.statistics.strategy_report import compute_win_rate

from ai_layer.ai_engine.performance.models import PerformanceMetric, PerformanceRecord


def performance_records_to_win_rate_metric(
    records: Sequence[PerformanceRecord], period: str = "all"
) -> PerformanceMetric:
    """
    Reuses `backtesting_layer.statistics.strategy_report.compute_win_rate()` directly --
    counts `PerformanceRecord.result == "WIN"`/`"LOSS"` (the same
    free-text vocabulary `ai_layer.knowledge_ai.knowledge_base.trade_journal.models.TradeJournalEntry.result`
    already uses) and produces one `PerformanceMetric`. Never raises:
    an empty `records` sequence produces a `0.0` win rate (`compute_win_rate()`'s
    own zero-division-safe contract), not an exception.
    """
    wins = sum(1 for r in records if r.result == "WIN")
    losses = sum(1 for r in records if r.result == "LOSS")
    win_rate = compute_win_rate(wins, losses)

    return PerformanceMetric(
        metric_name="win_rate",
        value=win_rate,
        period=period,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
