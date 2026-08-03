"""
Telegram Layer — admin service (Phase 37; finalized Phase 41; feedback
review added Phase 46).

Bridges Telegram owner/admin commands to database.admin_repository.
AdminRepository (admin membership) and database.user_repository.
UserRepository / database.signal_repository.SignalRepository
(read-only, for get_statistics()/get_user_summary() counts). Also
sends broadcast messages via telegram.bot.TelegramBot -- unmodified,
same class Notifier already uses for outbound delivery. Feedback
review delegates to telegram.feedback_service.FeedbackService rather
than talking to FeedbackRepository directly -- FeedbackService already
owns validation/status logic, so AdminService reuses it instead of
duplicating it. No permission decisions here (that's
telegram/permissions.py) -- only admin CRUD, statistics aggregation,
system health, broadcast delivery, and feedback review, with exception
handling so a database or network failure never propagates up to a
command handler.

    Telegram Handler -> AdminService -> AdminRepository -> Database
                                      -> UserRepository -> Database
                                      -> SignalRepository -> Database
                                      -> TelegramBot -> Telegram API
                                      -> FeedbackService -> FeedbackRepository -> Database
"""

from typing import List, Optional
from dataclasses import dataclass, field

from database_layer.user_repository.admin_repository import AdminRepository
from database_layer.user_repository.admin_models import AdminRecord
from database_layer.user_repository.user_repository import UserRepository
from database_layer.trade_repository.signal_repository import SignalRepository
from database_layer.user_repository.feedback_models import FeedbackRecord
from telegram.bot import TelegramBot
from telegram.feedback_service import FeedbackService
from core_layer.secrets import Secrets
from core_layer.logger.logger import setup_logger

logger = setup_logger("AdminService")


@dataclass(frozen=True)
class AdminStatistics:
    total_users: int = 0
    total_signals: int = 0
    approved_signals: int = 0
    rejected_signals: int = 0
    # Fraction (0.0-1.0), not a percentage -- same convention as
    # SignalCandidate.confidence / TradeDecision.confidence elsewhere
    # in the codebase.
    average_confidence: float = 0.0


@dataclass(frozen=True)
class UserSummary:
    total: int = 0
    # "active" is the real Phase 45 lifecycle state (status='ACTIVE'),
    # not the Phase 41 notifications_enabled proxy that predated user
    # lifecycle tracking -- UserRepository.count_active_users() (the
    # old proxy) is left in place, unused here, for backward compat.
    active: int = 0
    created_today: int = 0
    new: int = 0
    banned: int = 0


@dataclass(frozen=True)
class SystemStatus:
    database: str = "N/A"
    telegram: str = "N/A"
    market_data: str = "N/A"
    ai: str = "N/A"
    api: str = "N/A"


@dataclass(frozen=True)
class BroadcastResult:
    sent: int = 0
    failed: int = 0


