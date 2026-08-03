"""
market/ facade — TrendState projection (TASK-CORE-005).

Proves the trend view relabels context.structure.trend onto the market
vocabulary without recomputing anything, and is honest (UNKNOWN) when
context reports no directional bias.
"""

from types import SimpleNamespace

from data_layer.live_data.market.trend_state import TrendState


def _schema(trend=None, bos=False, choch=False):
    return SimpleNamespace(structure=SimpleNamespace(trend=trend, bos=bos, choch=choch))


def test_bullish_and_bearish_map_through():
    assert TrendState.from_context(_schema("BULLISH")) is TrendState.BULLISH
    assert TrendState.from_context(_schema("bearish")) is TrendState.BEARISH


def test_range_maps_to_neutral():
    assert TrendState.from_context(_schema("RANGE")) is TrendState.NEUTRAL


def test_absent_trend_is_unknown():
    assert TrendState.from_context(_schema(None)) is TrendState.UNKNOWN
    assert TrendState.from_context(SimpleNamespace()) is TrendState.UNKNOWN


def test_bos_without_trend_reads_neutral_not_fabricated_direction():
    assert TrendState.from_context(_schema(None, bos=True)) is TrendState.NEUTRAL
    assert TrendState.from_context(_schema(None, choch=True)) is TrendState.NEUTRAL


def test_unrecognised_label_is_mixed():
    assert TrendState.from_context(_schema("SIDEWAYS_ISH")) is TrendState.MIXED
