"""
Phase 47 — User Layer tests: registration, settings, lifecycle state.
"""

import asyncio


def test_registration_creates_user_with_new_status():
    from telegram.user_service import UserService

    result = UserService().register_user("100", username="alice")
    assert result.success is True
    assert result.profile.status == "NEW"


def test_registration_duplicate_returns_existing_profile():
    from telegram.user_service import UserService

    service = UserService()
    service.register_user("101", username="bob")

    result = service.register_user("101", username="bob")
    assert result.success is False
    assert result.reason == "User already exists"
    assert result.profile is not None


def test_settings_change_risk_language_timeframe_strategy():
    from telegram.user_service import UserService

    service = UserService()
    service.register_user("102", username="carol")

    assert service.change_risk("102", 5.0).success is True
    assert service.change_language("102", "RU").success is True
    assert service.change_timeframe("102", "H1").success is True
    assert service.change_strategy("102", "FVG").success is True

    profile = service.get_profile("102").profile
    assert profile.risk_percent == 5.0
    assert profile.language == "RU"
    assert profile.timeframe == "H1"
    assert profile.strategy == "FVG"


def test_settings_change_notifications():
    from telegram.user_service import UserService

    service = UserService()
    service.register_user("103", username="dave")

    result = service.change_notifications("103", False)
    assert result.success is True
    assert result.profile.notifications_enabled is False


def test_lifecycle_touch_activity_promotes_new_to_active():
    from telegram.user_service import UserService

    service = UserService()
    service.register_user("104", username="erin")
    assert service.get_user_state("104").profile.status == "NEW"

    result = service.touch_activity("104")
    assert result.success is True
    assert result.profile.status == "ACTIVE"
    assert result.profile.last_activity is not None


def test_lifecycle_ban_and_activate():
    from telegram.user_service import UserService

    service = UserService()
    service.register_user("105", username="frank")

    banned = service.ban_user("105")
    assert banned.success is True
    assert banned.profile.status == "BANNED"

    activated = service.activate_user("105")
    assert activated.success is True
    assert activated.profile.status == "ACTIVE"


def test_lifecycle_banned_user_not_silently_reactivated_by_start():
    """A BANNED user calling /start again must stay BANNED (security-relevant)."""
    from telegram.handlers import start_handler
    from telegram.user_service import UserService

    service = UserService()
    service.register_user("106", username="gina")
    service.ban_user("106")

    asyncio.run(start_handler("106", username="gina"))

    assert service.get_user_state("106").profile.status == "BANNED"


def test_get_profile_unknown_user_returns_not_found():
    from telegram.user_service import UserService

    result = UserService().get_profile("does-not-exist")
    assert result.success is False
    assert result.reason == "User not found"
