"""
AI Layer — Failure Analysis Foundation (Phase 59 Real Market
Validation Foundation, TASK 7).

Not the same thing as ai/journal/trade_journal.py's TradeJournalEntry:
that is a general, richer completed-trade record (pnl, rr, exit_price,
ai_confidence, technical_score) covering WIN/LOSS/BREAK_EVEN alike.
This module is narrower and failure-specific -- it records *why* a
losing signal failed, in the shape this task's own brief names as its
goal:

    {"signal_id": "", "reason": "", "context": "H4 bullish but M15
    failed", "result": "SL"}

Placed inside the existing ai/journal/ package (not a new top-level
journal/ directory as the brief's own literal path suggests) since
ai/journal/ is already the established journal location (Phase 55 AI
folder restructure) -- a second, disconnected top-level journal/
package would just be a confusingly-parallel duplicate.

Advisory-only, like every other ai/ module: this file only records
structured failure observations for a future AI training dataset (this
task's own stated goal). It never reads risk/, decision/, or
signals/ directly, never blocks or approves anything, and is not
called from core/pipeline.py -- a foundation type, not yet wired.

In-memory only, like every other Phase 59 Real Market Validation
foundation type not explicitly authorized for a database migration
(TASK 2's raw_candles/market_snapshots tables were the one narrow,
explicit exception) -- persistence is a separate, future decision.
"""

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class FailureAnalysisEntry:
    """
    signal_id: the originating SignalSchema.signal_id -- required, the
        only way to trace this entry back to its signal/context/
        decision chain.
    reason: a short, human-written classification of why the signal
        failed (e.g. "M15 structure break against H4 bias"). Free
        text -- no fixed taxonomy exists yet; that is future work once
        a real dataset exists to classify.
    context: free-text market-context note at the time of failure
        (this task's own worked example: "H4 bullish but M15 failed").
        Not a ContextSnapshotSchema reference -- a human-readable
        summary, not a structured link.
    result: the PaperTrade result that produced this entry (typically
        "SL", but any lifecycle.paper_trade.ALLOWED_PAPER_TRADE_RESULTS
        value is accepted -- this module does not gate on it).
    created_at: when this entry was recorded. Additive, optional --
        not named in the brief's own worked example, but every other
        record type built this phase (SignalPerformance, RawCandle,
        ValidationReport) carries one, so a caller can order/window
        a growing dataset without adding a field later.
    """
    signal_id: str
    reason: str
    context: str
    result: str
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat() if self.created_at else None
        return data

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def create_failure_analysis_entry(
    signal_id: str,
    reason: str,
    context: str,
    result: str,
) -> FailureAnalysisEntry:
    """Pure, deterministic factory -- stamps created_at, same convention as generate_performance_id()'s caller in analytics/signal_performance.py."""
    return FailureAnalysisEntry(
        signal_id=signal_id,
        reason=reason,
        context=context,
        result=result,
        created_at=datetime.now(timezone.utc),
    )
