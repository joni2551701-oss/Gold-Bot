"""
PriceStream -- per-asset market lifecycle state machine that pulls from a
PriceProvider and feeds ordered StreamEvents into a sink (the module-3
CandleBuilder). v1.1 Phase 1, module 4.

Design (docs/architecture/PRICE_STREAM.md), honoring:
- DD-046 Lifecycle state machine (INITIALIZING -> CONNECTING -> STREAMING
  -> {WAITING_FOR_MARKET | RECONNECTING} -> SHUTDOWN), universal across
  METAL/FOREX/CRYPTO.
- DD-047 Waiting mode: when the market is closed the stream disconnects,
  makes no provider calls (no polling), preserves memory, idles, and
  auto-resumes on reopen. CRYPTO (24/7) never enters waiting mode.
- DD-048 Provider abstraction: depends only on PriceProvider.
- DD-050 Graceful shutdown: flush -> disconnect -> health snapshot ->
  memory preserved -> no candle lost.
- DD-051 Provider isolation: provider exceptions never reach the sink or
  memory; they are caught here and turned into standardized state/health.
- DD-052 StreamEvent ordering: events are delivered to the sink in strict
  timestamp order per asset; strictly-older events are dropped and flagged.

Clock independence: `tick(now)` / `shutdown(now)` take the current time as
a parameter; the stream never reads the system clock, so tests are
deterministic. A real deployment (StreamManager) calls `tick` in a loop.

This module never imports from any layer above data/.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional, List, Any, Dict, Protocol, runtime_checkable

from core.logger import setup_logger
from data.stream.provider import PriceProvider
from data.stream.stream_event import (
    StreamEvent, StreamState, ProviderStatus, AssetClass,
)

logger = setup_logger("PriceStream")


@runtime_checkable
class MarketCalendar(Protocol):
    """Whether an asset's market is open, and when it next opens."""
    def is_open(self, now: datetime) -> bool: ...
    def next_open(self, now: datetime) -> datetime: ...


class AlwaysOpenCalendar:
    """24/7 calendar (crypto)."""
    def is_open(self, now: datetime) -> bool:
        return True

    def next_open(self, now: datetime) -> datetime:
        return now


