import uuid
from dataclasses import dataclass
from datetime import datetime, timezone

from signals.models import SignalCandidate
from decision.models import TradeDecision
from risk.risk_manager import RiskResult


@dataclass(frozen=True)
class SignalRecord:
    """
    Minimal persistence-identity wrapper around a single pipeline
    result. Gives a (SignalCandidate, TradeDecision, RiskResult)
    triple a signal_id and a created_at timestamp -- neither of which
    exists on those objects -- without modifying or duplicating any
    of their fields.
    """
    signal_id: str
    created_at: datetime
    signal: SignalCandidate
    decision: TradeDecision
    risk_result: RiskResult


def create_signal_record(
    signal: SignalCandidate,
    decision: TradeDecision,
    risk_result: RiskResult,
) -> SignalRecord:
    """Wraps a pipeline result triple with a fresh signal_id and UTC timestamp."""
    return SignalRecord(
        signal_id=str(uuid.uuid4()),
        created_at=datetime.now(timezone.utc),
        signal=signal,
        decision=decision,
        risk_result=risk_result,
    )
