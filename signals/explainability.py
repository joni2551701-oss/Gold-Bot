"""
Signal Layer — Explainability foundation (Phase A9).

Turns a signal candidate's already-computed context into human-
readable reasons ("why did this signal fire?"). It does NOT generate
a signal, does NOT approve one, and does NOT compute a new confidence
value -- see docs/EXPLAINABILITY.md for the full contract.

Reuses existing detection output rather than re-deriving it:
- signals.signal_quality.SignalQualityResult.criteria_met (Phase A4)
  is the primary reason source -- each already-computed criterion
  name (HTF_ALIGNED, STRUCTURE_ALIGNED, LIQUIDITY_SWEPT,
  ORDER_BLOCK_ALIGNED, FVG_ALIGNED) is translated into a human-
  readable phrase via _REASON_PHRASES. No alignment check is
  re-implemented here.
- context.wyckoff.WyckoffEvent (Phase A5), context.session.SessionEvent
  (Phase A6), and context.market_regime.MarketRegimeResult (Phase A7)
  supply three additional reasons Signal Quality Score's 5 criteria
  don't cover -- read directly from ContextSnapshot, not re-detected.
- SignalCandidate.confidence is relayed as-is (multiplied by 100 for
  a percentage display, matching telegram/signal_formatter.py's own
  convention) -- never recomputed.
"""

from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Sequence

from signals.models import SignalType
from context.wyckoff import WyckoffPhase
from context.market_regime import MarketRegime, RegimeDirection

if TYPE_CHECKING:
    from signals.models import SignalCandidate
    from signals.signal_quality import SignalQualityResult
    from context.context_orchestrator import ContextSnapshot


@dataclass(frozen=True)
class SignalExplanation:
    """
    direction: "BUY"/"SELL"/"NONE" (SignalCandidate.signal_type.value).
    reasons: human-readable strings, in the order they were found --
        Signal Quality's criteria first, then Wyckoff/Session/Market
        Regime if directionally relevant. Empty if nothing supports
        the signal (never an error).
    quality: the letter grade (SignalQualityResult.grade.value).
    confidence: SignalCandidate.confidence * 100 -- relayed, not
        recomputed (0-100, matching every other Phase A output's
        convention).
    """
    direction: str
    reasons: Sequence[str]
    quality: str
    confidence: float


def _direction_word(signal_type: SignalType) -> str:
    return "bullish" if signal_type == SignalType.BUY else "bearish"


def _structure_word(signal_type: SignalType) -> str:
    return "HH/HL" if signal_type == SignalType.BUY else "LH/LL"


def _reason_phrase(criterion: str, signal_type: SignalType) -> str:
    """Translates one of Signal Quality Score's criteria_met names into a direction-aware, human-readable phrase."""
    phrases = {
        "HTF_ALIGNED": f"HTF {_direction_word(signal_type)} bias",
        "STRUCTURE_ALIGNED": f"{_structure_word(signal_type)} structure",
        "LIQUIDITY_SWEPT": "Liquidity sweep detected",
        "ORDER_BLOCK_ALIGNED": "Order block reaction",
        "FVG_ALIGNED": "FVG reaction",
    }
    return phrases.get(criterion, criterion)


def _session_label(session) -> str:
    return session.value.replace("_", " ").title()


def _wyckoff_reason(context: 'ContextSnapshot', signal_type: SignalType) -> List[str]:
    """A recent Wyckoff event only counts as a reason when its phase agrees with the signal's direction."""
    if not context.wyckoff_events:
        return []
    latest = context.wyckoff_events[-1]
    agrees = (
        (signal_type == SignalType.BUY and latest.phase == WyckoffPhase.ACCUMULATION)
        or (signal_type == SignalType.SELL and latest.phase == WyckoffPhase.DISTRIBUTION)
    )
    if not agrees:
        return []
    return [f"Wyckoff {latest.type.value.title()} ({latest.phase.value.title()})"]


def _session_reason(context: 'ContextSnapshot') -> List[str]:
    """Session is reported as context regardless of direction -- unlike Wyckoff/Regime, it has no bullish/bearish reading of its own."""
    if not context.session_events:
        return []
    current_session = context.session_events[-1].session
    return [f"{_session_label(current_session)} session"]


def _market_regime_reason(context: 'ContextSnapshot', signal_type: SignalType) -> List[str]:
    """A TRENDING regime only counts as a reason when its direction agrees with the signal's."""
    regime_result = context.market_regime
    if regime_result.regime != MarketRegime.TRENDING:
        return []
    agrees = (
        (signal_type == SignalType.BUY and regime_result.direction == RegimeDirection.BULLISH)
        or (signal_type == SignalType.SELL and regime_result.direction == RegimeDirection.BEARISH)
    )
    if not agrees:
        return []
    return [f"Market regime: {regime_result.regime.value} ({regime_result.direction.value})"]


def explain_signal(
    signal: 'SignalCandidate',
    context: 'ContextSnapshot',
    quality: 'SignalQualityResult',
) -> SignalExplanation:
    """
    Never raises: a signal_type of NONE, an empty context (no wyckoff/
    session events, an UNKNOWN market_regime), or an empty
    quality.criteria_met all simply produce fewer reasons -- an empty
    `reasons` list is a valid result, not an error.
    """
    reasons: List[str] = [_reason_phrase(name, signal.signal_type) for name in quality.criteria_met]
    reasons.extend(_wyckoff_reason(context, signal.signal_type))
    reasons.extend(_session_reason(context))
    reasons.extend(_market_regime_reason(context, signal.signal_type))

    return SignalExplanation(
        direction=signal.signal_type.value,
        reasons=tuple(reasons),
        quality=quality.grade.value,
        confidence=round(signal.confidence * 100, 2),
    )
