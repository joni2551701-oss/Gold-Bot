"""
Telegram Layer — notification service (Phase 43).

Bridges Telegram notification-preference checks/toggles to
database.user_repository.UserRepository directly (not through
UserService -- this is a peer service focused specifically on the
notification-permission gate, not general profile management). No
Telegram/aiogram objects here, no SQL -- only reads/writes
users.notifications_enabled through the repository, with exception
handling so a database failure never propagates up to a command
handler or a broadcast/notification-sending caller.

    Telegram Handler / AdminService -> NotificationService -> UserRepository -> Database
"""

from typing import List, Optional
from dataclasses import dataclass, field

from database_layer.user_repository.user_repository import UserRepository
from database_layer.user_repository.user_models import UserRecord
from core_layer.logger.logger import setup_logger

logger = setup_logger("NotificationService")


@dataclass(frozen=True)
class NotificationServiceResult:
    success: bool
    reason: str
    enabled: Optional[bool] = None
    users: List[UserRecord] = field(default_factory=list)


class NotificationService:
    """Telegram -> Repository bridge for notification permission management."""

    def __init__(self, user_repository: Optional[UserRepository] = None):
        # Lazy, same pattern as UserService/AdminService: constructing
        # UserRepository() touches disk (schema init). A bare
        # NotificationService() must not do that until a method is
        # actually called. May be injected for tests.
        self._user_repository = user_repository

    def _get_repository(self) -> UserRepository:
        if self._user_repository is None:
            self._user_repository = UserRepository()
        return self._user_repository

    def is_enabled(self, telegram_id) -> bool:
        """
        True if the user has notifications on. Fail-closed on any
        error or unknown user -- never crashes a sending/filtering
        path: unreachable database or missing user resolves to False,
        not a raised exception.
        """
        try:
            repository = self._get_repository()
            user = repository.get_user(telegram_id)
            return bool(user.notifications_enabled) if user is not None else False
        except Exception as e:
            logger.warning(f"is_enabled check failed for telegram_id={telegram_id}: {e}")
            return False

    def enable_notifications(self, telegram_id) -> NotificationServiceResult:
        """Turns notifications on for telegram_id. Never raises."""
        try:
            repository = self._get_repository()
            updated = repository.enable_notifications(telegram_id)
            if not updated:
                return NotificationServiceResult(success=False, reason="User not found")
            return NotificationServiceResult(success=True, reason="", enabled=True)
        except Exception as e:
            logger.warning(f"enable_notifications failed for telegram_id={telegram_id}: {e}")
            return NotificationServiceResult(success=False, reason=f"Database error: {e}")

    def disable_notifications(self, telegram_id) -> NotificationServiceResult:
        """Turns notifications off for telegram_id. Never raises."""
        try:
            repository = self._get_repository()
            updated = repository.disable_notifications(telegram_id)
            if not updated:
                return NotificationServiceResult(success=False, reason="User not found")
            return NotificationServiceResult(success=True, reason="", enabled=False)
        except Exception as e:
            logger.warning(f"disable_notifications failed for telegram_id={telegram_id}: {e}")
            return NotificationServiceResult(success=False, reason=f"Database error: {e}")

    def get_notification_users(self) -> NotificationServiceResult:
        """
        All users with notifications enabled -- the recipient list for
        a notification-respecting broadcast/signal send. Never raises;
        a database failure degrades to an empty list, not a crash.
        """
        try:
            repository = self._get_repository()
            users = repository.get_notification_users()
            return NotificationServiceResult(success=True, reason="", users=users)
        except Exception as e:
            logger.warning(f"get_notification_users failed: {e}")
            return NotificationServiceResult(success=False, reason=f"Database error: {e}")
