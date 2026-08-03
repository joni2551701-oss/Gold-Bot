# IMPLEMENTATION.md -- data_layer/event_system

## `event_bridge.py`

EventBridge -- interface for forwarding bus events to an external/remote

Classes: `EventBridge`, `NullBridge`

## `event_metrics.py`

EventMetrics -- counters for the Event Bus (v1.1 Phase 1, module 7).

Classes: `EventMetrics`

## `event_model.py`

Event model for the GoldBot Event Bus (v1.1 Phase 1, module 7).

Classes: `EventPriority`, `EventType`, `EventValidationError`, `Event`

Top-level functions: `validate_event()`

## `producer_bridges.py`

Producer bridges (v1.1 Phase 1, module 7).

Classes: `CandleEventBridge`, `BootstrapEventBridge`

## `replay_log.py`

Replay log for the Event Bus (v1.1 Phase 1, module 7).

Classes: `ReplayPolicy`, `RingBufferPolicy`, `TimeBasedPolicy`, `ReplayLog`

## Runtime / Algorithms / Pipeline / Event Flow / Sequence / Design Decisions / Performance Notes

Not authored at rollout time -- this section requires domain understanding beyond what can be mechanically derived from code, and is left for a future Development Phase to fill in (per Director Order No. 012/013, this rollout is documentation standardization only, not new authorship of technical narrative).

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013).*
