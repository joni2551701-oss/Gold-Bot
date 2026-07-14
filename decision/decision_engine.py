from enum import Enum
from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING

from decision.models import DecisionAction, TradeDecision
from context.htf_bias import HTFBias

if TYPE_CHECKING:
    from signals.models import SignalCandidate
    from ai.ai_analyzer import AIAnalysisResult
    from context.htf_bias import HTFBiasResult


class DecisionType(Enum):
    """
    Standardized decision states for the Risk Layer.
    """
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    NO_TRADE = "NO_TRADE"


@dataclass(frozen=True)
class DecisionResult:
    """
    Clean, immutable data contract passed to the Risk Layer.
    Strictly aligned with the finalized AIAnalysisResult contract.
    """
    decision: DecisionType
    ai_confidence: float
    risk_score: float
    explanation: str


@dataclass(frozen=True)
class DecisionConfig:
    """
    Configuration for the Decision Engine thresholds.
    Extracted to allow easy optimization and backtesting without code changes.

    Thresholds apply to the weighted final_confidence used by
    DecisionEngine.evaluate() (Phase A3: Decision Engine v2 -- see
    DecisionWeights below), on the same 0.0-1.0 scale used across
    SignalCandidate.confidence and AIAnalysisResult.confidence.
    """
    min_confidence: float = 0.50
    approve_confidence: float = 0.80


@dataclass(frozen=True)
class DecisionWeights:
    """
    Phase A3 (Decision Engine v2): named, constant weights for the
    weighted confidence formula. Never hardcoded inline in evaluate()
    -- see docs/ARCHITECTURE.md's Decision Engine v2 section and
    decision/README.md for the rationale. Weights sum to 1.0 by
    convention (not enforced) so `final_confidence` stays on the same
    0.0-1.0 scale every existing threshold/consumer already expects.
    """
    signal_weight: float = 0.40
    htf_weight: float = 0.25
    risk_weight: float = 0.20
    ai_weight: float = 0.15


# Phase A3 Step 4: HTFBias -> base score mapping. Kept on the same
# 0.0-1.0 scale as every other confidence field in this codebase
# (SignalCandidate.confidence, AIAnalysisResult.confidence,
# DecisionConfig's thresholds) rather than introducing a second,
# 0-100 scale into the Decision Engine -- HTFBiasResult.confidence
# (Phase A2's own "timeframe agreement" score) is a separate concept
# and is not read here; only HTFBiasResult.bias (the category) and
# .quality_score are consumed. UNKNOWN maps to the same neutral 0.5
# as NEUTRAL, matching HTF_BIAS.md's "context, not a decision" intent
# -- an unresolved HTF read must not itself push the outcome either
# direction.
HTF_BIAS_SCORE_MAP = {
    HTFBias.BULLISH: 1.0,
    HTFBias.NEUTRAL: 0.5,
    HTFBias.BEARISH: 0.0,
    HTFBias.UNKNOWN: 0.5,
}


@dataclass(frozen=True)
class DecisionInput:
    """
    Phase A3 Step 2: explicit input contract for the weighted
    confidence formula, replacing a growing list of loose evaluate()
    parameters with one typed object. All fields are 0.0-1.0 scale.
    Built by _build_decision_input() -- not constructed directly by
    callers of evaluate().
    """
    signal_confidence: float
    htf_bias: HTFBias
    htf_quality_score: float
    risk_score: float  # already inverted: 1.0 = lowest risk / best
    ai_score: float


def _build_decision_input(
    signal: 'SignalCandidate',
    ai_analysis: 'AIAnalysisResult',
    htf_bias: Optional['HTFBiasResult'],
) -> DecisionInput:
    """
    Derives a DecisionInput from the three objects evaluate() already
    receives -- no new fetch, no new computation beyond the risk_score
    inversion described below.

    risk_score is sourced from AIAnalysisResult.risk_score (already
    computed by the AI layer, before Decision Engine runs -- unlike
    risk.risk_manager.RiskResult, which is only produced AFTER a
    TradeDecision exists and therefore cannot be an input to this
    formula). AIAnalysisResult.risk_score is documented (ai/ai_analyzer.py)
    as 0.0 = no risk .. 1.0 = maximum risk; DecisionInput.risk_score is
    inverted (1.0 - ai_analysis.risk_score) so every one of the four
    components is consistently "higher is better," matching
    signal_confidence/htf_score/ai_score.

    A missing htf_bias (None -- e.g. a caller that predates Phase A2,
    or one that intentionally omits it) is treated as HTFBias.UNKNOWN
    with htf_quality_score=0.0 -- via the Step 5 quality-dampening
    formula in _weighted_score(), this always contributes exactly the
    neutral 0.5, identical to a real HTFBiasResult(bias=UNKNOWN,
    quality_score=0.0). No special-casing needed elsewhere.
    """
    if htf_bias is None:
        htf_bias_value = HTFBias.UNKNOWN
        htf_quality_score = 0.0
    else:
        htf_bias_value = htf_bias.bias
        htf_quality_score = htf_bias.quality_score

    return DecisionInput(
        signal_confidence=signal.confidence,
        htf_bias=htf_bias_value,
        htf_quality_score=htf_quality_score,
        risk_score=1.0 - ai_analysis.risk_score,
        ai_score=ai_analysis.confidence,
    )


