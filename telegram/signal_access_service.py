"""
Telegram Layer — signal access service (Phase 44).

Decides whether a Telegram user is allowed to receive signal content
(/signal). Pure access-decision logic: never touches the database
directly, never fetches or formats a signal -- that stays
telegram.signal_service.SignalService's job. OWNER/ADMIN always bypass
the plan check (telegram.permissions is the single source of truth
for that tier, same as command_router.py's command-permission gate).

    Handler -> SignalAccessService -> SubscriptionService -> SubscriptionRepository -> Database
                                    -> telegram.permissions (OWNER/ADMIN bypass)

/history is deliberately NOT gated by this service (Phase 44 design
decision -- see telegram/handlers.py's history_handler() docstring):
letting a FREE user see past signals but not the live one is the
better product funnel -- they see GoldBot's output is real before
deciding whether to upgrade.
"""

from typing import Optional

from telegram.subscription_service import SubscriptionService
from telegram.permissions import is_admin
from core_layer.logger.logger import setup_logger

logger = setup_logger("SignalAccessService")

DENIED_MESSAGE_TEMPLATE = (
    "🔒 Signal access unavailable.\n"
    "Your plan: {plan}\n"
    "Upgrade to Premium to receive trading signals."
)


class SignalAccessService:
    """Access-decision layer between a signal-related handler and SubscriptionService."""

    def __init__(self, subscription_service: Optional[SubscriptionService] = None):
        self._subscription_service = subscription_service or SubscriptionService()

    def can_access_signal(self, telegram_id) -> bool:
        """
        True if telegram_id may receive signal content. OWNER/ADMIN
        always True (permission tier outranks plan tier). Otherwise
        delegates to SubscriptionService.has_signal_access(). Never
        raises -- any failure resolves to False (fail-safe deny).
        """
        try:
            if is_admin(telegram_id):
                return True
            return self._subscription_service.has_signal_access(telegram_id)
        except Exception as e:
            logger.warning(f"can_access_signal failed for telegram_id={telegram_id}: {e}")
            return False

    def get_access_status(self, telegram_id) -> dict:
        """
        Returns {"telegram_id", "plan", "access", "bypass"} for the
        given telegram_id -- "access" is "ALLOWED"/"DENIED", "bypass"
        is True when OWNER/ADMIN granted access regardless of plan.
        Never raises: a lookup failure degrades to a safe FREE/DENIED
        status rather than propagating.
        """
        try:
            bypass = is_admin(telegram_id)
            plan_result = self._subscription_service.get_plan(telegram_id)
            plan = (
                plan_result.subscription.plan
                if plan_result.success and plan_result.subscription is not None
                else "FREE"
            )
            allowed = bypass or self._subscription_service.has_signal_access(telegram_id)
            return {
                "telegram_id": str(telegram_id),
                "plan": plan,
                "access": "ALLOWED" if allowed else "DENIED",
                "bypass": bypass,
            }
        except Exception as e:
            logger.warning(f"get_access_status failed for telegram_id={telegram_id}: {e}")
            return {"telegram_id": str(telegram_id), "plan": "FREE", "access": "DENIED", "bypass": False}

    def denied_message(self, telegram_id) -> str:
        """Renders the user-facing access-denied text, filled in with the caller's actual plan."""
        status = self.get_access_status(telegram_id)
        return DENIED_MESSAGE_TEMPLATE.format(plan=status["plan"])
