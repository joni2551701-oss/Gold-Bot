# signal_layer / signal_engine / lifecycle

**Module**

## Purpose

signal_layer/signal_engine/lifecycle/ — canonical signal build/publish lifecycle (STEP-08).

See signal_layer/signal_engine/lifecycle/state.py for the CanonicalSignalStatus state machine
and how it differs from trade_monitoring_layer/paper_trading/signal_state.py and
execution_layer/execution_monitor/signal_lifecycle.py.

## Files

- `__init__.py` -- signal_layer/signal_engine/lifecycle/ — canonical signal build/publish lifecycle (STEP-08).
- `state.py` -- Signals — Canonical Signal build/publish lifecycle (TASK-CORE-008 / STEP-08).

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `state.py`: class `CanonicalSignalStatus`
- `state.py`: class `SignalStatusTransitionResult`
- `state.py`: function `transition()`
- `state.py`: function `is_terminal()`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
