# GoldBot Platform Dependency Map

What the Platform Layer (`telegram/`, its four platform tables under
`database/`, `translation/`) may and must never import. Restates and
narrows `docs/ARCHITECTURE_RULES.md` §1.2 ("Telegram Layer") and
`docs/architecture/MODULE_DEPENDENCIES.md` specifically for Platform
Engineer scope — this document adds no new rule, it collects the
existing ones that bound this role's authorized area. Documentation
only; no import was changed to produce this map.

## 1. The layer chain (never skipped)

```
platform_layer/telegram/command_router.py
      -> platform_layer/telegram/commands.py, platform_layer/telegram/permissions.py, platform_layer/telegram/handlers.py
platform_layer/telegram/handlers.py  (or platform_layer/telegram/owner/<domain>_commands.py)
      -> telegram/*_service.py                      ONLY
telegram/*_service.py
      -> database/*_repository.py                   ONLY
database/*_repository.py
      -> database/*_models.py, database_layer/database_manager/database.py  ONLY (SQL, no business logic)
```

- `platform_layer/telegram/handlers.py` **never** imports `database.*` or
  `core.pipeline` directly — stated in the file's own module
  docstring and enforced by the codebase's layering discipline
  (`docs/telegram/TELEGRAM_ARCHITECTURE.md`).
- `database/*_repository.py` **never** imports `telegram/` — a
  repository knows nothing about Telegram, permissions, or commands
  (`CLAUDE.md`).
- `platform_layer/telegram/owner/*.py` follows the identical Handler → Service →
  Repository shape, gated additionally by `platform_layer/telegram/owner/owner_roles.py`
  (`docs/owner/OWNER_PANEL.md`).

## 2. What the Platform Layer must never import

Per `docs/ARCHITECTURE_RULES.md` §1.2: `telegram/` never imports
`strategies/`, `decision/`, or `risk/` — it formats and delivers what
those layers already decided, it never re-derives or re-evaluates a
trading decision. Extending this explicitly for Platform Engineer
scope, the Platform Layer must never import:

- `strategies/`, `signals/` (except the one typed-parameter exception
  in §3), `context/`, `decision/`, `risk/` — Trading Core, frozen for
  this role.
- `ai/` — with the one narrow, already-audited exception in §4
  (`ai/runtime/ai_service.py`, display content only).
- `core/pipeline.py` directly from any `telegram/` file (only
  `main.py` may construct/run it).

This is not a new restriction — it is the existing rule, restated
here because the Senior Platform Engineer role is explicitly not
authorized to touch Trading Core, Decision Engine, Risk Manager, or
Signal/Context Engine without a dedicated Director task.

## 3. The one typed-parameter exception

