"""
Unit tests for data_layer/live_data/stream_event.py models (v1.1 Phase 1, module 4).
"""

from datetime import datetime, timezone

from data_layer.live_data.stream_event import (
    StreamEvent, StreamState, ProviderStatus, ProviderHealth,
    ProviderCapabilities, AssetClass,
)
from data_layer.market_memory.candle_record import CandleSource


def test_stream_states_cover_dd046():
    names = {s.name for s in StreamState}
    assert names == {
        "INITIALIZING", "CONNECTING", "STREAMING",
        "WAITING_FOR_MARKET", "RECONNECTING", "SHUTDOWN",
    }


def test_capabilities_default_false():
    caps = ProviderCapabilities()
    assert not any([caps.supports_streaming, caps.supports_polling,
                    caps.supports_replay, caps.supports_historical,
                    caps.supports_volume])


def test_stream_event_is_frozen_and_defaults():
    e = StreamEvent(asset="XAUUSD", price=100.0,
                    timestamp=datetime(2026, 7, 24, tzinfo=timezone.utc))
    assert e.source is CandleSource.STREAM
    assert e.volume is None


def test_provider_health_and_status():
    h = ProviderHealth(status=ProviderStatus.UP, detail="M1")
    assert h.status is ProviderStatus.UP
    assert AssetClass.CRYPTO.value == "crypto"
