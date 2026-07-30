"""
Signals — Canonical Signal contract (TASK-CORE-008 / STEP-08).

base.py defines the common contract every canonical-signal producer honors:
validate(), build(), serialize(). signals/manager.py is the one concrete
implementation today; the ABC exists so a future alternate builder (a
replay/backtest signal source, say) plugs in with the same three-method
shape instead of inventing its own.

Read-only over already-computed inputs: a SignalContract implementation may
assemble, validate, label, enrich, and serialize a signal, but it computes
no market structure, chooses no strategy, sizes no risk, makes no decision,
and touches no platform (Telegram/mobile/desktop) API.
"""

from abc import ABC, abstractmethod


class SignalContract(ABC):
    """Base contract for anything that turns upstream setup output into a canonical signal."""

    @abstractmethod
    def validate(self, source) -> "object":
        """Return a ValidationResult for `source` (never raises)."""
        raise NotImplementedError

    @abstractmethod
    def build(self, source, **context):
        """Assemble a canonical signal (+ its derived views) from `source`. Never raises."""
        raise NotImplementedError

    @abstractmethod
    def serialize(self, built) -> dict:
        """Render a built canonical signal to a platform-independent dict."""
        raise NotImplementedError
