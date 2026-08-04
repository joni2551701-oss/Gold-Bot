"""
Market Layer — Trend State projection (TASK-CORE-005).

TrendState is a READ-ONLY projection of the trend context/ already
computed -- it performs NO trend calculation of its own (Director:
market/ never re-implements structure math; context/ is untouched).
`from_context()` maps context.snapshot.StructureInfo.trend
("BULLISH"/"BEARISH"/None -- context.market_structure's own output)
onto the market vocabulary the Director named.
"""

from enum import Enum


class TrendState(str, Enum):
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"
    MIXED = "mixed"
    UNKNOWN = "unknown"

    @classmethod
    def from_context(cls, context_schema) -> "TrendState":
        """
        Project the trend from an already-built
        context.snapshot.ContextSnapshotSchema. Reads
        schema.structure.trend only -- never recomputes. A missing/None
        trend is UNKNOWN (honest), not a fabricated direction. A
        conflicting BOS-without-a-trend reads as NEUTRAL.
        """
        structure = getattr(context_schema, "structure", None)
        raw = getattr(structure, "trend", None) if structure else None
        if raw is None:
            # No directional bias reported. If structure recorded a BOS
            # or CHoCH but no trend label, that's a NEUTRAL/mixed read.
            if structure and (getattr(structure, "bos", False) or getattr(structure, "choch", False)):
                return cls.NEUTRAL
            return cls.UNKNOWN
        token = str(raw).strip().upper()
        if token == "BULLISH":
            return cls.BULLISH
        if token == "BEARISH":
            return cls.BEARISH
        if token in ("NEUTRAL", "RANGE"):
            return cls.NEUTRAL
        return cls.MIXED
