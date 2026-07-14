"""
Pre-Phase 59 Architecture Readiness Review, AC-07 -- confirms
MarketDataNormalizer.get_candles()'s existing behavior (graceful
degradation to an empty list on any fetch failure) is unchanged after
wiring in classify_api_error() for richer logging only.
"""

import logging

from data.market_data import MarketDataNormalizer


def test_get_candles_still_returns_empty_list_on_fetch_failure(monkeypatch):
    """The AC-07 logging addition must not change the existing degrade-to-[] contract."""
    normalizer = MarketDataNormalizer()

    def _raise(*args, **kwargs):
        raise ValueError("TWELVE_DATA_API_KEY not configured.")

    monkeypatch.setattr(normalizer.client, "fetch_candles", _raise)

    result = normalizer.get_candles("XAUUSD", "M15", 200)

    assert result == []


def test_get_candles_never_raises_on_fetch_failure(monkeypatch):
    normalizer = MarketDataNormalizer()
    monkeypatch.setattr(normalizer.client, "fetch_candles", lambda *a, **k: (_ for _ in ()).throw(ConnectionError("network down")))

    result = normalizer.get_candles("XAUUSD", "M15", 200)  # must not raise

    assert result == []


def test_get_candles_logs_a_structured_error_on_failure(monkeypatch, caplog):
    normalizer = MarketDataNormalizer()

    def _raise(*args, **kwargs):
        raise ValueError("Twelve Data API Error: rate limit exceeded")

    monkeypatch.setattr(normalizer.client, "fetch_candles", _raise)

    with caplog.at_level(logging.ERROR, logger="MarketDataNormalizer"):
        normalizer.get_candles("XAUUSD", "M15", 200)

    messages = "\n".join(caplog.messages)
    assert "API_002" in messages  # the classified ExternalAPIError code appears in the structured log line
    assert "MarketDataNormalizer" in messages


def test_get_candles_still_works_normally_when_fetch_succeeds(monkeypatch):
    """Confirms the AC-07 change only touches the except path -- the success path is completely untouched."""
    from data.twelve_data_client import Candle
    from datetime import datetime, timezone

    normalizer = MarketDataNormalizer()
    real_candle = Candle(timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc), open=100.0, high=105.0, low=95.0, close=101.0)
    monkeypatch.setattr(normalizer.client, "fetch_candles", lambda *a, **k: [real_candle])

    result = normalizer.get_candles("XAUUSD", "M15", 200)

    assert result == [real_candle]
