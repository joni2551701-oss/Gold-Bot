# MODULE_MAP.md -- backtesting_layer/replay_engine/data_replay

| File | Role |
|---|---|
| `__init__.py` | backtesting_layer.replay_engine.data_replay — pre-freeze data/replay subsystem. |
| `replay_clock.py` | ReplayClock -- virtual time for the Replay Engine (v1.1 Phase 1, module 8). |
| `replay_controller.py` | ReplayController -- drives ONE running replay session (v1.1 Phase 1, |
| `replay_manager.py` | ReplayManager -- creates, tracks and ends replay sessions (v1.1 Phase 1, |
| `replay_metrics.py` | ReplayMetrics -- counters for a replay session (module 8). |
| `replay_session.py` | ReplaySession -- an isolated, bookmarkable replay session (module 8; |
| `replay_source.py` | Replay data sources (v1.1 Phase 1, module 8). |
| `replay_state.py` | Replay state machine (v1.1 Phase 1, module 8; amendment 1). |
| `replay_validation.py` | Replay validation (v1.1 Phase 1, module 8; amendment 4). |

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Table is mechanically generated from each file's own first docstring line.*