class PriceStream:
    """One asset's provider-agnostic lifecycle state machine."""

    def __init__(self, asset: str, provider: PriceProvider, sink: Any,
                 calendar: Optional[MarketCalendar] = None,
                 asset_class: AssetClass = AssetClass.METAL,
                 max_reconnect_attempts: int = 5,
                 backoff_base_seconds: float = 1.0,
                 backoff_cap_seconds: float = 60.0,
                 validator: Any = None):
        if provider is None:
            raise ValueError("provider must not be None")
        if sink is None or not hasattr(sink, "on_event"):
            raise ValueError("sink must provide on_event()")
        self._asset = asset
        self._provider = provider
        self._sink = sink
        self._asset_class = asset_class
        self._waiting_enabled = asset_class is not AssetClass.CRYPTO  # DD-047
        self._calendar = calendar or AlwaysOpenCalendar()
        self._max_attempts = max_reconnect_attempts
        self._backoff_base = backoff_base_seconds
        self._backoff_cap = backoff_cap_seconds
        # TASK-ARCH-101: optional canonical StreamValidator. When
        # supplied, an event failing validation is dropped (not
        # forwarded), mirroring the legacy stream/'s drop-on-invalid
        # behavior. Default None -> no validation, behavior unchanged.
        self._validator = validator

        self._state = StreamState.INITIALIZING
        self._last_ts: Optional[datetime] = None      # DD-052 ordering
        self._last_event: Optional[StreamEvent] = None  # for validator dup/seq
        self._reconnect_attempts = 0
        self._next_retry_at: Optional[datetime] = None
        self._waiting_since: Optional[datetime] = None
        self._last_error: Optional[str] = None
        self._stats: Dict[str, int] = {
            "forwarded": 0, "dropped_out_of_order": 0, "reads": 0,
            "connects": 0, "reconnects": 0, "provider_errors": 0,
            "waiting_entries": 0, "dropped_invalid": 0,
        }

    # -- identity / introspection --------------------------------------
    @property
    def asset(self) -> str:
        return self._asset

    @property
    def state(self) -> StreamState:
        return self._state

    def stats(self) -> Dict[str, int]:
        return dict(self._stats)

    def health(self) -> Dict[str, Any]:
        return {
            "asset": self._asset,
            "state": self._state.value,
            "asset_class": self._asset_class.value,
            "last_event_time": self._last_ts.isoformat() if self._last_ts else None,
            "reconnect_attempts": self._reconnect_attempts,
            "waiting_since": self._waiting_since.isoformat() if self._waiting_since else None,
            "last_error": self._last_error,
            "stats": dict(self._stats),
        }

    # -- state machine --------------------------------------------------
    def tick(self, now: datetime) -> StreamState:
        """Advance the state machine by one step, using caller-supplied `now`."""
        now = self._utc(now)
        st = self._state
        if st is StreamState.SHUTDOWN:
            return st
        if st is StreamState.INITIALIZING:
            self._set_state(StreamState.CONNECTING)
        elif st is StreamState.WAITING_FOR_MARKET:
            self._tick_waiting(now)
        elif st is StreamState.CONNECTING:
            self._tick_connecting(now)
        elif st is StreamState.STREAMING:
            self._tick_streaming(now)
        elif st is StreamState.RECONNECTING:
            self._tick_reconnecting(now)
        return self._state

    def _tick_waiting(self, now: datetime) -> None:
        # DD-047: no provider calls while waiting; resume on reopen.
        if self._market_open(now):
            self._waiting_since = None
            self._set_state(StreamState.CONNECTING)

    def _tick_connecting(self, now: datetime) -> None:
        if self._waiting_enabled and not self._market_open(now):
            self._enter_waiting(now)
            return
        if self._safe_connect():
            self._reconnect_attempts = 0
            self._stats["connects"] += 1
            self._set_state(StreamState.STREAMING)
        else:
            self._schedule_retry(now)
            self._set_state(StreamState.RECONNECTING)

    def _tick_streaming(self, now: datetime) -> None:
        if self._waiting_enabled and not self._market_open(now):
            self._enter_waiting(now)     # graceful: disconnect + idle
            return
        events, ok = self._safe_read()
        if not ok:
            self._schedule_retry(now)
            self._set_state(StreamState.RECONNECTING)
            return
        if self._provider_market_closed() and self._waiting_enabled:
            self._enter_waiting(now)
            return
        self._forward_ordered(events)

    def _tick_reconnecting(self, now: datetime) -> None:
        if self._waiting_enabled and not self._market_open(now):
            self._enter_waiting(now)
            return
        if self._next_retry_at is not None and now < self._next_retry_at:
            return  # still backing off
        if self._reconnect_attempts >= self._max_attempts:
            self._last_error = "reconnect attempts exhausted"
            self.shutdown(now)
            return
        if self._safe_connect():
            self._reconnect_attempts = 0
            self._stats["connects"] += 1
            self._set_state(StreamState.STREAMING)
        else:
            self._reconnect_attempts += 1
            self._stats["reconnects"] += 1
            self._schedule_retry(now)

    # -- graceful shutdown (DD-050) ------------------------------------
    def shutdown(self, now: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Flush any final events, disconnect, snapshot health, preserve
        memory, then enter SHUTDOWN. Returns the health snapshot.
        """
        if self._state is StreamState.SHUTDOWN:
            return self.health()
        # 1. flush pending (best-effort, isolated) so no candle is lost
        if self._provider_connected_state():
            events, ok = self._safe_read()
            if ok:
                self._forward_ordered(events)
        # 2. provider disconnect (isolated)
        self._safe_disconnect()
        # 3. enter terminal state, then snapshot it (Memory never touched)
        self._set_state(StreamState.SHUTDOWN)
        return self.health()

    # -- waiting / helpers ---------------------------------------------
    def _enter_waiting(self, now: datetime) -> None:
        self._safe_disconnect()          # DD-047: stop polling while closed
        self._waiting_since = now
        self._stats["waiting_entries"] += 1
        self._set_state(StreamState.WAITING_FOR_MARKET)

    def _market_open(self, now: datetime) -> bool:
        if not self._waiting_enabled:    # crypto -> always open (DD-047)
            return True
        return self._calendar.is_open(now)

    def _schedule_retry(self, now: datetime) -> None:
        backoff = min(self._backoff_base * (2 ** self._reconnect_attempts),
                      self._backoff_cap)
        self._next_retry_at = now + timedelta(seconds=backoff)

    def _forward_ordered(self, events: List[StreamEvent]) -> None:
        # DD-052: deliver in strict timestamp order; drop strictly-older.
        for e in sorted(events, key=lambda ev: ev.timestamp):
            if self._last_ts is not None and e.timestamp < self._last_ts:
                self._stats["dropped_out_of_order"] += 1
                continue
            # TASK-ARCH-101: optional canonical validation. An invalid
            # event is dropped (mirrors the legacy stream/ drop-on-invalid),
            # and does not advance _last_ts/_last_event. Fully fail-safe:
            # a validator error never blocks the stream.
            if self._validator is not None and not self._is_valid(e):
                self._stats["dropped_invalid"] += 1
                continue
            self._sink.on_event(e)
            self._last_ts = e.timestamp
            self._last_event = e
            self._stats["forwarded"] += 1

    def _is_valid(self, event: StreamEvent) -> bool:
        try:
            result = self._validator.validate(event, previous=self._last_event)
            return bool(result)
        except Exception as exc:  # noqa: BLE001 -- validator must never block the stream
            logger.warning("PriceStream[%s] validator error ignored: %s: %s",
                           self._asset, type(exc).__name__, str(exc)[:200])
            return True

    def _provider_market_closed(self) -> bool:
        try:
            return self._provider.status() is ProviderStatus.MARKET_CLOSED
        except Exception:
            return False

    def _provider_connected_state(self) -> bool:
        return self._state in (StreamState.STREAMING,)

    # -- provider isolation (DD-051): never let provider errors escape --
    def _safe_connect(self) -> bool:
        try:
            self._provider.connect()
            return True
        except Exception as exc:
            self._record_provider_error(exc)
            return False

    def _safe_disconnect(self) -> None:
        try:
            self._provider.disconnect()
        except Exception as exc:
            self._record_provider_error(exc)

    def _safe_read(self):
        try:
            events = self._provider.read() or []
            self._stats["reads"] += 1
            return list(events), True
        except Exception as exc:
            self._record_provider_error(exc)
            return [], False

    def _record_provider_error(self, exc: Exception) -> None:
        self._stats["provider_errors"] += 1
        self._last_error = f"{type(exc).__name__}: {exc}"
        logger.warning("PriceStream[%s] provider error isolated: %s",
                       self._asset, self._last_error)

    # -- misc -----------------------------------------------------------
    def _set_state(self, state: StreamState) -> None:
        self._state = state

    @staticmethod
    def _utc(now: datetime) -> datetime:
        if not isinstance(now, datetime) or now.tzinfo is None:
            raise ValueError("now must be a timezone-aware datetime (UTC)")
        return now.astimezone(timezone.utc)
