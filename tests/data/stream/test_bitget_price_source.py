"""Unit tests for data_layer/live_data/bitget_price_source.py (TASK-DATA-001)."""

import pytest

from data_layer.live_data.bitget_price_source import BitgetPriceSource
from data_layer.live_data.stream_event import ProviderStatus


def test_capabilities_declare_polling_and_volume_only():
    source = BitgetPriceSource()
    caps = source.capabilities
    assert caps.supports_polling is True
    assert caps.supports_streaming is False
    assert caps.supports_volume is True


def test_connect_reflects_stub_unavailability():
    source = BitgetPriceSource()
    source.connect()
    assert source.status() is ProviderStatus.DOWN
    assert source.health().last_error


def test_read_propagates_not_implemented_for_isolation():
    source = BitgetPriceSource()
    source.connect()
    with pytest.raises(NotImplementedError):
        source.read()


def test_disconnect_sets_down():
    source = BitgetPriceSource()
    source.disconnect()
    assert source.status() is ProviderStatus.DOWN
