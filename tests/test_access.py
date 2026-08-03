"""
Phase 47 — Signal Access Control tests (Phase 44 feature, re-verified
here as part of the v0.2 regression suite).
"""

from database_layer.user_repository.admin_repository import AdminRepository
from database_layer.user_repository.subscription_repository import SubscriptionRepository
from platform_layer.telegram.signal_access_service import SignalAccessService

OWNER_ID = "111"  # matches conftest's TELEGRAM_OWNER_ID


def test_free_plan_denied():
    access = SignalAccessService()
    assert access.can_access_signal("500") is False

    status = access.get_access_status("500")
    assert status["plan"] == "FREE"
    assert status["access"] == "DENIED"
    assert status["bypass"] is False


def test_premium_plan_allowed():
    SubscriptionRepository().create_subscription("501", plan="PREMIUM")
    access = SignalAccessService()

    assert access.can_access_signal("501") is True
    status = access.get_access_status("501")
    assert status["access"] == "ALLOWED"
    assert status["bypass"] is False


def test_vip_plan_allowed():
    SubscriptionRepository().create_subscription("502", plan="VIP")
    access = SignalAccessService()
    assert access.can_access_signal("502") is True


def test_owner_bypasses_free_plan():
    access = SignalAccessService()
    assert access.can_access_signal(OWNER_ID) is True

    status = access.get_access_status(OWNER_ID)
    assert status["plan"] == "FREE"  # plan itself is still FREE
    assert status["access"] == "ALLOWED"  # but bypass grants access
    assert status["bypass"] is True


def test_admin_bypasses_free_plan():
    AdminRepository().add_admin("503")
    access = SignalAccessService()
    assert access.can_access_signal("503") is True


def test_missing_subscription_auto_creates_free_and_denies():
    """A telegram_id with no prior /start or subscription row still gets a safe FREE/DENIED result."""
    access = SignalAccessService()
    assert access.can_access_signal("999999999") is False

    subscription = SubscriptionRepository().get_subscription("999999999")
    assert subscription is not None
    assert subscription.plan == "FREE"


def test_denied_message_includes_actual_plan():
    access = SignalAccessService()
    message = access.denied_message("504")
    assert "🔒 Signal access unavailable." in message
    assert "Your plan: FREE" in message
    assert "Upgrade to Premium" in message
