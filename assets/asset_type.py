"""
Asset Layer — asset type enum (Phase A12).

Six values only, per the roadmap's explicit scope -- no other value
is added. See docs/ASSET_INTELLIGENCE.md for the full contract.
"""

from enum import Enum


class AssetType(Enum):
    """
    GOLD: the only type this codebase actually trades today (XAUUSD).
    FOREX, CRYPTO, INDEX, STOCK: reserved for a future multi-asset
        phase -- no data provider, strategy, or execution path exists
        for any of these today.
    UNKNOWN: an asset whose type has not been classified.
    """
    GOLD = "GOLD"
    FOREX = "FOREX"
    CRYPTO = "CRYPTO"
    INDEX = "INDEX"
    STOCK = "STOCK"
    UNKNOWN = "UNKNOWN"
