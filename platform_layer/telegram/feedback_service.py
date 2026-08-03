"""
Telegram Layer — feedback service (Phase 46).

Bridges Telegram /feedback (user) and /feedbacks (admin) commands to
database.feedback_repository.FeedbackRepository. No Telegram/aiogram
objects here, no SQL -- only feedback submission/listing/status
updates, with validation and exception handling so a database failure
never propagates up to a command handler.

    Telegram Handler / AdminService -> FeedbackService -> FeedbackRepository -> Database
"""

from typing import List, Optional
from dataclasses import dataclass, field

from database_layer.user_repository.feedback_repository import FeedbackRepository
from database_layer.user_repository.feedback_models import FeedbackRecord
from core_layer.logger.logger import setup_logger

logger = setup_logger("FeedbackService")

VALID_STATUSES = {"OPEN", "REVIEWED", "RESOLVED"}


@dataclass(frozen=True)
class FeedbackServiceResult:
    success: bool
    reason: str
    feedback: Optional[FeedbackRecord] = None
    feedback_list: List[FeedbackRecord] = field(default_factory=list)


class FeedbackService:
    """Telegram -> Repository bridge for feedback submission and admin review."""

    def __init__(self, feedback_repository: Optional[FeedbackRepository] = None):
        # Lazy, same pattern as UserService/AdminService: constructing
        # FeedbackRepository() touches disk (schema init). A bare
        # FeedbackService() must not do that until a method is
        # actually called. May be injected for tests.
        self._feedback_repository = feedback_repository

    def _get_repository(self) -> FeedbackRepository:
        if self._feedback_repository is None:
            self._feedback_repository = FeedbackRepository()
        return self._feedback_repository

    def send_feedback(self, telegram_id, message: str) -> FeedbackServiceResult:
        """
        Submits a new feedback entry. Rejects an empty/blank message
        without touching the database. Never raises.
        """
        if not message or not message.strip():
            return FeedbackServiceResult(success=False, reason="Feedback message is empty")

        try:
            repository = self._get_repository()
            created = repository.create_feedback(telegram_id, message.strip())
            return FeedbackServiceResult(success=True, reason="", feedback=created)
        except Exception as e:
            logger.warning(f"send_feedback failed for telegram_id={telegram_id}: {e}")
            return FeedbackServiceResult(success=False, reason=f"Database error: {e}")

    def get_feedback_list(self, limit: int = 50) -> FeedbackServiceResult:
        """Most recent feedback entries, newest first. Never raises."""
        try:
            repository = self._get_repository()
            items = repository.get_all_feedback(limit=limit)
            return FeedbackServiceResult(success=True, reason="", feedback_list=items)
        except Exception as e:
            logger.warning(f"get_feedback_list failed: {e}")
            return FeedbackServiceResult(success=False, reason=f"Database error: {e}")

    def resolve_feedback(self, feedback_id, status: str = "RESOLVED") -> FeedbackServiceResult:
        """Updates a feedback entry's status (OPEN/REVIEWED/RESOLVED). Never raises."""
        normalized = status.strip().upper() if status else ""
        if normalized not in VALID_STATUSES:
            return FeedbackServiceResult(success=False, reason=f"Invalid status: {status}")

        try:
            repository = self._get_repository()
            updated = repository.update_status(feedback_id, normalized)
            if not updated:
                return FeedbackServiceResult(success=False, reason="Feedback not found")
            return FeedbackServiceResult(success=True, reason="", feedback=repository.get_feedback(feedback_id))
        except Exception as e:
            logger.warning(f"resolve_feedback failed for feedback_id={feedback_id}: {e}")
            return FeedbackServiceResult(success=False, reason=f"Database error: {e}")
