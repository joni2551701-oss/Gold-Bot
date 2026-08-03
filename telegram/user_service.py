"""
Telegram Layer — user service foundation.

Bridges Telegram commands to database.user_repository.UserRepository.
No Telegram/aiogram objects here, no permission logic (that's
telegram/permissions.py) -- only user registration and profile
read/update, safe defaults, and exception handling so a database
failure never propagates up to a command handler.

    Telegram Handler -> UserService -> UserRepository -> Database

register_phone() (Phase 61.5: AI Production Integration Foundation,
TASK 4) is the real Phone Share Button flow's service-layer step:
Phone Hash -> UserRecord -> Trial Check -> FREE account. It imports
`core_layer.secrets.phone_hash`/`ai.access.identity_checker`/`ai.access.trial_manager`
directly -- the same "telegram/ may consume already-built ai/ output"
relationship `telegram/owner/ai_commands.py` already established (this
codebase's pipeline layering is data -> ... -> ai -> decision -> ...
-> telegram, so telegram consuming ai/'s already-computed facts is
downstream consumption, not a reversed dependency). The raw phone
number is never retained beyond this method's own local variable --
only `core_layer.secrets.phone_hash.hash_phone_number()`'s output is ever passed to
the repository.
"""

from datetime import datetime, timezone
from typing import Optional
from dataclasses import dataclass

from database.user_repository import UserRepository
from database.user_models import UserRecord
from core_layer.logger.logger import setup_logger
from core_layer.secrets.phone_hash import hash_phone_number
from ai.access.identity_checker import is_phone_reused_by_another_account
from ai.access.trial_manager import DEFAULT_TRIAL_DURATION, trial_status_from_started_at

logger = setup_logger("UserService")


@dataclass(frozen=True)
class UserServiceResult:
    success: bool
    reason: str
    profile: Optional[UserRecord] = None


@dataclass(frozen=True)
class PhoneRegistrationResult:
    success: bool
    reason: str
    trial_active: bool = False
    trial_expires_at: Optional[datetime] = None


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

    def change_language(self, telegram_id, language: str) -> UserServiceResult:
        return self.update_settings(telegram_id, {"language": language})

    def change_risk(self, telegram_id, risk_percent: float) -> UserServiceResult:
        return self.update_settings(telegram_id, {"risk_percent": risk_percent})

    def change_timeframe(self, telegram_id, timeframe: str) -> UserServiceResult:
        return self.update_settings(telegram_id, {"timeframe": timeframe})

    def change_strategy(self, telegram_id, strategy: str) -> UserServiceResult:
        return self.update_settings(telegram_id, {"strategy": strategy})

    def change_notifications(self, telegram_id, enabled: bool) -> UserServiceResult:
        return self.update_settings(telegram_id, {"notifications_enabled": enabled})

    def get_user_state(self, telegram_id) -> UserServiceResult:
        """
        Returns the user's profile, including lifecycle status
        (NEW/ACTIVE/BANNED -- Phase 45). Deliberately separate from
        subscription plan (telegram.subscription_service.
        SubscriptionService). Never raises.
        """
        try:
            repository = self._get_repository()
            profile = repository.get_user(telegram_id)
            if profile is None:
                return UserServiceResult(success=False, reason="User not found")
            return UserServiceResult(success=True, reason="", profile=profile)
        except Exception as e:
            logger.warning(f"get_user_state failed for telegram_id={telegram_id}: {e}")
            return UserServiceResult(success=False, reason=f"Database error: {e}")

    def activate_user(self, telegram_id) -> UserServiceResult:
        """Sets the user's lifecycle status to ACTIVE. Never raises."""
        try:
            repository = self._get_repository()
            updated = repository.activate_user(telegram_id)
            if not updated:
                return UserServiceResult(success=False, reason="User not found")
            return UserServiceResult(success=True, reason="", profile=repository.get_user(telegram_id))
        except Exception as e:
            logger.warning(f"activate_user failed for telegram_id={telegram_id}: {e}")
            return UserServiceResult(success=False, reason=f"Database error: {e}")

    def ban_user(self, telegram_id) -> UserServiceResult:
        """Sets the user's lifecycle status to BANNED. Never raises."""
        try:
            repository = self._get_repository()
            updated = repository.ban_user(telegram_id)
            if not updated:
                return UserServiceResult(success=False, reason="User not found")
            return UserServiceResult(success=True, reason="", profile=repository.get_user(telegram_id))
        except Exception as e:
            logger.warning(f"ban_user failed for telegram_id={telegram_id}: {e}")
            return UserServiceResult(success=False, reason=f"Database error: {e}")

    def touch_activity(self, telegram_id) -> UserServiceResult:
        """
        Records this interaction as activity (updates last_activity;
        promotes a NEW user to ACTIVE, never touches a BANNED user's
        status -- see UserRepository.update_last_activity()). Called
        before /profile, /settings, /signal, /history, /plan,
        /subscription, and (conditionally) /start. Never raises.
        """
        try:
            repository = self._get_repository()
            updated = repository.update_last_activity(telegram_id)
            if not updated:
                return UserServiceResult(success=False, reason="User not found")
            return UserServiceResult(success=True, reason="", profile=repository.get_user(telegram_id))
        except Exception as e:
            logger.warning(f"touch_activity failed for telegram_id={telegram_id}: {e}")
            return UserServiceResult(success=False, reason=f"Database error: {e}")

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

    def register_phone(self, telegram_id, phone_number: str) -> PhoneRegistrationResult:
        """
        Real Phone Share Button flow (Phase 61.5 TASK 4): Phone Hash ->
        UserRecord -> Trial Check -> FREE account. `phone_number` (the
        raw Telegram-contact-shared string) is hashed immediately via
        `core_layer.secrets.phone_hash.hash_phone_number()` and never stored, logged,
        or returned by this method -- only the hash reaches
        `UserRepository`. Never raises: any failure is reported as
        success=False, not an exception.

        "1 phone = 1 trial": a phone_hash already used by a *different*
        telegram_id blocks a new trial outright (the phone_hash is
        still recorded on this account -- storage is unconditional, only
        the trial start is gated) -- see
        `ai.access.identity_checker.is_phone_reused_by_another_account()`.
        A telegram_id that already has `trial_started_at` set keeps its
        original start time; this method never resets an existing
        trial window.
        """
        try:
            repository = self._get_repository()
            user = repository.get_user(telegram_id)
            if user is None:
                return PhoneRegistrationResult(success=False, reason="User not found -- send /start first")

            phone_hash = hash_phone_number(phone_number)
            sharing_users = repository.get_users_by_phone_hash(phone_hash)
            phone_reused = is_phone_reused_by_another_account(
                str(telegram_id), [str(u.telegram_id) for u in sharing_users]
            )
            repository.set_phone_hash(telegram_id, phone_hash)

            if phone_reused:
                return PhoneRegistrationResult(
                    success=False, reason="This phone number is already registered on another account.",
                )

            if user.trial_started_at is None:
                started_at = datetime.now(timezone.utc)
                repository.set_trial_started_at(telegram_id, started_at.isoformat())
            else:
                started_at = datetime.fromisoformat(user.trial_started_at)

            status = trial_status_from_started_at(started_at, DEFAULT_TRIAL_DURATION)
            return PhoneRegistrationResult(
                success=True, reason="", trial_active=status.active, trial_expires_at=status.expires_at,
            )
        except Exception as e:
            logger.warning(f"register_phone failed for telegram_id={telegram_id}: {e}")
            return PhoneRegistrationResult(success=False, reason=f"Database error: {e}")
