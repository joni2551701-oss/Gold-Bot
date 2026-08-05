"""Chart Service Foundation — chart renderer (FLOW-016).

Renderer rule (Director Order): the renderer ONLY renders. It takes a
ChartModel and an output format and returns a ChartObject. It never
reads Market Memory, the database, or the platform, and holds no
business logic. In the Foundation build the output is a
contract-complete placeholder — real image/SVG bytes attach in a later
Flow without changing this signature.
"""
from __future__ import annotations

from chart_layer.chart_data import ChartModel, ChartObject, OutputFormat


class ChartRenderer:
    """Turns a ChartModel into a ChartObject. Pure, side-effect free."""

    def render(self, model: ChartModel, output_format: OutputFormat) -> ChartObject:
        if not isinstance(model, ChartModel):
            raise TypeError("render() expects a ChartModel")
        if not isinstance(output_format, OutputFormat):
            raise TypeError("output_format must be an OutputFormat")
        return ChartObject(
            asset=model.asset,
            timeframe=model.timeframe,
            chart_type=model.chart_type,
            output_format=output_format,
            payload=None,
            is_placeholder=True,
            width=0,
            height=0,
            metadata={
                "candle_count": model.candle_count,
                "renderer": "foundation-placeholder",
            },
        )
