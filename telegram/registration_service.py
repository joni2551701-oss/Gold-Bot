"""
Telegram Layer — Registration Wizard state machine (V2 Phase 3).

Tracks where an in-progress /start -> Language -> Phone Share flow
left off and advances it, using the users table's own
registration_step/registration_completed columns (V2 Phase 3 Stage 0
Audit, Option B) rather than inferring state from other columns.
Mirrors telegram.user_service.UserService's "own a lazy repository"
shape -- this is a sibling service, not a UserService subclass, since
its concern (Wizard sequencing) is distinct from UserService's
(profile CRUD):

    Telegram Handler -> RegistrationService -> UserRepository -> Database

Never raises: every method here follows the same never-raises
contract every other telegram/*_service.py method already keeps, so a
database hiccup degrades to "no Wizard step change" rather than
breaking /start or /language.
"""

from typing import Optional

from database.user_repository import UserRepository
from core.logger import setup_logger

logger = setup_logger("RegistrationService")


class RegistrationStep:
    """The three Wizard states a users.registration_step value can hold."""
    LANGUAGE = "LANGUAGE"
    PHONE = "PHONE"
    COMPLETE = "COMPLETE"


class RegistrationService:
    def __init__(self, user_repository: Optional[UserRepository] = None):
        # Lazy, same reason as UserService.__init__: constructing
        # UserRepository() touches disk (schema init/migration).
        self._user_repository = user_repository

    def _get_repository(self) -> UserRepository:
        if self._user_repository is None:
            self._user_repository = UserRepository()
        return self._user_repository

    def current_step(self, telegram_id) -> Optional[str]:
        """
        The Wizard step to show next, or None if the user doesn't
        exist, is BANNED (registration is stopped outright, never
        re-offered a Wizard step), or has already reached COMPLETE
        (nothing left to show). Never raises.
        """
        try:
            user = self._get_repository().get_user(telegram_id)
        except Exception as e:
            logger.warning(f"current_step failed for telegram_id={telegram_id}: {e}")
            return None
        if user is None or user.status == "BANNED":
            return None
        if user.registration_step == RegistrationStep.COMPLETE:
            return None
        return user.registration_step

    def advance_past_language(self, telegram_id) -> bool:
        """
        Called after a language selection lands. Advances LANGUAGE ->
        PHONE only if the user is actually mid-Wizard at the LANGUAGE
        step -- a no-op (returns False) for an already-registered user
        changing their language later via /language, so a completed
        registration is never reopened. Never raises.
        """
        try:
            repository = self._get_repository()
            user = repository.get_user(telegram_id)
            if user is None or user.registration_step != RegistrationStep.LANGUAGE:
                return False
            return repository.set_registration_step(telegram_id, RegistrationStep.PHONE)
        except Exception as e:
            logger.warning(f"advance_past_language failed for telegram_id={telegram_id}: {e}")
            return False

    def complete(self, telegram_id) -> bool:
        """
        Terminal transition after a successful Phone Share. Safe to
        call even if the user is already COMPLETE (idempotent
        UPDATE, no error). Never raises.
        """
        try:
            return self._get_repository().complete_registration(telegram_id)
        except Exception as e:
            logger.warning(f"complete failed for telegram_id={telegram_id}: {e}")
            return False

    def is_complete(self, telegram_id) -> bool:
        """
        True if this user's registration has reached COMPLETE (V2
        Phase 5) -- used by telegram.command_router.route_contact()
        to decide whether to attach the persistent Reply Keyboard
        right after a successful phone share. False for an unknown
        user. Never raises.
        """
        try:
            user = self._get_repository().get_user(telegram_id)
        except Exception as e:
            logger.warning(f"is_complete failed for telegram_id={telegram_id}: {e}")
            return False
        return user is not None and user.registration_completed
