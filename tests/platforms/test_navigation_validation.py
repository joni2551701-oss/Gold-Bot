"""
TASK-002E -- Navigation Validation (Director-authorized scope:
Navigation Validation, Edge Cases, Stack Consistency, Multi-session
Validation, Permission Validation, Event Validation, Recovery
Scenarios, Integration Validation).

Deeper coverage against the existing, FROZEN TASK-002D contracts
(`platform_layer/platform_service/navigation_core.py`, `platform_layer/platform_service/platform_adapter.py`,
`platform_layer/platform_service/navigation_events.py`, `platform_layer/platform_service/menu_registry.py`) --
this file adds test coverage only. No contract is changed, no
Trading Core file is touched, no concrete Telegram/Android/iOS
Platform Adapter is built. `tests/platforms/test_navigation_core.py`
(TASK-002D's own coverage) is left untouched; this is new,
additional depth, not a replacement.
"""

import pytest

from platform_layer.platform_service.menu_registry import (
    MenuDefinition,
    MenuRegistry,
    build_default_menu_registry,
)
from platform_layer.platform_service.navigation_core import NavigationCore, has_sufficient_permission
from platform_layer.platform_service.navigation_events import NavigationEventType
from platform_layer.platform_service.platform_adapter import PlatformAdapterBase
from platform_layer.platform_service.platform_model import PlatformName


def _registry():
    registry = MenuRegistry()
    registry.register(MenuDefinition(id="settings.main", permission="USER", platforms=[PlatformName.TELEGRAM_BOT]))
    registry.register(MenuDefinition(id="admin.panel", permission="ADMIN", platforms=[PlatformName.TELEGRAM_BOT]))
    registry.register(MenuDefinition(id="owner.panel", permission="OWNER", platforms=[PlatformName.TELEGRAM_BOT]))
    return registry


# ---------------------------------------------------------------------------
# Navigation Validation (general correctness beyond basic happy path)
# ---------------------------------------------------------------------------

def test_navigating_to_the_same_screen_twice_pushes_it_twice():
    """A navigation stack is not deduplicated -- revisiting a screen is a real, distinct stack entry, same as any real back-stack."""
    core = NavigationCore(_registry())
    core.navigate("s1", "settings.main", "USER", PlatformName.TELEGRAM_BOT)
    core.navigate("s1", "settings.main", "USER", PlatformName.TELEGRAM_BOT)

    assert core.current_screen("s1") == "settings.main"
    first_back = core.go_back("s1", PlatformName.TELEGRAM_BOT)
    assert first_back.screen.id == "settings.main"  # still on the stack once more


def test_long_navigation_chain_maintains_order():
    core = NavigationCore(_registry())
    core.navigate("s1", "settings.main", "OWNER", PlatformName.TELEGRAM_BOT)
    core.navigate("s1", "admin.panel", "OWNER", PlatformName.TELEGRAM_BOT)
    core.navigate("s1", "owner.panel", "OWNER", PlatformName.TELEGRAM_BOT)

    assert core.current_screen("s1") == "owner.panel"
    assert core.go_back("s1", PlatformName.TELEGRAM_BOT).screen.id == "admin.panel"
    assert core.go_back("s1", PlatformName.TELEGRAM_BOT).screen.id == "settings.main"
    assert core.go_back("s1", PlatformName.TELEGRAM_BOT).screen is None


# ---------------------------------------------------------------------------
# Edge Cases / Invalid Route Handling
# ---------------------------------------------------------------------------

def test_empty_session_id_is_a_valid_key_not_a_special_case():
    core = NavigationCore(_registry())
    result = core.navigate("", "settings.main", "USER", PlatformName.TELEGRAM_BOT)
    assert result.ok is True
    assert core.current_screen("") == "settings.main"


def test_navigate_to_empty_string_screen_id_fails_as_unregistered():
    core = NavigationCore(_registry())
    result = core.navigate("s1", "", "OWNER", PlatformName.TELEGRAM_BOT)
    assert result.ok is False
    assert result.event.event_type == NavigationEventType.NAVIGATION_FAILED


def test_navigate_to_malformed_but_plausible_screen_id_fails_cleanly():
    """A well-formatted-looking id that was simply never registered is an ordinary NAVIGATION_FAILED, not a crash."""
    core = NavigationCore(_registry())
    result = core.navigate("s1", "trading.core.override", "OWNER", PlatformName.TELEGRAM_BOT)
    assert result.ok is False
    assert result.screen is None
    assert "trading.core.override" in result.event.details


