"""
Signal Layer — Signal Quality Score (Phase A4).

Grades a SignalCandidate's alignment with existing SMC context
(HTF Bias, Structure, Liquidity, Order Blocks, Fair Value Gaps) into a
letter grade (A+/A/B/C). It does NOT generate a signal, does NOT
approve/reject a trade, and does NOT feed into DecisionEngine.evaluate()
in this phase -- see docs/SIGNAL_QUALITY.md for the full contract and
signals/README.md for what it does not do.

Only real, already-computed inputs are used: Session and Volume (both
named in the Phase A4 roadmap sketch) are deliberately NOT included --
Session Intelligence doesn't exist yet (planned as a later phase) and
this codebase has no volume data source at all (Twelve Data's candle
payload is OHLC-only). Both are documented, named future-extension
points in docs/SIGNAL_QUALITY.md, not faked with a placeholder score.

Reuses existing detection output rather than duplicating it:
- context.market_structure.most_recent_bias() (Phase A4: extracted
  from context_layer/trend/htf_bias.py's per-timeframe classification, now shared
  by both) reads ContextSnapshot.structure -- no new structure
  detection.
- ContextSnapshot.liquidity_sweeps, .order_blocks, .fair_value_gaps
  (context_orchestrator.py, unchanged) supply the other three
  criteria -- no new liquidity/OB/FVG detection.
- HTFBiasResult (context_layer/trend/htf_bias.py, Phase A2) supplies the HTF
  criterion -- no new HTF computation.
"""

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Callable, Optional, Sequence, Tuple

from context_layer.liquidity.liquidity import LiquidityType
from context_layer.order_block.order_block import OrderBlockType
from context_layer.fair_value_gap.fvg import FvgType
from context_layer.market_structure.market_structure import most_recent_bias
from context_layer.trend.htf_bias import HTFBias
from signals.models import SignalType
from core_layer.logger.logger import setup_logger

if TYPE_CHECKING:
    from signals.models import SignalCandidate
    from context_layer.context_engine.context_orchestrator import ContextSnapshot
    from context_layer.trend.htf_bias import HTFBiasResult

logger = setup_logger("SignalQualityEngine")


class QualityGrade(Enum):
    """Letter grade only -- never a trade action."""
    A_PLUS = "A+"
    A = "A"
    B = "B"
    C = "C"


@dataclass(frozen=True)
class SignalQualityResult:
    """
    Immutable signal-quality snapshot for one SignalCandidate.

    grade: QualityGrade (A+/A/B/C), derived from `score` (see
        _grade_for_score()).
    score: 0-100, `criteria_met_count / criteria_total * 100`.
    criteria_met: names of the criteria that passed, for
        explainability (e.g. ("HTF_ALIGNED", "LIQUIDITY_SWEPT")).
    criteria_total: always 5 today -- the 5 real, currently-available
        criteria. Session/Volume are not counted (see module
        docstring) -- criteria_total is exposed explicitly, not
        hardcoded to 5 in a caller, so a future phase adding a real
        Session or Volume criterion does not silently change what
        "100%" means without every caller noticing the total moved.
    """
    grade: QualityGrade
    score: float
    criteria_met: Sequence[str]
    criteria_total: int


def _htf_aligned(signal: 'SignalCandidate', htf_bias: Optional['HTFBiasResult']) -> bool:
    """BUY needs a BULLISH HTF read; SELL needs BEARISH. No bias (None) or NEUTRAL/UNKNOWN never counts."""
    if htf_bias is None:
        return False
    if signal.signal_type == SignalType.BUY:
        return htf_bias.bias == HTFBias.BULLISH
    if signal.signal_type == SignalType.SELL:
        return htf_bias.bias == HTFBias.BEARISH
    return False


def _structure_aligned(signal: 'SignalCandidate', context: 'ContextSnapshot') -> bool:
    """The execution timeframe's own most recent confirmed structure point agrees with the signal's direction."""
    bias = most_recent_bias(context.structure)
    if signal.signal_type == SignalType.BUY:
        return bias == "BULLISH"
    if signal.signal_type == SignalType.SELL:
        return bias == "BEARISH"
    return False


