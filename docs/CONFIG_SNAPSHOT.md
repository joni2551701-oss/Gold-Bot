# Configuration Snapshot

Point-in-time capture of a feature registry state, for a future
rollback (Phase 59.6: Audit & Observability Foundation, TASK 6).
Companion to `docs/FEATURE_REGISTRY.md`.

## `database/config_snapshot_repository.py`

```python
from configuration.feature_registry import build_feature_registry
from database.config_snapshot_models import create_config_snapshot
from database.config_snapshot_repository import ConfigSnapshotRepository

snapshot = create_config_snapshot(
    build_feature_registry(), taken_by="owner", reason="before feature toggle",
)
ConfigSnapshotRepository().save_snapshot(snapshot)
```

`ConfigSnapshotRecord(snapshot_id, feature_state, taken_at, taken_by,
reason)` — `feature_state` is a JSON object string of
`{feature_name: enabled}`, parsed back via
`ConfigSnapshotRecord.feature_state_dict()`. Only the enabled/disabled
value per name is captured — `implemented`/`source`/`description` are
static facts about the registry itself, not something that changes
between snapshots.

Real, persisted, append-only table (`config_snapshots`) — same
"no update/delete, a fixed point-in-time record" posture as
`database/audit_log_repository.py`. `get_latest()`/`get_all(limit=50)`
read snapshots back, newest first.

## What this phase does NOT do

**No apply/restore function exists.** This phase captures and reads
snapshots only — actually rolling a live configuration back to a
saved snapshot is a future, separately-approved step. It would first
need to decide how a `implemented=False` declared-only feature (see
`docs/FEATURE_REGISTRY.md`) becomes toggleable at all, which this
phase does not attempt. **No owner command calls
`create_config_snapshot()`/`save_snapshot()` automatically yet** —
"Har owner o'zgartirishidan oldin config_snapshot saqlanadi" (a
snapshot is saved before every owner change) describes a future
wiring step, once real owner mutations exist to snapshot before.
