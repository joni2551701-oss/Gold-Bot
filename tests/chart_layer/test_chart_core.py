"""FLOW-016 Chart Service Foundation -- Chart_Core unit/integration tests
(pipeline + engine).
"""

import pytest

from chart_layer.chart_core import ChartEngine, ChartPipeline, EmptyMarketDataSource, MarketDataSource
from chart_layer.chart_data import Candle, ChartModel, ChartObject, ChartRequest


class _FakeSource:
    def load_candles(self, asset, timeframe, history_size):
        return [Candle(timestamp=i, open=1, high=2, low=0, close=1) for i in range(history_size)]


def test_empty_source_satisfies_protocol():
    assert isinstance(EmptyMarketDataSource(), MarketDataSource)
    assert EmptyMarketDataSource().load_candles("XAUUSD", "M15", 100) == []


def test_pipeline_stages_and_run():
    pipe = ChartPipeline()
    req = ChartRequest(asset="XAUUSD", timeframe="M15")
    validated = pipe.validate_input(req)
    candles = pipe.load_market_data(validated)
    model = pipe.create_chart_model(validated, candles)
    assert isinstance(model, ChartModel)
    assert isinstance(pipe.render(validated, model), ChartObject)
    assert isinstance(pipe.run(req), ChartObject)


def test_pipeline_uses_injected_source():
    pipe = ChartPipeline(market_data_source=_FakeSource())
    req = ChartRequest(asset="XAUUSD", timeframe="M15", history_size=5)
    model = pipe.create_chart_model(req, pipe.load_market_data(req))
    assert model.candle_count == 5


def test_engine_process():
    obj = ChartEngine().process(ChartRequest(asset="XAUUSD", timeframe="M15"))
    assert isinstance(obj, ChartObject)
    assert obj.asset == "XAUUSD"


def test_engine_type_check():
    with pytest.raises(TypeError):
        ChartEngine().process("nope")