def test_empty_registry_always_fails_navigation():
    core = NavigationCore(MenuRegistry())
    result = core.navigate("s1", "anything", "OWNER", PlatformName.TELEGRAM_BOT)
    assert result.ok is False
    assert result.event.event_type == NavigationEventType.NAVIGATION_FAILED


# ---------------------------------------------------------------------------
# Stack Consistency
# ---------------------------------------------------------------------------

def test_stack_depth_matches_net_navigate_minus_back_calls():
    core = NavigationCore(_registry())
    for screen_id in ("settings.main", "admin.panel", "owner.panel"):
        core.navigate("s1", screen_id, "OWNER", PlatformName.TELEGRAM_BOT)
    assert core.current_screen("s1") == "owner.panel"

    core.go_back("s1", PlatformName.TELEGRAM_BOT)
    assert core.current_screen("s1") == "admin.panel"


def test_failed_navigate_never_changes_stack_depth():
    core = NavigationCore(_registry())
    core.navigate("s1", "settings.main", "USER", PlatformName.TELEGRAM_BOT)
    before = core.current_screen("s1")

    core.navigate("s1", "admin.panel", "USER", PlatformName.TELEGRAM_BOT)  # denied
    core.navigate("s1", "no.such.screen", "USER", PlatformName.TELEGRAM_BOT)  # unregistered

    assert core.current_screen("s1") == before


def test_interleaved_navigate_and_back_maintains_lifo_order():
    core = NavigationCore(_registry())
    core.navigate("s1", "settings.main", "OWNER", PlatformName.TELEGRAM_BOT)
    core.navigate("s1", "admin.panel", "OWNER", PlatformName.TELEGRAM_BOT)
    core.go_back("s1", PlatformName.TELEGRAM_BOT)  # back to settings.main
    core.navigate("s1", "owner.panel", "OWNER", PlatformName.TELEGRAM_BOT)  # settings.main -> owner.panel

    assert core.current_screen("s1") == "owner.panel"
    assert core.go_back("s1", PlatformName.TELEGRAM_BOT).screen.id == "settings.main"
    assert core.go_back("s1", PlatformName.TELEGRAM_BOT).screen is None


# ---------------------------------------------------------------------------
# Multi-session Validation
# ---------------------------------------------------------------------------

def test_many_sessions_maintain_fully_independent_stacks():
    core = NavigationCore(_registry())
    session_ids = [f"session-{i}" for i in range(20)]

    for i, session_id in enumerate(session_ids):
        depth = (i % 3) + 1
        screens = ["settings.main", "admin.panel", "owner.panel"][:depth]
        for screen_id in screens:
            core.navigate(session_id, screen_id, "OWNER", PlatformName.TELEGRAM_BOT)

    for i, session_id in enumerate(session_ids):
        expected_depth = (i % 3) + 1
        expected_top = ["settings.main", "admin.panel", "owner.panel"][expected_depth - 1]
        assert core.current_screen(session_id) == expected_top


def test_interleaved_operations_across_sessions_do_not_cross_contaminate():
    core = NavigationCore(_registry())
    core.navigate("A", "settings.main", "OWNER", PlatformName.TELEGRAM_BOT)
    core.navigate("B", "admin.panel", "OWNER", PlatformName.TELEGRAM_BOT)
    core.navigate("A", "owner.panel", "OWNER", PlatformName.TELEGRAM_BOT)
    core.go_back("B", PlatformName.TELEGRAM_BOT)

    assert core.current_screen("A") == "owner.panel"
    assert core.current_screen("B") is None


# ---------------------------------------------------------------------------
# Permission Validation
# ---------------------------------------------------------------------------

def test_full_permission_rank_matrix():
    expected = {
        ("OWNER", "OWNER"): True, ("OWNER", "ADMIN"): True, ("OWNER", "USER"): True,
        ("ADMIN", "OWNER"): False, ("ADMIN", "ADMIN"): True, ("ADMIN", "USER"): True,
        ("USER", "OWNER"): False, ("USER", "ADMIN"): False, ("USER", "USER"): True,
    }
    for (user_tier, required_tier), expected_result in expected.items():
        assert has_sufficient_permission(user_tier, required_tier) is expected_result, (user_tier, required_tier)


