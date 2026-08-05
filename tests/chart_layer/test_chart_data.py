"""FLOW-016 Chart Service Foundation -- Chart_Data unit tests
(models + request + response + cache).
"""

import time

import pytest

from chart_layer.chart_data import (
    Candle,
    ChartCache,
    ChartModel,
    ChartObject,
    ChartRequest,
    ChartRequestError,
    ChartResponse,
    ChartStatus,
    ChartType,
    OutputFormat,
)


# --- models ---------------------------------------------------------------
def test_enum_values():
    assert ChartType.CANDLESTICK.value == "candlestick"
    assert {f.value for f in OutputFormat} == {"png", "svg", "json"}
    assert {s.value for s in ChartStatus} == {"created", "placeholder", "cached", "failed"}


def test_candle_is_frozen():
    candle = Candle(timestamp=1, open=1.0, high=2.0, low=0.5, close=1.5)
    assert candle.volume == 0.0
    with pytest.raises(Exception):
        candle.close = 9.0  # type: ignore[misc]


def test_chart_model_candle_count():
    model = ChartModel(asset="XAUUSD", timeframe="M15", chart_type=ChartType.CANDLESTICK)
    assert model.candle_count == 0
    model.candles.append(Candle(timestamp=1, open=1, high=2, low=0, close=1))
    assert model.candle_count == 1


def test_chart_object_defaults_to_placeholder():
    obj = ChartObject(
        asset="XAUUSD", timeframe="M15", chart_type=ChartType.CANDLESTICK, output_format=OutputFormat.PNG
    )
    assert obj.is_placeholder is True
    assert obj.payload is None


# --- request --------------------------------------------------------------
def test_request_defaults_and_validate():
    req = ChartRequest(asset="XAUUSD", timeframe="M15")
    assert req.history_size == 100
    assert req.validate() is req


@pytest.mark.parametrize(
    "kwargs",
    [
        {"asset": "", "timeframe": "M15"},
        {"asset": "XAUUSD", "timeframe": ""},
        {"asset": "XAUUSD", "timeframe": "M15", "history_size": 0},
        {"asset": "XAUUSD", "timeframe": "M15", "history_size": -1},
    ],
)
def test_request_validate_rejects(kwargs):
    with pytest.raises(ChartRequestError):
        ChartRequest(**kwargs).validate()


def test_request_hash_deterministic_and_sensitive():
    base = ChartRequest(asset="XAUUSD", timeframe="M15").request_hash()
    assert base == ChartRequest(asset="XAUUSD", timeframe="M15").request_hash()
    assert base != ChartRequest(asset="EURUSD", timeframe="M15").request_hash()
    assert base != ChartRequest(asset="XAUUSD", timeframe="H1").request_hash()
    assert base != ChartRequest(asset="XAUUSD", timeframe="M15", output_format=OutputFormat.SVG).request_hash()


# --- response -------------------------------------------------------------
def test_response_variants():
    assert ChartResponse.success("ref").status is ChartStatus.CREATED
    assert ChartResponse.success("ref", cached=True).status is ChartStatus.CACHED
    assert ChartResponse.placeholder("ref").status is ChartStatus.PLACEHOLDER
    failed = ChartResponse.failed("boom")
    assert failed.status is ChartStatus.FAILED
    assert failed.ok is False
    assert failed.metadata["error"] == "boom"


# --- cache ----------------------------------------------------------------
def test_cache_set_get_invalidate_clear():
    cache = ChartCache()
    cache.set("k", "v")
    assert cache.get("k") == "v"
    assert cache.invalidate("k") is True
    assert cache.get("k") is None
    cache.set("a", 1)
    cache.clear()
    assert len(cache) == 0


def test_cache_ttl_expiry_and_never_expire():
    cache = ChartCache(default_ttl=None)
    cache.set("dead", 1, ttl=0.0)
    cache.set("live", 2)  # default None => never expires
    time.sleep(0.001)
    assert "dead" not in cache
    assert cache.get("live") == 2
    assert len(cache) == 1
