# backtesting_layer / replay_engine / data_replay

**Module**

## Purpose

backtesting_layer.replay_engine.data_replay — pre-freeze data/replay subsystem.

A second, independent replay implementation that arrived from the pre-freeze
`data/replay/` package. It is datetime-driven, whereas the Backtesting
Layer's own ReplayClock (one level up) is an integer-position play/pause
controller — two different designs with colliding names.

Kept whole and separated rather than merged (WAR-009); reconciling the two is
a Phase E duplicate-removal task, recorded in MIGRATION_TRACKER.

## Files

- `__init__.py` -- backtesting_layer.replay_engine.data_replay — pre-freeze data/replay subsystem.
- `replay_clock.py` -- ReplayClock -- virtual time for the Replay Engine (v1.1 Phase 1, module 8).
- `replay_controller.py` -- ReplayController -- drives ONE running replay session (v1.1 Phase 1,
- `replay_manager.py` -- ReplayManager -- creates, tracks and ends replay sessions (v1.1 Phase 1,
- `replay_metrics.py` -- ReplayMetrics -- counters for a replay session (module 8).
- `replay_session.py` -- ReplaySession -- an isolated, bookmarkable replay session (module 8;
- `replay_source.py` -- Replay data sources (v1.1 Phase 1, module 8).
- `replay_state.py` -- Replay state machine (v1.1 Phase 1, module 8; amendment 1).
- `replay_validation.py` -- Replay validation (v1.1 Phase 1, module 8; amendment 4).

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `replay_clock.py`: class `ReplayClock`
- `replay_controller.py`: class `MemoryReplaySink`
- `replay_controller.py`: class `ReplayController`
- `replay_manager.py`: class `ReplayCreationError`
- `replay_manager.py`: class `ReplayManager`
- `replay_metrics.py`: class `ReplayMetrics`
- `replay_session.py`: class `ReplaySession`
- `replay_source.py`: class `Frame`
- `replay_source.py`: class `ReplayDataSource`
- `replay_source.py`: class `SnapshotReplaySource`
- `replay_source.py`: class `HistoricalReplaySource`
- `replay_source.py`: class `SimulationSource`
- `replay_state.py`: class `ReplayState`
- `replay_state.py`: class `ReplayStateError`
- `replay_state.py`: function `can_transition()`
- `replay_state.py`: function `assert_transition()`
- `replay_validation.py`: class `ReplayValidation`
- `replay_validation.py`: function `validate_replay()`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
