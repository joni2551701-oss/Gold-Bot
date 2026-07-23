"""
Platform Layer — Universal Menu Registry / Route Registry (PLATFORM-001;
extended TASK-002C per the approved `docs/NAVIGATION_ARCHITECTURE.md`
§4 and ADR-002/ADR-003).

A `MenuDefinition` is registered by id/permission/platforms/version/
dependencies/target_bindings -- never hardcoded inline, per the
Director's brief. **Foundation only, deliberately unwired**: this does
not replace or modify `telegram/commands.py`'s live `COMMANDS`/
`ADMIN_COMMANDS`/`OWNER_COMMANDS` registries, which remain the single
source of truth `telegram/command_router.py` actually dispatches from
today (see `docs/PLATFORM_DEPENDENCY_MAP.md`). A future,
separately-authorized task would decide whether/how to migrate the
live registries onto this one (ADR-003: a platform never creates a
Screen itself -- but `telegram/`'s own code still does today, unwired
to this registry, until that future task).

Foundation Reuse Audit (Constitution Article 11): `telegram/commands.py`
is the existing Telegram-specific registry (a `Dict[str, str]` command
name -> description); it is not a cross-platform, dependency-aware
contract, so this is not a duplicate -- see this module's own
docstring above for why a new module was justified. No other
Foundation/Manager/Contract/Model/Capability/Registry addresses a
cross-platform menu contract. TASK-002C extends this existing module
(`target_bindings`, `DEFAULT_MENUS`) rather than creating a separate
"Route Registry" module, since one `MenuDefinition` already serves
both concerns at this scale (docs/NAVIGATION_ARCHITECTURE.md §4's own
reasoning).

Never imports `telegram/`, `database/`, or any Trading Core package.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from platforms.platform_model import PlatformName


@dataclass(frozen=True)
class MenuDefinition:
    """
    id: new registrations should follow ADR-002's Universal Screen
    Identity convention (`platforms.navigation_model.is_valid_screen_id()`)
    -- not enforced at construction time, same reasoning as
    `NavigationNode.id` (see that module's docstring).
    target_bindings: per-platform concrete navigation target -- e.g.
    `{PlatformName.TELEGRAM_BOT: "/settings"}`. The Route Registry
    concept from `docs/NAVIGATION_ARCHITECTURE.md` §4, added TASK-002C.
    Empty by default -- a platform with no entry here has no known
    binding yet (honest, not fabricated).
    """

    id: str
    permission: str
    platforms: List[PlatformName] = field(default_factory=list)
    version: str = "0.1"
    dependencies: List[str] = field(default_factory=list)
    target_bindings: Dict[PlatformName, str] = field(default_factory=dict)


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


# ---------------------------------------------------------------------------
# Default registry (TASK-002C): GoldBot's real, currently-live Telegram
# screens only, under ADR-002 Universal Screen IDs, with a real
# Telegram target binding each. No AI/Education/Marketplace/Trading
# screens are pre-registered here -- those modules do not exist yet;
# the Registry mechanism above being dynamic/open is what makes it
# *extensible* for them later (docs/NAVIGATION_ARCHITECTURE.md's Future
# Expansion section), not a reason to invent placeholder entries now.
# Every id/target_binding below is verified against
# docs/commands_reference.md and telegram/reply_keyboard_manager.py's
# real _SECTION_BY_COMMAND/_SECTION_LABEL_KEYS maps -- not guessed.
# ---------------------------------------------------------------------------

_TELEGRAM = PlatformName.TELEGRAM_BOT

DEFAULT_MENUS: Tuple[MenuDefinition, ...] = (
    MenuDefinition(id="main.home", permission="USER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/start"}),
    MenuDefinition(id="settings.main", permission="USER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/settings"}),
    MenuDefinition(id="settings.language", permission="USER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/language"}),
    MenuDefinition(id="settings.risk", permission="USER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/risk"}),
    MenuDefinition(id="settings.strategy", permission="USER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/strategy"}),
    MenuDefinition(id="settings.timeframe", permission="USER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/timeframe"}),
    MenuDefinition(id="settings.notifications", permission="USER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/notifications"}),
    MenuDefinition(id="profile.main", permission="USER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/profile"}),
    MenuDefinition(id="profile.subscription", permission="USER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/subscription"}),
    MenuDefinition(id="signals.live", permission="USER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/signal"}),
    MenuDefinition(id="signals.history", permission="USER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/history"}),
    MenuDefinition(id="signals.upgrade", permission="USER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/upgrade"}),
    MenuDefinition(id="admin.panel", permission="ADMIN", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/admin"}),
    MenuDefinition(id="admin.users", permission="ADMIN", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/users"}),
    MenuDefinition(id="admin.stats", permission="ADMIN", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/stats"}),
    MenuDefinition(id="admin.system", permission="ADMIN", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/system"}),
    MenuDefinition(id="admin.broadcast", permission="ADMIN", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/broadcast"}),
    # "Admin Management" re-opens the Admin Panel, never a direct action -- matches
    # telegram/reply_keyboard_manager.py's own Director Review correction 1.
    MenuDefinition(id="admin.management", permission="ADMIN", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/admin"}),
    MenuDefinition(id="owner.panel", permission="OWNER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/owner"}),
    MenuDefinition(id="owner.runtime", permission="OWNER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/runtime"}),
    MenuDefinition(id="owner.health", permission="OWNER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/health"}),
    MenuDefinition(id="owner.performance", permission="OWNER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/performance"}),
    MenuDefinition(id="owner.errors", permission="OWNER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/errors"}),
    MenuDefinition(id="owner.pipeline", permission="OWNER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/pipeline"}),
    MenuDefinition(id="owner.reports", permission="OWNER", platforms=[_TELEGRAM], target_bindings={_TELEGRAM: "/report"}),
)


def build_default_menu_registry() -> MenuRegistry:
    """Returns a fresh MenuRegistry seeded with DEFAULT_MENUS -- a read-only mirror of GoldBot's real, live Telegram screens, not a replacement for telegram/commands.py."""
    registry = MenuRegistry()
    for definition in DEFAULT_MENUS:
        registry.register(definition)
    return registry
