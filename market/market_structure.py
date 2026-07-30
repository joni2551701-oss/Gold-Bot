"""
Market Layer — Market Structure view (TASK-CORE-005).

MarketStructureView is a READ-ONLY projection of the market structure
context/ ALREADY computes. It is NOT a second structure detector.

CRITICAL (Director decision + CLAUDE.md Trading Safety): the real
structure math -- swing points, HH/HL/LH/LL classification, BOS, CHoCH,
order blocks, FVGs, liquidity -- lives in context/ (market_structure.py,
bos.py, choch.py, order_block.py, fvg.py, liquidity.py) and is FROZEN
for this task. This module reads the already-built
context.snapshot.ContextSnapshotSchema (structure + zones groups) and
exposes it under the market façade's names. It never recomputes and
never modifies context/. A name like `market/market_structure.py`
matches the Director's file list, but its body is a projection, not a
detector.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class MarketStructureView:
    """
    trend: context.structure.trend ("BULLISH"/"BEARISH"/None).
    bos / choch: presence booleans from context (were any detected).
    swing_state: context's most-recent StructureType label ("HH"/"HL"/
        "LH"/"LL") or None.
    order_block / fvg: presence booleans from context.zones.
    All fields are direct reads of context's already-classified output.
    """
    trend: Optional[str] = None
    bos: bool = False
    choch: bool = False
    swing_state: Optional[str] = None
    order_block: bool = False
    fvg: bool = False

    @classmethod
    def from_context(cls, context_schema) -> "MarketStructureView":
        """Project structure + zones from an already-built context.snapshot.ContextSnapshotSchema. Never recomputes; empty context -> empty view."""
        structure = getattr(context_schema, "structure", None)
        zones = getattr(context_schema, "zones", None)
        return cls(
            trend=getattr(structure, "trend", None) if structure else None,
            bos=bool(getattr(structure, "bos", False)) if structure else False,
            choch=bool(getattr(structure, "choch", False)) if structure else False,
            swing_state=getattr(structure, "swing_state", None) if structure else None,
            order_block=bool(getattr(zones, "order_block", False)) if zones else False,
            fvg=bool(getattr(zones, "fvg", False)) if zones else False,
        )
