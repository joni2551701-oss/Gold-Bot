"""
Learning Layer — Trade Outcome Analyzer (Phase 60.6: Learning Loop
Foundation, TASK 3).

Explains a single already-closed trade: what happened, which
already-detected structural facts support that outcome, and one short
takeaway. Purely observational -- reads `lifecycle.paper_trade.PaperTrade`
(the trade's own real result), `context.context_orchestrator.ContextSnapshot`
(already-detected BOS/CHoCH/liquidity/OB/FVG events), an optional
`context.htf_bias.HTFBiasResult`, and an optional
`analytics.signal_performance.SignalPerformance` (session/market_phase/
timeframe) -- and computes nothing these modules haven't already
detected. No new structure detection, no new HTF bias computation, no
new R-multiple formula.

Per this whole phase's hard boundary: `analyze_trade_result()` never
approves/rejects anything, never calls `decision/`, `risk/`, or
`strategies/`, and nothing downstream reads its output back into a
live decision path -- `observe -> analyze -> report`, not
`observe -> mutate`.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Sequence, TYPE_CHECKING

from context_layer.trend.htf_bias import HTFBias

if TYPE_CHECKING:
    from context_layer.context_engine.context_orchestrator import ContextSnapshot
    from context_layer.trend.htf_bias import HTFBiasResult
    from analytics.signal_performance import SignalPerformance
    from lifecycle.paper_trade import PaperTrade


@dataclass(frozen=True)
class TradeAnalysis:
    """
    trade_id: the analyzed `PaperTrade.trade_id`.
    result: relayed directly from `PaperTrade.result` -- never
        recomputed.
    reasons: a list of short, structural observations already detected
        by `context/` (e.g. "Against HTF bias", "No liquidity sweep
        observed") -- empty when no `context`/`htf_bias` was supplied,
        or when nothing notable was detected either way. Matches the
        Director's own worked example shape.
    lesson: one short, synthesized takeaway sentence built from
        `reasons` -- never fabricated beyond what `reasons` already
        states; see `_synthesize_lesson()`.
    """
    trade_id: str
    result: Optional[str]
    reasons: List[str] = field(default_factory=list)
    lesson: str = "No specific lesson available."


def _htf_alignment_reason(direction: str, htf_bias: 'HTFBiasResult') -> Optional[str]:
    """None when htf_bias itself is NEUTRAL/UNKNOWN -- an undecided HTF bias supports neither "aligned" nor "against"."""
    if htf_bias.bias not in (HTFBias.BULLISH, HTFBias.BEARISH):
        return None

    aligned = (
        (direction == "BUY" and htf_bias.bias == HTFBias.BULLISH)
        or (direction == "SELL" and htf_bias.bias == HTFBias.BEARISH)
    )
    return "HTF bias aligned" if aligned else "Against HTF bias"


def _structural_reasons(context: 'ContextSnapshot', is_loss: bool, is_win: bool) -> List[str]:
    """Reads already-detected event presence only -- never re-derives BOS/CHoCH/liquidity/OB/FVG itself."""
    reasons: List[str] = []
    has_structural_break = bool(context.bos_events) or bool(context.choch_events)
    has_liquidity_sweep = bool(context.liquidity_sweeps)
    has_order_block = bool(context.order_blocks)
    has_fvg = bool(context.fair_value_gaps)

    if is_loss:
        if not has_structural_break:
            reasons.append("No confirmed structural break")
        if not has_liquidity_sweep:
            reasons.append("No liquidity sweep observed")
    elif is_win:
        if has_liquidity_sweep:
            reasons.append("Liquidity sweep present")
        if has_order_block:
            reasons.append("OB reaction present")
        if has_fvg:
            reasons.append("FVG fill")

    return reasons


def _synthesize_lesson(is_loss: bool, is_win: bool, reasons: Sequence[str], session: Optional[str]) -> str:
    """
    One disclosed pattern match for the Director's own worked example
    shape ("Avoid London reversal without BOS"): a loss with both
    "Against HTF bias" and "No confirmed structural break" present,
    with a known session, produces exactly that sentence shape.
    Anything else degrades to a generic, still-honest summary of
    `reasons` -- never invents a lesson `reasons` doesn't support.
    """
    if is_loss and "Against HTF bias" in reasons and "No confirmed structural break" in reasons and session:
        return f"Avoid {session} reversal without BOS"
    if is_loss and reasons:
        return f"Review: {', '.join(reasons)}"
    if is_win and reasons:
        return f"Repeat: {', '.join(reasons)}"
    return "No specific lesson available."


def analyze_trade_result(
    paper_trade: 'PaperTrade',
    context: Optional['ContextSnapshot'] = None,
    performance: Optional['SignalPerformance'] = None,
    htf_bias: Optional['HTFBiasResult'] = None,
) -> TradeAnalysis:
    """
    Never raises: a `paper_trade` with no `context`/`performance`/
    `htf_bias` supplied produces a `TradeAnalysis` with empty `reasons`
    and the default "No specific lesson available." message, not an
    exception.
    """
    is_loss = paper_trade.result == "SL"
    is_win = paper_trade.result == "TP"

    reasons: List[str] = []
    if htf_bias is not None:
        alignment_reason = _htf_alignment_reason(paper_trade.direction, htf_bias)
        if alignment_reason is not None:
            reasons.append(alignment_reason)

    if context is not None:
        reasons.extend(_structural_reasons(context, is_loss, is_win))

    session = performance.session if performance is not None else None
    lesson = _synthesize_lesson(is_loss, is_win, reasons, session)

    return TradeAnalysis(
        trade_id=paper_trade.trade_id,
        result=paper_trade.result,
        reasons=reasons,
        lesson=lesson,
    )
