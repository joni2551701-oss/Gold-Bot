# configuration/

## Purpose
Configuration & Feature Flags foundation (Phase A13) — a standard
layer (`Environment`, `ApplicationSettings`, `FeatureFlags`) additive
to `config.py`, which stays exactly as it is today. Exists because
GoldBot's roadmap (development/testing/production separation, AI
modules, Multi-Asset, a Mini App) will outgrow `config.py`'s current
single flat class. See `docs/CONFIGURATION_MANAGEMENT.md` for the
full contract.

## Usage
```python
from configuration.settings import build_settings_from_config

settings = build_settings_from_config()
# settings.environment -> Environment.DEVELOPMENT (from Config.APP_ENV)
# settings.symbol == "XAUUSD", settings.default_timeframe == "M15"
# settings.timezone == "UTC" (str(Config.TIMEZONE))

from configuration.feature_flags import FeatureFlags
flags = FeatureFlags()  # every flag False -- the safe default
```

## Module layout
- `environment.py` — `Environment` (`DEVELOPMENT`/`TESTING`/
  `PRODUCTION`, no other value) and `resolve_environment()`, a safe
  adapter from a raw string that never raises.
- `settings.py` — `ApplicationSettings` (`environment`, `symbol`,
  `default_timeframe`, `timezone`) and `build_settings_from_config()`,
  the minimal adapter from the existing `config.Config`.
- `feature_flags.py` — `FeatureFlags` (`enable_ai`, `enable_crypto`,
  `enable_swing`, `enable_ai_memory`, `enable_replay`, every default
  `False`) and `DEFAULT_FLAGS`.
- `feature_registry.py` (Phase 59.6, TASK 4) — `FeatureDescriptor` +
  `build_feature_registry()`, a structured catalog combining every
  real flag above with `config.Config`'s `ENABLE_MT5`/
  `ENABLE_TWELVEDATA`/`VALIDATION_MODE`, plus declared-only names
  (`ENABLE_EXECUTION`, `ENABLE_NEWS`, etc.) that have no real backing
  yet — always `enabled=False`, `implemented=False`. Not runtime: does
  not gate anything. See `docs/FEATURE_REGISTRY.md`.
- `feature_dependency_validator.py` (Phase 59.6, TASK 5) —
  `DEPENDENCY_RULES` + `validate_feature_dependencies()`, checking a
  feature registry for internally-consistent enable/disable
  combinations (e.g. `ENABLE_EXECUTION` requires `ENABLE_RISK`/
  `ENABLE_DECISION`). Read-only — never corrects a feature. See
  `docs/FEATURE_REGISTRY.md`.
- `runtime_state.py` (Phase 59.7, TASK 2) — `FeatureRuntimeState`
  (`name`, `enabled`, `source` — `"default"` or `"runtime"` —,
  `created_at`, `last_changed`, `changed_by`, `reason`) +
  `RuntimeStateCache`, a plain in-memory holder with no I/O of its
  own. See `docs/RUNTIME_FEATURE_CONTROL.md`.
- `runtime_feature_manager.py` (Phase 59.7, TASK 1/4/5/6/7/8) —
  `RuntimeFeatureManager`: `enable()`/`disable()`/`toggle()` (plus
  `enable_feature()`/`disable_feature()` aliases), `status()`/
  `get_feature_state()`, `list_features()`, `load()`/`reload()`,
  `validate_dependencies()`. Turns the static registry above into an
  actual runtime toggle — validated (dry run against
  `feature_dependency_validator.py`), persisted
  (`database_layer/journal_repository/runtime_feature_repository.py`), audited
  (`database_layer/audit_log/audit_log_repository.py`), and snapshotted
  (`database_layer/journal_repository/config_snapshot_repository.py`) on every successful
  change. Never called from `core/pipeline.py` or any Telegram
  handler in this phase. See `docs/RUNTIME_FEATURE_CONTROL.md`.
- `runtime_api.py` (Phase 59.7, TASK 9) — `enable_feature()`/
  `disable_feature()`/`feature_status()`/`list_runtime_features()`,
  the service-layer functions a future Owner Dashboard (Phase 59.8)
  would call. No `telegram/` import, no command registered yet.

## What this does NOT do
- Does not rewrite or replace `config.py` — `Config` is untouched and
  every existing reader keeps working exactly as before.
- Does not change deployment configuration, Docker, Kubernetes, or
  CI/CD.
- Does not change `core/pipeline.py`, `strategies/`, `signals/`,
  `ai/`, `decision/`, `risk/`, `execution/`, `context/`, or any
  Telegram handler/`telegram/command_router.py` — none import from
  `configuration/` in any phase to date, and `runtime_feature_manager.py`
  is never constructed from any of them. Toggling a feature at runtime
  (Phase 59.7) changes only what `RuntimeFeatureManager`/`runtime_api.py`
  themselves report — no pipeline stage, decision, or execution path
  reads a runtime feature's state.
- Does not read a credential — `TELEGRAM_BOT_TOKEN`/
  `TWELVE_DATA_API_KEY`/etc. stay exclusively behind
  `core_layer/secrets/secrets.py`, per the existing rule (`docs/SECURITY.md`).
  `configuration/` only ever reads `Config.APP_ENV`/`Config.TIMEZONE`,
  neither a credential.
- Does not break `config.Config.ENABLE_MT5`/`ENABLE_TWELVEDATA`/etc.
  themselves — those remain os.getenv-read, process-start constants;
  toggling their same-named entry in the runtime registry changes only
  the in-memory/persisted runtime view, never `Config`'s own attribute.

## Dependencies
`environment.py`/`settings.py`/`feature_flags.py`/`feature_registry.py`/
`feature_dependency_validator.py` import `config.Config` only — no
dependency on `database/`, `telegram/`, or any pipeline layer.
`runtime_state.py` imports nothing beyond the standard library.
`runtime_feature_manager.py` (Phase 59.7) is the first module in this
package with a `database/` dependency — imports
`database_layer.journal_repository.runtime_feature_repository`, `database_layer.audit_log.audit_log_repository`,
`database_layer.journal_repository.config_snapshot_repository`/`config_snapshot_models` — a
new, one-directional `configuration/` → `database/` dependency, never
reversed (no `database/*_repository.py` imports `configuration/`).
`runtime_api.py` imports only `configuration.runtime_feature_manager`
— no `telegram/` dependency, keeping the existing one-directional
`telegram/` → `configuration/` relationship intact. No module in this
package imports `core/pipeline.py`, `strategies/`, `signals/`, `ai/`,
`decision/`, `risk/`, `execution/`, `context/`, or `assets/`.

## Future extension
See `docs/CONFIGURATION_MANAGEMENT.md`'s "Future" section —
deployment configuration, cloud secrets sourcing, and
`Environment`-driven behavior differences (e.g. stricter validation in
`PRODUCTION`) are all named, explicit future steps, none implemented
in this phase.
