"""Chart Service Foundation — chart pipeline (FLOW-016).

Processing stages (Director Order):
    Input Validation -> Market Data Loading -> Chart Model Creation
    -> Render Pipeline -> (Cache/Response handled by the API/Service)

Canonical home: Chart_Core owns the Chart Engine / Lifecycle / State,
i.e. the orchestration of how a request becomes a rendered chart. The
pipeline is the ordered sequence of steps that turns a validated
ChartRequest into a rendered ChartObject. Market data enters through a
MarketDataSource port (Market Memory plugs in here later); the
Foundation ships EmptyMarketDataSource so the chain is end-to-end
runnable today without a live data feed.
"""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from chart_layer.chart_data import ChartModel, ChartObject, ChartRequest
from chart_layer.chart_renderer import ChartRenderer


@runtime_checkable
class MarketDataSource(Protocol):
    """Port for market data. Market Memory implements this later."""

    def load_candles(self, asset: str, timeframe: str, history_size: int) -> list:
        ...


class EmptyMarketDataSource:
    """Foundation default: returns no candles, always succeeds."""

    def load_candles(self, asset: str, timeframe: str, history_size: int) -> list:
        return []


class ChartPipeline:
    """Ordered Input->Processing chain producing a ChartObject."""

    def __init__(self, renderer: ChartRenderer = None, market_data_source: MarketDataSource = None) -> None:
        self._renderer = renderer or ChartRenderer()
        self._market_data_source = market_data_source or EmptyMarketDataSource()

    # --- stages -------------------------------------------------------
    def validate_input(self, request: ChartRequest) -> ChartRequest:
        return request.validate()

    def load_market_data(self, request: ChartRequest) -> list:
        return list(
            self._market_data_source.load_candles(
                request.asset, request.timeframe, request.history_size
            )
        )

    def create_chart_model(self, request: ChartRequest, candles: list) -> ChartModel:
        return ChartModel(
            asset=request.asset,
            timeframe=request.timeframe,
            chart_type=request.chart_type,
            candles=list(candles),
            metadata={"history_size": request.history_size},
        )

    def render(self, request: ChartRequest, model: ChartModel) -> ChartObject:
        return self._renderer.render(model, request.output_format)

    # --- orchestration ------------------------------------------------
    def run(self, request: ChartRequest) -> ChartObject:
        validated = self.validate_input(request)
        candles = self.load_market_data(validated)
        model = self.create_chart_model(validated, candles)
        return self.render(validated, model)