def test_case_sensitive_tier_strings_fail_closed():
    """Tiers are exact-match strings, not case-insensitive -- "user" is not "USER"."""
    assert has_sufficient_permission("user", "USER") is False
    assert has_sufficient_permission("Owner", "USER") is False


def test_empty_user_tier_fails_closed():
    assert has_sufficient_permission("", "USER") is False


def test_empty_or_malformed_required_tier_is_permissive_not_restrictive():
    """
    Validation finding, documented rather than silently changed:
    _TIER_RANK.get(required_tier, -1) ranks an unrecognized REQUIRED
    tier at -1 -- below every real tier -- so ANY recognized user tier
    satisfies it. This is the opposite of "fail closed" for this one
    malformed-data direction (a bad *user* tier still fails closed;
    a bad *required* tier does not). Not exploitable today: every
    `DEFAULT_MENUS` entry's `permission` field is already validated
    elsewhere to be exactly USER/ADMIN/OWNER
    (`tests/platforms/test_menu_registry.py::test_default_menus_permissions_match_real_tiers`).
    `platform_layer/platform_service/navigation_core.py` is Frozen (TASK-002D) -- fixing this
    requires its own critical-bug/ADR/Migration Task authorization per
    the Freeze Checklist, not a change bundled into this validation task.
    """
    assert has_sufficient_permission("OWNER", "") is True
    assert has_sufficient_permission("USER", "") is True


def test_permission_denied_details_name_both_tiers():
    core = NavigationCore(_registry())
    result = core.navigate("s1", "owner.panel", "USER", PlatformName.TELEGRAM_BOT)
    assert "OWNER" in result.event.details
    assert "USER" in result.event.details


# ---------------------------------------------------------------------------
# Event Validation
# ---------------------------------------------------------------------------

def test_every_navigation_outcome_produces_exactly_one_correctly_typed_event():
    core = NavigationCore(_registry())

    success = core.navigate("s1", "settings.main", "USER", PlatformName.TELEGRAM_BOT)
    assert success.event.event_type == NavigationEventType.SCREEN_OPENED

    denied = core.navigate("s1", "owner.panel", "USER", PlatformName.TELEGRAM_BOT)
    assert denied.event.event_type == NavigationEventType.PERMISSION_DENIED

    failed = core.navigate("s1", "no.such.screen", "USER", PlatformName.TELEGRAM_BOT)
    assert failed.event.event_type == NavigationEventType.NAVIGATION_FAILED

    back = core.go_back("s1", PlatformName.TELEGRAM_BOT)
    assert back.event.event_type == NavigationEventType.BACK_PRESSED

    empty_back = core.go_back("s1", PlatformName.TELEGRAM_BOT)
    assert empty_back.event.event_type == NavigationEventType.NAVIGATION_FAILED


@pytest.mark.parametrize("platform", list(PlatformName))
def test_events_carry_the_platform_they_were_raised_on_for_every_platform_value(platform):
    """NavigationCore is platform-agnostic -- it accepts any PlatformName, never branching on which one, per its own no-hardcoded-platform-logic rule."""
    core = NavigationCore(_registry())
    result = core.navigate("s1", "settings.main", "USER", platform)
    assert result.event.platform == platform


def test_back_pressed_event_references_the_closed_screen_not_the_destination():
    core = NavigationCore(_registry())
    core.navigate("s1", "settings.main", "OWNER", PlatformName.TELEGRAM_BOT)
    core.navigate("s1", "admin.panel", "OWNER", PlatformName.TELEGRAM_BOT)

    result = core.go_back("s1", PlatformName.TELEGRAM_BOT)
    assert result.event.screen_id == "admin.panel"
    assert result.screen.id == "settings.main"


# ---------------------------------------------------------------------------
# Recovery Scenarios
# ---------------------------------------------------------------------------

def test_navigation_recovers_after_permission_denied():
    core = NavigationCore(_registry())
    core.navigate("s1", "admin.panel", "USER", PlatformName.TELEGRAM_BOT)  # denied, no-op
    result = core.navigate("s1", "settings.main", "USER", PlatformName.TELEGRAM_BOT)  # should still work

    assert result.ok is True
    assert core.current_screen("s1") == "settings.main"


