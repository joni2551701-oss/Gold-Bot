"""
Analytics Layer — Signal Performance (Phase 59 Preparation, TASK 3:
Trading Performance Schema Foundation).

NOT the same thing as performance/ (Phase A19): that package measures
*system* performance (pipeline stage duration, API latency) via
PerformanceMetric/PerformanceCollector/PerformanceTimer -- pure code
timing, no trading outcome involved. This package measures *trading*
performance -- did a signal make money, how many R did it realize, in
which strategy/session/market phase -- an entirely different question,
explicitly kept separate per this task's own brief.

Also distinct from monitoring/performance.py's pre-existing
PerformanceTracker: that class already computes win/loss/win_rate,
grouped by strategy_name, from the persisted "signals" database table
(via SignalRepository.get_open_signals()/get_closed_signals(), reading
the "result" column set by update_signal_result()) -- a real, working,
if narrower, trading-performance calculator, wired to nothing today.
SignalPerformance (this module) is a richer per-signal schema
(r_multiple, session, market_phase, context_id -- fields the "signals"
table has no columns for at all) built from already-computed
SignalSchema/PaperTrade objects, not from the database. This module
does not read the database, does not call SignalRepository, and does
not replace PerformanceTracker; strategy_report.py (same package)
intentionally reuses PerformanceTracker's own WIN/(WIN+LOSS) win-rate
convention rather than inventing a different formula for the same
question -- see strategy_report.py's own docstring.

A standardization layer, like SignalSchema/ContextSnapshotSchema
before it: computes nothing new except r_multiple (a pure arithmetic
derivation from already-approved price levels, not a risk-sizing
change -- risk/risk_manager.py is untouched). profit_loss stays an
honest None hook -- no lot-value/account-currency PnL computation
exists anywhere in this codebase today, and building one would need
sizing/currency-conversion logic this task's own boundary
("Risk o'zgarmaydi") puts out of scope.
"""

import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

from lifecycle.trade_state import TradeState

if TYPE_CHECKING:
    from lifecycle.paper_trade import PaperTrade
    from signals.schema import SignalSchema


@dataclass(frozen=True)
class SignalPerformance:
    """
    Identity: performance_id (generate_performance_id()), signal_id
        (the originating SignalSchema.signal_id, required).
    Strategy reference: strategy_id -- SignalSchema.strategy_name's
        real value (e.g. "LIQUIDITY_SWEEP_STRATEGY"). Not a new field
        anywhere: the same "strategy_name already equals strategy_id"
        convention docs/SIGNAL_SCHEMA.md's AC-03 update already
        established.
    Context reference: context_id -- SignalSchema.context_id, real as
        of AC-03. session/market_phase -- read from a
        ContextSnapshotSchema/MarketPhaseResult when supplied by the
        caller, else None (this module never (re)computes context).
    timeframe (Phase 59 Real Market Validation Foundation, TASK 6):
        SignalSchema.timeframe's own value (e.g. "M15"), copied
        directly -- not recomputed, not a new concept. Lets
        strategy_report.filter_performances() slice a strategy's
        results by timeframe, one of the four dimensions this task's
        own brief names (strategy_id, market_phase, session,
        timeframe).
    Result: result -- one of lifecycle.paper_trade.ALLOWED_PAPER_TRADE_RESULTS
        ("TP"/"SL"/"BE"/"EXPIRED"), read from a closed PaperTrade, OR
        "CANCELLED" (Phase 59.4, TASK 1 -- derived from
        PaperTrade.status == TradeState.CANCELLED, since a cancelled
        trade never gets a result via close_paper_trade()). None if
        the trade hasn't closed/cancelled (or no PaperTrade was
        supplied).
    profit_loss: always None in this phase -- an honest hook, no PnL
        computation exists anywhere in this codebase (see module
        docstring).
    r_multiple: the realized risk-multiple, using the SAME formula
        database/signal_record.py's _calculate_rr_ratio() already uses
        for the *planned* R (a small, deliberate, documented
        duplication -- see compute_r_multiple()'s own docstring for
        why it is not imported from there instead), applied against
        whichever price level `result` says was hit. None when result
        is None or "EXPIRED" (no R was realized).
    duration: seconds between PaperTrade.opened_at and closed_at, when
        both are known; else None.
    created_at: when this record was built.
    """
    performance_id: str
    signal_id: str
    strategy_id: Optional[str] = None
    context_id: Optional[str] = None
    result: Optional[str] = None
    profit_loss: Optional[float] = None
    r_multiple: Optional[float] = None
    duration: Optional[float] = None
    session: Optional[str] = None
    market_phase: Optional[str] = None
    timeframe: Optional[str] = None
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        data = asdict(self)
        data["created_at"] = self.created_at.isoformat() if self.created_at else None
        return data

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


