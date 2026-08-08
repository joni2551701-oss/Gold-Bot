"""
REAL-DATA-008 -- unit tests for
data_layer/providers/twelve_data_client.py::TwelveDataClient.get_price().

Mocks requests.get (no real network / no real key). Verifies the /price
real-time endpoint contract: success returns a float, an API error body
raises, and a missing key raises. The api key is never asserted into any
message text.
"""

import pytest

from data_layer.providers.twelve_data_client import TwelveDataClient
import data_layer.providers.twelve_data_client.twelve_data_client as tdc_mod


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


def _client_with_key(monkeypatch, key="fake-key"):
    client = TwelveDataClient()
    monkeypatch.setattr(client, "api_key", key)
    return client


def test_get_price_success_returns_float(monkeypatch):
    client = _client_with_key(monkeypatch)
    captured = {}

    def _fake_get(url, params=None, timeout=None):
        captured["url"] = url
        captured["params"] = params
        return _FakeResponse({"price": "2412.34"})

    monkeypatch.setattr(tdc_mod.requests, "get", _fake_get)

    price = client.get_price("XAUUSD")

    assert price == 2412.34
    assert isinstance(price, float)
    # hits the /price endpoint, NOT the /time_series candle endpoint
    assert captured["url"] == TwelveDataClient.PRICE_URL
    assert captured["url"] != TwelveDataClient.BASE_URL
    # symbol formatted XAUUSD -> XAU/USD via the existing formatter
    assert captured["params"]["symbol"] == "XAU/USD"
    # no interval/outputsize (that is the candle endpoint's shape)
    assert "interval" not in captured["params"]


def test_get_price_api_error_body_raises(monkeypatch):
    client = _client_with_key(monkeypatch)

    def _fake_get(url, params=None, timeout=None):
        return _FakeResponse({"status": "error", "code": 400,
                              "message": "symbol not found"})

    monkeypatch.setattr(tdc_mod.requests, "get", _fake_get)

    with pytest.raises(ValueError):
        client.get_price("XAUUSD")


def test_get_price_missing_key_raises(monkeypatch):
    client = TwelveDataClient()
    monkeypatch.setattr(client, "api_key", None)

    with pytest.raises(ValueError) as exc:
        client.get_price("XAUUSD")
    assert "TWELVE_DATA_API_KEY not configured" in str(exc.value)


def test_get_price_none_price_returns_none(monkeypatch):
    client = _client_with_key(monkeypatch)

    def _fake_get(url, params=None, timeout=None):
        return _FakeResponse({"symbol": "XAU/USD"})  # no "price" key

    monkeypatch.setattr(tdc_mod.requests, "get", _fake_get)

    assert client.get_price("XAUUSD") is None


def test_get_price_network_error_raises_connection_error(monkeypatch):
    client = _client_with_key(monkeypatch)

    def _fake_get(url, params=None, timeout=None):
        raise tdc_mod.requests.exceptions.ConnectionError("network down")

    monkeypatch.setattr(tdc_mod.requests, "get", _fake_get)
    # skip real backoff sleeps
    monkeypatch.setattr(tdc_mod.time, "sleep", lambda *_a, **_k: None)

    with pytest.raises(ConnectionError):
        client.get_price("XAUUSD")
