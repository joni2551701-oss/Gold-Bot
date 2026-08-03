"""backtesting_layer.replay_engine.data_replay — pre-freeze data/replay subsystem.

A second, independent replay implementation that arrived from the pre-freeze
`data/replay/` package. It is datetime-driven, whereas the Backtesting
Layer's own ReplayClock (one level up) is an integer-position play/pause
controller — two different designs with colliding names.

Kept whole and separated rather than merged (WAR-009); reconciling the two is
a Phase E duplicate-removal task, recorded in MIGRATION_TRACKER.
"""