def generate_performance_id() -> str:
    """Same generation convention as every other Phase A/AC/Phase-59 identity field (str(uuid.uuid4())) -- not a new scheme."""
    return str(uuid.uuid4())


def compute_r_multiple(
    direction: str,
    entry: float,
    stop_loss: float,
    take_profit: float,
    result: Optional[str],
) -> Optional[float]:
    """
    A pure, deterministic arithmetic derivation -- not a new risk
    formula, and it never touches risk/risk_manager.py. Deliberately
    mirrors database/signal_record.py's _calculate_rr_ratio() (BUY:
    (TP-Entry)/(Entry-SL); SELL: (Entry-TP)/(SL-Entry)) rather than
    importing it, since that function is a private, database-layer
    helper and analytics/ has no reason to depend on database/ for a
    three-line formula -- the same small, disclosed duplication this
    codebase already accepted for Wyckoff-vs-AMD
    (context_layer/wyckoff/wyckoff.py's own "Relationship to AMD" docstring) and
    Data Quality-vs-market_data.py (data_layer/data_validation/data_quality.py's own
    docstring).

    "TP" -> the planned R actually realized (using take_profit).
    "SL" -> -1.0 by definition (stop_loss always marks -1R).
    "BE" -> 0.0.
    "EXPIRED" or None -> None (no R was realized; the trade never
        resolved to a price-based outcome).
    """
    if result not in ("TP", "SL", "BE"):
        return None

    if result == "SL":
        return -1.0
    if result == "BE":
        return 0.0

    # result == "TP"
    if direction == "BUY":
        denominator = entry - stop_loss
        if denominator == 0:
            return 0.0
        return (take_profit - entry) / denominator
    if direction == "SELL":
        denominator = stop_loss - entry
        if denominator == 0:
            return 0.0
        return (entry - take_profit) / denominator
    return None


def compute_signal_performance(
    signal: 'SignalSchema',
    *,
    paper_trade: Optional['PaperTrade'] = None,
    session: Optional[str] = None,
    market_phase: Optional[str] = None,
) -> SignalPerformance:
    """
    Builds a SignalPerformance from an already-computed SignalSchema,
    plus optional already-computed PaperTrade/session/market_phase.
    Never raises: a signal with no linked PaperTrade produces a record
    with result/r_multiple/duration all None, not an exception.

    Phase 59.4 (TASK 1) fix: a CANCELLED PaperTrade previously produced
    result=None here (PaperTrade.result stays unset by
    cancel_paper_trade() -- CANCELLED is a status, not one of
    ALLOWED_PAPER_TRADE_RESULTS). This left "Cancelled" invisible to
    any report built from SignalPerformance, even though this task's
    own brief explicitly lists it as a displayable Result value
    alongside TP/SL/Expired. result now reads "CANCELLED" directly off
    trade.status for that one case -- still never fabricated, since
    CANCELLED is the trade's own real, already-set status.
    """
    result = None
    if paper_trade is not None:
        if paper_trade.status == TradeState.CANCELLED:
            result = "CANCELLED"
        else:
            result = paper_trade.result

    duration = None
    if paper_trade is not None and paper_trade.opened_at is not None and paper_trade.closed_at is not None:
        duration = (paper_trade.closed_at - paper_trade.opened_at).total_seconds()

    r_multiple = None
    if (
        result is not None
        and signal.entry_price is not None
        and signal.stop_loss is not None
        and signal.take_profit is not None
    ):
        r_multiple = compute_r_multiple(
            signal.direction, signal.entry_price, signal.stop_loss, signal.take_profit, result
        )

    return SignalPerformance(
        performance_id=generate_performance_id(),
        signal_id=signal.signal_id,
        strategy_id=signal.strategy_name,
        context_id=signal.context_id,
        result=result,
        profit_loss=None,
        r_multiple=r_multiple,
        duration=duration,
        session=session,
        market_phase=market_phase,
        timeframe=signal.timeframe,
        created_at=datetime.now(timezone.utc),
    )
