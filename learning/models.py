"""
Learning Layer — Learning Data Model (Phase 60.6: Learning Loop
Foundation, TASK 2).

`learning/` is a new top-level package — TASK 1's reuse audit (see
`docs/LEARNING_LOOP_AUDIT.md`) confirmed no existing module covers this
ground: `analytics/signal_performance.py`'s `SignalPerformance` shares
7 of this dataclass's 11 fields but is an in-memory, computed-on-demand
analytics type with no persistence story, while `LearningRecord` is
meant to be persisted append-only (TASK 5) — a genuinely different
lifecycle, not a competing view of the same data.

This is a **learning foundation, not an autonomous learner**: nothing
in this package (or this whole phase) reads `LearningRecord.failure_type`/
`success_pattern` back into `strategies/`, `decision/`, or `risk/` to
change behavior. The model exists to observe and record only —
`observe -> analyze -> report`, per the Director's own hard boundary
for this phase.
"""

import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class LearningRecord:
    """
    Deliberately excludes a database `id` — same convention
    `database/audit_log_models.py`'s `AuditLogEntry` already
    established ("repository-internal detail... same convention as
    every other Phase 59.x model"): a `LearningRecord` built here has
    no database row yet, so an auto-increment id doesn't belong on it.
    `database/learning_models.py`'s `LearningRecordRow` (TASK 5) is
    the separate, database-layer type that does carry one.

    record_id: this record's own generated identity
        (generate_learning_record_id()) — distinct from a future
        database `id`; lets a caller reference one `LearningRecord`
        before it is ever persisted.
    trade_id/signal_id: the originating `lifecycle.paper_trade.PaperTrade.trade_id`/
        `signal_id` — required references, never copies of the trade
        or signal themselves.
    strategy_name: matches `SignalSchema.strategy_name`'s own value —
        the same "strategy_name already equals strategy_id" convention
        `analytics/signal_performance.py` already uses.
    market_phase/session/timeframe: the same three context dimensions
        `analytics/signal_performance.py`/`context_report.py` already
        carry — relayed, not recomputed.
    result: one of `lifecycle.paper_trade.ALLOWED_PAPER_TRADE_RESULTS`
        ("TP"/"SL"/"BE"/"EXPIRED"), or "CANCELLED" — the same
        vocabulary `analytics.signal_performance.SignalPerformance.result`
        already uses.
    r_multiple: the realized risk-multiple — same value
        `analytics.signal_performance.compute_r_multiple()` already
        computes; this module does not recompute it, a caller supplies
        an already-known value.
    failure_type: a short, free-text classification of *why* a losing
        trade failed (e.g. "No HTF confirmation") — None for a
        winning/breakeven/undecided trade. No fixed taxonomy yet, same
        "free text, no fixed taxonomy" posture
        `ai.journal.failure_analysis.FailureAnalysisEntry.reason`
        already established.
    success_pattern: a short, free-text description of *why* a winning
        trade succeeded (e.g. "HTF aligned + OB reaction + FVG fill")
        — None for a losing/breakeven/undecided trade. The Director's
        own worked example's mirror-image field; no prior module in
        this codebase has anything like it.
    created_at: when this record was built.
    """
    record_id: str
    trade_id: str
    signal_id: str
    strategy_name: Optional[str] = None
    market_phase: Optional[str] = None
    session: Optional[str] = None
    timeframe: Optional[str] = None
    result: Optional[str] = None
    r_multiple: Optional[float] = None
    failure_type: Optional[str] = None
    success_pattern: Optional[str] = None
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat() if self.created_at else None
        return data


def generate_learning_record_id() -> str:
    """Same generation convention as every other Phase A/AC/Phase-59 identity field (str(uuid.uuid4())) -- not a new scheme."""
    return str(uuid.uuid4())


def create_learning_record(
    trade_id: str,
    signal_id: str,
    *,
    strategy_name: Optional[str] = None,
    market_phase: Optional[str] = None,
    session: Optional[str] = None,
    timeframe: Optional[str] = None,
    result: Optional[str] = None,
    r_multiple: Optional[float] = None,
    failure_type: Optional[str] = None,
    success_pattern: Optional[str] = None,
) -> LearningRecord:
    """Pure, deterministic factory -- stamps created_at, same convention as every other create_X() factory in this codebase."""
    return LearningRecord(
        record_id=generate_learning_record_id(),
        trade_id=trade_id,
        signal_id=signal_id,
        strategy_name=strategy_name,
        market_phase=market_phase,
        session=session,
        timeframe=timeframe,
        result=result,
        r_multiple=r_multiple,
        failure_type=failure_type,
        success_pattern=success_pattern,
        created_at=datetime.now(timezone.utc),
    )
