# Configuration & Feature Flags Foundation (Phase A13)

## Purpose

Builds a standard configuration and feature-flag layer —
`Environment`, `ApplicationSettings`, `FeatureFlags` — entirely
additive to `config.py`, which stays exactly as it is today. **This
is a foundation for future config growth, not a rewrite.** No
deployment configuration, no Docker/Kubernetes/CI/CD, no new feature
actually enabled, no AI-flag logic, no strategy-logic change, and no
database migration are introduced in this phase.

This phase exists because `config.py` today is one flat class with a
handful of attributes (`TIMEZONE`, `APP_ENV`, `DEBUG`, `BASE_DIR`,
`DB_PATH`, `TIMEFRAME_HISTORY`) — adequate for a single-environment,
single-asset bot, but GoldBot's own roadmap (development/testing/
production separation, AI modules, Multi-Asset, a Mini App) will
outgrow that shape. `configuration/` is the standard place that
growth lands, without disturbing what already works.

## Configuration layer nima?

Three pieces, each independently usable:

- **`Environment`** (`configuration/environment.py`) — an enum
  classifying which environment the app is running in
  (`DEVELOPMENT`/`TESTING`/`PRODUCTION`), plus a safe adapter
  (`resolve_environment()`) from a raw string.
- **`ApplicationSettings`** (`configuration/settings.py`) — a
  standard, typed settings model that could, in the future, replace
  ad-hoc `config.Config.*` attribute reads across the codebase. A
  minimal adapter (`build_settings_from_config()`) builds one from the
  real, already-set `config.Config` values today.
- **`FeatureFlags`** (`configuration/feature_flags.py`) — a standard
  model for future feature gating, every flag defaulting to `False`.

None of the three is read by `core/pipeline.py`, `strategies/`,
`signals/`, `ai/`, `decision/`, or `risk/` in this phase — see
"Pipeline integration" below.

## Pre-implementation audit

Before writing any code, `config.py`, `main.py`, `.env.example`/
`.env.production`, `requirements.txt`, and `tests/` were searched for
every existing config variable, environment usage, hardcoded value,
and any feature-flag-shaped code, to reuse rather than invent:

| Found | Location | Reused as |
|---|---|---|
| `Config.APP_ENV = os.getenv("APP_ENV", "development")` | `config.py` | `Environment`'s three values are lowercased to match this exact convention; `build_settings_from_config()` reads `Config.APP_ENV` directly. |
| `Config.TIMEZONE = timezone.utc` | `config.py` | `ApplicationSettings.timezone` is `str(Config.TIMEZONE)` (`"UTC"`), never a separately hardcoded literal. |
| `symbol="XAUUSD", interval="M15"` | `main.py`'s `TradingPipeline(...)` | `ApplicationSettings.symbol`/`.default_timeframe` — `config.py` has no `SYMBOL`/`DEFAULT_TIMEFRAME` constant of its own, so these are the same literals `main.py` (and Phase A11/A12's `strategies/lifecycle/`/`assets/`) already use. |
| `APP_ENV=development`, `DEBUG=False` in `.env.example`/`.env.production` | root | Confirms `.env.example`'s own comment: "Not currently read by any code path beyond `config.py` itself" — `configuration/` is the first consumer of `Config.APP_ENV` beyond `config.py`'s own definition. |
| `Config.DB_PATH` used across `database_layer/database_manager/database.py`, `data_layer/market_memory/data_cache.py`, `scripts/health_check.py`, and most of `tests/` | multiple | Left untouched — `configuration/` never reads or writes `Config.DB_PATH`. |
| `core/secrets.py`'s `Secrets` class | `core/secrets.py` | Confirms the existing rule (`docs/SECURITY.md`) that credentials are read exclusively through `core/secrets.py` — `configuration/` never reads `TELEGRAM_BOT_TOKEN`/`TWELVE_DATA_API_KEY`/etc.; `Environment`/`ApplicationSettings` only ever touch `Config.APP_ENV`/`Config.TIMEZONE`, neither a credential. |

