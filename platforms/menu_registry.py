"""
Platform Layer — Universal Menu Registry (PLATFORM-001).

A `MenuDefinition` is registered by id/permission/platforms/version/
dependencies -- never hardcoded inline, per the Director's brief.
**Foundation only, deliberately unwired**: this does not replace or
modify `telegram/commands.py`'s live `COMMANDS`/`ADMIN_COMMANDS`/
`OWNER_COMMANDS` registries, which remain the single source of truth
`telegram/command_router.py` actually dispatches from today (see
`docs/PLATFORM_DEPENDENCY_MAP.md`). A future, separately-authorized
task would decide whether/how to migrate the live registries onto
this one.

Foundation Reuse Audit (Constitution Article 11): `telegram/commands.py`
is the existing Telegram-specific registry (a `Dict[str, str]` command
name -> description); it is not a cross-platform, dependency-aware
contract, so this is not a duplicate -- see this module's own
docstring above for why a new module was justified. No other
Foundation/Manager/Contract/Model/Capability/Registry addresses a
cross-platform menu contract.

Never imports `telegram/`, `database/`, or any Trading Core package.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from platforms.platform_model import PlatformName


@dataclass(frozen=True)
class MenuDefinition:
    id: str
    permission: str
    platforms: List[PlatformName] = field(default_factory=list)
    version: str = "0.1"
    dependencies: List[str] = field(default_factory=list)


class DuplicateMenuIdError(ValueError):
    """Raised by register() when the menu id is already present in the registry."""


class MenuRegistry:
    def __init__(self) -> None:
        self._definitions: Dict[str, MenuDefinition] = {}

    def register(self, definition: MenuDefinition) -> None:
        """Raises DuplicateMenuIdError if definition.id is already registered."""
        if definition.id in self._definitions:
            raise DuplicateMenuIdError(f"Menu id already registered: {definition.id}")
        self._definitions[definition.id] = definition

    def get(self, menu_id: str) -> Optional[MenuDefinition]:
        """Returns None if menu_id was never registered -- never raises."""
        return self._definitions.get(menu_id)

    def list(self) -> List[MenuDefinition]:
        """Every registered MenuDefinition."""
        return list(self._definitions.values())

    def by_platform(self, platform: PlatformName) -> List[MenuDefinition]:
        """Only MenuDefinitions that list the given platform."""
        return [d for d in self._definitions.values() if platform in d.platforms]
