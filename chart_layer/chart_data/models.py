"""Chart Service Foundation — core data models (FLOW-016).

Canonical home: Chart_Data owns Candle / OHLCV / chart data structures
(chart_layer/chart_data/README.md). FLOW-016 Core Infrastructure only —
no drawing tools, indicators, templates, or real rendering here; those
attach in later Flows on top of this Foundation.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ChartType(str, Enum):
    CANDLESTICK = "candlestick"
    LINE = "line"
    BAR = "bar"
    AREA = "area"


class OutputFormat(str, Enum):
    PNG = "png"
    SVG = "svg"
    JSON = "json"


class ChartStatus(str, Enum):
    CREATED = "created"
    PLACEHOLDER = "placeholder"
    CACHED = "cached"
    FAILED = "failed"


@dataclass(frozen=True)
class Candle:
    """A single OHLCV candle — the minimal market data unit for a chart."""

    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0


@dataclass
class ChartModel:
    """The intermediate model the pipeline builds before rendering."""

    asset: str
    timeframe: str
    chart_type: ChartType
    candles: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    @property
    def candle_count(self) -> int:
        return len(self.candles)


@dataclass
class ChartObject:
    """Renderer output. In the Foundation build the payload is a
    contract-complete placeholder (real image bytes attach later)."""

    asset: str
    timeframe: str
    chart_type: ChartType
    output_format: OutputFormat
    payload: Optional[bytes] = None
    is_placeholder: bool = True
    width: int = 0
    height: int = 0
    metadata: dict = field(default_factory=dict)
