"""
Market Layer — Volatility State projection (TASK-CORE-005).

VolatilityState is a READ-ONLY projection. context/ does NOT expose a
standalone volatility label -- volatility only appears inside
context.market_regime's regime enum as HIGH_VOLATILITY / LOW_VOLATILITY
(see context_layer/trend/market_regime.py). This module therefore PROJECTS the
volatility level from the already-computed regime; it performs NO
volatility calculation of its own and adds no new detector (that would
be new structure math, which market/ must never do).

An honest UNKNOWN is returned when the regime carries no volatility
signal -- NORMAL is only asserted for a known non-volatility regime
(e.g. TRENDING/RANGE), never fabricated.
"""

from enum import Enum


class VolatilityLevel(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    EXTREME = "extreme"
    UNKNOWN = "unknown"

    @classmethod
    def from_context(cls, context_schema) -> "VolatilityLevel":
        """
        Project the volatility level from an already-built
        context.snapshot.ContextSnapshotSchema.regime. Mapping (no new
        math -- a pure relabel of context's own regime):
            HIGH_VOLATILITY -> HIGH
            LOW_VOLATILITY  -> LOW
            a known non-volatility regime (TRENDING/RANGE/ACCUMULATION/
                DISTRIBUTION) -> NORMAL
            UNKNOWN/absent  -> UNKNOWN
        EXTREME is reserved for a future dedicated detector and is never
        fabricated from today's regime signal.
        """
        regime = str(getattr(context_schema, "regime", "") or "").strip().upper()
        if regime == "HIGH_VOLATILITY":
            return cls.HIGH
        if regime == "LOW_VOLATILITY":
            return cls.LOW
        if regime in ("TRENDING", "RANGE", "ACCUMULATION", "DISTRIBUTION"):
            return cls.NORMAL
        return cls.UNKNOWN
