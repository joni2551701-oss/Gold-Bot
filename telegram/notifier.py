from typing import Optional
from dataclasses import dataclass
from telegram.signal_formatter import FormattedSignal


@dataclass(frozen=True)
class NotifierConfig:
    enabled: bool = True


@dataclass(frozen=True)
class NotifierResult:
    sent: bool
    reason: str


class Notifier:
    """
    Telegram Layer — signal delivery contract only.
    No Telegram Bot API, no aiogram, no HTTP, no requests, no asyncio,
    no queue, no retry, no chat_id, no bot token, no logger,
    no markdown/html/emoji, no file upload, no database.

    Actual delivery mechanics belong to telegram/bot.py (future phase).
    """

    def __init__(
        self,
        config: Optional[NotifierConfig] = None,
    ):
        self.config = config or NotifierConfig()

    def send(
        self,
        formatted_signal: FormattedSignal,
    ) -> NotifierResult:
        """
        Entry point for signal delivery. Currently unimplemented —
        no network call is made. Real Telegram integration will be
        wired in telegram/bot.py.
        """
        return NotifierResult(
            sent=False,
            reason="Not implemented"
        )
