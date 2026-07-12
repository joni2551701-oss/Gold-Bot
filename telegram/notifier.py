import asyncio
from typing import Optional
from dataclasses import dataclass

from telegram.signal_formatter import FormattedSignal
from telegram.bot import TelegramBot
from core.secrets import Secrets
from core.logger import setup_logger

logger = setup_logger("Notifier")


@dataclass(frozen=True)
class NotifierConfig:
    enabled: bool = True


@dataclass(frozen=True)
class NotifierResult:
    sent: bool
    reason: str


class Notifier:
    """
    Telegram Layer — signal delivery.

    send_message() only delivers text. It must never analyze signals,
    calculate risk, approve trades, or modify decisions -- those
    remain the exclusive responsibility of the AI Analyzer, Decision
    Engine, Risk Manager, and SignalFormatter respectively.
    """

    def __init__(
        self,
        config: Optional[NotifierConfig] = None,
    ):
        self.config = config or NotifierConfig()
        # TelegramBot fails gracefully (self._bot = None) when the token
        # is missing/invalid, so this construction never raises.
        self._bot = TelegramBot()

    def send(
        self,
        formatted_signal: FormattedSignal,
    ) -> NotifierResult:
        """
        Legacy placeholder entry point, retained for backward
        compatibility with existing callers (main.py). Use
        send_message() for real delivery.
        """
        return NotifierResult(
            sent=False,
            reason="Not implemented"
        )

    def send_message(
        self,
        message: str,
        chat_id: Optional[str] = None,
    ) -> bool:
        """
        Sends a single text message via TelegramBot. Exception-safe:
        any failure (disabled config, empty message, missing token,
        missing chat_id, network/API error) is caught and reported as
        False -- this method must never raise, so a caller (e.g. the
        pipeline) can call it without risking a crash.
        """
        if not self.config.enabled:
            return False

        if not message:
            return False

        resolved_chat_id = chat_id
        if resolved_chat_id is None:
            try:
                resolved_chat_id = Secrets().TELEGRAM_CHAT_ID
            except Exception as e:
                logger.warning(f"Cannot send message: no chat_id provided and TELEGRAM_CHAT_ID unavailable ({e}).")
                return False

        try:
            result = asyncio.run(self._bot.send_message(message, resolved_chat_id))
        except Exception as e:
            logger.warning(f"Telegram delivery failed: {e}")
            return False

        if not result.sent:
            logger.warning(f"Telegram delivery failed: {result.reason}")
        return result.sent
