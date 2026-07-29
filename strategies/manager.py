"""
Strategies — setup-layer manager (TASK-CORE-007).

SetupManager orchestrates the setup-detection strategies: it takes a
context.context_orchestrator.ContextSnapshot, evaluates every registered
SetupStrategy, and returns their StrategyResults ranked strongest-first.

This is DISTINCT from strategies/strategy_manager.py's StrategyManager,
which runs the live SignalCandidate path into signals/. SetupManager
produces StrategyResult only — it emits no signal, makes no decision,
computes no risk, and is not wired into core/pipeline.py. Never raises
for a data-driven condition (a None/empty context yields all-NO_SETUP /
INVALID results, ranked deterministically).
"""

from dataclasses import dataclass
from typing import List, Optional

from strategies.registry import SetupRegistry, build_setup_registry
from strategies.result import StrategyResult, SetupStatus


@dataclass(frozen=True)
class SetupEvaluation:
    """The whole layer's output for one context: every result, plus the found subset, ranked."""
    results: List[StrategyResult]

    @property
    def setups(self) -> List[StrategyResult]:
        """Only the results that actually found a setup (SETUP_FOUND), strongest first."""
        return [r for r in self.results if r.status == SetupStatus.SETUP_FOUND]

    @property
    def best(self) -> Optional[StrategyResult]:
        found = self.setups
        return found[0] if found else None


class SetupManager:
    """
    Runs all registered setup strategies against a ContextSnapshot and
    ranks the results. Ranking: SETUP_FOUND first, then by confidence
    (desc), then by strategy name (stable tie-break).
    """

    def __init__(self, registry: Optional[SetupRegistry] = None) -> None:
        self._registry = registry or build_setup_registry()

    @property
    def registry(self) -> SetupRegistry:
        return self._registry

    def evaluate(self, context) -> List[StrategyResult]:
        """
        Evaluate every strategy and return the results ranked
        strongest-first. Every strategy always contributes exactly one
        StrategyResult (setup, no-setup, or invalid) — never raises.
        """
        results = [strategy.evaluate(context) for strategy in self._registry.all()]
        return self._rank(results)

    def evaluate_full(self, context) -> SetupEvaluation:
        """evaluate() wrapped in a SetupEvaluation (adds .setups / .best convenience)."""
        return SetupEvaluation(results=self.evaluate(context))

    @staticmethod
    def _rank(results: List[StrategyResult]) -> List[StrategyResult]:
        found_order = {SetupStatus.SETUP_FOUND: 0, SetupStatus.NO_SETUP: 1, SetupStatus.INVALID: 2}
        return sorted(
            results,
            key=lambda r: (found_order.get(r.status, 3), -r.confidence, r.strategy_name),
        )
