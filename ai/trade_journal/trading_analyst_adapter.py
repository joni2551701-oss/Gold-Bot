"""
AI Layer — Trade Journal Trading Analyst / Chart Intelligence
Integration (Phase 66.2: AI Trade Journal Intelligence Foundation,
TASK 5).

Composes an existing `TradingAnalysis` (`ai/trading_analyst/`, Phase
66.0) and an existing `ChartAnalysis` (`ai/chart_intelligence/`, Phase
66.1) into a single `TradeJournalEntry` -- the pipeline's own
"TradingAnalysis -> ChartAnalysis -> TradeJournal" order (see the
Position diagram in `docs/ai/AI_TRADE_JOURNAL.md`). Zero new business
logic: both objects are read type-only (never mutated, never
re-computed); `direction`/`market_bias` are relayed from `trading`
unchanged -- this module never produces its own BUY/SELL/NO_TRADE
verdict either (Rule 2).

This is the one file in `ai/trade_journal/` permitted to import
`ai.trading_analyst.models` and `ai.chart_intelligence.models` --
`models.py`, `access.py`, `journal_runtime.py`, and `memory_adapter.py`
never do.
"""

from typing import Optional, Sequence

from ai.access.permissions import AIRole
from ai.chart_intelligence.models import ChartAnalysis
from ai.trade_journal.journal_runtime import TradeJournalRuntime
from ai.trade_journal.models import TradeJournalEntry
from ai.trading_analyst.models import TradingAnalysis


def journal_entry_from_trading_and_chart(
    trading: TradingAnalysis,
    chart: ChartAnalysis,
    trade_id: str,
    runtime: TradeJournalRuntime,
    role: AIRole,
    entry: Optional[float] = None,
    sl: Optional[float] = None,
    tp: Optional[float] = None,
    result: Optional[str] = None,
    mistakes: Sequence[str] = (),
) -> Optional[TradeJournalEntry]:
    """
    TASK 5's "TradingAnalysis -> ChartAnalysis -> TradeJournal"
    pipeline leg. `entry`/`sl`/`tp`/`result` are accepted as optional
    pass-through parameters -- neither `TradingAnalysis` nor
    `ChartAnalysis` carries price levels or a realized result in its
    own output contract, so this Foundation-only adapter never
    fabricates them; a future live-wiring phase supplies the real
    values. `reason` relays `trading.recommendation` (falling back to
    `trading.summary`); `lesson` relays `chart.notes` -- both already
    primitive strings, never re-derived.
    """
    reason = trading.recommendation or trading.summary
    return runtime.create(
        chart_id=chart.chart_id,
        trade_id=trade_id,
        symbol=trading.symbol,
        timeframe=chart.timeframe,
        direction=trading.direction,
        role=role,
        entry=entry,
        sl=sl,
        tp=tp,
        result=result,
        confidence=trading.confidence,
        reason=reason,
        lesson=chart.notes,
        mistakes=mistakes,
    )
