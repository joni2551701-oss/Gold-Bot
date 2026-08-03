"""
Lifecycle Layer — Paper Trade (Phase 59 Preparation, TASK 2: Paper
Trading Contract Foundation).

Phase 59 validates the pipeline against the real market by paper
trading first -- simulating a trade's outcome without ever placing a
real order. This module is the standard shape for that simulation:

    Signal -> Decision APPROVED -> Paper Trade OPEN -> Monitor -> CLOSE -> Result

PaperTrade never calls a broker, never places a real order, and never
changes risk sizing -- see "What this module does NOT do" below.

Distinct from execution_layer/execution_engine/execution_engine.py and
execution_layer/execution_monitor/signal_lifecycle.py (both pre-existing, both untouched by
this phase): those live in the Trading-Safety-protected execution/
package, are both deliberately inert stubs (ExecutionEngine.dispatch()
and SignalLifecycle.transition() each always return a "Not
implemented" result), and execution_layer/execution_monitor/signal_lifecycle.py's own
SignalState enum (CREATED/SENT/ACKNOWLEDGED/CLOSED) describes Telegram
message delivery, not a trade's own lifecycle. PaperTrade is a new,
separate, simulation-only concept in a new top-level package -- it
never imports from or calls execution/, and does not make that
package's own stubs any less inert. Also distinct from
strategies/lifecycle/ (Phase A11, StrategyDefinition/StrategyRegistry
-- per-strategy metadata, unrelated to any individual trade) despite
the shared "lifecycle" word.

What this module does NOT do:
- Does not call a broker, MT5, or any execution/ code -- no real order
  is ever placed.
- Does not change risk sizing, RiskManager, or any Risk Manager output
  -- entry/stop_loss/take_profit are copied from an already-approved
  SignalSchema, never recomputed.
- Does not persist to the database -- no new table, no migration.
  PaperTrade exists only as an in-memory record in this phase, ready
  for a future, separately-approved persistence step (same posture as
  data_layer/live_data/market_data_snapshot.py, this phase's TASK 1).
- Does not decide APPROVE/REJECT -- create_paper_trade() requires an
  already-APPROVED SignalSchema; Decision Engine is untouched.
"""

import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from lifecycle.trade_state import TradeState

if TYPE_CHECKING:
    from signal_layer.signal_builder.schema import SignalSchema

# The Phase 59 Validation Report's own Result vocabulary
# (docs/PHASE59_VALIDATION.md's "Result" section: TP/SL/BE/expired) --
# deliberately NOT database/signal_repository.py's pre-existing
# ALLOWED_RESULTS ({"WIN","LOSS","BE","CANCELLED"}), since that set
# belongs to the real, persisted "signals" table (untouched by this
# phase) and already uses CANCELLED as a *result*, whereas PaperTrade
# already has CANCELLED as a *status* (TradeState) -- reusing it as a
# result too would be ambiguous. "EXPIRED" (a signal whose entry zone
# was never reached before the setup invalidated) has no equivalent in
# the signals-table vocabulary at all.
ALLOWED_PAPER_TRADE_RESULTS = ("TP", "SL", "BE", "EXPIRED")


@dataclass(frozen=True)
class PaperTrade:
    """
    trade_id: a real, generated identity (generate_trade_id()).
    signal_id: the originating SignalSchema.signal_id -- a required
        reference, never a copy of the signal itself.
    symbol/direction/entry/stop_loss/take_profit: copied directly from
        the SignalSchema this trade simulates -- never recomputed.
    status: one of TradeState -- see trade_state.py.
    result: one of ALLOWED_PAPER_TRADE_RESULTS, only set by
        close_paper_trade(); None until then.
    opened_at/closed_at: set only by open_paper_trade()/
        close_paper_trade() respectively; both None on a freshly
        created trade.
    created_at: when this record was built (create_paper_trade()).
    """
    trade_id: str
    signal_id: str
    symbol: str
    direction: str
    entry: float
    stop_loss: float
    take_profit: float
    status: TradeState = TradeState.CREATED
    result: Optional[str] = None
    opened_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        """JSON-safe dict -- status/result as plain strings, datetimes as ISO-8601."""
        data = asdict(self)
        data["status"] = self.status.value
        data["created_at"] = self.created_at.isoformat() if self.created_at else None
        data["opened_at"] = self.opened_at.isoformat() if self.opened_at else None
        data["closed_at"] = self.closed_at.isoformat() if self.closed_at else None
        return data


@dataclass(frozen=True)
class PaperTradeTransitionResult:
    """
    Never raises: an invalid transition (e.g. closing a trade that was
    never opened) produces PaperTradeTransitionResult(success=False,
    reason=...) with the ORIGINAL, unchanged trade returned in `trade`
    -- the same "structured result, never raise" convention as
    ValidationResult/RiskResult elsewhere in this codebase.
    """
    trade: PaperTrade
    success: bool
    reason: str


