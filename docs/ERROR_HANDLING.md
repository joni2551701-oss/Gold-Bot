# Error Classification Foundation (Phase A18)

## Purpose

Builds one standard error hierarchy — `GoldBotError` and nine
category subclasses — plus a standard error-code registry, so any
error raised anywhere in GoldBot is understood, logged, and (in the
future) monitored/recovered from the same way. **This is a
foundation, not a retrofit.** No existing raise site is migrated to
the new hierarchy in this phase — `core/secrets.py`'s existing bare
`ValueError`, `assets.asset_registry.DuplicateAssetSymbolError`, and
`strategies.lifecycle.strategy_registry.DuplicateStrategyIdError` are
all untouched. This phase implements the hierarchy
`contracts/error_contract.md` (Phase A17) specified but explicitly
deferred as a future phase's job — this is that phase.

## Error flow

```
Module
  |
  v
Raise GoldBotError (a specific subclass)
  |
  v
Logger (logger.error(error.to_dict()))
  |
  v
Monitoring   -- not implemented in this phase
  |
  v
Recovery     -- not implemented in this phase
```

Only the first two stages exist today: a module raises a specific
`GoldBotError` subclass, and a caller logs it via
`logger.error(error.to_dict())`. Monitoring and Recovery are named,
not-yet-approved future stages — this phase adds no monitoring
dashboard, no alerting, and no automatic recovery logic.

## Error categories

| Category | Purpose | Exception class |
|---|---|---|
| Configuration | Bad/missing settings | `ConfigurationError` |
| Data | Market data | `DataError` |
| API | External service | `ExternalAPIError` |
| Database | Storage | `DatabaseError` |
| Validation | Input | `ValidationError` |
| Permission | Access | `PermissionError` |
| Strategy | Strategy failure | `StrategyError` |
| Decision | Decision failure | `DecisionError` |
| Execution | Order layer | `ExecutionError` |

## Hierarchy

```
GoldBotError
 │
 ├── ConfigurationError
 │
 ├── ValidationError
 │
 ├── DataError
 │
 ├── ExternalAPIError
 │
 ├── DatabaseError
 │
 ├── PermissionError
 │
 ├── StrategyError
 │
 ├── DecisionError
 │
 └── ExecutionError
```

`core/errors/base.py`'s `GoldBotError` carries the standard payload
every subclass inherits: `code`, `message`, `module`, `timestamp`
(set automatically, UTC, at construction), `details` (optional,
defaults to `{}`). None of the nine subclasses
(`core/errors/exceptions.py`) overrides `__init__` or adds a field —
each exists purely so `except DataError` is more precise than
`except GoldBotError`, which is in turn more precise than
`except Exception`.

## A completed gap

This phase's own brief lists error codes for only six of the nine
categories (Configuration, Data, API, Database, Validation,
Permission) despite naming all nine exception classes in the
hierarchy. `core/errors/codes.py` adds the three missing prefixes
(`STRATEGY_001`, `DECISION_001`, `EXECUTION_001`) so every exception
class has at least one valid code to raise with — documented here
rather than left as a silent gap between the hierarchy and the code
registry.

## Usage

```python
from core.errors.exceptions import DataError
from core.errors import codes

raise DataError(
    code=codes.DATA_001,
    message="Missing candle data",
    module="MarketDataLayer",
)
```

## Serialization

Every `GoldBotError` has a `to_dict()` method:

```python
{
    "type": "DataError",
    "code": "DATA_001",
    "message": "Invalid candle",
    "module": "MarketData",
    "timestamp": "2026-07-14T10:00:00+00:00",
    "details": {},
}
```

`type` is the actual subclass name (`type(self).__name__`), so a
caller inspecting a serialized error doesn't need the original
Python object to know which category it was. `timestamp` is
ISO-8601, always parseable back via `datetime.fromisoformat()`.
`details` is always present (never omitted, never `null`) — an empty
dict, not `None`, when no extra context was supplied.

Future consumers of this shape (not implemented in this phase):
Telegram alerts, a monitoring pipeline, a dashboard — the same
"standard, serializable shape now, real consumer later" pattern every
Phase A foundation module has followed (`SignalSchema`,
`ContextSnapshotSchema`).

## Logging integration

Existing logging (`core/logger.py`'s `setup_logger()`) is unchanged —
this phase adds no new logging infrastructure, only a rule for how an
error should be logged once caught:

```python
logger.error(error.to_dict())
```

Not `logger.error(str(error))`, not `logger.error(error.message)` —
the full structured dict, so a log aggregator or future monitoring
system can parse `code`/`module`/`details` without re-parsing a
free-text message. `tests/errors/test_serialization.py` verifies
`logging.Logger.error()` accepts `to_dict()`'s output directly
without raising.

## Developer rules

- ❌ **Never raise a bare `Exception`.** `raise Exception("...")`
  loses category information a caller might need to handle
  differently (a `DataError` should probably degrade gracefully; a
  `PermissionError` should not).
- ✅ **Always raise the most specific `GoldBotError` subclass.**
  `raise DataError(code=..., message=..., module=...)`, not
  `raise ValueError(...)` or `raise Exception(...)`.
- **This is a rule for new code, not a retrofit requirement.**
  Existing raise sites (`core/secrets.py`'s `ValueError`,
  `DuplicateAssetSymbolError`, `DuplicateStrategyIdError`) are
  untouched by this phase — see "What this phase does NOT do" below.

## When to raise vs. return a structured result

Unchanged from `contracts/error_contract.md`'s own guidance, restated
here since it governs whether this hierarchy applies at all:

1. **Expected, data-driven conditions** (an invalid signal, missing
   market data, an unapproved decision) stay a structured result
   object (`ValidationResult`, `RiskResult`, `TradeDecision`) — this
   phase does not change that dominant pattern anywhere in this
   codebase.
2. **Genuine programmer/integrity errors** (a duplicate registration,
   a truly-missing required secret with no sane default) are where a
   raised `GoldBotError` subclass belongs.

## What this phase does NOT do

- Does not migrate `core/secrets.py`'s existing bare `ValueError` to
  `ConfigurationError` — a named, explicitly deferred future step
  (`contracts/error_contract.md`'s own "Future Extension" section).
- Does not migrate `DuplicateAssetSymbolError`/
  `DuplicateStrategyIdError` to subclass `GoldBotError` — doing so
  would be a breaking change for any caller catching `ValueError`
  specifically, requiring explicit approval per `CLAUDE.md`'s "No
  breaking changes" rule.
- Does not change `core/pipeline.py`, any strategy, `ai/`,
  `decision/`, `risk/`, `telegram/`, or the database schema.
- Does not add monitoring, alerting, or automatic recovery — both are
  drawn in the error flow diagram above as named future stages.
- Does not change `core/logger.py` — existing logging infrastructure
  is untouched; only a *rule* for how to call it with an error is
  added.

## Future extension

- **Monitoring/Recovery**: the two undrawn stages in the error flow
  diagram above.
- **Migrating existing raise sites**: `core/secrets.py` and the two
  `Duplicate*Error` classes, each requiring explicit approval per
  `CLAUDE.md`.
- **Telegram alerting**: a future consumer of `to_dict()`'s
  serialized shape, named but not implemented.
- **A19 Performance Metrics**: the next named phase in the v0.3.5
  roadmap (see `docs/SYSTEM_OVERVIEW.md`), independent of this one.
