"""
Producer bridges (v1.1 Phase 1, module 7).

Adapters that implement the existing producer hook interfaces
(CandleEventHook from module 3 / DD-028, BootstrapEventHook from module 5
/ DD-066) and publish onto the EventBus. Producers stay decoupled: they
emit through the hook they already accept as a parameter; the bus is
invisible to them (no change to CandleBuilder or HistoricalBootstrap).

This module never imports from any layer above data/.
"""

from __future__ import annotations

import itertools
import uuid
from datetime import datetime, timezone
from typing import Callable, Optional

from data.candle_builder import CandleEventHook
from data.bootstrap.bootstrap_events import BootstrapEventHook
from data.bootstrap.bootstrap_state import BootstrapState
from data.events.event_bus import EventBus
from data.events.event_model import Event, EventType, EventPriority


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class CandleEventBridge(CandleEventHook):
    """Publishes candle lifecycle events (MARKET.*) to the bus (DD-028)."""

    def __init__(self, bus: EventBus, asset: str, use_async: bool = False):
        self._bus = bus
        self._asset = asset
        self._async = use_async
        self._seq = itertools.count(1)

    def _emit(self, event_type: EventType, record, priority) -> None:
        event = Event(
            type=event_type,
            payload=record,
            asset=self._asset,
            priority=priority,
            event_id=f"{record.candle_id}:{event_type.value}:{next(self._seq)}",
            timestamp=record.last_update_time,          # event time (record)
            source="CandleBuilder",
            correlation_id=record.candle_id,            # ties one candle's events
        )
        (self._bus.publish_async if self._async else self._bus.publish)(event)

    def on_new_candle(self, record) -> None:
        self._emit(EventType.MARKET_CANDLE_OPENED, record, EventPriority.NORMAL)

    def on_candle_update(self, record) -> None:
        self._emit(EventType.MARKET_CANDLE_UPDATED, record, EventPriority.LOW)

    def on_candle_close(self, record) -> None:
        self._emit(EventType.MARKET_CANDLE_CLOSED, record, EventPriority.HIGH)


class BootstrapEventBridge(BootstrapEventHook):
    """Publishes bootstrap lifecycle events (BOOTSTRAP.*) to the bus (DD-066)."""

    _TYPE = {
        "started": EventType.BOOTSTRAP_STARTED,
        "completed": EventType.BOOTSTRAP_COMPLETED,
        "failed": EventType.BOOTSTRAP_FAILED,
        "cancelled": EventType.BOOTSTRAP_CANCELLED,
    }

    def __init__(self, bus: EventBus,
                 now_fn: Optional[Callable[[], datetime]] = None,
                 use_async: bool = False):
        self._bus = bus
        self._now = now_fn or _utcnow
        self._async = use_async
        self._seq = itertools.count(1)
        self._correlation: dict = {}     # asset -> correlation id for the run

    def _corr(self, asset: str) -> str:
        return self._correlation.setdefault(asset, uuid.uuid4().hex)

    def _emit(self, event_type: EventType, asset: str, payload=None,
              priority=EventPriority.NORMAL) -> None:
        event = Event(
            type=event_type, payload=payload, asset=asset, priority=priority,
            event_id=f"{asset}:{event_type.value}:{next(self._seq)}",
            timestamp=self._now(), source="HistoricalBootstrap",
            correlation_id=self._corr(asset))
        (self._bus.publish_async if self._async else self._bus.publish)(event)

    def on_bootstrap_started(self, asset: str) -> None:
        self._correlation[asset] = uuid.uuid4().hex     # new run correlation
        self._emit(EventType.BOOTSTRAP_STARTED, asset)

    def on_timeframe_completed(self, asset: str, timeframe: str,
                               state: BootstrapState) -> None:
        self._emit(EventType.BOOTSTRAP_TIMEFRAME_COMPLETED, asset,
                   payload={"timeframe": timeframe, "state": state.value})

    def on_progress_updated(self, progress) -> None:
        self._emit(EventType.BOOTSTRAP_PROGRESS_UPDATED, progress.asset,
                   payload=progress, priority=EventPriority.LOW)

    def on_bootstrap_completed(self, asset: str) -> None:
        self._emit(EventType.BOOTSTRAP_COMPLETED, asset,
                   priority=EventPriority.HIGH)
        self._correlation.pop(asset, None)

    def on_bootstrap_failed(self, asset: str) -> None:
        self._emit(EventType.BOOTSTRAP_FAILED, asset, priority=EventPriority.HIGH)
        self._correlation.pop(asset, None)

    def on_bootstrap_cancelled(self, asset: str) -> None:
        self._emit(EventType.BOOTSTRAP_CANCELLED, asset)
        self._correlation.pop(asset, None)
