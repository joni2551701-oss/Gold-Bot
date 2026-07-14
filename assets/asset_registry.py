"""
Asset Layer — registry (Phase A12).

AssetRegistry stores AssetDefinition metadata only -- it does not
fetch market data, does not run a strategy, does not size a position,
and does not write to the database. See docs/ASSET_INTELLIGENCE.md
for the full contract.

build_default_registry() registers the one asset this codebase
actually trades today -- GOLD_ASSET (assets/profiles/gold.py) -- no
new market integration, no Forex/Crypto/Index/Stock asset is added.
"""

from typing import Dict, List, Optional, Tuple

from assets.asset_model import AssetDefinition
from assets.asset_type import AssetType
from assets.profiles.gold import GOLD_ASSET

DEFAULT_ASSETS: Tuple[AssetDefinition, ...] = (
    GOLD_ASSET,
)


class DuplicateAssetSymbolError(ValueError):
    """Raised by register() when the symbol is already present in the registry."""


class AssetRegistry:
    """
    An in-memory metadata store, keyed by AssetDefinition.symbol.
    Never imports data/, execution/, risk/, strategies/, or
    telegram/ -- it stores metadata about an asset, it does not fetch
    its data, trade it, or size a position in it.
    """

    def __init__(self) -> None:
        self._definitions: Dict[str, AssetDefinition] = {}

    def register(self, definition: AssetDefinition) -> None:
        """Raises DuplicateAssetSymbolError if definition.symbol is already registered."""
        if definition.symbol in self._definitions:
            raise DuplicateAssetSymbolError(
                f"Asset symbol already registered: {definition.symbol}"
            )
        self._definitions[definition.symbol] = definition

    def get(self, symbol: str) -> Optional[AssetDefinition]:
        """Returns None if symbol was never registered -- never raises."""
        return self._definitions.get(symbol)

    def list(self) -> List[AssetDefinition]:
        """Every registered AssetDefinition, regardless of type."""
        return list(self._definitions.values())

    def by_type(self, asset_type: AssetType) -> List[AssetDefinition]:
        """Only AssetDefinitions with the given asset_type."""
        return [d for d in self._definitions.values() if d.asset_type == asset_type]


def build_default_registry() -> AssetRegistry:
    """
    Returns a fresh AssetRegistry with the one real, currently-traded
    asset registered (DEFAULT_ASSETS) -- not a shared singleton, so
    tests/future callers each get an independent registry unaffected
    by another caller's register() calls.
    """
    registry = AssetRegistry()
    for definition in DEFAULT_ASSETS:
        registry.register(definition)
    return registry
