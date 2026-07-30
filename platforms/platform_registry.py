"""
Platform Layer — registry (PLATFORM-001).

Same shape as `assets/asset_registry.py` (this repo's established
registry pattern): an in-memory metadata store, a duplicate-key error,
and a `build_default_registry()` factory returning a fresh instance
per call (never a shared singleton), so tests/future callers each get
an independent registry unaffected by another caller's `register()`
calls.

Foundation Reuse Audit: see `platforms/platform_model.py`'s docstring
— no prior Foundation/Manager/Contract/Model/Capability/Registry for
a client-platform registry existed in this repo.

Never imports `telegram/`, `database/`, or any Trading Core package —
this stores metadata about a platform, it does not run one.
"""

from typing import Dict, List, Optional

from platforms.platform_model import PlatformDefinition, PlatformName, PlatformStatus


class DuplicatePlatformError(ValueError):
    """Raised by register() when the platform name is already present in the registry."""


class PlatformRegistry:
    def __init__(self) -> None:
        self._definitions: Dict[PlatformName, PlatformDefinition] = {}

    def register(self, definition: PlatformDefinition) -> None:
        """Raises DuplicatePlatformError if definition.name is already registered."""
        if definition.name in self._definitions:
            raise DuplicatePlatformError(
                f"Platform already registered: {definition.name.value}"
            )
        self._definitions[definition.name] = definition

    def get(self, name: PlatformName) -> Optional[PlatformDefinition]:
        """Returns None if name was never registered -- never raises."""
        return self._definitions.get(name)

    def list(self) -> List[PlatformDefinition]:
        """Every registered PlatformDefinition, regardless of status."""
        return list(self._definitions.values())

    def by_status(self, status: PlatformStatus) -> List[PlatformDefinition]:
        """Only PlatformDefinitions with the given status."""
        return [d for d in self._definitions.values() if d.status == status]


DEFAULT_PLATFORMS = (
    PlatformDefinition(
        name=PlatformName.TELEGRAM_BOT,
        status=PlatformStatus.LIVE,
        version="v0.2",
        features=["signal_delivery", "registration", "settings", "subscription", "admin_panel", "owner_panel"],
        compatibility="telegram/polling.py — see docs/PLATFORM_ARCHITECTURE.md",
    ),
    PlatformDefinition(
        name=PlatformName.TELEGRAM_MINI_APP,
        status=PlatformStatus.NOT_STARTED,
        version="n/a",
        features=[],
        compatibility="Named on the roadmap (v0.8 Mini App, docs/roadmap/VERSIONS.md) — no code exists yet.",
    ),
    PlatformDefinition(
        name=PlatformName.ANDROID,
        status=PlatformStatus.NOT_STARTED,
        version="n/a",
        features=[],
        compatibility="No client code exists yet.",
    ),
    PlatformDefinition(
        name=PlatformName.IOS,
        status=PlatformStatus.NOT_STARTED,
        version="n/a",
        features=[],
        compatibility="No client code exists yet.",
    ),
    PlatformDefinition(
        name=PlatformName.DESKTOP,
        status=PlatformStatus.NOT_STARTED,
        version="n/a",
        features=[],
        compatibility="No client code exists yet.",
    ),
)


def build_default_registry() -> PlatformRegistry:
    """Returns a fresh PlatformRegistry seeded with DEFAULT_PLATFORMS' honest, current state."""
    registry = PlatformRegistry()
    for definition in DEFAULT_PLATFORMS:
        registry.register(definition)
    return registry
