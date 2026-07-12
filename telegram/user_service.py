"""
Telegram Layer — user service foundation.

Bridges Telegram commands to database.user_repository.UserRepository.
No Telegram/aiogram objects here, no permission logic (that's
telegram/permissions.py) -- only user registration and profile
read/update, safe defaults, and exception handling so a database
failure never propagates up to a command handler.

    Telegram Handler -> UserService -> UserRepository -> Database
"""

from typing import Optional
from dataclasses import dataclass

from database.user_repository import UserRepository
from database.user_models import UserRecord
from core.logger import setup_logger

logger = setup_logger("UserService")


@dataclass(frozen=True)
class UserServiceResult:
    success: bool
    reason: str
    profile: Optional[UserRecord] = None


class UserService:
    """Telegram -> Repository bridge for user registration and profile management."""

    def __init__(self, user_repository: Optional[UserRepository] = None):
        # Lazy, same pattern as ResultHandler/PerformanceTracker: constructing
        # UserRepository() touches disk (schema init). A bare UserService()
        # must not do that until a method is actually called. May be
        # injected for tests.
        self._user_repository = user_repository

    def _get_repository(self) -> UserRepository:
        if self._user_repository is None:
            self._user_repository = UserRepository()
        return self._user_repository

    def register_user(self, telegram_id, username: Optional[str] = None) -> UserServiceResult:
        """
        Creates a new user with safe defaults. If telegram_id already
        has a profile, returns it instead of creating a duplicate.
        Never raises: a database failure is reported as
        success=False, not an exception.
        """
        try:
            repository = self._get_repository()
            existing = repository.get_user(telegram_id)
            if existing is not None:
                return UserServiceResult(success=False, reason="User already exists", profile=existing)

            created = repository.create_user(telegram_id=telegram_id, username=username)
            if created is None:
                # Lost a race against a concurrent /start; return the winner's profile.
                return UserServiceResult(
                    success=False, reason="User already exists", profile=repository.get_user(telegram_id)
                )

            return UserServiceResult(success=True, reason="", profile=created)
        except Exception as e:
            logger.warning(f"register_user failed for telegram_id={telegram_id}: {e}")
            return UserServiceResult(success=False, reason=f"Database error: {e}")

    def get_profile(self, telegram_id) -> UserServiceResult:
        """Reads an existing profile. Never raises."""
        try:
            repository = self._get_repository()
            profile = repository.get_user(telegram_id)
            if profile is None:
                return UserServiceResult(success=False, reason="User not found")
            return UserServiceResult(success=True, reason="", profile=profile)
        except Exception as e:
            logger.warning(f"get_profile failed for telegram_id={telegram_id}: {e}")
            return UserServiceResult(success=False, reason=f"Database error: {e}")

    def update_language(self, telegram_id, language: str) -> UserServiceResult:
        return self.update_settings(telegram_id, {"language": language})

    def update_settings(self, telegram_id, settings: dict) -> UserServiceResult:
        """Updates one or more profile fields. Never raises."""
        try:
            repository = self._get_repository()
            updated = repository.update_user(telegram_id, **settings)
            if not updated:
                return UserServiceResult(success=False, reason="User not found or no valid fields to update")
            return UserServiceResult(success=True, reason="", profile=repository.get_user(telegram_id))
        except Exception as e:
            logger.warning(f"update_settings failed for telegram_id={telegram_id}: {e}")
            return UserServiceResult(success=False, reason=f"Database error: {e}")
