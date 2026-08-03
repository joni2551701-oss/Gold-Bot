# Runtime Feature Control

The full module-by-module contract for Phase 59.7 (Runtime Feature
Toggle Center). Companion to `docs/FEATURE_REGISTRY.md` (the static
registry and dependency rules this phase turns into a runtime toggle),
`docs/AUDIT_SYSTEM.md` (the audit log this phase writes to), and
`docs/CONFIG_SNAPSHOT.md` (the snapshot mechanism this phase writes
to).

## Scope

A control layer only. Per the Director's own brief: *"Bu phase hali
pipeline'ni o'zgartirmaydi. Faqat Runtime Controller quriladi."* (This
phase does not change the pipeline yet — only the Runtime Controller
is built.) Nothing here changes `core/pipeline.py`, `decision/`,
`risk/`, `execution/`, `strategies/`, `signals/`, `context/`, `ai/`,
any Telegram handler, `platform_layer/telegram/command_router.py`, or any existing
Owner command module. No signal is blocked, no trade is closed, no
order is stopped, no Telegram command is registered — that is
explicitly Phase 59.9 (Emergency Layer)'s job, not this one's.

## The four new modules

### `configuration/runtime_state.py`

`FeatureRuntimeState(name, enabled, last_changed, changed_by, reason,
source, created_at)` — one feature's current runtime value.
`source` is `"default"` (never toggled, value comes only from
`configuration.feature_registry.build_feature_registry()`) or
`"runtime"` (toggled at least once, persisted). `RuntimeStateCache` is
a plain in-memory `{name: FeatureRuntimeState}` holder — no database
access, no validation, no audit logging; those are
`runtime_feature_manager.py`'s job.

### `database_layer/journal_repository/runtime_feature_repository.py` / `runtime_feature_models.py`

`RuntimeFeatureRecord(feature, enabled, created_at, updated_at,
updated_by, reason)` persisted in the `runtime_features` table — one
row per feature name, `feature UNIQUE NOT NULL`.
`RuntimeFeatureRepository.set_feature()` upserts: `UPDATE` if the row
exists (never touches `created_at`), `INSERT` otherwise (stamps
`created_at` for the only time in that row's life). Schema is
additive-only (`CREATE TABLE IF NOT EXISTS`) — no existing table is
touched, no migration of pre-existing data.

### `configuration/runtime_feature_manager.py`

`RuntimeFeatureManager` — the actual controller, composing every piece
above plus the Phase 59.6 foundation:

| Method | Behavior |
|---|---|
| `load()` / `reload()` | Clears the in-memory cache, seeds it from the static registry (`source="default"`), then overlays every persisted `runtime_features` row (`source="runtime"`). Called automatically from `__init__` — a fresh manager is always ready to query immediately. |
| `status(name)` / `get_feature_state(name)` | The cached `FeatureRuntimeState`, or (for `get_feature_state()`) the plain-dict view `{"feature", "state": "ACTIVE"/"INACTIVE", "source", "updated_at"}`. `None` for a name never seen. |
| `list_features()` | Every feature currently known (registry-declared or persisted-only). |
| `enable(name)` / `disable(name)` / `toggle(name)` (+ `enable_feature()`/`disable_feature()` aliases) | Validates (dry run), persists, audits, and snapshots — see below. Returns a `ToggleResult(success, feature, enabled, reason)`. |
| `validate_dependencies(name=None, new_enabled=None)` | With `name`: checks the hypothetical post-toggle state. With no arguments: checks the manager's actual current state as-is. |

**Every successful toggle**, in order:
1. **Dry run** — builds a hypothetical `{name: enabled}` snapshot (the
   current cache with the one change applied) and runs
   `configuration.feature_dependency_validator.validate_feature_dependencies()`
   against it. If invalid, the toggle stops here — nothing below runs,
   except a `REJECTED` audit entry (step 3, adapted).
2. **Persist** — `RuntimeFeatureRepository.set_feature()`.
3. **Audit** — `AuditLogRepository.log_action(actor, action, target,
   result, details)`. `action` is `FEATURE_ENABLED`/`FEATURE_DISABLED`
   on success; a rejected attempt logs `action="TOGGLE_FEATURE"`,
   `result="REJECTED"`, `details=<the rejection reason>`.
4. **Snapshot** — `ConfigSnapshotRepository.save_snapshot()` of the
   full current runtime state (every feature's current `enabled`
   value), via `database_layer.journal_repository.config_snapshot_models.create_config_snapshot()`
   (Phase 59.6, reused unmodified).

### Dependency safety — the two rejection directions

`DEPENDENCY_RULES` (`configuration/feature_dependency_validator.py`,
Phase 59.6) is symmetric: a toggle is rejected whenever it would leave
the *overall* state invalid, whichever direction caused it.

- **Enabling** a feature whose dependency isn't enabled:
  `format_dependency_violations()`'s existing phrasing — *"Invalid
  configuration: ENABLE_EXECUTION requires ENABLE_RISK"*.
- **Disabling** a feature that an already-enabled dependent still
  needs: a friendlier, this-task's-own-worked-example phrasing —
  *"Cannot disable ENABLE_RISK. Dependent features active:
  ENABLE_EXECUTION"*.

Neither direction cascades — a rejected disable never auto-disables
the dependent, and a rejected enable never auto-enables the missing
dependency. The toggle is simply refused; the caller decides what to
do next (e.g. disable the dependent first).

### `configuration/runtime_api.py`

The service-layer functions a future Phase 59.8 Owner Dashboard would
call: `enable_feature(name, actor, reason)`, `disable_feature(name,
actor, reason)`, `feature_status(name)`, `list_runtime_features()`.
Each returns a `RuntimeApiResult(success, message, data)` and never
raises. No `telegram/` import anywhere in this module — the existing
one-directional `telegram/` → `configuration/` dependency stays intact
(never reversed). No Telegram command is registered against these
functions in this phase.

## Worked example

```python
from configuration.runtime_feature_manager import RuntimeFeatureManager

manager = RuntimeFeatureManager()

manager.enable("ENABLE_BACKTEST", changed_by="owner")
# -> ToggleResult(success=False, reason="Invalid configuration:\n"
#                  "  ENABLE_BACKTEST requires ENABLE_DATASET_SYNC\n"
#                  "  ENABLE_BACKTEST requires ENABLE_ANALYTICS")

manager.enable("ENABLE_DATASET_SYNC")
manager.enable("ENABLE_ANALYTICS")
manager.enable("ENABLE_BACKTEST", changed_by="owner")
# -> ToggleResult(success=True, feature="ENABLE_BACKTEST", enabled=True)

manager.disable("ENABLE_DATASET_SYNC")
# -> ToggleResult(success=False,
#                  reason="Cannot disable ENABLE_DATASET_SYNC. Dependent features active: ENABLE_BACKTEST")

manager.get_feature_state("ENABLE_BACKTEST")
# -> {"feature": "ENABLE_BACKTEST", "state": "ACTIVE", "source": "runtime", "updated_at": "..."}

second_manager = RuntimeFeatureManager()  # a fresh process/restart
second_manager.get_feature_state("ENABLE_BACKTEST")["state"]
# -> "ACTIVE" -- survived the restart
```

(Phase 60.9: re-anchored from the original `ENABLE_EXECUTION`/
`ENABLE_RISK`/`ENABLE_DECISION` worked example — see the Phase 60.9
section below for why.)

## What this phase does NOT do

- Does not read a runtime feature's state from `core/pipeline.py`,
  `decision/`, `risk/`, `execution/`, `strategies/`, `signals/`,
  `context/`, or `ai/` — none of them import `configuration/` at all.
  (`core/pipeline.py` briefly did, via `PipelineGuard`, during Phase
  60.8; Phase 60.9 removed that dependency entirely — see below.)
- Does not block a signal, close a trade, or stop an order — that is
  `EmergencyManager`'s job (Phase 59.9, wired into the pipeline in
  Phase 60.8).
