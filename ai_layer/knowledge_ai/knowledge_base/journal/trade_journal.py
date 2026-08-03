from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from signal_layer.signal_builder.models import SignalType  # Reusing established SignalType


class TradeOutcome(Enum):
    WIN = "WIN"
    LOSS = "LOSS"
    BREAK_EVEN = "BREAK_EVEN"


class DecisionType(Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    NO_TRADE = "NO_TRADE"


@dataclass(frozen=True)
class TradeJournalRecord:
    """
    An immutable, type-safe record of a completed trade.

    TASK-AI-000A (AI Architecture Cleanup, Stage 2): renamed from
    `TradeJournalEntry` to `TradeJournalRecord`. A second, unrelated
    class named `TradeJournalEntry` (the Phase 66.2 *narrative* journal
    entry) lives at `ai_layer.knowledge_ai.knowledge_base.trade_journal.models.TradeJournalEntry`; the
    two shared a bare class name, a real duplicate-name hazard for any
    reader importing by name alone. This older,
    `signals.SignalType`-coupled *completed-trade record* takes the
    `...Record` name; the newer narrative *entry* keeps
    `TradeJournalEntry`. Fields and the `create_journal_entry()`
    factory are unchanged -- only the class name.
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
) -> TradeJournalRecord:
    """
    Pure, deterministic factory function using type-safe Enums.
    """
    return TradeJournalRecord(
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
