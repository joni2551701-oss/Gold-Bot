"""16_Chart_Layer / Chart_API — chart_layer.chart_api.

Foundation Freeze v1.0 — canonical architecture skeleton.

Canonical documentation: 16_Chart_Layer/Chart_API/README.md

FLOW-016 Chart Service Foundation migrates the single Platform entry
point into this package — Chart_API is the Public / Event / Plugin API
boundary gateway:
  * api      — ChartAPI (create_chart / get_chart / update_chart /
               clear_cache), the single Platform entry point
  * service  — ChartService (coordinates Engine + Cache + Events,
               assembles ChartResponse)
  * events   — Event API: ChartEvent, ChartEventRecorder and the
               chart_requested/created/updated/failed factories
"""
from .api import ChartAPI
from .events import (
    ChartEvent,
    ChartEventRecorder,
    chart_created,
    chart_failed,
    chart_requested,
    chart_updated,
)
from .service import ChartService

__all__ = [
    "ChartAPI",
    "ChartService",
    "ChartEvent",
    "ChartEventRecorder",
    "chart_requested",
    "chart_created",
    "chart_updated",
    "chart_failed",
]
