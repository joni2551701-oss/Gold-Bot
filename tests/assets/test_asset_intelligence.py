"""
Phase A12 -- Asset Intelligence foundation tests (assets/).

No mocking -- real AssetDefinition/AssetRegistry objects, same
convention as tests/strategies/test_strategy_lifecycle.py.

Asset Intelligence stores metadata only: it does not fetch market
data, does not run a strategy, does not size a position, and does not
write to the database.
"""

import dataclasses

import pytest

from assets.asset_model import AssetDefinition
from assets.asset_type import AssetType
from assets.asset_registry import (
    AssetRegistry,
    DuplicateAssetSymbolError,
    DEFAULT_ASSETS,
    build_default_registry,
)
from assets.profiles.gold import GOLD_ASSET


def _definition(symbol="TEST", asset_type=AssetType.UNKNOWN):
    return AssetDefinition(
        symbol=symbol,
        name="Test Asset",
        asset_type=asset_type,
        market="TEST_MARKET",
        base_currency="XXX",
        quote_currency="YYY",
    )


def test_asset_creation_matches_director_example():
    definition = AssetDefinition(
        symbol="XAUUSD",
        name="Gold",
        asset_type=AssetType.GOLD,
        market="FOREX",
        base_currency="USD",
        quote_currency="USD",
    )

    assert definition.symbol == "XAUUSD"
    assert definition.name == "Gold"
    assert definition.asset_type == AssetType.GOLD
    assert definition.market == "FOREX"
    assert definition.base_currency == "USD"
    assert definition.quote_currency == "USD"
    # Future hooks -- never fabricated, always None unless explicitly passed.
    assert definition.trading_session is None
    assert definition.volatility_class is None
    assert definition.news_sensitivity is None
    assert definition.fundamental_profile is None
    assert definition.session_profile is None
    assert definition.risk_profile is None
    assert definition.news_profile is None


def test_asset_definition_is_immutable():
    definition = _definition()
    with pytest.raises(dataclasses.FrozenInstanceError):
        definition.symbol = "CHANGED"


def test_registry_register_get_list():
    registry = AssetRegistry()
    a = _definition(symbol="A")
    b = _definition(symbol="B")

    registry.register(a)
    registry.register(b)

    assert registry.get("A") is a
    assert registry.get("B") is b
    listed = registry.list()
    assert len(listed) == 2
    assert a in listed
    assert b in listed


def test_get_returns_none_for_unknown_symbol():
    registry = AssetRegistry()
    assert registry.get("DOES_NOT_EXIST") is None


def test_duplicate_symbol_raises():
    registry = AssetRegistry()
    registry.register(_definition(symbol="DUP"))

    with pytest.raises(DuplicateAssetSymbolError):
        registry.register(_definition(symbol="DUP"))


def test_by_type_filters_correctly():
    registry = AssetRegistry()
    registry.register(_definition(symbol="G", asset_type=AssetType.GOLD))
    registry.register(_definition(symbol="F1", asset_type=AssetType.FOREX))
    registry.register(_definition(symbol="F2", asset_type=AssetType.FOREX))
    registry.register(_definition(symbol="C", asset_type=AssetType.CRYPTO))

    forex_symbols = {d.symbol for d in registry.by_type(AssetType.FOREX)}
    assert forex_symbols == {"F1", "F2"}
    assert [d.symbol for d in registry.by_type(AssetType.GOLD)] == ["G"]
    assert registry.by_type(AssetType.STOCK) == []


def test_gold_profile_exists_and_uses_real_codebase_values():
    """
    GOLD_ASSET.symbol must match the exact string this codebase
    already runs (main.py's TradingPipeline(symbol="XAUUSD"),
    telegram/signal_service.py's DEFAULT_SYMBOL) -- not a placeholder.
    """
    assert GOLD_ASSET.symbol == "XAUUSD"
    assert GOLD_ASSET.name == "Gold"
    assert GOLD_ASSET.asset_type == AssetType.GOLD
    assert GOLD_ASSET.base_currency == "XAU"
    assert GOLD_ASSET.quote_currency == "USD"
    # Future hooks -- never fabricated for Gold either.
    assert GOLD_ASSET.trading_session is None
    assert GOLD_ASSET.volatility_class is None
    assert GOLD_ASSET.news_sensitivity is None
    assert GOLD_ASSET.fundamental_profile is None
    assert GOLD_ASSET.session_profile is None
    assert GOLD_ASSET.risk_profile is None
    assert GOLD_ASSET.news_profile is None


def test_default_registry_contains_only_gold():
    """
    build_default_registry() must register exactly the one asset this
    codebase actually trades today -- no Forex/Crypto/Index/Stock
    asset is introduced.
    """
    registry = build_default_registry()

    assert len(DEFAULT_ASSETS) == 1
    assert [d.symbol for d in registry.list()] == ["XAUUSD"]
    assert registry.get("XAUUSD") is GOLD_ASSET
    assert registry.by_type(AssetType.GOLD) == [GOLD_ASSET]
    assert registry.by_type(AssetType.FOREX) == []
    assert registry.by_type(AssetType.CRYPTO) == []


def test_build_default_registry_returns_independent_instances():
    """Each call returns its own registry -- mutating one must not affect another."""
    first = build_default_registry()
    second = build_default_registry()

    first.register(_definition(symbol="EXTRA"))

    assert first.get("EXTRA") is not None
    assert second.get("EXTRA") is None


def test_future_compatibility_field_shape_is_stable():
    """AssetDefinition is a plain, introspectable dataclass -- a future consumer can rely on its field set."""
    field_names = {f.name for f in dataclasses.fields(AssetDefinition)}
    assert field_names == {
        "symbol", "name", "asset_type", "market", "base_currency", "quote_currency",
        "trading_session", "volatility_class", "news_sensitivity",
        "fundamental_profile", "session_profile", "risk_profile", "news_profile",
    }

    # Direct construction without any hook must still work (defaults apply).
    minimal = AssetDefinition(
        symbol="MIN", name="Minimal", asset_type=AssetType.UNKNOWN,
        market="TEST", base_currency="XXX", quote_currency="YYY",
    )
    assert minimal.trading_session is None
    assert minimal.volatility_class is None
    assert minimal.news_sensitivity is None
    assert minimal.fundamental_profile is None
    assert minimal.session_profile is None
    assert minimal.risk_profile is None
    assert minimal.news_profile is None


def test_no_fake_data_across_all_asset_types():
    """Every AssetType, when a definition is built without explicitly setting a hook, must leave every hook None."""
    for asset_type in AssetType:
        definition = _definition(symbol=f"SYM_{asset_type.value}", asset_type=asset_type)
        assert definition.trading_session is None
        assert definition.volatility_class is None
        assert definition.news_sensitivity is None
        assert definition.fundamental_profile is None
        assert definition.session_profile is None
        assert definition.risk_profile is None
        assert definition.news_profile is None
