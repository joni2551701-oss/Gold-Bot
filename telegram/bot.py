from typing import Optional
from dataclasses import dataclass
from aiogram import Bot
from core_layer.secrets import Secrets
from core_layer.logger.logger import setup_logger

logger = setup_logger("TelegramBot")


@dataclass(frozen=True)
class BotConfig:
    enabled: bool = True


@dataclass(frozen=True)
class BotResult:
    sent: bool
    reason: str


class TelegramBot:
    """
    Telegram Layer — bot initialization and raw message delivery.
    No signal logic, no formatter logic, no decision/risk/execution
    imports, no database, no retry system, no queue, no commands.

    Token is sourced strictly from core_layer.secrets.Secrets — never
    hardcoded.
    """

    def __init__(
        self,
        config: Optional[BotConfig] = None,
    ):
        self.config = config or BotConfig()
        self._secrets = Secrets()
        self._bot: Optional[Bot] = None
        try:
            self._bot = Bot(token=self._secrets.TELEGRAM_BOT_TOKEN)
        except Exception as e:
            # Token missing/invalid: fail gracefully. send_message() will
            # report this per-call instead of crashing at construction time.
            logger.warning(f"TelegramBot init failed (token missing/invalid): {e}")
            self._bot = None

    async def send_message(
        self,
        text: str,
        chat_id: str,
    ) -> BotResult:
        """
        Sends a raw text message via the Telegram Bot API.
        No formatting, no retry, no queueing.
        """
        if not self.config.enabled:
            return BotResult(sent=False, reason="Bot disabled")

        if self._bot is None:
            return BotResult(sent=False, reason="Telegram bot token not configured")

        try:
            await self._bot.send_message(chat_id=chat_id, text=text)
            return BotResult(sent=True, reason="")
        except Exception as e:
            # message text intentionally not logged (Phase 51 privacy rule)
            logger.warning(f"send_message failed for chat_id={chat_id}: {e}")
            return BotResult(sent=False, reason=str(e))

    async def close(self) -> None:
        """
        Closes the underlying aiohttp session/connector (aiogram lazily
        creates it on the first send_message() call, bound to whichever
        event loop is running at that moment). Must be awaited from
        inside the same event loop the session was created in -- calling
        it after that loop has already closed cannot clean anything up.
        No-op if the bot never initialized (self._bot is None) or no
        message was ever sent (session never created).
        """
        if self._bot is not None:
            await self._bot.session.close()
