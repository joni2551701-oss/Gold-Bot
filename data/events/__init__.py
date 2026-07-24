"""
data.events -- GoldBot v1.1 Market Data Foundation: Event Bus (Phase 1
module 7).

Central publish/subscribe hub with typed, versioned, namespaced events,
priority + wildcard subscription, sync/async dispatch, a policy-governed
replay log, metrics, and a distributed-bridge hook. Producers connect via
their existing hooks (CandleEventHook, BootstrapEventHook) through the
producer bridges; consumers subscribe. The bus depends on no producer and
no consumer.

Not wired into core/pipeline.py; carries no signal/risk/decision logic
(Trading Safety). Never imports from telegram/, ai/, decision/, risk/,
strategies/, signals/, context/, or database/.
"""

from data.events.event_model import (
    Event, EventType, EventPriority, EVENT_SCHEMA_VERSION,
    validate_event, EventValidationError,
)
from data.events.event_bus import EventBus, SubscriptionHandle, WILDCARD
from data.events.replay_log import (
    ReplayLog, ReplayPolicy, RingBufferPolicy, TimeBasedPolicy,
)
from data.events.event_metrics import EventMetrics
from data.events.event_bridge import EventBridge, NullBridge
from data.events.producer_bridges import CandleEventBridge, BootstrapEventBridge

__all__ = [
    "Event", "EventType", "EventPriority", "EVENT_SCHEMA_VERSION",
    "validate_event", "EventValidationError",
    "EventBus", "SubscriptionHandle", "WILDCARD",
    "ReplayLog", "ReplayPolicy", "RingBufferPolicy", "TimeBasedPolicy",
    "EventMetrics",
    "EventBridge", "NullBridge",
    "CandleEventBridge", "BootstrapEventBridge",
]
