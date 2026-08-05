"""Chart Service Foundation — chart engine (FLOW-016).

Engine rule (Director Order): the Engine holds the business logic and
drives the Pipeline. It does NOT render (that is the Renderer's job)
and it does NOT own caching or the public API surface (that is the
Service/API's job). Given a ChartRequest, the Engine produces a
ChartObject by running the pipeline.

Canonical home: Chart_Core is the "Chart Engine, Lifecycle, State"
orchestrator per chart_layer/chart_core/README.md.
"""
from __future__ import annotations

from chart_layer.chart_data import ChartObject, ChartRequest

from .pipeline import ChartPipeline


class ChartEngine:
    """Business orchestrator over the Chart Pipeline."""

    def __init__(self, pipeline: ChartPipeline = None) -> None:
        self._pipeline = pipeline or ChartPipeline()

    def process(self, request: ChartRequest) -> ChartObject:
        if not isinstance(request, ChartRequest):
            raise TypeError("process() expects a ChartRequest")
        return self._pipeline.run(request)