@dataclass(frozen=True)
class AdminServiceResult:
    success: bool
    reason: str
    admin: Optional[AdminRecord] = None
    statistics: Optional[AdminStatistics] = None
    user_summary: Optional[UserSummary] = None
    system_status: Optional[SystemStatus] = None
    broadcast: Optional[BroadcastResult] = None
    feedback_item: Optional[FeedbackRecord] = None
    feedback_list: List[FeedbackRecord] = field(default_factory=list)


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
        total signals (open + closed), approved/rejected counts (from
        the Phase 39 ai_decision column -- NO_TRADE is counted with
        REJECT, since the display only has two buckets), and average
        confidence across all persisted signals. Never raises: any
        repository failure degrades to success=False rather than
        propagating.
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

            approved_signals = sum(1 for row in all_signals if row.get("ai_decision") == "APPROVE")
            rejected_signals = len(all_signals) - approved_signals

            return AdminServiceResult(
                success=True,
                reason="",
                statistics=AdminStatistics(
                    total_users=total_users,
                    total_signals=len(all_signals),
                    approved_signals=approved_signals,
                    rejected_signals=rejected_signals,
                    average_confidence=average_confidence,
                ),
            )
        except Exception as e:
            logger.warning(f"get_statistics failed: {e}")
            return AdminServiceResult(success=False, reason=f"Database error: {e}")

    def get_user_summary(self) -> AdminServiceResult:
        """
        Aggregates basic user-table counts for /users: total
        registered, active/new/banned (Phase 45 lifecycle status), and
        created today (UTC). Never raises.
        """
        try:
            repository = UserRepository()
            return AdminServiceResult(
                success=True,
                reason="",
                user_summary=UserSummary(
                    total=repository.count_users(),
                    active=repository.count_by_status("ACTIVE"),
                    created_today=repository.count_users_created_today(),
                    new=repository.count_by_status("NEW"),
                    banned=repository.count_by_status("BANNED"),
                ),
            )
        except Exception as e:
            logger.warning(f"get_user_summary failed: {e}")
            return AdminServiceResult(success=False, reason=f"Database error: {e}")

    def get_system_status(self) -> SystemStatus:
        """
        Lightweight health summary for /system: database reachability
        plus whether the required environment keys are present. No
        live network calls to Telegram/TwelveData/Gemini -- out of
        scope, and a status command must never block on external I/O.
        "API" has no dedicated check today -- always "N/A", per the
        Phase 41 spec's own fallback for an unavailable check. Never
        raises.
        """
        database = "OK" if self.check_database() else "FAIL"

        try:
            secrets = Secrets()
        except Exception:
            return SystemStatus(database=database, telegram="FAIL", market_data="FAIL", ai="FAIL", api="N/A")

        def _has_key(getter) -> str:
            try:
                getter()
                return "OK"
            except Exception:
                return "FAIL"

        return SystemStatus(
            database=database,
            telegram=_has_key(lambda: secrets.TELEGRAM_BOT_TOKEN),
            market_data=_has_key(lambda: secrets.TWELVE_DATA_API_KEY),
            ai=_has_key(lambda: secrets.GEMINI_API_KEY),
            api="N/A",
        )

    async def _broadcast_all(self, message: str, chat_ids: List[str]) -> BroadcastResult:
        """
        Sends `message` to every chat_id using one TelegramBot instance
        inside one event loop, closing its session once at the end --
        same event-loop-safety pattern as Notifier._send_all() (Phase
        33.1): a fresh asyncio.run() per recipient would reopen the
        "Event loop is closed" bug that phase fixed. One recipient's
        failure is caught and counted, never stops the rest.
        """
        bot = TelegramBot()
        sent = 0
        failed = 0
        try:
            for chat_id in chat_ids:
                try:
                    result = await bot.send_message(message, str(chat_id))
                except Exception as e:
                    logger.warning(f"Broadcast to {chat_id} failed: {e}")
                    failed += 1
                    continue
                if result.sent:
                    sent += 1
                else:
                    failed += 1
        finally:
            await bot.close()
        return BroadcastResult(sent=sent, failed=failed)

    async def broadcast(self, message: str) -> AdminServiceResult:
        """
        Sends `message` to every registered user who has notifications
        enabled (Phase 43 -- respects users.notifications_enabled;
        previously sent to every registered user regardless).

        Phase 47 audit fix: this used to be a *synchronous* method that
        wrapped _broadcast_all() in its own asyncio.run() call -- the
        same nested-event-loop trap Notifier.send_message() hit before
        Phase 33.1 (see this module's own module docstring / telegram/
        handlers.py's note on it). broadcast_handler() is itself async
        and runs inside telegram/polling.py's already-active event
        loop, so calling asyncio.run() from in there always raised
        "asyncio.run() cannot be called from a running event loop" in
        real Telegram usage. Now broadcast() is async and the caller
        awaits it directly -- one event loop for the whole call chain,
        exactly like the Phase 33.1 fix.

        Never raises: a total failure (empty message, no eligible
        users, database error) is reported as success=False rather
        than propagating; a single recipient's delivery failure is
        only ever counted, never fatal.
        """
        if not message or not message.strip():
            return AdminServiceResult(success=False, reason="Broadcast message is empty")

        # message content intentionally not logged (Phase 51 privacy rule)
        logger.info("Broadcast started.")

        try:
            users = UserRepository().get_notification_users()
        except Exception as e:
            logger.warning(f"broadcast failed to load users: {e}")
            return AdminServiceResult(success=False, reason=f"Database error: {e}")

        if not users:
            logger.info("Broadcast finished: 0 sent, 0 failed (no eligible users).")
            return AdminServiceResult(success=True, reason="", broadcast=BroadcastResult(sent=0, failed=0))

        chat_ids = [u.telegram_id for u in users]
        try:
            result = await self._broadcast_all(message, chat_ids)
        except Exception as e:
            logger.warning(f"broadcast failed: {e}")
            return AdminServiceResult(success=False, reason=f"Broadcast error: {e}")

        logger.info(f"Broadcast finished: {result.sent} sent, {result.failed} failed.")
        return AdminServiceResult(success=True, reason="", broadcast=result)

    def get_feedback(self, limit: int = 50) -> AdminServiceResult:
        """
        Most recent feedback entries for /feedbacks, newest first.
        Never raises.
        """
        try:
            result = FeedbackService().get_feedback_list(limit=limit)
        except Exception as e:
            logger.warning(f"get_feedback failed: {e}")
            return AdminServiceResult(success=False, reason=f"Database error: {e}")

        if not result.success:
            return AdminServiceResult(success=False, reason=result.reason)
        return AdminServiceResult(success=True, reason="", feedback_list=result.feedback_list)
