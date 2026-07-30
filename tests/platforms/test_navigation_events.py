"""TASK-002C -- Navigation Event Bus interface tests (ADR-004). Interface only -- no dispatcher exists to test."""

from platforms.navigation_events import NavigationEvent, NavigationEventType
from platforms.platform_model import PlatformName


def test_event_type_vocabulary_matches_adr004_exactly():
    expected = {
        "ScreenOpened",
        "ScreenClosed",
        "BackPressed",
        "PermissionDenied",
        "NavigationFailed",
        "DeepLinkOpened",
        "SessionExpired",
    }
    actual = {member.value for member in NavigationEventType}
    assert actual == expected


def test_navigation_event_defaults():
    event = NavigationEvent(event_type=NavigationEventType.SCREEN_OPENED, platform=PlatformName.TELEGRAM_BOT)
    assert event.screen_id is None
    assert event.details is None


def test_navigation_event_with_screen_and_details():
    event = NavigationEvent(
        event_type=NavigationEventType.NAVIGATION_FAILED,
        platform=PlatformName.TELEGRAM_BOT,
        screen_id="signals.live",
        details="Screen not registered",
    )
    assert event.event_type == NavigationEventType.NAVIGATION_FAILED
    assert event.screen_id == "signals.live"
    assert event.details == "Screen not registered"


def test_session_expired_event_has_no_screen():
    """A SESSION_EXPIRED event concerns no specific screen -- screen_id stays None, never fabricated."""
    event = NavigationEvent(event_type=NavigationEventType.SESSION_EXPIRED, platform=PlatformName.TELEGRAM_BOT)
    assert event.screen_id is None
