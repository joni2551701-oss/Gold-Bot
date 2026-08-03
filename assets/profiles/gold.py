"""
Asset Layer — Gold profile (Phase A12).

The one real, currently-traded asset this codebase runs today. Every
field here is either the exact symbol/name this codebase already uses
(main.py, platform_layer/telegram/signal_service.py's DEFAULT_SYMBOL) or a real,
verifiable market-convention fact (base/quote currency) -- never a
fabricated value. See docs/ASSET_INTELLIGENCE.md for the full
contract.
"""

from assets.asset_model import AssetDefinition
from assets.asset_type import AssetType

GOLD_ASSET = AssetDefinition(
    symbol="XAUUSD",
    name="Gold",
    asset_type=AssetType.GOLD,
    market="FOREX",
    base_currency="XAU",
    quote_currency="USD",
)
