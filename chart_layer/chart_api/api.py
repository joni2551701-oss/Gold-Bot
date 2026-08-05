"""Chart Service Foundation — chart API (FLOW-016).

API rule (Director Order): the Chart API is the single Platform entry
point into the Chart subsystem. Nothing outside chart_layer should
reach the Engine, Pipeline, Renderer or Cache directly — they come
through here. The API is a thin facade over the Service; it adds no
business logic of its own.

Public surface: create_chart(), update_chart(), get_chart(),
clear_cache().
"""
from __future__ import annotations

from chart_layer.chart_data import ChartRequest, ChartResponse

from .service import ChartService


class ChartAPI:
    """The single Platform-facing entry point for charts."""

    def __init__(self, service: ChartService = None) -> None:
        self._service = service or ChartService()

    def create_chart(self, request: ChartRequest) -> ChartResponse:
        return self._service.create_chart(request)

    def get_chart(self, request: ChartRequest) -> ChartResponse:
        return self._service.get_chart(request)

    def update_chart(self, request: ChartRequest) -> ChartResponse:
        return self._service.update_chart(request)

    def clear_cache(self) -> None:
        self._service.clear_cache()
