"""
EventBridge -- interface for forwarding bus events to an external/remote
bus (v1.1 Phase 1, module 7). A future RedisEventBridge /
WebSocketEventBridge forwards events for multi-process / multi-node
fan-out WITHOUT the bus knowing the transport.

This phase ships the interface + a no-op bridge; real transports come
later (Distributed Event Bridge). This module never imports from any
layer above data/.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from data_layer.event_system.event_model import Event


class EventBridge(ABC):
    @abstractmethod
    def forward(self, event: Event) -> None:
        """Forward an event to the external bus. Must not raise into the bus."""
        raise NotImplementedError


class NullBridge(EventBridge):
    """No-op bridge (in-process only); records nothing."""

    def forward(self, event: Event) -> None:
        return None
