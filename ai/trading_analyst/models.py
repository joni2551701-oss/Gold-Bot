"""
AI Layer — Trading Analyst Model (Phase 66.0: AI Trading Analyst
Foundation, TASK 2).

`TradingAnalysisInput` follows `ai/explanation/explanation_input.py`'s
own Article 3 resolution exactly: every field is a primitive
(`str`/`float`/`Sequence[str]`) or an enum defined in this same file —
never a `decision.models.TradeDecision`, `risk.risk_manager.RiskResult`,
`signals.models.SignalCandidate`, or any other Trading Core object
reference. `ai/trading_analyst/` itself never imports `decision/`,
`risk/`, `execution/`, `strategies/`, `signals/`, `context/`, or
`monitoring/` — a future, separately-approved live-wiring phase would
have `core/pipeline.py` (the only place already permitted to see every
trading layer's own output) extract these plain values from its own
`TradeDecision`/`RiskResult` and pass them in. See
`docs/PHASE66_0_AUDIT.md`'s "central architectural resolution" section.

`signal_score`/`htf_score`/`risk_score`/`ai_score` mirror
`decision.models.TradeDecision`'s own five-component breakdown by
field name only (Decision Engine v2) — relayed, never recomputed;
this module has no formula of its own. `risk_level` is likewise
caller-supplied, never computed here — Rule 4 ("AI faqat READ ONLY")
means this module narrates an already-made risk classification, it
never classifies risk itself.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Sequence


class TradingRiskLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


@dataclass(frozen=True)
class TradingAnalysisInput:
    """
    symbol: e.g. "XAUUSD" — a plain string, never a data/ type import.
    direction: the Decision Engine's own already-decided action,
        narrated only (e.g. "BUY"/"SELL"/"WAIT"/"SKIP") — this module
        never computes or overrides it (Director Note 1).
    market_bias: the HTF bias already computed upstream (e.g.
        "BULLISH"/"BEARISH"/"NEUTRAL") — relayed, not recomputed.
    confidence: 0-100 (percentage scale, matching `ExplanationInput`'s
        own convention) — converted to `TradingAnalysis.confidence`'s
        0.0-1.0 scale by `analyst_runtime.py`, never stored as-is.
    signal_score/htf_score/risk_score/ai_score: TradeDecision's own
        five-component breakdown (Decision Engine v2), relayed for
        explainability only.
    risk_level: caller-supplied, never computed here.
    strengths/weaknesses: short, free-text bullet points a caller
        (a future live-wiring phase) extracts from the already-computed
        Trading Core context — this module renders them, never derives
        them.
    """

    symbol: str
    direction: str
    market_bias: str
    confidence: float = 0.0
    signal_score: float = 0.0
    htf_score: float = 0.0
    risk_score: float = 0.0
    ai_score: float = 0.0
    risk_level: TradingRiskLevel = TradingRiskLevel.MEDIUM
    risk_reward: Optional[float] = None
    entry: Optional[float] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    technical_reason: Optional[str] = None
    risk_reason: Optional[str] = None
    invalidation: Optional[str] = None

    # TASK 4 — Market Analysis fields, all optional plain strings,
    # relayed only.
    session: Optional[str] = None
    htf_trend: Optional[str] = None
    liquidity_note: Optional[str] = None
    structure_note: Optional[str] = None
    volume_note: Optional[str] = None
    volatility_note: Optional[str] = None

    strengths: Sequence[str] = field(default_factory=tuple)
    weaknesses: Sequence[str] = field(default_factory=tuple)
    language: str = "en"


@dataclass(frozen=True)
class TradingAnalysis:
    """
    The TASK 2 output contract. `confidence` is 0.0-1.0, matching
    `ExplanationOutput`'s own scale. `recommendation` is a narrative
    string built from `TradingAnalysisInput.direction` (already
    decided) — never a new BUY/SELL/NO_TRADE verdict (Director Note 1:
    "U hech qachon BUY/SELL/NO TRADE qarorini chiqarmaydi").
    """

    symbol: str
    direction: str
    confidence: float
    market_bias: str
    risk_level: TradingRiskLevel
    rr: Optional[float]
    summary: str
    strengths: Sequence[str]
    weaknesses: Sequence[str]
    recommendation: str
    educational_note: Optional[str] = None
    generated_at: str = ""
