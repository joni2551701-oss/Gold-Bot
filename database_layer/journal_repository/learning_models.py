"""
Database Layer — Learning Record persistence model (Phase 60.6:
Learning Loop Foundation, TASK 5).

`LearningRecordRow` deliberately does not reuse `learning.models.LearningRecord`
directly -- same disambiguation-by-naming discipline this codebase has
used repeatedly (`RawCandle` vs. `data_layer.providers.twelve_data_client.Candle`,
`FundamentalContextSnapshot` vs. `FundamentalSnapshot`,
`ExecutionSimulationResult` vs. `ExecutionResult`): every existing
repository in this codebase owns its own row-shaped model
(`database_layer.trade_repository.signal_record.SignalRecord`, `database_layer.market_repository.raw_candle_models.RawCandle`,
`database_layer.audit_log.audit_log_models.AuditLogEntry`), never imports a domain
type from a non-`database/` package directly. `LearningRecordRow`
mirrors `learning.models.LearningRecord`'s fields exactly, plus the one
field that domain type intentionally excludes: a real database `id`
(see `LearningRecord`'s own docstring for why).

Phase 60.7 (Adaptive Intelligence Layer Foundation, TASK 3) extends
this same `LearningRecordRow` with the same six additional fields
`learning.models.LearningRecord` gained in lockstep
(`htf_bias`/`volatility_state`/`fundamental_bias`/`confidence_score`/
`engine_version`/`sample_size`) — see that module's own docstring for
each field's meaning.
"""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Optional


@dataclass(frozen=True)
class LearningRecordRow:
    """
    Mirrors the 'learning_records' table row shape.
    id: the real, autoincrement database identity -- None until a row
        has actually been inserted and re-read (same convention every
        other Phase 59.x/60.x model that carries a real db id uses).
    record_id: the originating `learning.models.LearningRecord.record_id`
        -- unique, generated before persistence.
    trade_id/signal_id: the originating `PaperTrade.trade_id`/
        `signal_id` -- required.
    strategy_name/market_phase/session/timeframe/result/r_multiple/
        failure_type/success_pattern: relayed directly from the
        `LearningRecord` this row persists -- never recomputed here.
    created_at: when this record was built (not when it was inserted
        -- relayed from the originating `LearningRecord`).
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
    id: Optional[int] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat() if self.created_at else None
        return data


def create_learning_record_row(
    record_id: str,
    trade_id: str,
    signal_id: str,
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
    engine_version: Optional[str] = None,
    sample_size: Optional[int] = None,
) -> LearningRecordRow:
    """Pure, deterministic factory -- stamps created_at, same convention as every other create_X() factory in this codebase. `id` stays None until the repository inserts and re-reads it."""
    return LearningRecordRow(
        record_id=record_id,
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
