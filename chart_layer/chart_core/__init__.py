"""16_Chart_Layer / Chart_Core — chart_layer.chart_core.

Foundation Freeze v1.0 — canonical architecture skeleton.

Canonical documentation: 16_Chart_Layer/Chart_Core/README.md

FLOW-016 Chart Service Foundation migrates the Chart Engine and its
Pipeline into their canonical home here — Chart_Core owns the Chart
Engine / Lifecycle / State orchestration:
  * pipeline — ChartPipeline (Input Validation -> Market Data Loading
               -> Chart Model Creation -> Render), plus the
               MarketDataSource port and EmptyMarketDataSource default
  * engine   — ChartEngine (business orchestrator driving the pipeline)
"""
from .engine import ChartEngine
from .pipeline import ChartPipeline, EmptyMarketDataSource, MarketDataSource

__all__ = ["ChartEngine", "ChartPipeline", "MarketDataSource", "EmptyMarketDataSource"]
