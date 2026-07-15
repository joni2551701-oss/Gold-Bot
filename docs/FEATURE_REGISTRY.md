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

## What this phase does NOT do

- Does not make any declared-only feature real or toggleable.
- Does not add a `/feature enable`/`/feature disable` command (Phase
  59.7, per the Director's own roadmap).
- Does not call `validate_feature_dependencies()` from anywhere in the
  live pipeline or Telegram routing.
