# Error Contract

> **Update (Phase A18)**: the hierarchy this document specifies is
> now implemented — see `core_layer/errors/` and `docs/ERROR_HANDLING.md`.
> Phase A18 added `core_layer/errors/base.py`'s `GoldBotError`,
> `core_layer/errors/exceptions.py`'s nine subclasses (four more than this
> document originally proposed — `DatabaseError`, `StrategyError`,
> `DecisionError`, `ExecutionError`, added for the categories
> `contracts/*.md`'s own module contracts already needed), and
> `core_layer/errors/codes.py`'s code registry. This document's original
> text below is kept as the historical specification — the "Current
> state" section describing zero shared base class is now superseded
> by A18's real implementation, not by a further edit here.

## Responsibility
A standard exception hierarchy every module should raise from,
instead of each module inventing its own ad-hoc exception shape. **Not
implemented in this phase** — this is a specification for how errors
*should* be structured going forward, not a new `core/errors.py` file
(Phase A17 is documentation-only; see this contract's own "Future
Extension" section for what implementing it would involve).

## Current state (audited, not invented)
Before writing this specification, the whole codebase was searched for
existing custom exceptions. Exactly two exist today, both independent,
both subclassing `ValueError` directly:

- `assets.asset_registry.DuplicateAssetSymbolError(ValueError)`
  (Phase A12)
- `strategy_layer.strategy_manager.lifecycle.strategy_registry.DuplicateStrategyIdError(ValueError)`
  (Phase A11)

No shared base class, no `GoldBotError`, exists anywhere. Every other
"error" condition in this codebase (an invalid signal, an empty
context, a rejected decision) is handled the way
`docs/ARCHITECTURE_RULES.md`'s Enforcement section and every Phase A
module's own docs describe: a structured result object
(`ValidationResult`, `RiskResult.approved`, `TradeDecision.action`),
never a raised exception. This contract does not propose changing
that pattern — see "When to raise vs. return a result" below.

## Proposed hierarchy

```
GoldBotError
 |
 +-- DataError            -- malformed/missing market or persisted data
 |
 +-- ValidationError      -- a schema/contract check failed (SignalSchema, ContextSnapshotSchema, ...)
 |
 +-- ConfigurationError   -- bad/missing configuration (env var, config.py value, database path)
 |
 +-- PermissionError      -- an actor lacked authorization (Telegram command, admin action)
 |
 +-- ExternalAPIError     -- a third-party call failed (Twelve Data, Telegram Bot API, a future AI provider)
```

Each subtype maps onto a real, already-identified failure surface in
this codebase:

| Type | Where it would apply | Today's real behavior |
|---|---|---|
| `DataError` | `data_layer/providers/twelve_data_client.py` fetch failures, malformed `Candle` | Logged, degrades to 0 candles — never raises past `MarketDataNormalizer.get_candles()`. |
| `ValidationError` | `signal_layer.signal_builder.schema.validate_signal()`, `context.snapshot.validate_snapshot()` | Returns `ValidationResult(valid=False, errors=[...])` — never raises today; see "When to raise vs. return a result" below. |
| `ConfigurationError` | `core_layer/secrets/secrets.py`'s `Secrets.get()` (raises a bare `ValueError` today when a required secret is missing and no default given) | A real, existing raise-on-missing-required-secret path — the first concrete candidate for this subtype. |
| `PermissionError` | `platform_layer/telegram/permissions.py` (fail-closed: nobody is `OWNER` if `TELEGRAM_OWNER_ID` is unset) | Currently a boolean/role check, not an exception. |
| `ExternalAPIError` | `data_layer/providers/twelve_data_client.py`, `platform_layer/telegram/notifier.py`, a future real AI provider call | Currently caught and logged at the call site, degrading to an empty/failed result, never propagated as a typed exception. |

## When to raise vs. return a result

Two distinct failure categories exist in this codebase, and this
contract keeps them distinct rather than collapsing them into "always
raise" or "always return a result":

1. **Expected, data-driven conditions** (an invalid signal, missing
   market data, an unapproved decision) — always a structured result
   (`ValidationResult`, `RiskResult`, `TradeDecision`), never an
   exception. This is the dominant pattern in this codebase and this
   contract does not change it.
2. **Genuine programmer/integrity errors** (registering a duplicate
   strategy id, a required secret truly absent with no sane default,
   a schema the code itself constructed incorrectly) — a raised
   exception is appropriate, since there is no sensible "degraded"
   value to return. `DuplicateAssetSymbolError`/
   `DuplicateStrategyIdError` are the two real, existing examples;
   under this hierarchy, both would become `GoldBotError` (or a
   dedicated subtype) instead of a bare `ValueError`, once a future
   phase implements this change.

## Allowed Dependencies
None — this is a foundation type hierarchy every layer may depend on
(same cross-cutting status as `core/`), not a layer with its own
business logic.

## Forbidden Dependencies
❌ No subtype may import `strategies/`, `signals/`, `ai/`,
`decision/`, `risk/`, `telegram/`, or `database/` — an error type
must never depend on the layer that raises it, or every layer would
have to import every error subtype's dependencies transitively.

## Error Contract
This document *is* the error contract for every other
`contracts/*.md` file — each one's own "Error Contract" section
references the subtype above that would apply to its failure modes,
once implemented.

## Future Extension
Implementing this hierarchy (a real `core/errors.py` or similar) is
explicitly **not** part of Phase A17 — this phase is documentation
only, per its own scope ("Kod refactor yo'q, Business logic
o'zgartirish yo'q"). A future, separately-approved phase would: (1)
add the six classes above, (2) migrate `core_layer/secrets/secrets.py`'s bare
`ValueError` to `ConfigurationError`, (3) migrate
`DuplicateAssetSymbolError`/`DuplicateStrategyIdError` to subclass
`GoldBotError` instead of `ValueError` directly (a breaking change for
any caller catching `ValueError` specifically — requires explicit
approval per `CLAUDE.md`'s "No breaking changes" rule), and (4) decide
whether `data/`/`telegram/`'s currently-swallowed external-API
failures should start raising `ExternalAPIError` instead of only
logging.
