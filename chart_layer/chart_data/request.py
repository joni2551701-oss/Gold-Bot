"""Chart Service Foundation — Chart Request contract (FLOW-016).

Minimal contract per Director Order: asset, timeframe, history_size,
chart_type, output_format. Extensible via `extra`. Lives in Chart_Data
because it is a chart-data input contract.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from .models import ChartType, OutputFormat


class ChartRequestError(ValueError):
    """Raised when a ChartRequest fails validation."""


@dataclass
class ChartRequest:
    asset: str
    timeframe: str
    history_size: int = 100
    chart_type: ChartType = ChartType.CANDLESTICK
    output_format: OutputFormat = OutputFormat.PNG
    extra: dict = field(default_factory=dict)

    def validate(self) -> "ChartRequest":
        if not self.asset or not str(self.asset).strip():
            raise ChartRequestError("asset is required")
        if not self.timeframe or not str(self.timeframe).strip():
            raise ChartRequestError("timeframe is required")
        if not isinstance(self.history_size, int) or self.history_size <= 0:
            raise ChartRequestError("history_size must be a positive integer")
        if not isinstance(self.chart_type, ChartType):
            raise ChartRequestError("chart_type must be a ChartType")
        if not isinstance(self.output_format, OutputFormat):
            raise ChartRequestError("output_format must be an OutputFormat")
        return self

    def request_hash(self) -> str:
        key = "|".join(
            [
                str(self.asset),
                str(self.timeframe),
                str(self.history_size),
                self.chart_type.value,
                self.output_format.value,
            ]
        )
        return hashlib.sha256(key.encode("utf-8")).hexdigest()
