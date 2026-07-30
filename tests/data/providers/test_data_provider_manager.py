"""
TASK-CORE-003 -- tests for the Provider Manager
(data/providers/provider_manager.py): primary/fallback selection,
availability, and symbol-based routing.
"""

from types import SimpleNamespace
from typing import List, Optional, Tuple

from data.providers.base_provider import MarketCandle, MarketDataProvider, ProviderStatus
from data.providers.provider_manager import ProviderManager
from data.providers.registry import ProviderRegistry, build_default_registry


class _FakeProvider(MarketDataProvider):
    """A controllable market provider double -- name + availability set at construction."""

    def __init__(self, name: str, available: bool):
        self._name = name
        self._available = available

    def get_provider_name(self) -> str:
        return self._name

    def get_supported_timeframes(self) -> Tuple[str, ...]:
        return ("M15",)

    def get_candles(self, symbol: str, timeframe: str, limit: int) -> List[MarketCandle]:
        return []

    def get_latest_price(self, symbol: str) -> Optional[float]:
        return None

    def get_market_status(self) -> ProviderStatus:
        return ProviderStatus(available=self._available, reason="" if self._available else "down")


def _settings(primary="twelvedata", **enable):
    flags = {
        "market_data_provider": primary,
        "enable_twelvedata": True,
        "enable_mt5": True,
        "enable_binance": True,
        "enable_bitget": True,
        "enable_keynorq": True,
    }
    flags.update(enable)
    return SimpleNamespace(providers=SimpleNamespace(**flags))


def _registry(*providers) -> ProviderRegistry:
    reg = ProviderRegistry()
    for p in providers:
        reg.register(p)
    return reg


def test_construction_never_raises_with_defaults():
    # Uses the real default registry + real config singleton.
    mgr = ProviderManager()
    assert isinstance(mgr, ProviderManager)


def test_primary_name_from_settings():
    mgr = ProviderManager(registry=_registry(), settings=_settings(primary="Bitget"))
    assert mgr.primary_name == "bitget"


def test_provider_chain_primary_first_then_priority():
    reg = _registry(
        _FakeProvider("twelvedata", True),
        _FakeProvider("binance", False),
        _FakeProvider("bitget", False),
    )
    mgr = ProviderManager(registry=reg, settings=_settings(primary="bitget"))
    chain = mgr.provider_chain()
    assert chain[0] == "bitget"          # configured primary leads
    assert set(chain) == {"bitget", "twelvedata", "binance"}


def test_provider_chain_excludes_disabled():
    reg = _registry(_FakeProvider("twelvedata", True), _FakeProvider("binance", True))
    mgr = ProviderManager(registry=reg, settings=_settings(primary="twelvedata", enable_binance=False))
    assert "binance" not in mgr.provider_chain()


def test_get_active_provider_returns_first_available():
    reg = _registry(
        _FakeProvider("twelvedata", False),
        _FakeProvider("binance", True),
    )
    mgr = ProviderManager(registry=reg, settings=_settings(primary="twelvedata"))
    active = mgr.get_active_provider()
    assert active is not None
    assert active.get_provider_name() == "binance"


def test_get_active_provider_none_when_all_unavailable():
    reg = _registry(_FakeProvider("twelvedata", False), _FakeProvider("mt5", False))
    mgr = ProviderManager(registry=reg, settings=_settings(primary="twelvedata"))
    assert mgr.get_active_provider() is None


def test_is_available_and_available_providers():
    reg = _registry(_FakeProvider("twelvedata", True), _FakeProvider("bitget", False))
    mgr = ProviderManager(registry=reg, settings=_settings())
    assert mgr.is_available("twelvedata") is True
    assert mgr.is_available("bitget") is False
    assert mgr.is_available("nonexistent") is False
    assert "twelvedata" in mgr.available_providers()


def test_resolve_crypto_symbol_prefers_available_crypto_provider():
    reg = _registry(
        _FakeProvider("twelvedata", True),
        _FakeProvider("bitget", True),
    )
    mgr = ProviderManager(registry=reg, settings=_settings(primary="twelvedata"))
    chosen = mgr.resolve("BTCUSDT")
    assert chosen is not None
    assert chosen.get_provider_name() == "bitget"


def test_resolve_non_crypto_symbol_uses_normal_chain():
    reg = _registry(
        _FakeProvider("twelvedata", True),
        _FakeProvider("bitget", True),
    )
    mgr = ProviderManager(registry=reg, settings=_settings(primary="twelvedata"))
    chosen = mgr.resolve("XAUUSD")
    assert chosen is not None
    assert chosen.get_provider_name() == "twelvedata"


def test_resolve_crypto_falls_back_when_no_crypto_available():
    reg = _registry(
        _FakeProvider("twelvedata", True),
        _FakeProvider("bitget", False),
    )
    mgr = ProviderManager(registry=reg, settings=_settings(primary="twelvedata"))
    chosen = mgr.resolve("ETHUSDT")
    assert chosen is not None
    assert chosen.get_provider_name() == "twelvedata"


def test_default_registry_has_all_five_market_providers_plus_fred():
    reg = build_default_registry()
    names = set(reg.all_names())
    assert {"twelvedata", "mt5", "binance", "bitget", "keynorq"}.issubset(names)
    assert "fred" in names  # fundamental provider also catalogued


def test_manager_over_default_registry_active_is_twelvedata_or_none():
    # With the real default registry, only TwelveData can be live (and
    # only if a key is configured); every stub reports unavailable. So
    # the active provider is either twelvedata or None, never a stub.
    mgr = ProviderManager(registry=build_default_registry(), settings=_settings(primary="twelvedata"))
    active = mgr.get_active_provider()
    assert active is None or active.get_provider_name() == "twelvedata"


def test_fundamental_provider_excluded_from_market_routing():
    # FRED is registered but is not a MarketDataProvider -> never chosen.
    reg = build_default_registry()
    mgr = ProviderManager(registry=reg, settings=_settings(primary="twelvedata"))
    assert "fred" not in mgr.provider_chain()
