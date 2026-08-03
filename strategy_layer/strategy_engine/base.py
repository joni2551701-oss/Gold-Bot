"""
Strategies — SetupStrategy base contract (TASK-CORE-007, setup layer).

SetupStrategy is the common interface every setup-detection strategy
implements. Contract (Director spec): name(), evaluate(context),
validate(context), score(context). A strategy READS a
context.context_orchestrator.ContextSnapshot (already computed by the
frozen context/ layer) and returns a StrategyResult — it never
recomputes market structure, never emits a signal, and never makes a
decision. It reads no .env and holds no secret.

Reads are done defensively (getattr) so a None / empty / malformed
context yields a defined StrategyResult (NO_SETUP / INVALID), never a
raise — satisfying the "empty context" and "invalid context" contract.
"""

from abc import ABC, abstractmethod

from strategy_layer.strategy_engine.result import StrategyResult


class SetupStrategy(ABC):
    """Base class for all setup-detection strategies. Stateless and read-only."""

    @abstractmethod
    def name(self) -> str:
        """Stable strategy identifier (also used as StrategyResult.strategy_name)."""
        raise NotImplementedError

    @abstractmethod
    def evaluate(self, context) -> StrategyResult:
        """Read the ContextSnapshot and return a StrategyResult. Never raises."""
        raise NotImplementedError

    def validate(self, context) -> bool:
        """
        True when the context is usable (present and carrying at least
        candles or one detector sequence). Overridable; the default is
        deliberately permissive — individual strategies decide what
        "enough data" means inside evaluate().
        """
        if context is None:
            return False
        return any(
            getattr(context, attr, None)
            for attr in (
                "candles", "structure", "bos_events", "choch_events",
                "liquidity_zones", "liquidity_sweeps", "order_blocks",
                "fair_value_gaps", "amd_events", "wyckoff_events", "session_events",
            )
        ) or getattr(context, "market_regime", None) is not None

    def score(self, context) -> float:
        """The setup's confidence (0.0–1.0). Defaults to evaluate()'s confidence."""
        return self.evaluate(context).confidence

    # -- shared read helpers (no computation, just safe reads) -------------

    def _guard(self, context):
        """Return a StrategyResult.invalid when context is unusable, else None."""
        if context is None:
            return StrategyResult.invalid(self.name(), "context is None")
        if not self.validate(context):
            return StrategyResult.invalid(self.name(), "context carries no usable data")
        return None

    def _last_price(self, context):
        """Latest close from the context candles, or None. Pure read."""
        candles = getattr(context, "candles", None)
        if not candles:
            return None
        return getattr(candles[-1], "close", None)

    def _regime(self, context):
        """The context's MarketRegimeResult, or None."""
        return getattr(context, "market_regime", None)
