"""TASK-002D -- Navigation Core tests (platforms/). Real Registry + real stack behavior, no mocking."""

from platform_layer.platform_service.menu_registry import MenuDefinition, MenuRegistry
from platform_layer.platform_service.navigation_core import NavigationCore, has_sufficient_permission
from platform_layer.platform_service.navigation_events import NavigationEventType
from platform_layer.platform_service.platform_model import PlatformName


def _registry():
    registry = MenuRegistry()
    registry.register(MenuDefinition(id="settings.main", permission="USER", platforms=[PlatformName.TELEGRAM_BOT]))
    registry.register(MenuDefinition(id="admin.panel", permission="ADMIN", platforms=[PlatformName.TELEGRAM_BOT]))
    registry.register(MenuDefinition(id="owner.panel", permission="OWNER", platforms=[PlatformName.TELEGRAM_BOT]))
    return registry


def test_has_sufficient_permission_rank_order():
    assert has_sufficient_permission("OWNER", "USER") is True
    assert has_sufficient_permission("OWNER", "ADMIN") is True
    assert has_sufficient_permission("OWNER", "OWNER") is True
    assert has_sufficient_permission("USER", "ADMIN") is False
    assert has_sufficient_permission("ADMIN", "OWNER") is False
    assert has_sufficient_permission("USER", "USER") is True


def test_has_sufficient_permission_fails_closed_on_unknown_tier():
    assert has_sufficient_permission("NOT_A_TIER", "USER") is False


def test_navigate_success_pushes_stack_and_emits_screen_opened():
    core = NavigationCore(_registry())
    result = core.navigate("session-1", "settings.main", "USER", PlatformName.TELEGRAM_BOT)

    assert result.ok is True
    assert result.screen.id == "settings.main"
    assert result.event.event_type == NavigationEventType.SCREEN_OPENED
    assert result.event.screen_id == "settings.main"
    assert core.current_screen("session-1") == "settings.main"


def test_navigate_unregistered_screen_fails_without_touching_stack():
    core = NavigationCore(_registry())
    result = core.navigate("session-1", "does.not.exist", "OWNER", PlatformName.TELEGRAM_BOT)

    assert result.ok is False
    assert result.screen is None
    assert result.event.event_type == NavigationEventType.NAVIGATION_FAILED
    assert core.current_screen("session-1") is None


def test_navigate_permission_denied_never_pushes_stack():
    """Request -> Permission -> Navigation -> Screen: an unauthorized screen is never reached."""
    core = NavigationCore(_registry())
    result = core.navigate("session-1", "admin.panel", "USER", PlatformName.TELEGRAM_BOT)

    assert result.ok is False
    assert result.screen is None
    assert result.event.event_type == NavigationEventType.PERMISSION_DENIED
    assert core.current_screen("session-1") is None


def test_go_back_pops_and_returns_destination_not_closed_screen():
    core = NavigationCore(_registry())
    core.navigate("session-1", "settings.main", "OWNER", PlatformName.TELEGRAM_BOT)
    core.navigate("session-1", "admin.panel", "OWNER", PlatformName.TELEGRAM_BOT)

    result = core.go_back("session-1", PlatformName.TELEGRAM_BOT)

    assert result.ok is True
    assert result.event.event_type == NavigationEventType.BACK_PRESSED
    assert result.event.screen_id == "admin.panel"  # the screen that closed
    assert result.screen.id == "settings.main"  # the destination, not the closed screen
    assert core.current_screen("session-1") == "settings.main"


def test_go_back_from_single_screen_returns_no_destination():
    core = NavigationCore(_registry())
    core.navigate("session-1", "settings.main", "USER", PlatformName.TELEGRAM_BOT)

    result = core.go_back("session-1", PlatformName.TELEGRAM_BOT)

    assert result.ok is True
    assert result.screen is None
    assert core.current_screen("session-1") is None


def test_go_back_on_empty_stack_fails_without_raising():
    core = NavigationCore(_registry())
    result = core.go_back("never-navigated", PlatformName.TELEGRAM_BOT)

    assert result.ok is False
    assert result.event.event_type == NavigationEventType.NAVIGATION_FAILED


def test_sessions_are_independent():
    core = NavigationCore(_registry())
    core.navigate("session-A", "settings.main", "USER", PlatformName.TELEGRAM_BOT)

    assert core.current_screen("session-A") == "settings.main"
    assert core.current_screen("session-B") is None
