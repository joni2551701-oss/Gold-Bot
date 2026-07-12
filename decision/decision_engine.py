from enum import Enum
from dataclasses import dataclass
from typing import TYPE_CHECKING

from decision.models import DecisionAction, TradeDecision

if TYPE_CHECKING:
    from signals.models import SignalCandidate
    from ai.ai_analyzer import AIAnalysisResult


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

    Thresholds apply to the blended (signal + AI) confidence used by
    DecisionEngine.evaluate(), on the same 0.0-1.0 scale used across
    SignalCandidate.confidence and AIAnalysisResult.confidence.
    """
    min_confidence: float = 0.50
    approve_confidence: float = 0.80


class DecisionEngine:
    """
    Evaluates AI analysis results against configured confidence thresholds
    to produce a final trading decision status.
    """

    def __init__(self, config: DecisionConfig = None):
        """
        Initializes the engine with the provided config,
        or defaults to standard thresholds if none provided.
        """
        self.config = config or DecisionConfig()

    def evaluate(
        self,
        signal: 'SignalCandidate',
        ai_analysis: 'AIAnalysisResult'
    ) -> TradeDecision:
        """
        Produces a TradeDecision from a SignalCandidate + AIAnalysisResult
        pair. The AI Analyzer's verdict is never accepted blindly: both
        the signal's own confidence and the AI's confidence are blended,
        and the AI's explicit approval flag is checked as a hard gate.
        """
        final_confidence = (signal.confidence + ai_analysis.confidence) / 2

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
        )
