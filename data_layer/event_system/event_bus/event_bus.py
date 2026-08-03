"""
EventBus -- central publish/subscribe hub for GoldBot (v1.1 Phase 1,
module 7).

Loose coupling: the bus depends on no producer and no consumer, only on
the typed Event. Producers publish; consumers subscribe. Supports:
- typed subscription, namespace-wildcard ("MARKET") and full wildcard
  ("*") subscription (amendments 4 + 6);
- priority-ordered dispatch (HIGH first);
- sync `publish` and async `publish_async` (bounded priority queue +
  worker thread);
- pre-publish validation (amendment 3);
- replay log (policy-governed) and a distributed bridge hook;
- handler-exception isolation and metrics.

Not wired into core/pipeline.py; carries no signal/risk/decision logic
(Trading Safety). This module never imports from any layer above data/.
"""

from __future__ import annotations

import itertools
import queue
import threading
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Union

from core_layer.logger.logger import setup_logger
from data_layer.event_system.event_model import (
    Event, EventType, EventPriority, validate_event, EventValidationError,
)
from data_layer.event_system.replay_log import ReplayLog, ReplayPolicy
from data_layer.event_system.event_metrics import EventMetrics
from data_layer.event_system.event_bridge import EventBridge

logger = setup_logger("EventBus")

WILDCARD = "*"
Handler = Callable[[Event], None]
Selector = Union[EventType, str]


@dataclass
class SubscriptionHandle:
    id: int
    key: str


@dataclass
class _Subscription:
    handle: SubscriptionHandle
    handler: Handler
    priority: EventPriority


class EventBus:
    def __init__(self, require_payload: bool = False):
        self._subs: Dict[str, List[_Subscription]] = {}
        self._lock = threading.RLock()
        self._ids = itertools.count(1)
        self._metrics = EventMetrics()
        self._replay: Optional[ReplayLog] = None
        self._bridge: Optional[EventBridge] = None
        self._require_payload = require_payload
        # async
        self._queue: "queue.PriorityQueue" = None
        self._worker: Optional[threading.Thread] = None
        self._running = False
        self._seq = itertools.count(1)

    # -- subscription ---------------------------------------------------
    @staticmethod
    def _key(selector: Selector) -> str:
        if isinstance(selector, EventType):
            return selector.value
        return selector   # "*" or a namespace like "MARKET"

    def subscribe(self, selector: Selector, handler: Handler,
                  priority: EventPriority = EventPriority.NORMAL
                  ) -> SubscriptionHandle:
        """
        Subscribe to a specific EventType, a namespace ("MARKET"), or all
        events ("*"). Returns a handle for unsubscribe.
        """
        key = self._key(selector)
        with self._lock:
            handle = SubscriptionHandle(id=next(self._ids), key=key)
            self._subs.setdefault(key, []).append(
                _Subscription(handle, handler, priority))
            return handle

    def unsubscribe(self, handle: SubscriptionHandle) -> None:
        with self._lock:
            subs = self._subs.get(handle.key)
            if not subs:
                return
            self._subs[handle.key] = [s for s in subs
                                      if s.handle.id != handle.id]

    # -- configuration --------------------------------------------------
    def enable_replay(self, policy: Optional[ReplayPolicy] = None) -> None:
        self._replay = ReplayLog(policy)

    def attach_bridge(self, bridge: EventBridge) -> None:
        self._bridge = bridge

    def metrics(self) -> EventMetrics:
        return self._metrics

    @property
    def replay_log(self) -> Optional[ReplayLog]:
        return self._replay

    # -- publish (sync) -------------------------------------------------
    def publish(self, event: Event) -> None:
        """Validate, record, and dispatch an event synchronously."""
        try:
            validate_event(event, require_payload=self._require_payload)
        except EventValidationError:
            self._metrics.rejected += 1
            raise
        self._metrics.record_published(event.type)
        if self._replay is not None:
            self._replay.record(event, event.timestamp)
        if self._bridge is not None:
            self._safe(self._bridge.forward, event, bridge=True)
        self._dispatch(event)

    def _dispatch(self, event: Event) -> None:
        # collect handlers matching type + namespace + wildcard, priority-ordered
        with self._lock:
            matches: List[_Subscription] = []
            for key in (event.type.value, event.namespace, WILDCARD):
                matches.extend(self._subs.get(key, ()))
            ordered = sorted(matches, key=lambda s: s.priority.value)
        for sub in ordered:
            self._safe(sub.handler, event)

    def _safe(self, fn, event: Event, bridge: bool = False) -> None:
        try:
            fn(event)
            if not bridge:
                self._metrics.delivered += 1
        except Exception:
            self._metrics.handler_errors += 1
            logger.exception("EventBus handler raised on %s; isolated",
                             event.type.value)

    # -- publish (async) ------------------------------------------------
    def start(self, max_queue: int = 10000) -> None:
        """Start the async dispatch worker."""
        with self._lock:
            if self._running:
                return
            self._queue = queue.PriorityQueue(maxsize=max_queue)
            self._running = True
            self._worker = threading.Thread(target=self._run, daemon=True,
                                            name="EventBusWorker")
            self._worker.start()

    def publish_async(self, event: Event) -> None:
        """Enqueue for the worker; priority-ordered, non-blocking."""
        try:
            validate_event(event, require_payload=self._require_payload)
        except EventValidationError:
            self._metrics.rejected += 1
            raise
        if not self._running or self._queue is None:
            # no worker -> fall back to synchronous delivery
            self.publish(event)
            return
        item = (event.priority.value, next(self._seq), event)
        try:
            self._queue.put_nowait(item)
            self._metrics.queue_depth = self._queue.qsize()
        except queue.Full:
            self._metrics.dropped += 1

    def _run(self) -> None:
        while self._running:
            try:
                _, _, event = self._queue.get(timeout=0.1)
            except queue.Empty:
                continue
            self._metrics.record_published(event.type)
            if self._replay is not None:
                self._replay.record(event, event.timestamp)
            if self._bridge is not None:
                self._safe(self._bridge.forward, event, bridge=True)
            self._dispatch(event)
            self._queue.task_done()
            self._metrics.queue_depth = self._queue.qsize()

    def flush(self) -> None:
        """Block until the async queue is drained (test/shutdown helper)."""
        if self._queue is not None:
            self._queue.join()

    def stop(self) -> None:
        self._running = False
        worker = self._worker
        if worker is not None:
            worker.join(timeout=2.0)
        self._worker = None