def generate_trade_id() -> str:
    """Same generation convention as every other Phase A/AC identity field (str(uuid.uuid4())) -- not a new scheme."""
    return str(uuid.uuid4())


def create_paper_trade(signal: 'SignalSchema') -> PaperTrade:
    """
    Builds a PaperTrade in TradeState.CREATED from an already-APPROVED
    SignalSchema (signal.decision == "APPROVED", entry/stop_loss/
    take_profit all present -- validate_signal() is expected to have
    already run upstream; this function itself does not re-validate
    Decision Engine's verdict, it only reads it). Raises ValueError if
    the signal is not eligible -- a genuine programmer error (calling
    this on a REJECTED/PENDING or price-incomplete signal), not a
    data-driven condition PaperTrade itself should silently tolerate.
    """
    if signal.decision != "APPROVED":
        raise ValueError(
            f"create_paper_trade() requires an APPROVED signal, got decision={signal.decision!r}"
        )
    if signal.entry_price is None or signal.stop_loss is None or signal.take_profit is None:
        raise ValueError("create_paper_trade() requires entry_price, stop_loss, and take_profit")

    return PaperTrade(
        trade_id=generate_trade_id(),
        signal_id=signal.signal_id,
        symbol=signal.symbol,
        direction=signal.direction,
        entry=signal.entry_price,
        stop_loss=signal.stop_loss,
        take_profit=signal.take_profit,
        status=TradeState.CREATED,
        created_at=datetime.now(timezone.utc),
    )


def open_paper_trade(trade: PaperTrade) -> PaperTradeTransitionResult:
    """CREATED -> OPEN only. Sets opened_at. Never raises."""
    if trade.status != TradeState.CREATED:
        return PaperTradeTransitionResult(
            trade=trade,
            success=False,
            reason=f"Cannot open a trade that is not CREATED (current status: {trade.status.value})",
        )

    opened = PaperTrade(
        trade_id=trade.trade_id,
        signal_id=trade.signal_id,
        symbol=trade.symbol,
        direction=trade.direction,
        entry=trade.entry,
        stop_loss=trade.stop_loss,
        take_profit=trade.take_profit,
        status=TradeState.OPEN,
        result=trade.result,
        opened_at=datetime.now(timezone.utc),
        closed_at=trade.closed_at,
        created_at=trade.created_at,
    )
    return PaperTradeTransitionResult(trade=opened, success=True, reason="")


def close_paper_trade(trade: PaperTrade, result: str) -> PaperTradeTransitionResult:
    """OPEN -> CLOSED only. `result` must be one of ALLOWED_PAPER_TRADE_RESULTS. Sets closed_at. Never raises."""
    if trade.status != TradeState.OPEN:
        return PaperTradeTransitionResult(
            trade=trade,
            success=False,
            reason=f"Cannot close a trade that is not OPEN (current status: {trade.status.value})",
        )
    if result not in ALLOWED_PAPER_TRADE_RESULTS:
        return PaperTradeTransitionResult(
            trade=trade,
            success=False,
            reason=f"result must be one of {ALLOWED_PAPER_TRADE_RESULTS}, got {result!r}",
        )

    closed = PaperTrade(
        trade_id=trade.trade_id,
        signal_id=trade.signal_id,
        symbol=trade.symbol,
        direction=trade.direction,
        entry=trade.entry,
        stop_loss=trade.stop_loss,
        take_profit=trade.take_profit,
        status=TradeState.CLOSED,
        result=result,
        opened_at=trade.opened_at,
        closed_at=datetime.now(timezone.utc),
        created_at=trade.created_at,
    )
    return PaperTradeTransitionResult(trade=closed, success=True, reason="")


def cancel_paper_trade(trade: PaperTrade) -> PaperTradeTransitionResult:
    """CREATED or OPEN -> CANCELLED. Sets closed_at; result stays None (a cancellation is not a TP/SL/BE/EXPIRED outcome). Never raises."""
    if trade.status not in (TradeState.CREATED, TradeState.OPEN):
        return PaperTradeTransitionResult(
            trade=trade,
            success=False,
            reason=f"Cannot cancel a trade that is already {trade.status.value}",
        )

    cancelled = PaperTrade(
        trade_id=trade.trade_id,
        signal_id=trade.signal_id,
        symbol=trade.symbol,
        direction=trade.direction,
        entry=trade.entry,
        stop_loss=trade.stop_loss,
        take_profit=trade.take_profit,
        status=TradeState.CANCELLED,
        result=trade.result,
        opened_at=trade.opened_at,
        closed_at=datetime.now(timezone.utc),
        created_at=trade.created_at,
    )
    return PaperTradeTransitionResult(trade=cancelled, success=True, reason="")