def _liquidity_swept(signal: 'SignalCandidate', context: 'ContextSnapshot') -> bool:
    """A BUY wants sell-side liquidity (a low) swept first; a SELL wants buy-side liquidity (a high) swept first -- the classic SMC reversal precursor."""
    if signal.signal_type == SignalType.BUY:
        return any(sweep.type == LiquidityType.SSL for sweep in context.liquidity_sweeps)
    if signal.signal_type == SignalType.SELL:
        return any(sweep.type == LiquidityType.BSL for sweep in context.liquidity_sweeps)
    return False


def _order_block_aligned(signal: 'SignalCandidate', context: 'ContextSnapshot') -> bool:
    """The signal's entry price falls inside a same-direction Order Block's [low, high] zone."""
    wanted_type = {
        SignalType.BUY: OrderBlockType.BULLISH,
        SignalType.SELL: OrderBlockType.BEARISH,
    }.get(signal.signal_type)
    if wanted_type is None:
        return False
    return any(
        ob.type == wanted_type and ob.low <= signal.entry <= ob.high
        for ob in context.order_blocks
    )


def _fvg_aligned(signal: 'SignalCandidate', context: 'ContextSnapshot') -> bool:
    """The signal's entry price falls inside a same-direction Fair Value Gap's [bottom, top] zone."""
    wanted_type = {
        SignalType.BUY: FvgType.BULLISH,
        SignalType.SELL: FvgType.BEARISH,
    }.get(signal.signal_type)
    if wanted_type is None:
        return False
    return any(
        fvg.type == wanted_type and fvg.bottom <= signal.entry <= fvg.top
        for fvg in context.fair_value_gaps
    )


# Ordered (criterion name, check function) pairs -- the single source
# of truth for both criteria_total and which names can appear in
# criteria_met. Extending this tuple (e.g. once Session Intelligence
# lands) is the one place a future phase needs to touch.
_CRITERIA: Tuple[Tuple[str, Callable], ...] = (
    ("HTF_ALIGNED", lambda signal, context, htf_bias: _htf_aligned(signal, htf_bias)),
    ("STRUCTURE_ALIGNED", lambda signal, context, htf_bias: _structure_aligned(signal, context)),
    ("LIQUIDITY_SWEPT", lambda signal, context, htf_bias: _liquidity_swept(signal, context)),
    ("ORDER_BLOCK_ALIGNED", lambda signal, context, htf_bias: _order_block_aligned(signal, context)),
    ("FVG_ALIGNED", lambda signal, context, htf_bias: _fvg_aligned(signal, context)),
)


def _grade_for_score(score: float) -> QualityGrade:
    """4-5 of 5 criteria (80-100) -> A+; 3 (60) -> A; 2 (40) -> B; 0-1 (0-20) -> C."""
    if score >= 80.0:
        return QualityGrade.A_PLUS
    if score >= 60.0:
        return QualityGrade.A
    if score >= 40.0:
        return QualityGrade.B
    return QualityGrade.C


def compute_signal_quality(
    signal: 'SignalCandidate',
    context: 'ContextSnapshot',
    htf_bias: Optional['HTFBiasResult'] = None,
) -> SignalQualityResult:
    """
    Grades `signal`'s alignment with `context` (and, if available,
    `htf_bias`) into a QualityGrade. Never raises: a signal_type of
    NONE, an empty context, or a missing htf_bias all simply fail
    every criterion, producing grade C, not an error.
    """
    criteria_met = tuple(
        name for name, check in _CRITERIA if check(signal, context, htf_bias)
    )
    score = round(len(criteria_met) / len(_CRITERIA) * 100, 2)
    grade = _grade_for_score(score)

    logger.info(
        f"Signal quality computed: strategy={signal.strategy_name} "
        f"grade={grade.value} score={score:.2f} criteria_met={list(criteria_met)}"
    )

    return SignalQualityResult(
        grade=grade,
        score=score,
        criteria_met=criteria_met,
        criteria_total=len(_CRITERIA),
    )
