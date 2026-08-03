"""
Phase 47 — Subscription Layer tests: FREE/PREMIUM/VIP create/read/access.
"""


def test_get_plan_auto_creates_free_subscription():
    from platform_layer.telegram.subscription_service import SubscriptionService

    result = SubscriptionService().get_plan("200")
    assert result.success is True
    assert result.subscription.plan == "FREE"
    assert result.subscription.status == "ACTIVE"


def test_repository_duplicate_subscription_blocked():
    from database_layer.user_repository.subscription_repository import SubscriptionRepository

    repo = SubscriptionRepository()
    first = repo.create_subscription("201")
    assert first is not None

    duplicate = repo.create_subscription("201")
    assert duplicate is None


def test_update_plan_free_to_premium_to_vip():
    from database_layer.user_repository.subscription_repository import SubscriptionRepository

    repo = SubscriptionRepository()
    repo.create_subscription("202")

    assert repo.update_plan("202", "PREMIUM") is True
    assert repo.get_subscription("202").plan == "PREMIUM"

    assert repo.update_plan("202", "VIP") is True
    assert repo.get_subscription("202").plan == "VIP"


def test_has_signal_access_free_denied():
    from platform_layer.telegram.subscription_service import SubscriptionService

    service = SubscriptionService()
    service.get_plan("203")  # creates FREE subscription
    assert service.has_signal_access("203") is False


def test_has_signal_access_premium_and_vip_allowed():
    from platform_layer.telegram.subscription_service import SubscriptionService
    from database_layer.user_repository.subscription_repository import SubscriptionRepository

    service = SubscriptionService()
    service.get_plan("204")

    repo = SubscriptionRepository()
    repo.update_plan("204", "PREMIUM")
    assert service.has_signal_access("204") is True

    repo.update_plan("204", "VIP")
    assert service.has_signal_access("204") is True


def test_has_signal_access_unknown_plan_fails_safe_deny():
    from platform_layer.telegram.subscription_service import SubscriptionService
    from database_layer.user_repository.subscription_repository import SubscriptionRepository

    service = SubscriptionService()
    service.get_plan("205")

    SubscriptionRepository().update_plan("205", "SOME_UNKNOWN_PLAN")
    assert service.has_signal_access("205") is False


def test_upgrade_request_never_changes_plan():
    """Phase 42/44 foundation: /upgrade must not actually change the plan (no payment gateway)."""
    from platform_layer.telegram.subscription_service import SubscriptionService

    service = SubscriptionService()
    service.get_plan("206")

    result = service.upgrade_request("206")
    assert result.success is True
    assert result.subscription.plan == "FREE"  # unchanged