def _weighted_score(decision_input: DecisionInput, weights: DecisionWeights):
    """
    Phase A3 Steps 3 and 5: computes each component score plus the
    final weighted blend. Returns (signal_score, htf_score, risk_score,
    ai_score, final_score) -- the exact five values TradeDecision's
    explainability fields carry.

    Step 5 (quality handling): a poor-quality HTF read is dampened
    toward the neutral midpoint (0.5), never rejected outright --
    htf_quality_score=1.0 (100%) keeps the full base_htf_score
    ("full weight"); 0.0 (0%) collapses entirely to 0.5 ("neutral
    contribution"), regardless of what the underlying bias was.
    """
    signal_score = decision_input.signal_confidence
    base_htf_score = HTF_BIAS_SCORE_MAP[decision_input.htf_bias]
    htf_score = (
        base_htf_score * decision_input.htf_quality_score
        + 0.5 * (1.0 - decision_input.htf_quality_score)
    )
    risk_score = decision_input.risk_score
    ai_score = decision_input.ai_score

    final_score = (
        weights.signal_weight * signal_score
        + weights.htf_weight * htf_score
        + weights.risk_weight * risk_score
        + weights.ai_weight * ai_score
    )

    return signal_score, htf_score, risk_score, ai_score, final_score


class DecisionEngine:
    """
    Phase A3 (Decision Engine v2): evaluates a weighted blend of
    signal confidence, HTF bias, (inverted) AI risk score, and AI
    confidence against configured thresholds to produce a final
    trading decision status. Replaces the pre-A3 flat
    (signal + ai) / 2 average -- see docs/ARCHITECTURE.md's Decision
    Engine v2 section for the full rationale and
    docs/v0.3.5_SPECIFICATION.md for the phase that first proposed it.
    """

    def __init__(self, config: DecisionConfig = None, weights: DecisionWeights = None):
        """
        Initializes the engine with the provided config/weights, or
        defaults to the standard thresholds/weights if none provided.
        """
        self.config = config or DecisionConfig()
        self.weights = weights or DecisionWeights()

    def evaluate(
        self,
        signal: 'SignalCandidate',
        ai_analysis: 'AIAnalysisResult',
        htf_bias: Optional['HTFBiasResult'] = None,
    ) -> TradeDecision:
        """
        Produces a TradeDecision from a SignalCandidate +
        AIAnalysisResult pair, optionally weighted by an HTFBiasResult
        (Phase A2/A3). The AI Analyzer's verdict is never accepted
        blindly: signal confidence, HTF bias, (inverted) AI risk
        score, and AI confidence are blended per DecisionWeights, and
        the AI's explicit approval flag is checked as a hard gate --
        unchanged from the pre-A3 engine, and not affected by the
        weighted formula in any way.

        htf_bias defaults to None for backward compatibility with any
        caller that does not have one available -- see
        _build_decision_input()'s docstring for exactly how that
        degrades (always a neutral 0.5 HTF contribution, never an
        error).
        """
        decision_input = _build_decision_input(signal, ai_analysis, htf_bias)
        signal_score, htf_score, risk_score, ai_score, final_confidence = _weighted_score(
            decision_input, self.weights
        )

        if not ai_analysis.approved:
            action = DecisionAction.REJECT
            reason = f"AI Analyzer did not approve this signal: {ai_analysis.explanation}"
        elif final_confidence < self.config.min_confidence:
            action = DecisionAction.NO_TRADE
            reason = (
                f"Combined confidence {final_confidence:.2f} is below the "
                f"minimum threshold ({self.config.min_confidence:.2f})."
            )
        elif final_confidence < self.config.approve_confidence:
            action = DecisionAction.REJECT
            reason = (
                f"Combined confidence {final_confidence:.2f} is below the "
                f"approval threshold ({self.config.approve_confidence:.2f})."
            )
        else:
            action = DecisionAction.APPROVE
            reason = (
                f"Signal and AI analysis aligned with sufficient confidence "
                f"({final_confidence:.2f})."
            )

        return TradeDecision(
            action=action,
            confidence=final_confidence,
            reason=reason,
            signal=signal,
            ai_analysis=ai_analysis,
            signal_score=signal_score,
            htf_score=htf_score,
            risk_score=risk_score,
            ai_score=ai_score,
            final_score=final_confidence,
        )
