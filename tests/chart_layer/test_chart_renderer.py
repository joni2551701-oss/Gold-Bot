"""FLOW-016 Chart Service Foundation -- Chart_Renderer unit tests."""

import pytest

from chart_layer.chart_data import ChartModel, ChartObject, ChartType, OutputFormat
from chart_layer.chart_renderer import ChartRenderer


def _model():
    return ChartModel(asset="XAUUSD", timeframe="M15", chart_type=ChartType.CANDLESTICK)


def test_render_returns_placeholder_chart_object():
    obj = ChartRenderer().render(_model(), OutputFormat.PNG)
    assert isinstance(obj, ChartObject)
    assert obj.asset == "XAUUSD"
    assert obj.output_format is OutputFormat.PNG
    assert obj.is_placeholder is True
    assert obj.metadata["candle_count"] == 0
    assert obj.metadata["renderer"] == "foundation-placeholder"


def test_render_type_checks():
    with pytest.raises(TypeError):
        ChartRenderer().render("not-a-model", OutputFormat.PNG)
    with pytest.raises(TypeError):
        ChartRenderer().render(_model(), "png")
