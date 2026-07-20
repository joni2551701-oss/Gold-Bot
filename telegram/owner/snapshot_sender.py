"""
Telegram Layer — Owner Snapshot Sender (GoldBot Core Owner Snapshot
Reporter Alpha, TASK 4).

Reuses telegram.bot.TelegramBot outright -- no new Telegram client
(this phase's Foundation Reuse Audit, docs/PHASE_OWNER_SNAPSHOT_AUDIT.md).
Sends only to TELEGRAM_OWNER_ID, never a broadcast to regular users.

Security (TASK 4's own rule): the token value and the owner chat_id
are never logged here -- every log line below is a fixed, generic
string with no interpolated secret. `SnapshotSendResult.reason` is
returned to the caller (for the workflow's own exit-code/log
decisions) but this module itself never writes it to the log.
"""

from dataclasses import dataclass
from typing import Optional

from core.logger import setup_logger
from core.secrets import Secrets
from telegram.bot import TelegramBot

logger = setup_logger("SnapshotSender")


@dataclass(frozen=True)
class SnapshotSendResult:
    sent: bool
    reason: str


async def send_snapshot(message: str, bot: Optional[TelegramBot] = None) -> SnapshotSendResult:
    """Never raises: a missing owner or a send failure both return a SnapshotSendResult, never propagate."""
    owner_id = Secrets().TELEGRAM_OWNER_ID  # "" if unset, never raises
    if not owner_id:
        logger.warning("send_snapshot: TELEGRAM_OWNER_ID not configured, skipping send.")
        return SnapshotSendResult(sent=False, reason="TELEGRAM_OWNER_ID not configured")

    owns_bot = bot is None
    telegram_bot = bot or TelegramBot()
    try:
        result = await telegram_bot.send_message(text=message, chat_id=owner_id)
    finally:
        # Only close a bot this function constructed itself -- a
        # caller-supplied bot is the caller's to close (same
        # ownership convention telegram.notifier.Notifier's own
        # ephemeral-vs-shared TelegramBot handling uses).
        if owns_bot:
            await telegram_bot.close()

    if result.sent:
        logger.info("send_snapshot: snapshot delivered to owner.")
    else:
        logger.warning("send_snapshot: delivery failed.")

    return SnapshotSendResult(sent=result.sent, reason=result.reason)