`platform_layer/telegram/signal_formatter.py` imports `signal_layer.signal_builder.models.SignalCandidate`,
`ai_layer.ai_engine.ai_analyzer.AIAnalysisResult`, and `decision_layer.decision_engine.models.TradeDecision`
— for its own dataclass field type hints only. It calls no method on
Trading Core, it only reads already-computed values off objects those
layers already produced and handed it. This is the pre-existing,
documented boundary (`telegram/README.md`: "this layer only ever sees
their already-computed output via `platform_layer/telegram/signal_formatter.py`'s
typed parameters") — not a live dependency to extend, and not
authorization to add a second such import elsewhere without a
dedicated review.

## 4. Where AI enters the Platform Layer (narrow, existing, one-directional)

A Telegram handler may call `ai/runtime/ai_service.py`'s
`AIService.ask()` to get an explanation of already-decided pipeline
output — used today by `platform_layer/telegram/owner/ai_commands.py` and
`platform_layer/telegram/owner/runtime_commands.py`. This is a Service-layer call
like any other: the AI's response is content to display, never a
decision that changes what the handler does next
(`docs/telegram/TELEGRAM_ARCHITECTURE.md`, `docs/constitution/CONSTITUTION.md`
Article 1). `runtime_commands.py` additionally depends on `ai/runtime/`'s
`RuntimeManager`/`self_check` for the same reason
(`docs/architecture/MODULE_DEPENDENCIES.md`).

No other file in `telegram/` or `platform_layer/telegram/owner/` imports `ai/` today.

## 5. The reverse direction: `ai/` reading Platform concepts (one-directional, not a Platform dependency)

`ai/access/subscription_policy.py` maps `subscriptions.plan` string
values (`"FREE"`/`"PREMIUM"`/`"VIP"`) to an `AIRole` enum, for the AI
foundation's own unwired access-control layer. This is `ai/` depending
on a concept the Platform Layer defines (the plan string values
`platform_layer/telegram/subscription_service.py`'s `SIGNAL_ACCESS_PLANS`/
`DEFAULT_PLAN` establish) — **never the reverse**: no file under
`telegram/` or `database/` imports anything from `ai/access/`. Recorded
here so a future change to either side checks both directions before
adding a third, same convention `docs/ARCHITECTURE.md`'s own
Dependency Rules section uses for cross-package references elsewhere
in the codebase.

## 6. Process boundary: pipeline vs. Platform Layer

`main.py` (the scheduled `TradingPipeline` run) and
`platform_layer/telegram/polling.py` (the long-running Platform Layer) are separate
OS processes, never invoked from one another, sharing no in-memory
state — only the SQLite file connects them
(`docs/ARCHITECTURE.md` System Overview). The pipeline's only
Telegram-layer touchpoint is outbound: `core/pipeline.py` →
`platform_layer/telegram/notifier.py` → `platform_layer/telegram/bot.py`, using a separate `Bot`
instance from `polling.py`'s inbound listener. This outbound path
does **not** call into `NotificationService`, `SignalAccessService`,
or any other Platform service — a deliberate scope boundary, not a
missing integration to add as Platform work (see
`docs/PLATFORM_ARCHITECTURE.md` §7).

## 7. Internal Platform Layer shape (summary)

| Module | Depends on |
|---|---|
| `platform_layer/telegram/handlers.py` | `telegram/*_service.py` only |
| `platform_layer/telegram/command_router.py` | `platform_layer/telegram/commands.py`, `platform_layer/telegram/permissions.py`, `platform_layer/telegram/handlers.py`, `platform_layer/telegram/reply_keyboard_manager.py`, `platform_layer/telegram/keyboards.py` |
| `platform_layer/telegram/callback_router.py` | `platform_layer/telegram/handlers.py` (language + settings-value paths only) |
| `platform_layer/telegram/reply_keyboard_manager.py`, `platform_layer/telegram/keyboards.py` | `media_layer/translation/ui_catalog.py` (`t()`) |
| `telegram/*_service.py` (admin/feedback/notification/signal/subscription/user) | the corresponding `database/*_repository.py` only |
| `platform_layer/telegram/owner/*.py` (24 files) | the corresponding service/repository for their domain; `runtime_commands.py` additionally → `ai/runtime/` (see §4) |
| `platform_layer/telegram/menu_commands.py` | `database_layer.user_repository.admin_repository.AdminRepository`, `database_layer.user_repository.user_repository.UserRepository` (read-only tier/language lookups), `platform_layer/telegram/commands.py` |
| `database/*_repository.py` (platform tables) | `database/*_models.py`, `database_layer/database_manager/database.py` only |
| `translation/*` | standard library only — no dependency on `telegram/`, `database/`, or any Trading Core package |

## Enforcement

Same mechanism as the rest of the codebase — not a separate process
for the Platform Layer:

- The CI import sweep (`.github/workflows/ci.yml`) surfaces a new
  circular or upward import.
- `pyflakes` and the full `pytest` suite (`tests/telegram/`, 465 tests
  across 13 files as of `docs/PHASE6_FREEZE.md` Stage 8, plus
  `tests/platform_layer/telegram/owner/`, 27 files) run before every commit per
  `CLAUDE.md`'s Commit Protocol.

A change that would require violating one of the boundaries above is
a signal to stop and request a dedicated Director task before adding
the import — per `CLAUDE.md`'s Architecture Rules and this role's own
"not authorized to change Trading Core" boundary.

## Related documents

- `docs/PLATFORM_ARCHITECTURE.md` — the narrative flow this map bounds.
- `docs/PLATFORM_MODULE_MAP.md` — file-by-file responsibility list.
- `docs/ARCHITECTURE_RULES.md`, `docs/architecture/MODULE_DEPENDENCIES.md`,
  `docs/ARCHITECTURE.md` (Dependency Rules section) — the whole-system
  rules this document narrows for Platform Engineer scope.
