"""
Market Layer — Regime State projection (TASK-CORE-005).

RegimeState is a READ-ONLY projection of the market regime context/
already classified (context.market_regime ->
context.snapshot.ContextSnapshotSchema.regime, one of the context
layer's ALLOWED_REGIMES). It performs NO regime calculation of its own
and never overrides context's label. This is advisory market context
only -- it is NOT a strategy choice (Director: "keyinchalik strategy
tanlashga yordam beradi, lekin strategy emas").
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class RegimeState:
    """
    regime: context's own regime string (e.g. "TRENDING", "RANGE",
        "ACCUMULATION", "DISTRIBUTION", "HIGH_VOLATILITY",
        "LOW_VOLATILITY", "UNKNOWN"). Never re-derived here.
    """
    regime: str = "UNKNOWN"

    @classmethod
    def from_context(cls, context_schema) -> "RegimeState":
        """Project from an already-built context.snapshot.ContextSnapshotSchema.regime. Empty/absent -> UNKNOWN."""
        regime = getattr(context_schema, "regime", None) or "UNKNOWN"
        return cls(regime=str(regime).strip().upper() or "UNKNOWN")

    @property
    def is_trending(self) -> bool:
        return self.regime == "TRENDING"

    @property
    def is_ranging(self) -> bool:
        return self.regime == "RANGE"

    @property
    def is_known(self) -> bool:
        return self.regime != "UNKNOWN"
