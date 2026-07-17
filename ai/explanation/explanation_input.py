"""
AI Layer — Explanation Input Contract (Phase 63.1: AI Explanation
Intelligence Layer, TASK 2).

The "Primitive Explanation Data" the Director's own architecture
decision names: `core/pipeline.py` (the only place already permitted
to see every trading layer's output) extracts these plain values from
its own `DecisionResult`/`RiskResult`/`MarketContext` and passes them
in -- `ai/explanation/` never imports `decision/` or `risk/` itself
(Constitution Article 3, no exceptions for those two packages).

`ExplanationInput` is not `TradeContext` -- the Director's Phase 63.1
Decision explicitly ruled `TradeContext` out as a real type. This is a
narrower, `ai/`-owned contract carrying only already-extracted
primitives, never a `decision/`/`risk/` object reference.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ExplanationMode(Enum):
    """Which of TASK 3's three templates applies."""

    TRADE = "TRADE"
    NO_TRADE = "NO_TRADE"
    EDUCATION = "EDUCATION"


@dataclass(frozen=True)
class ExplanationInput:
    """
    mode: which template `explanation_templates.py` builds from.
    symbol: e.g. "XAUUSD" -- a plain string, never a data/ type import.
    confidence: 0-100 (percentage scale, matching the Director's own
        worked example and `HTFBiasResult.confidence`'s existing
        convention) -- converted to `ExplanationOutput.confidence`'s
        0.0-1.0 scale by `explanation_builder.py`, never stored as-is.

    TRADE fields: market_bias, entry, stop_loss, take_profit,
        risk_reward, technical_reason, fundamental_reason,
        risk_reason, invalidation.
    NO_TRADE fields: market_condition, missing_confirmation,
        waiting_condition (risk_reason is reused for "Risk Reason").
    EDUCATION fields: concept, example, lesson.

    Every field beyond `mode`/`symbol` is optional -- a caller
    supplies only the fields its `mode` actually needs; an unused
    field for the current mode is simply left `None`, never fabricated.
    """

    mode: ExplanationMode
    symbol: str
    language: str = "en"
    persona_name: Optional[str] = None

    # TRADE
    market_bias: Optional[str] = None
    entry: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    confidence: Optional[float] = None
    risk_reward: Optional[float] = None
    technical_reason: Optional[str] = None
    fundamental_reason: Optional[str] = None
    risk_reason: Optional[str] = None
    invalidation: Optional[str] = None

    # NO_TRADE
    market_condition: Optional[str] = None
    missing_confirmation: Optional[str] = None
    waiting_condition: Optional[str] = None

    # EDUCATION
    concept: Optional[str] = None
    example: Optional[str] = None
    lesson: Optional[str] = None
