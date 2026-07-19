"""
AI Layer — Chart Intelligence Model (Phase 66.1: AI Chart Intelligence
Foundation, TASK 2/3).

Follows `ai/trading_analyst/models.py`'s own Article 3 resolution
exactly: every field is a primitive (`str`/`float`/`Sequence[str]`) or
an enum defined in this same file — never a `decision.models.TradeDecision`,
`risk.risk_manager.RiskResult`, or any other Trading Core object
reference. `ai/chart_intelligence/` never imports `decision/`, `risk/`,
`execution/`, `strategies/`, `signals/`, `context/`, or `monitoring/`.

Per the Director's own framing of this phase: Chart Intelligence is
the *chart interpretation layer*, not a single-screenshot tool — a
future, separately-approved live-wiring phase would route TradingView
screenshots, MT5 screenshots, Telegram images, and PDF charts through
this same pipeline. `ChartImageType` names that wide vocabulary now,
even though no Vision API call exists yet (Rule 4).

`ChartContext` (TASK 3) is deliberately image-free: `image_hash` is a
content-hash *reference* only — this Foundation never stores image
bytes or binary data anywhere (Director Note 4).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Sequence


class ChartImageType(Enum):
    """The visual source vocabulary a future live-wiring phase would route through one pipeline (Director's own framing)."""

    TRADINGVIEW_SCREENSHOT = "TRADINGVIEW_SCREENSHOT"
    MT5_SCREENSHOT = "MT5_SCREENSHOT"
    TELEGRAM_IMAGE = "TELEGRAM_IMAGE"
    PDF_CHART = "PDF_CHART"
    OTHER = "OTHER"


class ChartAnalysisType(Enum):
    """Which kind of chart reading this analysis represents -- caller-supplied, never inferred by this package (Rule 2)."""

    STRUCTURE = "STRUCTURE"
    TREND = "TREND"
    LIQUIDITY = "LIQUIDITY"
    ORDER_BLOCK = "ORDER_BLOCK"
    FVG = "FVG"
    SUPPORT_RESISTANCE = "SUPPORT_RESISTANCE"
    GENERAL = "GENERAL"


@dataclass(frozen=True)
class ChartContext:
    """
    TASK 3 — metadata about the image itself, never the image. No field
    on this dataclass carries image bytes, a base64 blob, or a binary
    payload -- `image_hash` is a plain string reference only (e.g. a
    SHA-256 hex digest a future phase would compute upstream of this
    package), matching `MediaAsset`'s own "never store the asset,
    reference it" convention (`media/models.py`).

    source: e.g. "telegram" / "tradingview" / "mt5" / "pdf" -- plain
        string, caller-supplied.
    resolution: e.g. "1920x1080", optional.
    platform: e.g. "TradingView Desktop", "MT5 Mobile" -- optional.
    created_at: ISO-8601 timestamp string, caller-supplied.
    image_hash: a content-hash reference, never the image itself.
    """

    source: str
    resolution: Optional[str] = None
    platform: Optional[str] = None
    created_at: str = ""
    image_hash: Optional[str] = None


def has_minimum_context(context: ChartContext) -> bool:
    """Never raises: deterministic completeness check -- True only when `source` is a non-empty string."""
    return bool(context.source)


@dataclass(frozen=True)
class ChartAnalysisInput:
    """
    TASK 2's own input shape -- every field is caller-supplied and
    relayed, never computed or inferred by this package (Rule 2 "READ
    ONLY", Rule 4 "no Vision API"). `confidence` is 0-100 (percentage
    scale, matching `TradingAnalysisInput`'s own convention) --
    converted to `ChartAnalysis.confidence`'s 0.0-1.0 scale by
    `chart_runtime.py`, never stored as-is.

    order_blocks/fvg/support/resistance are short, free-text
    descriptions (e.g. "3400 (H4 bullish OB)") a caller extracts --
    this package renders them, never derives them.
    """

    symbol: str
    timeframe: str
    image_type: ChartImageType = ChartImageType.OTHER
    analysis_type: ChartAnalysisType = ChartAnalysisType.GENERAL
    market_structure: Optional[str] = None
    trend: Optional[str] = None
    liquidity: Optional[str] = None
    order_blocks: Sequence[str] = field(default_factory=tuple)
    fvg: Sequence[str] = field(default_factory=tuple)
    support: Sequence[str] = field(default_factory=tuple)
    resistance: Sequence[str] = field(default_factory=tuple)
    confidence: float = 0.0
    notes: Optional[str] = None
    language: str = "en"


@dataclass(frozen=True)
class ChartAnalysis:
    """
    TASK 2's own exact output contract: symbol, timeframe, image_type,
    analysis_type, market_structure, trend, liquidity, order_blocks,
    fvg, support, resistance, confidence, notes. `confidence` is
    0.0-1.0, matching `TradingAnalysis.confidence`'s own scale. Never
    carries a BUY/SELL/NO_TRADE verdict of any kind (Rule 2).
    """

    symbol: str
    timeframe: str
    image_type: ChartImageType
    analysis_type: ChartAnalysisType
    market_structure: Optional[str]
    trend: Optional[str]
    liquidity: Optional[str]
    order_blocks: Sequence[str]
    fvg: Sequence[str]
    support: Sequence[str]
    resistance: Sequence[str]
    confidence: float
    notes: Optional[str]
    generated_at: str = ""
