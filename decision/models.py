from dataclasses import dataclass
from enum import Enum

from signals.models import SignalCandidate
from ai.ai_analyzer import AIAnalysisResult


class DecisionAction(Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    NO_TRADE = "NO_TRADE"


@dataclass(frozen=True)
class TradeDecision:
    """
    Immutable final verdict produced by the Decision Engine from a
    SignalCandidate + AIAnalysisResult pair. Carries the originating
    signal and AI analysis alongside the verdict so downstream layers
    (Risk, Execution, logging) do not need to re-fetch context.
    """
    action: DecisionAction
    confidence: float
    reason: str
    signal: SignalCandidate
    ai_analysis: AIAnalysisResult
