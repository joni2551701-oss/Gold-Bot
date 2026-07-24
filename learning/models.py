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

Phase 60.7 (Adaptive Intelligence Layer Foundation, TASK 3) extends
this same `LearningRecord` with six additional `Optional` fields
(`htf_bias`/`volatility_state`/`fundamental_bias`/`confidence_score`/
`sample_size`, all default `None`, plus `engine_version` defaulting to
`LEARNING_ENGINE_VERSION`) rather than creating a second, competing
model — purely additive, so every Phase 60.6 caller/test keeps working
unmodified. `database/learning_models.py`'s `LearningRecordRow` and
the `learning_records` table (`database/models.py`) were extended in
lockstep, via an additive `ALTER TABLE` migration (`PRAGMA table_info()`-
guarded, same pattern `signals`/`users` already established) — no
existing row's meaning changes.
"""

import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Optional

LEARNING_ENGINE_VERSION = "60.7"


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
    htf_bias (Phase 60.7): the `context.htf_bias.HTFBiasResult.bias`
        value active at analysis time (e.g. "BULLISH"/"BEARISH"), as a
        plain string — relayed, not recomputed. None if no HTF bias
        was supplied.
    volatility_state (Phase 60.7): the `context.market_regime.MarketRegime`
        value, but ONLY when it is one of the two volatility-shaped
        regimes (`"HIGH_VOLATILITY"`/`"LOW_VOLATILITY"`) — every other
        regime (`TRENDING`/`RANGE`/etc.) says nothing about volatility
        specifically, so this stays None rather than reporting a
        misleading label for a non-volatility regime. Relayed, not
        recomputed.
    fundamental_bias (Phase 60.7): the
        `context.fundamental_context.FundamentalContextSnapshot.gold_bias`
        value active at analysis time (e.g. "BULLISH GOLD" per
        `context.fundamental_scoring.format_fundamental_score()`'s own
        convention, or the raw "BULLISH"/"BEARISH"/"NEUTRAL" value) —
        relayed, not recomputed.
    confidence_score (Phase 60.7): whatever single confidence measure
        the caller supplies at analysis time — deliberately not tied
        to one fixed source, since this codebase has several honest
        confidence values (signal quality score, AI confidence,
        `FundamentalScoreResult.confidence`) and none is "the"
        confidence for a trade. None if the caller supplies none. Not
        to be confused with `learning.confidence.compute_pattern_confidence()`
        (TASK 5) — that is a LOW/MEDIUM/HIGH classification over a
        *group* of records (sample size, consistency, recency,
        performance), a different, pattern-level question this
        per-record field does not answer.
    engine_version (Phase 60.7): which version of this learning
        pipeline produced the record — defaults to
        `LEARNING_ENGINE_VERSION` (`create_learning_record()`), so a
        future schema change can distinguish old records from new ones
        without guessing.
    sample_size (Phase 60.7): an honest hook, always None unless a
        caller explicitly annotates it — pattern-level sample counts
        live on `learning.pattern_detector.PatternInsight.occurrences`
        (computed across the whole dataset), not here; auto-computing
        a per-record sample size would need a full-table query at
        record-creation time, out of this task's own additive-schema
        scope.
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
    htf_bias: Optional[str] = None
    volatility_state: Optional[str] = None
    fundamental_bias: Optional[str] = None
    confidence_score: Optional[float] = None
    engine_version: Optional[str] = None
    sample_size: Optional[int] = None
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
    htf_bias: Optional[str] = None,
    volatility_state: Optional[str] = None,
    fundamental_bias: Optional[str] = None,
    confidence_score: Optional[float] = None,
    engine_version: Optional[str] = LEARNING_ENGINE_VERSION,
    sample_size: Optional[int] = None,
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
        htf_bias=htf_bias,
        volatility_state=volatility_state,
        fundamental_bias=fundamental_bias,
        confidence_score=confidence_score,
        engine_version=engine_version,
        sample_size=sample_size,
        created_at=datetime.now(timezone.utc),
    )
