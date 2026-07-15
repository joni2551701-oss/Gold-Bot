# Feature Registry

A single, structured catalog of every feature name GoldBot knows about
(Phase 59.6: Audit & Observability Foundation, TASK 4/5). Companion to
`docs/AUDIT_SYSTEM.md` and `docs/CONFIGURATION_MANAGEMENT.md` (the
pre-existing `configuration/feature_flags.py` contract this module
reads from, unmodified).

## `configuration/feature_registry.py`

`build_feature_registry() -> List[FeatureDescriptor]` returns one
`FeatureDescriptor(name, enabled, implemented, source, description)`
per known feature. Two kinds of entry:

| `implemented` | Meaning | Example |
|---|---|---|
| `True` | A real flag with a real backing source — `enabled` reflects that source's actual current value. | `ENABLE_MT5` (`config.Config`), `enable_ai` (`configuration.feature_flags.FeatureFlags`) |
| `False` | A name this phase's own brief lists that has no real backing anywhere in this codebase yet. `enabled` is always a fixed, safe `False`. | `ENABLE_EXECUTION`, `ENABLE_NEWS`, `ENABLE_PAPER` |

Declaring a name with `implemented=False` does **not** create a new
environment variable, dataclass field, or any other real switch — it
only gives `configuration/feature_dependency_validator.py` (and a
future Owner Dashboard) a stable name to reference before that
feature is ever actually built. This is the same "a flag existing
here does not mean the feature exists" posture
`configuration/feature_flags.py`'s own docstring already established
for `enable_ai`/`enable_crypto`/`enable_swing` in Phase A13 — this
phase just makes it structured and extends the list.

### Full current registry

| Name | Implemented | Source |
|---|---|---|
| `ENABLE_MT5` | Yes | `config.Config` |
| `ENABLE_TWELVEDATA` | Yes | `config.Config` |
| `VALIDATION_MODE` | Yes | `config.Config` |
| `enable_ai` | Yes | `configuration.feature_flags.FeatureFlags` |
| `enable_crypto` | Yes | `configuration.feature_flags.FeatureFlags` |
| `enable_swing` | Yes | `configuration.feature_flags.FeatureFlags` |
| `enable_ai_memory` | Yes | `configuration.feature_flags.FeatureFlags` |
| `enable_replay` | Yes | `configuration.feature_flags.FeatureFlags` |
| `ENABLE_NEWS`, `ENABLE_PAPER`, `ENABLE_EXECUTION`, `ENABLE_BACKTEST`, `ENABLE_ANALYTICS`, `ENABLE_OWNER`, `ENABLE_DATASET_SYNC`, `ENABLE_MARKET_PHASE`, `ENABLE_BITGET`, `ENABLE_BINANCE`, `ENABLE_FRED`, `ENABLE_RISK`, `ENABLE_DECISION` | No | `declared` |

### Relationship to `telegram/owner/feature_commands.py`'s `list_features()`

That function (Phase 59.3) already reads the same two real sources
(`Config`, `DEFAULT_FLAGS`) and renders them as ad-hoc text for a
future `/features` command — unmodified by this phase. `build_feature_registry()`
is the structured data layer underneath that same idea, extended with
the declared-only names above; a future command could be rebuilt atop
it, but that rewiring is not done here.

## `configuration/feature_dependency_validator.py`

```python
DEPENDENCY_RULES = {
    "ENABLE_EXECUTION": ("ENABLE_RISK", "ENABLE_DECISION"),
}
```

`validate_feature_dependencies(registry, rules=DEPENDENCY_RULES) ->
DependencyValidationResult(valid, violations)` checks: for every
*enabled* feature with a declared rule, are all of its required
features also enabled? A disabled feature has nothing to require and
never produces a violation.

Since `ENABLE_EXECUTION`/`ENABLE_RISK`/`ENABLE_DECISION` are all
`implemented=False` (always `enabled=False`) in today's registry, no
real configuration can ever violate this rule yet —
`format_dependency_violations()` always reports `"Valid configuration"`
against `build_feature_registry()`'s own output today. The rule exists
now so that whichever future phase makes `ENABLE_EXECUTION` (or any
other name) real and toggleable has an already-tested contract to
build against, not a decision made from scratch under pressure.

**Read-only**: this validator never enables, disables, or "fixes" a
feature — it only reports whether the current registry state is
internally consistent.

## Runtime lifecycle (Phase 59.7: Runtime Feature Toggle Center)

Phase 59.7 turns this static registry into an actual runtime toggle —
`configuration/runtime_feature_manager.py`'s `RuntimeFeatureManager`.
Every feature moves through the same lifecycle:

```
DEFAULT
  |   (build_feature_registry()'s own static value -- never toggled)
  v
RUNTIME ENABLE  (RuntimeFeatureManager.enable()/enable_feature())
  |
  v
ACTIVE   (source="runtime", enabled=True, persisted in `runtime_features`)
  |
  v
RUNTIME DISABLE  (RuntimeFeatureManager.disable()/disable_feature())
  |
  v
INACTIVE   (source="runtime", enabled=False, persisted in `runtime_features`)
```

A feature that has never been toggled stays at `DEFAULT` forever —
`RuntimeFeatureManager.get_feature_state()` reports `source="default"`
for it, `"state": "INACTIVE"` or `"ACTIVE"` matching whatever
`build_feature_registry()` itself says (e.g. `ENABLE_TWELVEDATA`
starts `ACTIVE` by default, since `config.Config.ENABLE_TWELVEDATA`
defaults `True`). Once toggled even once, a feature is permanently
`source="runtime"` from then on (moving between `ACTIVE`/`INACTIVE` on
further toggles, never back to `"default"`) — `RuntimeFeatureRepository`
never deletes a row.

Every enable/disable is:
1. **Validated** (dry run) — `configuration/feature_dependency_validator.py`'s
   `DEPENDENCY_RULES` checked against the hypothetical post-toggle
   state. An enable is rejected if a required dependency isn't
   enabled; a disable is rejected if an already-enabled feature still
   depends on it (this task's own worked example: `Cannot disable
   ENABLE_RISK. Dependent features active: ENABLE_EXECUTION`).
2. **Persisted** — `database/runtime_feature_repository.py`'s
   `runtime_features` table, surviving a restart.
3. **Audited** — `database/audit_log_repository.py`, action
   `FEATURE_ENABLED`/`FEATURE_DISABLED` (`TOGGLE_FEATURE`/`REJECTED`
   for a blocked attempt).
4. **Snapshotted** — `database/config_snapshot_repository.py`, one
   snapshot of the full runtime feature state after every successful
   change, for a future rollback.

A rejected toggle does none of the above except step 3 (a `REJECTED`
audit entry is still written, so the attempt itself is never silently
lost) — the underlying state is left completely unchanged.

See `docs/RUNTIME_FEATURE_CONTROL.md` for the full module-by-module
contract, and `telegram/owner/README.md`/`docs/OWNER_PERMISSIONS.md`
for why no Telegram command calls any of this yet.

## What this phase does NOT do

- Does not make signal generation, decision-making, risk, or execution
  actually read a runtime feature's state — `core/pipeline.py`,
  `decision/`, `risk/`, `execution/`, `strategies/`, `signals/`,
  `context/`, and `ai/` are all unmodified and import nothing from
  `configuration/`.
- Does not register a `/feature enable`/`/feature disable` Telegram
  command (Phase 59.8, per the Director's own roadmap) —
  `configuration/runtime_api.py` has no `telegram/` dependency.
- Does not add cascading auto-disable — disabling a feature whose
  dependent is still active is rejected outright, not applied with a
  side effect on the dependent.
