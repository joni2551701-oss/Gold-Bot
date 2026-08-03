"""
Strategies — Support / Resistance setup strategy (TASK-CORE-007, setup layer).

Director-required, kept as its own strategy. It reads the frozen
context/ liquidity zones as its S/R reference — equal-high (BSL) zones
are resistance, equal-low (SSL) zones are support — plus the latest
price. It does NOT compute new levels or structure; it classifies the
price's relationship to the already-detected zones:

    support bounce      price just above an SSL support level
    resistance rejection price just below a BSL resistance level
    support break       price below an SSL support level
    resistance break    price above a BSL resistance level
    retest confluence   a near zone that also coincides with a break

Returns a StrategyResult; emits no signal.
"""

from strategies.base import SetupStrategy
from strategies.result import StrategyResult, StrategyDirection, SetupStatus
from context_layer.liquidity.liquidity import LiquidityType

_NEAR_FRACTION = 0.002  # 0.2% of price counts as "at" a level.


class SNRStrategy(SetupStrategy):
    def name(self) -> str:
        return "SUPPORT_RESISTANCE_SETUP"

    def evaluate(self, context) -> StrategyResult:
        guard = self._guard(context)
        if guard:
            return guard

        zones = list(getattr(context, "liquidity_zones", ()) or ())
        price = self._last_price(context)
        if not zones or price is None:
            return StrategyResult.none(self.name(), "no S/R zones or no price")

        zone = min(zones, key=lambda z: abs(z.price - price))
        level = zone.price
        tol = abs(price) * _NEAR_FRACTION
        is_support = zone.type == LiquidityType.SSL
        near = abs(price - level) <= tol

        if is_support:
            if near and price >= level:
                pattern, direction = "support bounce", StrategyDirection.LONG
            elif price < level - tol:
                pattern, direction = "support break", StrategyDirection.SHORT
            elif near:
                pattern, direction = "support retest", StrategyDirection.LONG
            else:
                return StrategyResult.none(self.name(), "price not engaging support", level=level)
        else:  # resistance (BSL)
            if near and price <= level:
                pattern, direction = "resistance rejection", StrategyDirection.SHORT
            elif price > level + tol:
                pattern, direction = "resistance break", StrategyDirection.LONG
            elif near:
                pattern, direction = "resistance retest", StrategyDirection.SHORT
            else:
                return StrategyResult.none(self.name(), "price not engaging resistance", level=level)

        # Retest confluence: a structural break near the same zone strengthens it.
        breaks = list(getattr(context, "bos_events", ()) or ()) + list(getattr(context, "choch_events", ()) or ())
        confluence = any(zone.start_index <= b.index <= zone.end_index + 50 for b in breaks)
        confidence = 0.7 if confluence else 0.6
        reasons = [f"{pattern} @ level {level} (strength {zone.strength})"]
        if confluence:
            reasons.append("retest confluence with a structural break")

        return StrategyResult(
            strategy_name=self.name(),
            direction=direction,
            confidence=confidence,
            entry_zone=(level - tol, level + tol),
            invalidation=level,
            reasons=reasons,
            status=SetupStatus.SETUP_FOUND,
            metadata={"level": level, "zone_type": zone.type.value, "pattern": pattern, "confluence": confluence},
        )
