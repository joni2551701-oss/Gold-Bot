"""GoldBot Core Owner Monitoring Alpha, TASK 3 -- core_layer/health_monitor/market_monitor.py tests."""

from unittest.mock import MagicMock

from core_layer.health_monitor.market_monitor import get_market_health
from core_layer.health_monitor.models import MarketHealth
from core_layer.health_monitor.provider_health import ProviderHealthReport, ProviderHealthStatus


def _registry_with_provider(provider):
    registry = MagicMock()
    registry.get.return_value = provider
    return registry


def test_get_market_health_returns_market_health():
    registry = _registry_with_provider(MagicMock())
    health = get_market_health("XAUUSD", "twelvedata", registry=registry)
    assert isinstance(health, MarketHealth)


def test_get_market_health_relays_symbol():
    registry = _registry_with_provider(MagicMock())
    health = get_market_health("XAUUSD", "twelvedata", registry=registry)
    assert health.symbol == "XAUUSD"


def test_get_market_health_unknown_provider_returns_unknown_status():
    registry = MagicMock()
    registry.get.return_value = None
    health = get_market_health("XAUUSD", "does-not-exist", registry=registry)
    assert health.data_source_status == "UNKNOWN"


def test_get_market_health_relays_latency_and_status(monkeypatch):
    registry = _registry_with_provider(MagicMock())
    report = ProviderHealthReport(provider_name="twelvedata", status=ProviderHealthStatus.ONLINE, latency_ms=42.0)
    monkeypatch.setattr("core_layer.health_monitor.market_monitor.check_provider_health", lambda provider: report)
    health = get_market_health("XAUUSD", "twelvedata", registry=registry)
    assert health.data_source_status == "ONLINE"
    assert health.latency_ms == 42.0


def test_get_market_health_never_raises_on_health_check_failure(monkeypatch):
    registry = _registry_with_provider(MagicMock())

    def _raise(provider):
        raise Exception("boom")

    monkeypatch.setattr("core_layer.health_monitor.market_monitor.check_provider_health", _raise)
    health = get_market_health("XAUUSD", "twelvedata", registry=registry)
    assert health.data_source_status == "UNKNOWN"


def test_get_market_health_last_price_defaults_none():
    registry = _registry_with_provider(MagicMock())
    health = get_market_health("XAUUSD", "twelvedata", registry=registry)
    assert health.last_price is None


def test_get_market_health_last_update_defaults_none():
    registry = _registry_with_provider(MagicMock())
    health = get_market_health("XAUUSD", "twelvedata", registry=registry)
    assert health.last_update is None


def test_get_market_health_relays_caller_supplied_last_price():
    registry = _registry_with_provider(MagicMock())
    health = get_market_health("XAUUSD", "twelvedata", last_price=2345.67, registry=registry)
    assert health.last_price == 2345.67


def test_get_market_health_relays_caller_supplied_last_update():
    registry = _registry_with_provider(MagicMock())
    health = get_market_health("XAUUSD", "twelvedata", last_update="2026-01-01T00:00:00Z", registry=registry)
    assert health.last_update == "2026-01-01T00:00:00Z"


def test_get_market_health_never_fabricates_a_price():
    """Never invents last_price when none was supplied and the provider has no price concept."""
    registry = _registry_with_provider(MagicMock())
    health = get_market_health("XAUUSD", "twelvedata", registry=registry)
    assert health.last_price is None


def test_get_market_health_never_computes_a_trading_verdict():
    from dataclasses import fields
    field_names = {f.name for f in fields(MarketHealth)}
    forbidden = {"signal", "decision", "verdict", "direction"}
    assert field_names.isdisjoint(forbidden)


def test_get_market_health_default_provider_uses_real_registry():
    """Never raises when no registry override is supplied -- build_default_registry() is used."""
    health = get_market_health("XAUUSD", "twelvedata")
    assert health.symbol == "XAUUSD"


def test_get_market_health_different_symbols_independent():
    registry = _registry_with_provider(MagicMock())
    gold = get_market_health("XAUUSD", "twelvedata", registry=registry)
    silver = get_market_health("XAGUSD", "twelvedata", registry=registry)
    assert gold.symbol != silver.symbol
