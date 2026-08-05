"""Chart Service Foundation — chart service (FLOW-016).

The Service is the coordination layer behind the public API gateway. It
owns the cache lifecycle and emits lifecycle events; it turns an
Engine-produced ChartObject into a ChartResponse. It does not render and
holds no chart business logic beyond caching/response assembly —
rendering stays in the Renderer, orchestration in the Engine.

Canonical home: Chart_API is the single Public/Event API boundary, so
the Service that assembles responses and emits events lives here.

Full processing chain (Director Order):
    Input Validation -> Market Data Loading -> Chart Model Creation
    -> Render Pipeline -> Cache -> Chart Response
"""
from __future__ import annotations

from chart_layer.chart_core import ChartEngine
from chart_layer.chart_data import ChartCache, ChartRequest, ChartRequestError, ChartResponse

from .events import (
    ChartEventRecorder,
    chart_created,
    chart_failed,
    chart_requested,
    chart_updated,
)


class ChartService:
    """Coordinates Engine + Cache + Events into a ChartResponse."""

    def __init__(
        self,
        engine: ChartEngine = None,
        cache: ChartCache = None,
        events: ChartEventRecorder = None,
    ) -> None:
        self._engine = engine or ChartEngine()
        self._cache = cache or ChartCache()
        self._events = events or ChartEventRecorder()

    @property
    def events(self) -> ChartEventRecorder:
        return self._events

    @property
    def cache(self) -> ChartCache:
        return self._cache

    def create_chart(self, request: ChartRequest, use_cache: bool = True) -> ChartResponse:
        try:
            request.validate()
        except ChartRequestError as exc:
            self._events.emit(chart_failed(None, reason=str(exc)))
            return ChartResponse.failed(str(exc))

        key = request.request_hash()
        self._events.emit(chart_requested(key, asset=request.asset, timeframe=request.timeframe))

        if use_cache:
            cached = self._cache.get(key)
            if cached is not None:
                return self._respond(cached, key, cached=True)

        try:
            chart_object = self._engine.process(request)
        except Exception as exc:  # noqa: BLE001 - Foundation surfaces any engine error as a failed response
            self._events.emit(chart_failed(key, reason=str(exc)))
            return ChartResponse.failed(str(exc))

        if use_cache:
            self._cache.set(key, chart_object)
        self._events.emit(chart_created(key, is_placeholder=chart_object.is_placeholder))
        return self._respond(chart_object, key, cached=False)

    def get_chart(self, request: ChartRequest) -> ChartResponse:
        key = request.request_hash()
        cached = self._cache.get(key)
        if cached is None:
            return self.create_chart(request)
        return self._respond(cached, key, cached=True)

    def update_chart(self, request: ChartRequest) -> ChartResponse:
        key = request.request_hash()
        self._cache.invalidate(key)
        response = self.create_chart(request)
        self._events.emit(chart_updated(key))
        return response

    def clear_cache(self) -> None:
        self._cache.clear()

    # --- helpers ------------------------------------------------------
    def _respond(self, chart_object, key: str, cached: bool) -> ChartResponse:
        metadata = {
            "asset": chart_object.asset,
            "timeframe": chart_object.timeframe,
            "chart_type": chart_object.chart_type.value,
            "output_format": chart_object.output_format.value,
            "is_placeholder": chart_object.is_placeholder,
        }
        if chart_object.is_placeholder:
            return ChartResponse.placeholder(chart_reference=key, metadata=metadata)
        return ChartResponse.success(chart_reference=key, metadata=metadata, cached=cached)
