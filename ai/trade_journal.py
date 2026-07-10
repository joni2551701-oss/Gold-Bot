from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from signal.models import SignalType  # Reusing established SignalType

class TradeOutcome(Enum):
    WIN = "WIN"
    LOSS = "LOSS"
    BREAK_EVEN = "BREAK_EVEN"

class DecisionType(Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    NO_TRADE = "NO_TRADE"

@dataclass(frozen=True)
class TradeJournalEntry:
    """
    An immutable, type-safe record of a completed trade.
    """
    signal_id: str
    strategy_name: str
    signal_type: SignalType
    technical_score: float
    ai_confidence: float
    decision: DecisionType
    entry: float
    stop_loss: float
    take_profit: float
    exit_price: float
    pnl: float
    rr: float
    outcome: TradeOutcome
    timestamp: datetime
    notes: str

def create_journal_entry(
    signal_id: str,
    strategy_name: str,
    signal_type: SignalType,
    technical_score: float,
    ai_confidence: float,
    decision: DecisionType,
    entry: float,
    stop_loss: float,
    take_profit: float,
    exit_price: float,
    pnl: float,
    rr: float,
    outcome: TradeOutcome,
    timestamp: datetime,
    notes: str = ""
) -> TradeJournalEntry:
    """
    Pure, deterministic factory function using type-safe Enums.
    """
    return TradeJournalEntry(
        signal_id=signal_id,
        strategy_name=strategy_name,
        signal_type=signal_type,
        technical_score=technical_score,
        ai_confidence=ai_confidence,
        decision=decision,
        entry=entry,
        stop_loss=stop_loss,
        take_profit=take_profit,
        exit_price=exit_price,
        pnl=pnl,
        rr=rr,
        outcome=outcome,
        timestamp=timestamp,
        notes=notes
    )
