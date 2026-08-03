# IMPLEMENTATION.md -- backtesting_layer/replay_engine/data_replay

## `replay_clock.py`

ReplayClock -- virtual time for the Replay Engine (v1.1 Phase 1, module 8).

Classes: `ReplayClock`

## `replay_controller.py`

ReplayController -- drives ONE running replay session (v1.1 Phase 1,

Classes: `MemoryReplaySink`, `ReplayController`

## `replay_manager.py`

ReplayManager -- creates, tracks and ends replay sessions (v1.1 Phase 1,

Classes: `ReplayCreationError`, `ReplayManager`

## `replay_metrics.py`

ReplayMetrics -- counters for a replay session (module 8).

Classes: `ReplayMetrics`

## `replay_session.py`

ReplaySession -- an isolated, bookmarkable replay session (module 8;

Classes: `ReplaySession`

## `replay_source.py`

Replay data sources (v1.1 Phase 1, module 8).

Classes: `Frame`, `ReplayDataSource`, `SnapshotReplaySource`, `HistoricalReplaySource`, `SimulationSource`

## `replay_state.py`

Replay state machine (v1.1 Phase 1, module 8; amendment 1).

Classes: `ReplayState`, `ReplayStateError`

Top-level functions: `can_transition()`, `assert_transition()`

## `replay_validation.py`

Replay validation (v1.1 Phase 1, module 8; amendment 4).

Classes: `ReplayValidation`

Top-level functions: `validate_replay()`

## Runtime / Algorithms / Pipeline / Event Flow / Sequence / Design Decisions / Performance Notes

Not authored at rollout time -- this section requires domain understanding beyond what can be mechanically derived from code, and is left for a future Development Phase to fill in (per Director Order No. 012/013, this rollout is documentation standardization only, not new authorship of technical narrative).

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013).*
