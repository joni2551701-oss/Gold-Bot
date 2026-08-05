"""16_Chart_Layer / Chart_Renderer — chart_layer.chart_renderer.

Foundation Freeze v1.0 — canonical architecture skeleton.

Canonical documentation: 16_Chart_Layer/Chart_Renderer/README.md

FLOW-016 Chart Service Foundation migrates the renderer into this
package: ChartRenderer takes a ChartModel + OutputFormat and returns a
ChartObject placeholder. It only renders — no Market Memory, DB or
Platform reads.
"""
from .renderer import ChartRenderer

__all__ = ["ChartRenderer"]