No existing feature-flag system, `Environment`-equivalent enum, or
settings-model pattern was found anywhere (`platform_layer/telegram/handlers.py`'s
`is_enabled()` hit during the search is `NotificationService`'s
per-user notification toggle — a database-driven, unrelated concern,
not an app-wide feature flag).

## Environment

```python
class Environment(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"
```

Three values only. `resolve_environment(raw, default=Environment.DEVELOPMENT)`
is the safe adapter: a missing or unrecognized value degrades to
`default` rather than raising — the same fail-safe posture every
other Phase A foundation module uses for a missing/invalid input
(`HTFBias.UNKNOWN`, `MarketRegime.UNKNOWN`, etc.). `Environment(raw)`
itself (the plain enum constructor) is untouched and still raises
`ValueError` for a caller that wants that behavior instead.

## Feature Flags

```python
@dataclass(frozen=True)
class FeatureFlags:
    enable_ai: bool = False
    enable_crypto: bool = False
    enable_swing: bool = False
    enable_ai_memory: bool = False
    enable_replay: bool = False
```

Every flag defaults to `False` — the roadmap's explicit rule ("Default
holat xavfsiz bo'lishi kerak"). A flag existing here does not mean
its feature exists or is safe to use:

| Flag | Status |
|---|---|
| `enable_ai` | OFF — `ai/ai_analyzer.py` is still a heuristic stub regardless of this flag's value. |
| `enable_crypto` | OFF — no Crypto data provider or `AssetType.CRYPTO` profile (`assets/`, Phase A12) exists. |
| `enable_swing` | OFF — no swing-timeframe strategy exists. |
| `enable_ai_memory` | OFF — reserved for a future AI Assistant memory feature. |
| `enable_replay` | OFF — no backtest/replay harness exists. |

`FeatureFlags` is frozen, like every other Phase A model — "toggling"
a flag means constructing a new `FeatureFlags` (e.g. via
`dataclasses.replace()`), not mutating one in place. Nothing in this
codebase reads a `FeatureFlags` instance yet.

## Existing config compatibility

`config.py` is **not** rewritten, and its `Config` class is untouched
— every existing reader (`database_layer/database_manager/database.py`'s `Config.DB_PATH`,
`main.py`'s `Config.TIMEFRAME_HISTORY["M15"]`, `tests/conftest.py`'s
`Config.DB_PATH` test-isolation override, etc.) keeps working exactly
as before. The new layer sits *above* it:

```
config.py
      |
      v
configuration layer (Environment / ApplicationSettings / FeatureFlags)
```

`configuration/settings.py`'s `build_settings_from_config()` is the
one, minimal adapter — it reads `Config.APP_ENV`/`Config.TIMEZONE`
and produces an `ApplicationSettings`; nothing in `configuration/`
writes to `Config`, and `config.py` itself has zero dependency on
`configuration/` (a one-directional relationship, never a circular
import).

## Pipeline integration

None. `core/pipeline.py` does not construct, read, or import
`Environment`/`ApplicationSettings`/`FeatureFlags` anywhere in this
phase — Configuration & Feature Flags do not change the pipeline
flow, do not affect `DecisionEngine`, and do not enable or disable
any strategy. If a future phase wires this in, the rule is:
availability only — reading `ApplicationSettings`/`FeatureFlags` to
know what's configured, never a hidden behavior change to signal
generation, decision, risk, or execution triggered by a flag flip
without an explicit, separately-approved phase.

## Future

- **Deployment configuration**: Docker/Kubernetes/CI/CD environment
  wiring — named as a natural future consumer of `Environment`, not
  implemented in this phase.
- **Cloud**: environment-specific settings sourced from a cloud
  secrets manager instead of `.env` files — not implemented.
- **Multi environment**: `TESTING`/`PRODUCTION` distinctions actually
  changing behavior (e.g. stricter validation in `PRODUCTION`) — the
  enum exists, but no code branches on `Environment` yet.

None of the above is implemented in this phase — this section exists
to document the shape a future, separately-approved phase would fill
in, not to promise a timeline.