def test_navigation_recovers_after_unregistered_screen_failure():
    core = NavigationCore(_registry())
    core.navigate("s1", "no.such.screen", "OWNER", PlatformName.TELEGRAM_BOT)  # fails, no-op
    result = core.navigate("s1", "owner.panel", "OWNER", PlatformName.TELEGRAM_BOT)

    assert result.ok is True
    assert core.current_screen("s1") == "owner.panel"


def test_repeated_go_back_past_empty_stays_consistently_failed_then_recovers():
    core = NavigationCore(_registry())
    core.navigate("s1", "settings.main", "USER", PlatformName.TELEGRAM_BOT)
    core.go_back("s1", PlatformName.TELEGRAM_BOT)  # back to empty

    for _ in range(5):
        result = core.go_back("s1", PlatformName.TELEGRAM_BOT)
        assert result.ok is False
        assert result.event.event_type == NavigationEventType.NAVIGATION_FAILED

    # session is not corrupted -- a fresh navigate still works after repeated failed backs
    recovered = core.navigate("s1", "admin.panel", "OWNER", PlatformName.TELEGRAM_BOT)
    assert recovered.ok is True
    assert core.current_screen("s1") == "admin.panel"


# ---------------------------------------------------------------------------
# Integration Validation (Registry + Core + Adapter interface together;
# no concrete per-platform adapter -- a minimal test-only stand-in)
# ---------------------------------------------------------------------------

class _RecordingAdapter(PlatformAdapterBase):
    """Test-only stand-in -- never a real per-platform implementation, not exported."""

    def __init__(self):
        self.rendered = []
        self.permission_denied_count = 0
        self.failures = []

    def render_screen(self, screen):
        self.rendered.append(screen.id)

    def render_permission_denied(self):
        self.permission_denied_count += 1

    def render_navigation_failed(self, message):
        self.failures.append(message)


def test_full_request_flow_against_the_real_default_registry():
    """Registry (real GoldBot screens) + Core + Adapter interface, composed end-to-end -- still zero telegram/ dependency anywhere in this chain."""
    core = NavigationCore(build_default_menu_registry())
    adapter = _RecordingAdapter()

    result = core.navigate("s1", "settings.main", "USER", PlatformName.TELEGRAM_BOT)
    if result.ok:
        adapter.render_screen(result.screen)
    assert adapter.rendered == ["settings.main"]

    result = core.navigate("s1", "owner.panel", "USER", PlatformName.TELEGRAM_BOT)
    if not result.ok and result.event.event_type == NavigationEventType.PERMISSION_DENIED:
        adapter.render_permission_denied()
    assert adapter.permission_denied_count == 1

    result = core.navigate("s1", "no.such.screen", "USER", PlatformName.TELEGRAM_BOT)
    if not result.ok and result.event.event_type == NavigationEventType.NAVIGATION_FAILED:
        adapter.render_navigation_failed(result.event.details)
    assert adapter.failures == ["Screen not registered: no.such.screen"]


def test_default_registry_owner_screens_reachable_only_by_owner():
    core = NavigationCore(build_default_menu_registry())
    assert core.navigate("s1", "owner.panel", "OWNER", PlatformName.TELEGRAM_BOT).ok is True
    assert core.navigate("s2", "owner.panel", "ADMIN", PlatformName.TELEGRAM_BOT).ok is False
    assert core.navigate("s3", "owner.panel", "USER", PlatformName.TELEGRAM_BOT).ok is False


# ---------------------------------------------------------------------------
# Stress
# ---------------------------------------------------------------------------

def test_stress_many_operations_across_many_sessions_stay_consistent():
    core = NavigationCore(_registry())
    screens = ["settings.main", "admin.panel", "owner.panel"]
    session_count = 50
    ops_per_session = 20

    for i in range(session_count):
        session_id = f"stress-{i}"
        for op in range(ops_per_session):
            core.navigate(session_id, screens[op % 3], "OWNER", PlatformName.TELEGRAM_BOT)

    for i in range(session_count):
        session_id = f"stress-{i}"
        assert core.current_screen(session_id) == screens[(ops_per_session - 1) % 3]
        for _ in range(ops_per_session):
            core.go_back(session_id, PlatformName.TELEGRAM_BOT)
        assert core.current_screen(session_id) is None
