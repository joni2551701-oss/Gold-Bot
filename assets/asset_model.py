"""
Asset Layer — data model (Phase A12).

AssetDefinition is standard metadata about a tradable asset -- not a
data provider, not a strategy, not an execution path. It carries no
market-data-fetching logic and generates no signal -- see
docs/ASSET_INTELLIGENCE.md for the full contract and
assets/profiles/gold.py for the one real, currently-traded asset this
codebase registers.
"""

from dataclasses import dataclass
from typing import Any, Optional

from assets.asset_type import AssetType


@dataclass(frozen=True)
class AssetDefinition:
    """
    symbol: the real ticker this codebase already uses (e.g.
        "XAUUSD", matching main.py's TradingPipeline(symbol=...) and
        telegram/signal_service.py's DEFAULT_SYMBOL) -- not a new
        naming scheme.
    name: human-readable display name (e.g. "Gold").
    asset_type: AssetType (GOLD/FOREX/CRYPTO/INDEX/STOCK/UNKNOWN).
    market: the broker/platform market grouping this asset trades
        under (e.g. "FOREX" -- Gold/XAUUSD is commonly offered
        alongside currency pairs on retail forex platforms). A plain
        string, not a new enum -- only asset_type is a controlled
        vocabulary in this phase.
    base_currency: the asset's base currency per standard ticker
        convention (e.g. "XAU" for Gold -- one troy ounce of gold is
        the base unit XAUUSD quotes a USD price against). A real,
        verifiable market-convention fact, not a computed/fabricated
        value.
    quote_currency: the currency the asset is priced in (e.g. "USD").
        Same rationale as base_currency.
    trading_session: always None in this phase -- an explicit hook.
        This codebase's Session Intelligence (context_layer/session/session.py,
        Phase A6) classifies a *candle's* session, not a per-asset
        "typical session" label; computing the latter is a distinct,
        not-yet-done future step.
    volatility_class: always None in this phase -- an explicit hook.
        context_layer/trend/market_regime.py (Phase A7) classifies volatility per
        *cycle*, not a fixed per-asset volatility class; never
        fabricated here.
    news_sensitivity: always None in this phase -- an explicit hook.
        No news/fundamental data source exists anywhere in this
        codebase; never fabricated.
    fundamental_profile: always None in this phase -- reserved for a
        future, not-yet-defined type (e.g. FED/CPI/NFP sensitivity for
        Gold, Interest Rate/Currency Strength for Forex -- see
        docs/ASSET_INTELLIGENCE.md's "Future" section). Never
        fabricated.
    session_profile: always None in this phase -- reserved for a
        future, not-yet-defined type (a richer, asset-specific session
        characterization, distinct from trading_session above). Never
        fabricated.
    risk_profile: always None in this phase -- reserved for a future,
        not-yet-defined type. risk_layer/risk_engine/risk_manager.py is entirely
        unmodified by this phase and does not read this field. Never
        fabricated.
    news_profile: always None in this phase -- reserved for a future,
        not-yet-defined type (a richer counterpart to
        news_sensitivity, e.g. per-event-type sensitivity). Never
        fabricated.
    """
    symbol: str
    name: str
    asset_type: AssetType
    market: str
    base_currency: str
    quote_currency: str
    trading_session: Optional[str] = None
    volatility_class: Optional[str] = None
    news_sensitivity: Optional[str] = None
    fundamental_profile: Optional[Any] = None
    session_profile: Optional[Any] = None
    risk_profile: Optional[Any] = None
    news_profile: Optional[Any] = None
