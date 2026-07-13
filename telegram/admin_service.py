"""
Telegram Layer — admin service (Phase 37).

Bridges Telegram owner/admin commands to database.admin_repository.
AdminRepository (admin membership) and database.user_repository.
UserRepository / database.signal_repository.SignalRepository
(read-only, for get_statistics() counts). No Telegram/aiogram objects
here, no permission decisions (that's telegram/permissions.py) --
only admin CRUD and basic statistics aggregation, with exception
handling so a database failure never propagates up to a command
handler.

    Telegram Handler -> AdminService -> AdminRepository -> Database
                                      -> UserRepository -> Database
                                      -> SignalRepository -> Database
"""

from typing import Optional
from dataclasses import dataclass

from database.admin_repository import AdminRepository
from database.admin_models import AdminRecord
from database.user_repository import UserRepository
from database.signal_repository import SignalRepository
from core.logger import setup_logger

logger = setup_logger("AdminService")


@dataclass(frozen=True)
class AdminStatistics:
    total_users: int = 0
    total_signals: int = 0
    # Fraction (0.0-1.0), not a percentage -- same convention as
    # SignalCandidate.confidence / TradeDecision.confidence elsewhere
    # in the codebase.
    average_confidence: float = 0.0


@dataclass(frozen=True)
class AdminServiceResult:
    success: bool
    reason: str
    admin: Optional[AdminRecord] = None
    statistics: Optional[AdminStatistics] = None


class AdminService:
    """Telegram -> Repository bridge for admin membership and basic statistics."""

    def __init__(self, admin_repository: Optional[AdminRepository] = None):
        # Lazy, same pattern as UserService: constructing AdminRepository()
        # touches disk (schema init). A bare AdminService() must not do
        # that until a method is actually called. May be injected for tests.
        self._admin_repository = admin_repository

    def _get_repository(self) -> AdminRepository:
        if self._admin_repository is None:
            self._admin_repository = AdminRepository()
        return self._admin_repository

    def add_admin(self, telegram_id, role: str = "ADMIN") -> AdminServiceResult:
        """Grants admin access to telegram_id. Never raises."""
        try:
            repository = self._get_repository()
            if repository.is_admin(telegram_id):
                return AdminServiceResult(success=False, reason="Already an admin")

            created = repository.add_admin(telegram_id, role=role)
            if created is None:
                return AdminServiceResult(success=False, reason="Already an admin")

            return AdminServiceResult(success=True, reason="", admin=created)
        except Exception as e:
            logger.warning(f"add_admin failed for telegram_id={telegram_id}: {e}")
            return AdminServiceResult(success=False, reason=f"Database error: {e}")

    def remove_admin(self, telegram_id) -> AdminServiceResult:
        """Revokes admin access from telegram_id. Never raises."""
        try:
            repository = self._get_repository()
            removed = repository.remove_admin(telegram_id)
            if not removed:
                return AdminServiceResult(success=False, reason="Admin not found")
            return AdminServiceResult(success=True, reason="")
        except Exception as e:
            logger.warning(f"remove_admin failed for telegram_id={telegram_id}: {e}")
            return AdminServiceResult(success=False, reason=f"Database error: {e}")

    def get_admin_info(self, telegram_id) -> AdminServiceResult:
        """Looks up a specific admin's record. Never raises."""
        try:
            repository = self._get_repository()
            admin = repository.get_admin(telegram_id)
            if admin is None:
                return AdminServiceResult(success=False, reason="Not an admin")
            return AdminServiceResult(success=True, reason="", admin=admin)
        except Exception as e:
            logger.warning(f"get_admin_info failed for telegram_id={telegram_id}: {e}")
            return AdminServiceResult(success=False, reason=f"Database error: {e}")

    def is_admin(self, telegram_id) -> bool:
        """
        Convenience membership check used by telegram.permissions.
        Never raises -- a database failure resolves to False
        (fail-closed: unknown/unreachable stays not-admin).
        """
        try:
            repository = self._get_repository()
            return repository.is_admin(telegram_id)
        except Exception as e:
            logger.warning(f"is_admin check failed for telegram_id={telegram_id}: {e}")
            return False

    def check_database(self) -> bool:
        """
        True if the admins table is reachable. Used by /system as a
        lightweight database health check. Never raises.
        """
        try:
            self._get_repository()
            return True
        except Exception as e:
            logger.warning(f"Database health check failed: {e}")
            return False

    def get_statistics(self) -> AdminServiceResult:
        """
        Aggregates basic bot-wide statistics: total registered users,
        total signals (open + closed), and average confidence across
        all persisted signals. Never raises: any repository failure
        degrades to success=False rather than propagating.
        """
        try:
            total_users = UserRepository().count_users()

            signal_repository = SignalRepository()
            all_signals = signal_repository.get_open_signals() + signal_repository.get_closed_signals()

            confidence_scores = [
                row.get("confidence_score")
                for row in all_signals
                if isinstance(row.get("confidence_score"), (int, float))
            ]
            average_confidence = (
                sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
            )

            return AdminServiceResult(
                success=True,
                reason="",
                statistics=AdminStatistics(
                    total_users=total_users,
                    total_signals=len(all_signals),
                    average_confidence=average_confidence,
                ),
            )
        except Exception as e:
            logger.warning(f"get_statistics failed: {e}")
            return AdminServiceResult(success=False, reason=f"Database error: {e}")
