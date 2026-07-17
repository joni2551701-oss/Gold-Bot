# GoldBot — Naming Conventions

Governed by `docs/constitution/CONSTITUTION.md` Article 7 (Reuse
Principle). A consistent file suffix signals a module's role before
its contents are even read, and lets Article 11's Foundation Reuse
Audit be answered by `grep`/`glob` rather than guesswork.

## File suffixes

| Suffix | Role | Example |
|---|---|---|
| `*_manager.py` | Owns runtime state + read/write ops over a domain | `runtime_manager.py`, `persona_manager.py`, `broadcast_manager.py` |
| `*_service.py` | Telegram-layer business logic, calls a repository | `signal_service.py`, `user_service.py`, `subscription_service.py` |
| `*_repository.py` | SQL only, no business logic (Constitution Article 4) | `user_repository.py`, `audit_log_repository.py` |
| `*_provider.py` | One concrete implementation of a `Base*Provider` contract | `gemini_provider.py`, `openai_provider.py` |
| `*_adapter.py` | Reshapes one module's type into another's | (pattern used inline more often than as a standalone file today — see `docs/architecture/DESIGN_PATTERNS.md`'s Adapter section) |
| `*_engine.py` | Runs a deterministic process end to end | `decision_engine.py`, `risk_manager.py` (named `_manager` but plays this role), `signal_engine.py`, `explanation_engine.py`, `backtest_engine.py` |
| `*_registry.py` | Static catalog, usually built by `build_*_registry()` | `provider_registry.py`, `persona_registry.py`, `media_registry.py` |
| `*_commands.py` | Telegram command handlers for one domain | `runtime_commands.py`, `broadcast_commands.py`, `emergency_commands.py` |
| `*_models.py` | Database ORM/dataclass row shapes | `emergency_models.py`, `learning_models.py` |

## Command handler naming (mechanical, not a convention — a contract)

A Telegram handler function **must** be named `<command>_handler` —
`telegram/command_router.py` resolves a command to its handler via
`getattr(handlers, f"{command}_handler")`, not a lookup table. A
mismatch is not a style violation; it is a silent dispatch failure
(the exact bug caught once in Phase 61.7 — see
`docs/telegram/TELEGRAM_ARCHITECTURE.md`).

## Package naming

- A new top-level package (a sibling of `ai/`, `telegram/`, `data/`) is
  the highest-cost naming decision available — Constitution Article 7
  says it "should be rare." `broadcast/`, `media/`, `translation/`,
  `knowledge/`, `lifecycle/`, `learning/`, `backtesting/` are the real
  precedents; each has its own Reuse Audit on record justifying why it
  is not a subpackage of something else.
- A subpackage under an existing top-level package
  (`ai/persona/`, `telegram/owner/`, `database/`) is the default,
  lower-cost choice for anything that is conceptually part of that
  package's domain.

## Class naming

`Capability`-style enums are singular nouns (`Capability`,
`ContentType`, `MediaType`, `Language`, `RuntimeState`,
`BroadcastProviderType`). Manager/Engine/Service classes are named
`<Domain><Role>` (`PersonaManager`, `DecisionEngine`,
`BroadcastTriggerManager`) — never a bare `Manager` or `Engine` with
no domain prefix, even in a small package.

## Related

- `docs/architecture/DESIGN_PATTERNS.md` — the patterns these suffixes
  signal.
- `docs/constitution/CONSTITUTION.md` Article 7, Article 11.
