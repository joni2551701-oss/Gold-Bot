# core/errors/

## Purpose
Error Classification foundation (Phase A18) — one standard error
hierarchy (`GoldBotError` + nine category subclasses), a standard
error-code registry, and serialization (`to_dict()`), so any error
raised anywhere in GoldBot is understood, logged, and (in the future)
monitored/recovered from the same way. Implements the hierarchy
`contracts/error_contract.md` (Phase A17) specified but explicitly
deferred. See `docs/ERROR_HANDLING.md` for the full contract.

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

```python
try:
    ...
except GoldBotError as error:
    logger.error(error.to_dict())
```

## Module layout
- `base.py` — `GoldBotError`, the base every subclass inherits.
  Carries `code`/`message`/`module`/`timestamp`/`details` and
  `to_dict()`. Never raised directly.
- `exceptions.py` — the nine subclasses:
  `ConfigurationError`, `ValidationError`, `DataError`,
  `ExternalAPIError`, `DatabaseError`, `PermissionError`,
  `StrategyError`, `DecisionError`, `ExecutionError`. Pure type
  markers — none adds a field.
- `codes.py` — `CODE_REGISTRY` (every valid code mapped to a
  description), `CODE_PATTERN` (the `PREFIX_NNN` format), and
  `is_valid_code_format()`/`is_known_code()`.

## What this does NOT do
- Does not migrate any existing raise site (`goldbot/core_layer/secrets/secrets.py`'s bare
  `ValueError`, `assets.asset_registry.DuplicateAssetSymbolError`,
  `strategies.lifecycle.strategy_registry.DuplicateStrategyIdError`)
  to this hierarchy — a named, explicitly deferred future step.
- Does not change `core/pipeline.py`, `core/logger.py`, or any
  strategy/AI/decision/risk/telegram/database logic.
- Does not add monitoring, alerting, or automatic recovery.
- Does not change how existing "expected, data-driven" conditions are
  reported — `ValidationResult`/`RiskResult`/`TradeDecision` stay
  structured results, never exceptions; this hierarchy is for
  genuine programmer/integrity errors instead (see
  `docs/ERROR_HANDLING.md`'s "When to raise vs. return a structured
  result").

## Dependencies
`core/errors/` imports only the standard library (`datetime`,
`typing`, `re`). No dependency on any other GoldBot package —
cross-cutting, like `core/logger.py`/`goldbot/core_layer/secrets/secrets.py`, so every
layer may import from it without creating a new architecture
boundary.

## Future extension
See `docs/ERROR_HANDLING.md`'s "Future extension" section — migrating
existing raise sites, Telegram alerting, and a monitoring/recovery
pipeline are all named, explicit future steps, none implemented in
this phase.
