"""
Signals — platform-independent formatter (TASK-CORE-008 / STEP-08).

Turns a canonical signal into a neutral presentation payload every platform
can render on its own terms: a summary, a title, a description, a short
reason and a set of tags. It writes NO platform markup — no Telegram HTML,
no mobile/desktop/mini-app widgets. Consumers read these plain strings and
decorate them however they like.

It only reads already-computed values (direction, prices, strength label,
the setup's own reason strings) — it computes no analysis and makes no
decision.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from signal_layer.signal_builder.schema import SignalSchema
from signal_layer.signal_scoring.quality import SignalStrength


@dataclass(frozen=True)
class SignalPresentation:
    """Neutral, platform-agnostic view of a canonical signal."""
    title: str
    summary: str
    description: str
    short_reason: str
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "summary": self.summary,
            "description": self.description,
            "short_reason": self.short_reason,
            "tags": list(self.tags),
        }


def format_signal(
    signal: SignalSchema,
    *,
    strength: Optional[SignalStrength] = None,
    reasons: Optional[List[str]] = None,
) -> SignalPresentation:
    """
    Build a SignalPresentation from an already-assembled canonical signal.
    Pure string assembly — never raises, never decides.
    """
    reasons = list(reasons or [])
    direction = signal.direction or "NONE"
    strength_label = strength.value if strength is not None else (signal.quality_grade or "NORMAL")

    title = f"{signal.symbol} {direction}"
    summary = f"{direction} {signal.symbol} [{strength_label}]"

    parts = [f"{direction} on {signal.symbol} ({signal.timeframe})"]
    if signal.entry_price is not None:
        parts.append(f"entry {signal.entry_price}")
    if signal.stop_loss is not None:
        parts.append(f"SL {signal.stop_loss}")
    if signal.take_profit is not None:
        parts.append(f"TP {signal.take_profit}")
    description = ", ".join(parts) + "."

    short_reason = reasons[0] if reasons else (signal.strategy_name or "setup")

    tags = [direction, strength_label, signal.symbol, signal.timeframe]
    if signal.strategy_name:
        tags.append(signal.strategy_name)
    if signal.session:
        tags.append(signal.session)

    return SignalPresentation(
        title=title,
        summary=summary,
        description=description,
        short_reason=short_reason,
        tags=[t for t in tags if t],
    )
