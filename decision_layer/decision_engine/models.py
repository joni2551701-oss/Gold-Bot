from dataclasses import dataclass
from enum import Enum

from signal_layer.signal_builder.models import SignalCandidate
from ai.ai_analyzer import AIAnalysisResult


class DecisionAction(Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    NO_TRADE = "NO_TRADE"


@dataclass(frozen=True)
class TradeDecision:
    """
    Immutable final verdict produced by the Decision Engine from a
    SignalCandidate + AIAnalysisResult (+ optional HTFBiasResult)
    triple. Carries the originating signal and AI analysis alongside
    the verdict so downstream layers (Risk, Execution, logging) do not
    need to re-fetch context.

    signal_score/htf_score/risk_score/ai_score/final_score (Phase A3,
    Decision Engine v2) are the weighted formula's individual
    components, all on the same 0.0-1.0 scale as `confidence` --
    exposed for explainability only (see docs/ARCHITECTURE.md's
    Decision Engine v2 section and decision/README.md). `final_score`
    always equals `confidence`; it exists as its own named field
    because it is one of the formula's five components, not because
    it carries different information. Default 0.0 only applies to a
    TradeDecision built outside DecisionEngine.evaluate() (no such
    caller exists in this codebase today) -- evaluate() itself always
    supplies all five explicitly.
    """
    action: DecisionAction
    confidence: float
    reason: str
    signal: SignalCandidate
    ai_analysis: AIAnalysisResult
    signal_score: float = 0.0
    htf_score: float = 0.0
    risk_score: float = 0.0
    ai_score: float = 0.0
    final_score: float = 0.0
