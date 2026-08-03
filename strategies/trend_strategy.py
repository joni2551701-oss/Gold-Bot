"""
Strategies — Trend continuation setup strategy (TASK-CORE-007, setup layer).

Reads the frozen context/ structure (via context.market_structure.
most_recent_bias) and market regime. A trend-continuation setup requires
a directional structural bias that the regime does not contradict.
Returns a StrategyResult; recomputes no structure, emits no signal.
"""

from strategies.base import SetupStrategy
from strategies.result import StrategyResult, StrategyDirection, SetupStatus
from context_layer.market_structure.market_structure import most_recent_bias


class TrendStrategy(SetupStrategy):
    def name(self) -> str:
        return "TREND_CONTINUATION_SETUP"

    def evaluate(self, context) -> StrategyResult:
        guard = self._guard(context)
        if guard:
            return guard

        structure = list(getattr(context, "structure", ()) or ())
        bias = most_recent_bias(structure) if structure else None
        if bias is None:
            return StrategyResult.none(self.name(), "no directional structure bias")

        regime = self._regime(context)
        regime_name = self._enum_value(getattr(regime, "regime", None))
        regime_dir = self._enum_value(getattr(regime, "direction", None))
        regime_conf = getattr(regime, "confidence", 0.0) or 0.0

        # Regime must not contradict the structural bias.
        if regime_dir in ("BULLISH", "BEARISH") and regime_dir != bias:
            return StrategyResult.none(self.name(), f"regime {regime_dir} contradicts structure {bias}")

        direction = StrategyDirection.LONG if bias == "BULLISH" else StrategyDirection.SHORT
        # Confidence: stronger when the regime is TRENDING and agrees.
        base = 0.6
        if regime_name == "TRENDING" and regime_dir == bias:
            base = min(0.9, 0.6 + regime_conf / 100.0 * 0.3)
        confidence = round(base, 2)

        return StrategyResult(
            strategy_name=self.name(),
            direction=direction,
            confidence=confidence,
            reasons=[f"structure bias {bias}", f"regime {regime_name or 'UNKNOWN'}/{regime_dir or 'NEUTRAL'}"],
            status=SetupStatus.SETUP_FOUND,
            metadata={"bias": bias, "regime": regime_name, "regime_direction": regime_dir},
        )

    @staticmethod
    def _enum_value(x):
        if x is None:
            return None
        return getattr(x, "value", str(x))
