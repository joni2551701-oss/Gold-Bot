"""
Signal Layer — backward-compatibility adapter (Phase A15).

Bridges the existing pipeline objects (SignalCandidate, and
optionally SignalQualityResult/TradeDecision) into a SignalSchema,
without changing any of them. Existing signal creation
(strategies/*.py, signals/signal_engine.py) is entirely untouched --
this module only reads what those already produce.

Not wired into core/pipeline.py in this phase (per the roadmap's
"Pipeline logikasi o'zgarmaydi" instruction) -- see
docs/SIGNAL_SCHEMA.md's "Integration" section for the intended future
call site.
"""

from datetime import datetime, timezone
from typing import Optional, TYPE_CHECKING

from signals.schema import SignalSchema, generate_signal_id

if TYPE_CHECKING:
    from signals.models import SignalCandidate
    from signals.signal_quality import SignalQualityResult
    from decision.models import TradeDecision

# The real, currently-singular symbol/timeframe/asset-type this
# codebase runs today (main.py's TradingPipeline(symbol="XAUUSD",
# interval="M15", ...), assets/profiles/gold.py's GOLD_ASSET) -- a
# caller with a different value (a future multi-asset cycle) can
# always override these keyword arguments; they are defaults, not
# hardcoded requirements.
_DEFAULT_SYMBOL = "XAUUSD"
_DEFAULT_TIMEFRAME = "M15"
_DEFAULT_ASSET_TYPE = "GOLD"  # matches assets.asset_type.AssetType.GOLD.value

# decision.models.DecisionAction's real values (APPROVE/REJECT/
# NO_TRADE) mapped onto SignalSchema's own decision vocabulary
# (APPROVED/REJECTED/PENDING). NO_TRADE collapses to REJECTED -- both
# mean "no signal reaches the user," and SignalSchema's decision field
# is a simplified status, not a re-derivation of DecisionAction's own
# meaning. This mapping is the one place that translation happens.
_DECISION_ACTION_TO_STATUS = {
    "APPROVE": "APPROVED",
    "REJECT": "REJECTED",
    "NO_TRADE": "REJECTED",
}


def from_signal_candidate(
    signal: 'SignalCandidate',
    *,
    symbol: str = _DEFAULT_SYMBOL,
    timeframe: str = _DEFAULT_TIMEFRAME,
    asset_type: str = _DEFAULT_ASSET_TYPE,
    session: Optional[str] = None,
    context_id: Optional[str] = None,
    strategy_version: Optional[str] = None,
    quality: Optional['SignalQualityResult'] = None,
    explanation_id: Optional[str] = None,
    decision: Optional['TradeDecision'] = None,
    risk_id: Optional[str] = None,
) -> SignalSchema:
    """
    Builds a SignalSchema from an existing SignalCandidate -- the
    minimum required input, matching "Strategy Output" as this
    phase's integration point. Every other parameter is optional:
    call this right after Strategy Engine with just `signal` and get
    a valid SignalSchema with decision="PENDING" and every reference
    field None; call it later in the pipeline with `quality`/
    `decision` supplied too, and those fields get populated from the
    already-computed SignalQualityResult/TradeDecision -- never
    recomputed here.

    strategy_name is signal.strategy_name exactly (e.g.
    "LIQUIDITY_SWEEP_STRATEGY") -- the real value every
    strategies/*.py file already produces, not a human-readable label.
    strategy_version has no source on SignalCandidate today; None
    unless the caller supplies one explicitly.
    """
    entry_price = signal.entry
    stop_loss = signal.stop_loss
    take_profit = signal.take_profit
    direction = signal.signal_type.value

    quality_grade = quality.grade.value if quality is not None else None
    confidence_score = quality.score if quality is not None else None

    if decision is not None:
        decision_status = _DECISION_ACTION_TO_STATUS.get(decision.action.value, "PENDING")
        decision_score = decision.confidence
    else:
        decision_status = "PENDING"
        decision_score = None

    return SignalSchema(
        signal_id=generate_signal_id(),
        created_at=datetime.now(timezone.utc),
        symbol=symbol,
        timeframe=timeframe,
        direction=direction,
        asset_type=asset_type,
        session=session,
        entry_price=entry_price,
        stop_loss=stop_loss,
        take_profit=take_profit,
        context_id=context_id,
        strategy_name=signal.strategy_name,
        strategy_version=strategy_version,
        quality_grade=quality_grade,
        confidence_score=confidence_score,
        explanation_id=explanation_id,
        decision=decision_status,
        decision_score=decision_score,
        risk_id=risk_id,
    )
