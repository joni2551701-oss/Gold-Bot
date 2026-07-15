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

## What this does NOT do
- Does not rewrite or replace `config.py` — `Config` is untouched and
  every existing reader keeps working exactly as before.
- Does not change deployment configuration, Docker, Kubernetes, or
  CI/CD.
- Does not enable any feature — every `FeatureFlags` default is
  `False`, and nothing in this codebase reads a `FeatureFlags`
  instance yet.
- Does not change `core/pipeline.py`, `strategies/`, `signals/`,
  `ai/`, `decision/`, or `risk/` — none import from `configuration/`
  in this phase.
- Does not read a credential — `TELEGRAM_BOT_TOKEN`/
  `TWELVE_DATA_API_KEY`/etc. stay exclusively behind
  `core/secrets.py`, per the existing rule (`docs/SECURITY.md`).
  `configuration/` only ever reads `Config.APP_ENV`/`Config.TIMEZONE`,
  neither a credential.
- Does not migrate the database — no schema change, no new table.

## Dependencies
`configuration/` imports `config.Config` only (a one-directional,
additive relationship — `config.py` has zero dependency on
`configuration/`). No dependency on `core/` (beyond the root
`config.py`), `data/`, `context/`, `strategies/`, `signals/`, `ai/`,
`decision/`, `risk/`, `execution/`, `assets/`, `database/`, or
`telegram/`.

## Future extension
See `docs/CONFIGURATION_MANAGEMENT.md`'s "Future" section —
deployment configuration, cloud secrets sourcing, and
`Environment`-driven behavior differences (e.g. stricter validation in
`PRODUCTION`) are all named, explicit future steps, none implemented
in this phase.