- Does not register any Telegram command — that is Phase 59.8's job.
- Does not cascade a toggle onto a dependency or dependent — every
  rejection leaves the state exactly as it was.
- Does not add a rollback/apply function for a saved config snapshot —
  still capture-and-read only (Phase 59.6's own boundary, unchanged).

## Phase 60.9: Runtime Registry Separation — RuntimeFeatureManager fully removed from the pipeline

Phase 60.8 briefly made `core_layer/pipeline/pipeline_guard.py`'s
`PipelineGuard` the first real caller of `RuntimeFeatureManager.status()`,
gating three pipeline stages by three new registry entries
(`ENABLE_SIGNALS`/`ENABLE_AI`/`ENABLE_DATABASE`) and leaving a fourth
(`ENABLE_EXECUTION`) unpromoted after it collided with
`DEPENDENCY_RULES` and broke 26 tests. Phase 60.9 resolved this at the
root: **all four names were removed from the registry**, and
`PipelineGuard` no longer imports or constructs a
`RuntimeFeatureManager` at all — every one of its four hooks
(`before_signal`/`before_ai`/`before_execution`/`before_database`) now
reads exclusively from `EmergencyManager`. `RuntimeFeatureManager` is,
once again, read only by its own tests, `platform_layer/telegram/owner/*.py`, and
`configuration/runtime_api.py` — never by `core/pipeline.py`. See
`docs/FEATURE_REGISTRY_SEPARATION.md` for the full audit and
`docs/PIPELINE_GUARD.md` for the current, EmergencyManager-only
pipeline-stage mapping.

## Phase 60.8: Safe Integration Layer — first real reader (superseded by Phase 60.9 above)

`core_layer/pipeline/pipeline_guard.py`'s `PipelineGuard` was the first real
caller of `RuntimeFeatureManager.status()` (read-only, never
`.enable()`/`.disable()`/`.toggle()`) — previously zero callers
existed outside this module's own tests and `platform_layer/telegram/owner/*.py`.
Three new, real, `config.Config`-backed registry entries were added
for it: `ENABLE_SIGNALS`, `ENABLE_AI`, `ENABLE_DATABASE` (all default
`True`). This entire arrangement was removed in Phase 60.9 above — kept
here for historical record only.

**`ENABLE_EXECUTION` was NOT promoted**, despite being the fourth name
the Director's brief explicitly requested. Promoting it (implemented=
True, enabled=True) was tried and reverted: this document's own
former worked example already showed why —
`configuration/feature_dependency_validator.py`'s `DEPENDENCY_RULES`
declares `ENABLE_EXECUTION` requires `ENABLE_RISK` and
`ENABLE_DECISION`, both still declared-only (always `False`). With
`ENABLE_EXECUTION` real and `True`, `validate_feature_dependencies()`
rejects *every* toggle to *any* feature (the dry-run's hypothetical
snapshot always carries `ENABLE_EXECUTION`'s permanently-unmet
dependency forward) — 26 tests failed, including 18 of this module's
own `RuntimeFeatureManager` tests. `PipelineGuard.before_execution()`
reads `EmergencyManager` only until the Director resolves this. Full
account in `docs/PIPELINE_GUARD.md`'s "Disclosed Findings" (finding
3).
