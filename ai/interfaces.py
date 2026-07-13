"""
AI Layer — provider interface foundation (Phase 55).

This module defines the *shape* a future AI provider must satisfy so
swapping providers (heuristic stub -> Gemini -> a different LLM later)
never requires touching core/pipeline.py, decision/decision_engine.py,
or any other caller. Nothing here calls a real AI/LLM -- this is a
contract, not an implementation.

The existing production analyzer (ai/ai_analyzer.py's AIAnalyzer,
wired into core/pipeline.py today) does NOT implement this interface
yet and is not required to for this phase -- retrofitting it is
explicitly out of scope ("existing pipeline flow o'zgarishi" is
forbidden). This interface exists so a *future* AI Assistant Core
(v0.4+) has an agreed shape to implement against from day one.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class MarketContext:
    """
    Read-only snapshot of what the AI layer is allowed to see about
    the market for one evaluation. Deliberately narrower than
    context.context_orchestrator.ContextSnapshot -- this is the
    AI-facing subset, not the full SMC detection output, so a future
    provider's input contract doesn't leak internal Context Layer
    types into ai/.
    """
    symbol: str
    timeframe: str
    summary: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class UserContext:
    """
    Read-only snapshot of what the AI layer is allowed to know about
    the requesting user for one evaluation. Optional -- a pure market
    analysis call (no personalization) may omit it entirely.
    """
    telegram_id: Optional[str] = None
    experience_level: Optional[str] = None
    preferred_strategy: Optional[str] = None
    risk_style: Optional[str] = None
    language: Optional[str] = None


@dataclass(frozen=True)
class AIResponse:
    """
    The one output shape every AI provider must return, regardless of
    which model/vendor produced it. `decision`/`confidence` are
    advisory only -- see AIAnalyzerInterface's docstring for the hard
    boundary this data contract does NOT cross.
    """
    decision: str
    confidence: float
    explanation: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class AIAnalyzerInterface(ABC):
    """
    Contract a future AI provider must implement.

    Hard boundary (unchanged from the existing production AIAnalyzer's
    documented contract, restated here so it travels with the
    interface): an AIAnalyzerInterface implementation is advisory
    input to decision.decision_engine.DecisionEngine only. It must
    never itself approve/reject a trade, must never call
    risk.risk_manager.RiskManager, and must never trigger execution or
    a Telegram send. Those responsibilities belong exclusively to the
    Decision Engine, Risk Manager, and TradingPipeline respectively --
    an AI provider answers a question, it does not act on the answer.
    """

    @abstractmethod
    def evaluate(self, market_context: MarketContext, user_context: Optional[UserContext] = None) -> AIResponse:
        """Evaluates a market context (and optional user context) and returns an AIResponse. Never raises."""
        raise NotImplementedError
