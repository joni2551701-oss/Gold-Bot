from typing import Optional
from dataclasses import dataclass
from aiogram import Bot
from core.secrets import Secrets


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

    Token is sourced strictly from core.secrets.Secrets — never
    hardcoded.
    """

    def __init__(
        self,
        config: Optional[BotConfig] = None,
    ):
        self.config = config or BotConfig()
        self._secrets = Secrets()
        self._bot = Bot(token=self._secrets.TELEGRAM_BOT_TOKEN)

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

        try:
            await self._bot.send_message(chat_id=chat_id, text=text)
            return BotResult(sent=True, reason="")
        except Exception as e:
            return BotResult(sent=False, reason=str(e))
