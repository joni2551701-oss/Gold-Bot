from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class FormatterConfig:
    enabled: bool = True


@dataclass(frozen=True)
class FormattedSignal:
    formatted: bool
    text: str


class SignalFormatter:
    """
    Telegram Layer — signal text formatting contract only.
    No Telegram Bot API, no aiogram, no requests, no HTML/Markdown,
    no emoji, no templates, no string building logic.
    No knowledge of NotificationPayload, SignalCandidate, or
    ExecutionResult (these do not yet exist / are out of scope).
    """

    def __init__(
        self,
        config: Optional[FormatterConfig] = None,
    ):
        self.config = config or FormatterConfig()

    def format(self) -> FormattedSignal:
        """
        Entry point for signal formatting. Currently a placeholder —
        takes no parameters, as NotificationPayload has not yet been
        defined. Signature will change once that contract exists.
        """
        return FormattedSignal(
            formatted=False,
            text=""
        )
