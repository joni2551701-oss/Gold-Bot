import asyncio
from typing import List, Optional
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

    def _resolve_chat_id(self, chat_id: Optional[str]) -> Optional[str]:
        if chat_id is not None:
            return chat_id
        try:
            return Secrets().TELEGRAM_CHAT_ID
        except Exception as e:
            logger.warning(f"Cannot send message: no chat_id provided and TELEGRAM_CHAT_ID unavailable ({e}).")
            return None

    async def _send_all(self, messages: List[str], chat_id: str) -> List[bool]:
        """
        Sends every message through the same TelegramBot instance
        inside one event loop, then closes its aiohttp session before
        returning -- so the caller's single asyncio.run() is the only
        event loop involved, and nothing is left open when it closes.
        """
        results = []
        try:
            for message in messages:
                try:
                    result = await self._bot.send_message(message, chat_id)
                except Exception as e:
                    logger.warning(f"Telegram delivery failed: {e}")
                    results.append(False)
                    continue
                if not result.sent:
                    logger.warning(f"Telegram delivery failed: {result.reason}")
                results.append(result.sent)
        finally:
            await self._bot.close()
        return results

    def send_message(
        self,
        message: str,
        chat_id: Optional[str] = None,
    ) -> bool:
        """
        Sends a single text message via TelegramBot. Exception-safe:
        any failure (disabled config, empty message, missing token,
        missing chat_id, network/API error) is caught and reported as
        False -- this method must never raise, so a caller can use it
        without risking a crash. Opens and fully closes its own event
        loop/session in one asyncio.run() call.
        """
        if not self.config.enabled:
            return False

        if not message:
            return False

        resolved_chat_id = self._resolve_chat_id(chat_id)
        if resolved_chat_id is None:
            return False

        try:
            results = asyncio.run(self._send_all([message], resolved_chat_id))
        except Exception as e:
            logger.warning(f"Telegram delivery failed: {e}")
            return False

        return results[0] if results else False

    def send_messages(
        self,
        messages: List[str],
        chat_id: Optional[str] = None,
    ) -> List[bool]:
        """
        Sends multiple messages using a single event loop, a single
        TelegramBot instance, and a single aiohttp session (Phase
        33.1). Fixes "Event loop is closed" / "Unclosed client
        session": calling send_message() once per signal used to open
        and close a brand new event loop per message while reusing the
        same aiogram Bot, whose lazily-created session stayed bound to
        the first (by-then-closed) loop -- message 1 succeeded,
        messages 2+ failed against a dead loop, and the orphaned
        session/connector from message 1 was never closed. Never
        raises: a total failure (disabled config, no chat_id, network
        error opening the loop) is reported as all-False.
        """
        if not messages:
            return []

        if not self.config.enabled:
            return [False] * len(messages)

        resolved_chat_id = self._resolve_chat_id(chat_id)
        if resolved_chat_id is None:
            return [False] * len(messages)

        try:
            return asyncio.run(self._send_all(messages, resolved_chat_id))
        except Exception as e:
            logger.warning(f"Telegram delivery failed: {e}")
            return [False] * len(messages)
