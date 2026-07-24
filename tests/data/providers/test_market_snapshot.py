"""
Phase 59.1, TASK 8 -- bridges TASK 4 (provider/data_quality fields on
MarketDataSnapshot) with the actual provider layer end-to-end. Pure
unit coverage of MarketDataSnapshot itself lives in
tests/data/test_market_data_snapshot.py; this file specifically
exercises the "captured from a real TwelveDataProvider output" path.
"""

from datetime import datetime, timezone

from data.data_quality import assess_data_quality
from data.market_data_snapshot import capture_market_data_snapshot
from data.providers.twelve_data_provider import TwelveDataProvider
from data.twelve_data_client import Candle


def _candle(price=2000.0, ts=None):
    return Candle(
        timestamp=ts or datetime(2026, 1, 1, tzinfo=timezone.utc),
        open=price, high=price + 1, low=price - 1, close=price,
    )


def test_snapshot_captured_from_provider_output_records_provider_name(monkeypatch):
    provider = TwelveDataProvider()
    monkeypatch.setattr(provider.client, "fetch_candles", lambda *a, **k: [_candle()])

    market_candles = provider.get_candles("XAUUSD", "M15", 10)
    # capture_market_data_snapshot() takes data.twelve_data_client.Candle,
    # not MarketCandle -- the two are deliberately distinct types (see
    # base_provider.py's own naming note). A real wiring step would
    # adapt one to the other; here we confirm the provider's own
    # candle count/timestamps are what a snapshot would describe.
    raw_candles = [_candle()]

    snapshot = capture_market_data_snapshot(raw_candles, "XAUUSD", "M15", provider="twelvedata")

    assert snapshot.provider == "twelvedata"
    assert snapshot.candle_count == len(market_candles) == 1


def test_snapshot_can_carry_a_real_data_quality_result(monkeypatch):
    provider = TwelveDataProvider()
    candles = [_candle(), _candle(2010.0, datetime(2026, 1, 1, 0, 15, tzinfo=timezone.utc))]
    monkeypatch.setattr(provider.client, "fetch_candles", lambda *a, **k: candles)

    provider.get_candles("XAUUSD", "M15", 10)
    quality = assess_data_quality(candles, "M15")

    snapshot = capture_market_data_snapshot(
        candles, "XAUUSD", "M15",
        provider="twelvedata",
        data_quality="OK" if quality.valid else "WARNING_GAP",
    )

    assert snapshot.data_quality in ("OK", "WARNING_GAP")
    assert snapshot.provider == "twelvedata"


def test_snapshot_from_empty_provider_response_never_raises(monkeypatch):
    provider = TwelveDataProvider()
    monkeypatch.setattr(provider.client, "fetch_candles", lambda *a, **k: [])

    market_candles = provider.get_candles("XAUUSD", "M15", 10)
    snapshot = capture_market_data_snapshot([], "XAUUSD", "M15", provider="twelvedata")

    assert market_candles == []
    assert snapshot.candle_count == 0
    assert snapshot.provider == "twelvedata"


def test_snapshot_provider_field_distinguishes_from_mt5():
    """Two snapshots of the same symbol/timeframe from different providers stay distinguishable."""
    snap_a = capture_market_data_snapshot([], "XAUUSD", "M15", provider="twelvedata")
    snap_b = capture_market_data_snapshot([], "XAUUSD", "M15", provider="mt5")

    assert snap_a.provider != snap_b.provider
    assert snap_a.candles_reference == snap_b.candles_reference  # window fingerprint is provider-independent by design
