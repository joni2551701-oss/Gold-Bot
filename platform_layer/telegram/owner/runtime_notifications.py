"""
Telegram Layer — Owner Runtime Notifications (Phase 61.6: AI
Operations & Reliability Foundation, TASK 7).

A genuinely different concern from every other `platform_layer/telegram/owner/
*_commands.py` module (per this phase's own reuse audit, `docs/
PHASE61_6_RUNTIME_OPERATIONS_AUDIT.md`): those are pull-based (a
command handler calls a function, gets a message back). This module is
push-based -- an `ai_layer.ai_service.event_bus.EventBus` subscriber that turns
a handful of already-existing/newly-added event types into queued
`RuntimeAlert`s, plus a small `deliver_alerts()` that actually sends
them, Owner-only, via the already-existing `platform_layer.telegram.notifier.
Notifier`. No new orchestration, no new provider-state store (Rule 4)
-- this module only *reacts* to events other modules already publish.

Six alert conditions (the Director's own list), three different
sourcing strategies depending on what already exists to trigger them:

  Provider DOWN / Circuit OPEN -- one signal, not two. This codebase's
  circuit breaker (`ai_layer.ai_engine.providers.circuit_breaker.ProviderCircuitBreaker`,
  extended this same task) is the thing that decides a provider is
  truly down (5 consecutive failures, not one), so "Provider DOWN" and
  "Circuit OPEN" collapse onto the same event: the breaker's `_open()`
  publishes the existing `EventType.PROVIDER_FAILED` with
  `payload["circuit_state"] = "OPEN"`. A raw per-attempt
  `ai_service.py` `PROVIDER_FAILED` (no `circuit_state` key) is not
  alerted on -- that fires on every single failed attempt and would
  spam the Owner long before the breaker ever trips.

  Provider RECOVERED -- the breaker's `record_success()` publishes the
  existing `EventType.PROVIDER_RECOVERED` when it closes from
  OPEN/HALF_OPEN.

  Runtime FAILED -- `ai_layer.ai_engine.runtime.runtime_manager.RuntimeManager.
  transition()` publishes the new `EventType.RUNTIME_FAILED` (this
  task's one, in-place `EventType` addition -- see `event_bus.py`'s
  own docstring) on any transition into `RuntimeState.FAILED`.

  Cost Protection DEGRADED (Phase 62.2 TASK 8) -- `ai_layer.ai_engine.runtime.
  ai_service.AIService._check_cost_protection()` transitions into
  `RuntimeState.DEGRADED` with a reason prefixed `"cost protection: "`
  on a daily cost/token breach. Every valid `RuntimeManager.transition()`
  already publishes the generic `EventType.RUNTIME_STATE_CHANGED` --
  reused here with a `to_state == "DEGRADED"` and reason-prefix filter
  (same "reuse the existing event, filter on payload" pattern as
  `PROVIDER_FAILED`'s `circuit_state` check above) rather than a new
  EventType. Any other `DEGRADED` transition (there is no other real
  trigger for one yet) is intentionally not alerted on here -- only a
  cost-protection-caused one is.

  High Cost / Cache Disabled -- neither has a real, already-firing
  control-flow point anywhere in this codebase yet (no code path
  currently crosses a cost threshold or flips a cache on/off flag), so
  inventing a fake EventBus publisher for either would fabricate a
  signal nothing actually produces. Consistent with this codebase's
  own "never fabricate" convention (see `ai_cost({})`'s honest $0.00,
  `doctor`'s honest "N/A" for Scheduler), these two are pure evaluator
  functions instead -- `evaluate_high_cost()`/`evaluate_cache_disabled()`
  take real data a caller already has (`ProviderStats`, a cache-enabled
  flag) and return alerts if the condition holds, ready for a future
  phase's periodic caller to invoke with live data.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

from ai_layer.ai_service.audit.provider_stats import ProviderStats
from ai_layer.ai_service.event_bus import EventBus, EventType, RuntimeEvent
from core_layer.logger.logger import setup_logger
from core_layer.secrets import Secrets
from platform_layer.telegram.notifier import Notifier

logger = setup_logger("RuntimeNotifications")


@dataclass(frozen=True)
class RuntimeAlert:
    title: str
    message: str


class RuntimeNotifier:
    """
    Subscribes to an `EventBus` for the three reliability-signal events
    this task cares about and queues a `RuntimeAlert` for each. Never
    sends a Telegram message itself -- `drain()` hands the queue to a
    caller, which passes it to `deliver_alerts()` (kept separate so
    "decide there's something to say" and "actually send it" can be
    tested independently, same separation `ai_layer.ai_service.audit.provider_stats.
    RuntimeMetricsCollector` already established for metrics).
    """

    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        self._event_bus = event_bus or EventBus()
        self._pending: List[RuntimeAlert] = []
        self._event_bus.subscribe(EventType.PROVIDER_FAILED, self._on_provider_failed)
        self._event_bus.subscribe(EventType.PROVIDER_RECOVERED, self._on_provider_recovered)
        self._event_bus.subscribe(EventType.RUNTIME_FAILED, self._on_runtime_failed)
        self._event_bus.subscribe(EventType.RUNTIME_STATE_CHANGED, self._on_runtime_state_changed)

    def _on_provider_failed(self, event: RuntimeEvent) -> None:
        if event.payload.get("circuit_state") != "OPEN":
            return  # a single ai_service.py attempt failure, not a tripped circuit -- not alert-worthy
        provider_name = event.payload.get("provider_name", "unknown")
        self._pending.append(RuntimeAlert(
            title="🔴 Provider DOWN (Circuit OPEN)",
            message=f"{provider_name} is now OFFLINE after repeated failures.",
        ))

    def _on_provider_recovered(self, event: RuntimeEvent) -> None:
        provider_name = event.payload.get("provider_name", "unknown")
        self._pending.append(RuntimeAlert(
            title="🟢 Provider RECOVERED",
            message=f"{provider_name} is back online.",
        ))

    def _on_runtime_failed(self, event: RuntimeEvent) -> None:
        reason = event.payload.get("reason") or "unknown reason"
        self._pending.append(RuntimeAlert(
            title="🔴 Runtime FAILED",
            message=f"AI runtime entered FAILED state: {reason}",
        ))

    def _on_runtime_state_changed(self, event: RuntimeEvent) -> None:
        reason = event.payload.get("reason") or ""
        if event.payload.get("to_state") != "DEGRADED" or not reason.startswith("cost protection: "):
            return  # not alert-worthy -- every other transition already has its own specific event above
        self._pending.append(RuntimeAlert(
            title="💰 AI Runtime DEGRADED (Cost Protection)",
            message=reason[len("cost protection: "):],
        ))

    def drain(self) -> List[RuntimeAlert]:
        """Returns and clears every alert queued since the last drain() -- never re-delivers the same alert twice."""
        pending = self._pending
        self._pending = []
        return pending


def evaluate_high_cost(provider_stats: Dict[str, ProviderStats], threshold: float) -> List[RuntimeAlert]:
    """
    Pure, no EventBus: a caller supplies real `ProviderStats` (`ai.
    audit.provider_stats.compute_provider_stats()`'s own output) and a
    configured threshold. One alert per provider whose `total_cost`
    exceeds it. Never raises; an empty dict returns an empty list.
    """
    return [
        RuntimeAlert(
            title="💰 High Cost",
            message=f"{name.title()} today's cost ${stats.total_cost:.2f} exceeds the ${threshold:.2f} threshold.",
        )
        for name, stats in sorted(provider_stats.items())
        if stats.total_cost > threshold
    ]


def evaluate_cache_disabled(cache_enabled: bool) -> Optional[RuntimeAlert]:
    """Pure, no EventBus: `cache_enabled` is supplied by the caller -- no live global cache on/off flag exists in this codebase yet (see this module's own docstring)."""
    if cache_enabled:
        return None
    return RuntimeAlert(title="⚠️ Cache Disabled", message="AI response cache is currently disabled.")


def _resolve_owner_chat_id() -> Optional[str]:
    """Never falls back to TELEGRAM_CHAT_ID (the general broadcast chat) -- an internal reliability alert with no configured Owner id goes undelivered, not to the public channel."""
    try:
        owner_id = Secrets().TELEGRAM_OWNER_ID
    except Exception as e:
        logger.warning(f"Cannot resolve owner chat id: {e}")
        return None
    return owner_id or None


def deliver_alerts(alerts: List[RuntimeAlert], notifier: Optional[Notifier] = None, chat_id: Optional[str] = None) -> int:
    """
    Owner-only delivery via the already-existing `Notifier.
    send_message()` -- no new Telegram-sending code. Returns the count
    actually delivered; `send_message()` itself never raises, so a
    per-message delivery failure just doesn't count, it never breaks
    the loop.
    """
    if not alerts:
        return 0

    notifier = notifier or Notifier()
    resolved_chat_id = chat_id if chat_id is not None else _resolve_owner_chat_id()
    if resolved_chat_id is None:
        logger.warning("deliver_alerts: no TELEGRAM_OWNER_ID configured -- alerts not delivered.")
        return 0

    delivered = 0
    for alert in alerts:
        if notifier.send_message(f"{alert.title}\n{alert.message}", chat_id=resolved_chat_id):
            delivered += 1
    return delivered
