"""
BootstrapEventHook -- lifecycle events emitted by the Historical Bootstrap
(DD-066). Module 5 follow-up.

The bootstrap emits BootstrapStarted, TimeframeCompleted, ProgressUpdated,
BootstrapCompleted, BootstrapFailed and BootstrapCancelled. The default
hook is a no-op; module 7 (Event Bus) subclasses / replaces it to fan
these out to subscribers. Hook methods must not raise into the bootstrap;
the bootstrap isolates exceptions regardless.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from data.bootstrap.bootstrap_state import BootstrapState
from data.bootstrap.bootstrap_progress import BootstrapProgress


class BootstrapEventHook:
    """No-op bootstrap lifecycle hook (DD-066)."""

    def on_bootstrap_started(self, asset: str) -> None:            # pragma: no cover
        pass

    def on_timeframe_completed(self, asset: str, timeframe: str,
                               state: BootstrapState) -> None:     # pragma: no cover
        pass

    def on_progress_updated(self, progress: BootstrapProgress) -> None:  # pragma: no cover
        pass

    def on_bootstrap_completed(self, asset: str) -> None:          # pragma: no cover
        pass

    def on_bootstrap_failed(self, asset: str) -> None:             # pragma: no cover
        pass

    def on_bootstrap_cancelled(self, asset: str) -> None:          # pragma: no cover
        pass
