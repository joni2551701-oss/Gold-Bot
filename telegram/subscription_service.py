"""
Telegram Layer — subscription service (Phase 42).

Bridges Telegram /plan, /subscription, /upgrade commands to
database.subscription_repository.SubscriptionRepository. No
Telegram/aiogram objects here, no payment/billing logic -- this is a
foundation only: no real upgrade happens, upgrade_request() just
records the request and reports a static "coming soon" outcome.
Exception handling ensures a database failure never propagates up to
a command handler.

    Telegram Handler -> SubscriptionService -> SubscriptionRepository -> Database
"""

from typing import Optional
from dataclasses import dataclass

from database.subscription_repository import SubscriptionRepository
from database.subscription_models import SubscriptionRecord
from core.logger import setup_logger

logger = setup_logger("SubscriptionService")

DEFAULT_PLAN = "FREE"
DEFAULT_STATUS = "ACTIVE"


@dataclass(frozen=True)
class SubscriptionServiceResult:
    success: bool
    reason: str
    subscription: Optional[SubscriptionRecord] = None


class SubscriptionService:
    """Telegram -> Repository bridge for plan/subscription lookups."""

    def __init__(self, subscription_repository: Optional[SubscriptionRepository] = None):
        # Lazy, same pattern as UserService/AdminService: constructing
        # SubscriptionRepository() touches disk (schema init). A bare
        # SubscriptionService() must not do that until a method is
        # actually called. May be injected for tests.
        self._subscription_repository = subscription_repository

    def _get_repository(self) -> SubscriptionRepository:
        if self._subscription_repository is None:
            self._subscription_repository = SubscriptionRepository()
        return self._subscription_repository

    def _get_or_create(self, telegram_id) -> SubscriptionRecord:
        """
        Returns the user's subscription, creating a default FREE/
        ACTIVE one on first lookup if none exists yet -- so a user
        registered before this phase, or any direct call that skipped
        /start, still gets a subscription instead of "not found."
        """
        repository = self._get_repository()
        existing = repository.get_subscription(telegram_id)
        if existing is not None:
            return existing

        created = repository.create_subscription(telegram_id, plan=DEFAULT_PLAN, status=DEFAULT_STATUS)
        if created is not None:
            return created

        # Lost a race against a concurrent creation; return the winner's row.
        return repository.get_subscription(telegram_id)

    def get_plan(self, telegram_id) -> SubscriptionServiceResult:
        """Returns the user's current plan, creating a default subscription if needed. Never raises."""
        try:
            subscription = self._get_or_create(telegram_id)
            return SubscriptionServiceResult(success=True, reason="", subscription=subscription)
        except Exception as e:
            logger.warning(f"get_plan failed for telegram_id={telegram_id}: {e}")
            return SubscriptionServiceResult(success=False, reason=f"Database error: {e}")

    def get_subscription(self, telegram_id) -> SubscriptionServiceResult:
        """Returns the user's full subscription record, creating a default one if needed. Never raises."""
        try:
            subscription = self._get_or_create(telegram_id)
            return SubscriptionServiceResult(success=True, reason="", subscription=subscription)
        except Exception as e:
            logger.warning(f"get_subscription failed for telegram_id={telegram_id}: {e}")
            return SubscriptionServiceResult(success=False, reason=f"Database error: {e}")

    def upgrade_request(self, telegram_id) -> SubscriptionServiceResult:
        """
        Records that an upgrade was requested. Foundation only -- no
        payment gateway, no plan change. Ensures the subscription row
        exists (same fallback as get_plan/get_subscription) so a
        request from a brand-new user doesn't fail. Never raises.
        """
        try:
            subscription = self._get_or_create(telegram_id)
            logger.info(f"Upgrade requested by telegram_id={telegram_id} (current plan: {subscription.plan})")
            return SubscriptionServiceResult(success=True, reason="", subscription=subscription)
        except Exception as e:
            logger.warning(f"upgrade_request failed for telegram_id={telegram_id}: {e}")
            return SubscriptionServiceResult(success=False, reason=f"Database error: {e}")
