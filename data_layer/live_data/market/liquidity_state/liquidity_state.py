"""
Market Layer — Liquidity State projection (TASK-CORE-005).

LiquidityState is a READ-ONLY projection of the liquidity context/
already detected (context.liquidity's sweeps/zones). It performs NO
liquidity detection of its own. `from_context()` reads
context.snapshot.LiquidityInfo (sweep_detected, liquidity_type) and
exposes buy-side/sell-side presence in the market vocabulary. Holds no
trade decision.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LiquidityState:
    """
    sweep_detected: whether context reported any liquidity sweep.
    liquidity_type: context's own most-recent sweep label (e.g.
        "SELL_SIDE_LIQUIDITY"/"BUY_SIDE_LIQUIDITY"), or None.
    buy_side / sell_side: convenience booleans derived from
        liquidity_type -- presence only, never a new detection.
    """
    sweep_detected: bool = False
    liquidity_type: Optional[str] = None
    buy_side: bool = False
    sell_side: bool = False

    @classmethod
    def from_context(cls, context_schema) -> "LiquidityState":
        """Project from an already-built context.snapshot.ContextSnapshotSchema.liquidity. Never recomputes; empty context -> empty state."""
        info = getattr(context_schema, "liquidity", None)
        if info is None:
            return cls()
        raw_type = getattr(info, "liquidity_type", None)
        token = str(raw_type).upper() if raw_type else ""
        return cls(
            sweep_detected=bool(getattr(info, "sweep_detected", False)),
            liquidity_type=raw_type,
            buy_side="BUY_SIDE" in token,
            sell_side="SELL_SIDE" in token,
        )
