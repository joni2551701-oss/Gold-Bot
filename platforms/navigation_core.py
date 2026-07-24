"""
Platform Layer — Navigation Core (TASK-002D, per the approved
`docs/NAVIGATION_ARCHITECTURE.md` and Director's TASK-002D brief).

The orchestrator sitting between a Platform Adapter (`platforms/
platform_adapter.py`) and the Navigation Registry
(`platforms/menu_registry.py`): `UI -> Platform Adapter -> Navigation
Core -> Application -> Business Logic` (the Universal UI Abstraction
rule, ADR-001). `NavigationCore` never talks to Business Logic itself
-- it resolves a Screen and hands it back to the caller (an Adapter);
what happens after that is Application-layer or Business-Logic
concern, entirely outside this file.

Permission Flow (Director's Q4 answer at TASK-002B): permission is
checked BEFORE navigation -- `Request -> Permission -> Navigation ->
Screen`. An unauthorized screen is never reached, not hidden after the
fact. `_TIER_RANK`/`has_sufficient_permission()` mirror
`telegram/permissions.py`'s own OWNER > ADMIN > USER rank comparison
by convention (same relationship `platforms/`'s `permission: str`
fields already have to `PermissionLevel` -- see
`platforms/navigation_model.py`'s docstring) -- not a duplicate, since
`telegram/permissions.py`'s version resolves a Telegram user's tier
from `TELEGRAM_OWNER_ID`/the `admins` table, a Telegram-specific
concern this module has no dependency on; this module only compares
two already-resolved tier strings.

Navigation State (Director's Q6 answer): lives here, in the Platform
Layer, per session id -- an in-memory stack, never persisted, never
read by any Business Logic module. Matches
`telegram/reply_keyboard_manager.py`'s own `_LAST_SECTION` precedent
(process-local, not centralized in `database/`), generalized across
every platform via `session_id` instead of being Telegram-specific.

Navigation Stack (Director's Q1 answer): one real, arbitrary-depth
stack for every platform -- no Telegram-specific "collapse to depth 1"
exception. A Platform Adapter that wants Telegram's actual flat UX
(every submenu's Back returns to Main) achieves it by always calling
`go_back()` until the stack is back at the root, or by calling
`navigate()` with the root screen directly -- that choice belongs to
the Adapter, not to this module.

Event Interface (ADR-004): `navigate()`/`go_back()` return a
`NavigationEvent` as part of their `NavigationResult` -- real
operations now produce real events. Still no dispatcher: nothing
publishes, queues, or delivers the event to any consumer.

Foundation Reuse Audit (Constitution Article 11): no prior Foundation/
Manager/Contract/Model/Capability/Registry orchestrates Registry
lookup + permission check + stack state in this repo --
`telegram/reply_keyboard_manager.py`'s `keyboard_for_command()`/
`_LAST_SECTION` is the Telegram-specific analog, not a reusable
cross-platform orchestrator.

No hardcoded platform-specific logic: this module never branches on
`PlatformName` -- a platform's own behavior lives in its Platform
Adapter, never inline here.

Never imports `telegram/`, `database/`, or any Trading Core package.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from platforms.menu_registry import MenuDefinition, MenuRegistry
from platforms.navigation_events import NavigationEvent, NavigationEventType
from platforms.platform_model import PlatformName

_TIER_RANK = {"USER": 0, "ADMIN": 1, "OWNER": 2}


def has_sufficient_permission(user_tier: str, required_tier: str) -> bool:
    """
    Never raises: an unrecognized tier string ranks below every known
    tier (fails closed -- no unearned access), matching
    `telegram/permissions.py`'s own fail-closed convention for an
    unresolved OWNER_ID.
    """
    return _TIER_RANK.get(user_tier, -1) >= _TIER_RANK.get(required_tier, -1)


@dataclass(frozen=True)
class NavigationResult:
    """ok: True only when the screen was actually reached (permission satisfied, screen registered). screen: the resolved MenuDefinition, None on any failure."""

    ok: bool
    screen: Optional[MenuDefinition]
    event: NavigationEvent


class NavigationCore:
    """
    One instance wraps one `MenuRegistry` (Registry integration -- it
    consumes the registry, never duplicates its data). Navigation
    State (`_stacks`) is per-session, in-memory, never persisted.
    """

    def __init__(self, registry: MenuRegistry) -> None:
        self._registry = registry
        self._stacks: Dict[str, List[str]] = {}

    def navigate(self, session_id: str, screen_id: str, user_permission: str, platform: PlatformName) -> NavigationResult:
        """
        Permission Flow: Request -> Permission -> Navigation -> Screen.
        The screen's own registration is looked up first only to know
        its required tier -- an unregistered screen and a
        permission-denied screen are both refused, neither is ever
        pushed onto the session's stack.
        """
        screen = self._registry.get(screen_id)
        if screen is None:
            event = NavigationEvent(
                event_type=NavigationEventType.NAVIGATION_FAILED,
                platform=platform,
                screen_id=screen_id,
                details=f"Screen not registered: {screen_id}",
            )
            return NavigationResult(ok=False, screen=None, event=event)

        if not has_sufficient_permission(user_permission, screen.permission):
            event = NavigationEvent(
                event_type=NavigationEventType.PERMISSION_DENIED,
                platform=platform,
                screen_id=screen_id,
                details=f"Requires {screen.permission}, has {user_permission}",
            )
            return NavigationResult(ok=False, screen=None, event=event)

        self._stacks.setdefault(session_id, []).append(screen_id)
        event = NavigationEvent(event_type=NavigationEventType.SCREEN_OPENED, platform=platform, screen_id=screen_id)
        return NavigationResult(ok=True, screen=screen, event=event)

    def go_back(self, session_id: str, platform: PlatformName) -> NavigationResult:
        """
        Pops the session's stack. `result.screen` is the DESTINATION
        (the new top of stack after the pop, i.e. what the caller
        should render next) -- not the screen that just closed. An
        empty stack is a NAVIGATION_FAILED event, never an exception --
        there is nowhere further back to go. Popping the last screen
        off an otherwise-empty stack is a successful back-out to no
        screen (`result.screen is None`, `result.ok is True`) -- never
        fabricates a "home" screen that was never actually navigated to.
        """
        stack = self._stacks.get(session_id, [])
        if not stack:
            event = NavigationEvent(
                event_type=NavigationEventType.NAVIGATION_FAILED,
                platform=platform,
                details="Back pressed with an empty navigation stack",
            )
            return NavigationResult(ok=False, screen=None, event=event)

        closed_screen_id = stack.pop()
        event = NavigationEvent(event_type=NavigationEventType.BACK_PRESSED, platform=platform, screen_id=closed_screen_id)
        destination_id = stack[-1] if stack else None
        destination_screen = self._registry.get(destination_id) if destination_id is not None else None
        return NavigationResult(ok=True, screen=destination_screen, event=event)

    def current_screen(self, session_id: str) -> Optional[str]:
        """The screen id at the top of the session's stack, or None if the session has never navigated anywhere -- never raises."""
        stack = self._stacks.get(session_id, [])
        return stack[-1] if stack else None
