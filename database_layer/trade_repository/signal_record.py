import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from signal_layer.signal_builder.models import SignalCandidate, SignalType
from decision_layer.decision_engine.models import TradeDecision
from risk_layer.risk_engine.risk_manager import RiskResult


@dataclass(frozen=True)
class SignalRecord:
    """
    Minimal persistence-identity wrapper around a single pipeline
    result. Gives a (SignalCandidate, TradeDecision, RiskResult)
    triple a signal_id and a created_at timestamp -- neither of which
    exists on those objects -- without modifying or duplicating any
    of their fields.

    strategy/rr_ratio/ai_decision/risk_status/risk_amount/
    signal_status (Phase 39) are flattened, persistence-ready copies
    of data already reachable via signal/decision/risk_result, and
    timeframe is supplied by the caller (no source on those objects)
    -- so SignalRepository.save_signal_record() never has to reach
    back into nested pipeline objects to populate the signals-table
    display columns.
    """
    signal_id: str
    created_at: datetime
    signal: SignalCandidate
    decision: TradeDecision
    risk_result: RiskResult
    strategy: str = "UNKNOWN"
    timeframe: str = "M15"
    rr_ratio: float = 0.0
    ai_decision: str = "N/A"
    risk_status: str = "N/A"
    risk_amount: float = 0.0
    signal_status: str = "NEW"


def _calculate_rr_ratio(signal: SignalCandidate) -> float:
    """
    Risk/reward ratio computed directly from entry/stop-loss/take-profit,
    independent of RiskResult.risk_reward (which RiskManager only
    computes for an APPROVE decision with an account_balance supplied).
    0.0 on a degenerate zero-division (entry == stop_loss) rather than
    raising.

        BUY:  (TP - Entry) / (Entry - SL)
        SELL: (Entry - TP) / (SL - Entry)
    """
    entry = signal.entry
    stop_loss = signal.stop_loss
    take_profit = signal.take_profit

    if signal.signal_type == SignalType.BUY:
        denominator = entry - stop_loss
        if denominator == 0:
            return 0.0
        return (take_profit - entry) / denominator

    if signal.signal_type == SignalType.SELL:
        denominator = stop_loss - entry
        if denominator == 0:
            return 0.0
        return (entry - take_profit) / denominator

    return 0.0


def create_signal_record(
    signal: SignalCandidate,
    decision: TradeDecision,
    risk_result: RiskResult,
    timeframe: str = "M15",
) -> SignalRecord:
    """
    Wraps a pipeline result triple with a fresh signal_id, UTC
    timestamp, and the Phase 39 flattened display fields. `timeframe`
    has no source on signal/decision/risk_result, so the caller (the
    pipeline, which knows the interval it queried) supplies it.
    """
    return SignalRecord(
        signal_id=str(uuid.uuid4()),
        created_at=datetime.now(timezone.utc),
        signal=signal,
        decision=decision,
        risk_result=risk_result,
        strategy=signal.strategy_name or "UNKNOWN",
        timeframe=timeframe,
        rr_ratio=_calculate_rr_ratio(signal),
        ai_decision=getattr(getattr(decision, "action", None), "value", "N/A"),
        risk_status="PASSED" if getattr(risk_result, "approved", False) else "BLOCKED",
        risk_amount=getattr(risk_result, "risk_amount", 0.0) or 0.0,
        signal_status="NEW",
    )
