from enum import Enum
from dataclasses import dataclass
from typing import TYPE_CHECKING

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
    """
    min_confidence: float = 0.65
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
        ai_result: 'AIAnalysisResult'
    ) -> DecisionResult:
        """
        Applies normalized confidence thresholds from config and AI approval flags
        to determine the final decision.
        """

        # 1. Mandatory Constraint & Configured Threshold Evaluation
        if not ai_result.approved:
            final_decision = DecisionType.NO_TRADE
        elif ai_result.confidence < self.config.min_confidence:
            final_decision = DecisionType.NO_TRADE
        elif ai_result.confidence < self.config.approve_confidence:
            final_decision = DecisionType.REJECTED
        else:
            final_decision = DecisionType.APPROVED

        # 2. Return Clean Immutable Contract
        return DecisionResult(
            decision=final_decision,
            ai_confidence=ai_result.confidence,
            risk_score=ai_result.risk_score,
            explanation=ai_result.explanation
        )
