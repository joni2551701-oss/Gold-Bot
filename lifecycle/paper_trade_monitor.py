"""
Lifecycle Layer — Paper Trade Monitor (Phase 59.4, TASK 2: Paper
Trading Engine — "ulash", connecting the pieces).

lifecycle/paper_trade.py (Phase 59 Preparation) already built the
state machine (CREATED/OPEN/CLOSED/CANCELLED — the Director's own
"RUNNING" is this codebase's real "OPEN" state, the same value under a
different label, not a new state) and the pure transition functions.
What was missing, named explicitly in lifecycle/README.md's own
"Future Roadmap": "a live monitor loop (checking OPEN trades against
fresh candles to decide TP/SL/EXPIRED) ... remains unimplemented."
This module is that monitor — still zero broker calls, pure
arithmetic over an already-fetched candle list, reusing
close_paper_trade() for the actual transition rather than
duplicating it.

EXPIRED, per lifecycle/paper_trade.py's own documented definition
("a signal whose entry zone was never reached before the setup
invalidated"), is about entry never being touched — not a time-based
timeout. No arbitrary duration threshold is invented here: the
monitoring "window" is simply however many candles the caller
supplies. If the entry price is never touched by any candle in that
window, the trade is EXPIRED; if entry is touched but neither TP nor
SL, the trade is still OPEN — genuinely undecided, not expired.

Ambiguity rule: if a single candle's high/low range covers both TP and
SL (a real possibility on a volatile candle), SL is assumed hit first
— the conservative, standard backtesting convention, disclosed here
rather than silently picking the more favorable outcome.
"""

from typing import List, TYPE_CHECKING

from lifecycle.paper_trade import PaperTradeTransitionResult, close_paper_trade
from lifecycle.trade_state import TradeState

if TYPE_CHECKING:
    from data_layer.providers.twelve_data_client import Candle
    from lifecycle.paper_trade import PaperTrade


def check_paper_trade_against_candles(
    trade: 'PaperTrade',
    candles: List['Candle'],
) -> PaperTradeTransitionResult:
    """
    Walks `candles` in the order given (the caller is responsible for
    chronological ordering, same convention every other candle-consuming
    function in this codebase relies on) looking for the first candle
    that touches the trade's entry price, then the first candle
    (starting from that same one) that touches take_profit or
    stop_loss. Returns the result of calling close_paper_trade() for a
    TP/SL/EXPIRED outcome, or the original trade unchanged
    (success=True, a descriptive reason) if it is still genuinely
    undecided. Never raises: `trade` not being OPEN, or an empty
    `candles` list, are both handled as ordinary "nothing to report"
    conditions, matching every other PaperTradeTransitionResult
    producer's own fail-safe posture.

    IMPORTANT — this function is stateless per call and has no memory
    of prior invocations: `candles` must be the FULL window from
    `trade.opened_at` onward (or at least back to before entry could
    plausibly have triggered), not just "whatever is new since the
    last check." Calling this once per pipeline cycle with only the
    latest one or two candles will incorrectly report EXPIRED the very
    first time entry hasn't triggered yet, instead of giving the setup
    its real remaining window. A caller that wants incremental,
    per-cycle monitoring must accumulate and re-pass the trade's full
    candle history itself (e.g. via database/raw_candle_repository.py,
    Phase 59.3) -- this module does not do that accumulation.
    """
    if trade.status != TradeState.OPEN:
        return PaperTradeTransitionResult(
            trade=trade,
            success=False,
            reason=f"Cannot monitor a trade that is not OPEN (current status: {trade.status.value})",
        )

    entry_touched = False

    for candle in candles:
        if not entry_touched:
            if candle.low <= trade.entry <= candle.high:
                entry_touched = True
            else:
                continue

        if trade.direction == "BUY":
            hit_take_profit = candle.high >= trade.take_profit
            hit_stop_loss = candle.low <= trade.stop_loss
        elif trade.direction == "SELL":
            hit_take_profit = candle.low <= trade.take_profit
            hit_stop_loss = candle.high >= trade.stop_loss
        else:
            hit_take_profit = False
            hit_stop_loss = False

        if hit_stop_loss:
            # Covers both the SL-only case and the ambiguous
            # both-touched-in-one-candle case -- see module docstring.
            return close_paper_trade(trade, "SL")
        if hit_take_profit:
            return close_paper_trade(trade, "TP")

    if not entry_touched:
        return close_paper_trade(trade, "EXPIRED")

    return PaperTradeTransitionResult(
        trade=trade,
        success=True,
        reason="Still OPEN -- entry touched, no TP/SL hit yet in the given candle window",
    )
