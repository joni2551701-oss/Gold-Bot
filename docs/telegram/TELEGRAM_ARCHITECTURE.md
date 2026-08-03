# GoldBot — Telegram Architecture

Governed by `docs/constitution/CONSTITUTION.md` Article 2 and 4. This
document is the real, current Telegram dispatch flow — verified
directly against `platform_layer/telegram/command_router.py`, not assumed.

## Flow

```
Telegram (incoming update)
      |
   Router          platform_layer/telegram/command_router.py
      |
 Permission       platform_layer/telegram/permissions.py (+ platform_layer/telegram/owner/owner_roles.py for Owner commands)
      |
   Handler         platform_layer/telegram/handlers.py (or platform_layer/telegram/owner/<domain>_commands.py)
      |
   Service         telegram/*_service.py
      |
  Repository       database/*_repository.py
      |
   Database
```

## Dispatch mechanism (real, not illustrative)

`platform_layer/telegram/command_router.py` resolves a command to its handler
**dynamically by name convention**, not a hand-written dispatch table:

```python
handler = getattr(handlers, f"{command}_handler", None)
```

A command named `"runtime_status"` is dispatched to
`handlers.runtime_status_handler` — nothing else. If a handler
function's name doesn't exactly match `<command>_handler`, the router
silently finds nothing and the command fails to dispatch. This is not
a hypothetical risk: a handler was briefly misnamed
`runtime_status_full_handler` during Phase 61.7 and would have been
invisible to this exact lookup had it not been caught before tests
ran. Anyone adding a new command must name the handler function to
match this convention exactly — see
`docs/architecture/EXTENSION_GUIDE.md` Pattern 2.

`_call_handler()` (`platform_layer/telegram/command_router.py:117`) invokes the
resolved handler with `telegram_id`, `username`, and `args`; the
`contact_handler` path (phone-number contact sharing) is the one
special-cased call in the router that bypasses the generic
`getattr` lookup, since it responds to a Telegram contact message
rather than a text command.

## Layer boundaries (Constitution Article 4)

- `platform_layer/telegram/handlers.py` never imports `database.*` or `core.pipeline`
  directly — stated in the file's own module docstring, enforced by
  the codebase's layering discipline.
- Handlers call services (`telegram/*_service.py`); services call
  repositories (`database/*_repository.py`); repositories own SQL
  only.
- Owner commands (`platform_layer/telegram/owner/*.py`) follow the identical flow,
  gated additionally by `owner_roles.py` before the handler runs. See
  `docs/owner/OWNER_PANEL.md` for the full section-by-section map of
  what lives under `platform_layer/telegram/owner/`.

## Where AI enters this flow

A Telegram handler may call `ai/runtime/ai_service.py`'s `AIService.ask()`
to obtain an explanation for already-decided pipeline output (e.g.
`platform_layer/telegram/owner/ai_commands.py`, `runtime_commands.py`). This is a
Service-layer call like any other — the AI's response is content to
display, never a decision that changes what the Handler does next.
See `docs/constitution/CONSTITUTION.md` Article 1.

## Language Foundation (V2 Phase 1 — FROZEN)

**Status: FROZEN as of commit `5c1f806`.** See
`docs/PHASE_V2_PHASE1_FREEZE.md` for the full freeze record.

A second dispatch path exists alongside the text-command flow above,
for the `/language` picker's inline keyboard:

```
Telegram (callback_query)
      |
platform_layer/telegram/polling.py            forwards callback_query, no branching
      |
platform_layer/telegram/callback_router.py    route_callback() -> translates
      |                        callback_data ("lang_uz") into the
      |                        same call the text command would make
   Handler                     telegram.handlers.language_status()
      |
   Service                     telegram.user_service.UserService
```

`route_callback()` never introduces a second business-logic path — a
`lang_uz` tap resolves to exactly what `/language UZ` resolves to via
`handlers.language_status()`. Every other keyboard's `callback_data`
(`risk_*`, `timeframe_*`, `strategy_*`, `notifications_*`,
`settings_*`, `admin_*`) is recognized but not yet wired to a handler
— `callback.answer()` still clears the client's spinner, matching the
"honestly inert until built" convention used elsewhere in this
codebase.

**Translation Engine.** `media_layer/translation/ui_catalog.py` is a static
UZ/RU/EN string catalog (77 keys) with a single lookup function,
`t(key, language, **kwargs)` — caller's language → EN → any entry,
never raises. It is intentionally distinct from
`media_layer.translation.translation_manager.TranslationManager`, which stays a
deliberate no-op for dynamic/AI-generated content (Rule 4: no
Google/DeepL/Gemini/OpenAI call anywhere in that package) — `t()` is
hand-written UI strings only, looked up, not machine-translated.

**What's localized (USER-tier only).** All 17 `COMMANDS`-registry
handlers, all USER-tier keyboards (`platform_layer/telegram/keyboards.py`), and
`/language`'s own reply text (`language_status()`/`language_handler()`)
route through `t()`. `contact_handler`'s failure path maps
`UserService.register_phone()`'s known failure reasons to localized
keys rather than echoing raw English.

**What stays English (by design, not oversight).**
- OWNER/ADMIN-tier commands (`platform_layer/telegram/owner/*.py`, `admin_handler`,
  `broadcast_handler`, `stats_handler`, `users_handler`,
  `userinfo_handler`, `vipinfo_handler`, `feedbacks_handler`, every
  `ai_*`/`owner_*`/`runtime_*` handler) — permanently English,
  internal operator tooling, Director decision.
- `platform_layer/telegram/signal_formatter.py` and
  `platform_layer/telegram/signal_access_service.py` — deferred to V2.1 (Signal
  Product Layer, will be touched anyway during Price Stream work).
- `platform_layer/telegram/command_router.py`'s generic constants
  (`UNKNOWN_COMMAND_TEXT`, `SERVICE_UNAVAILABLE_TEXT`,
  `PERMISSION_DENIED_TEXT`) — deferred to V2.2 (a future Generic Error
  Catalog).

**Default language.** `database_layer/database_manager/models.py`'s schema default is
`users.language = 'UZ'` — a fresh/unconfigured user gets Uzbek text,
not English. This is a deliberate GoldBot V2 product decision (not a
bug or a fallback-of-convenience); tests assert against this default,
not against English.

## Related documents

- `docs/architecture/MODULE_DEPENDENCIES.md` — Telegram's place in the
  full system dependency map.
- `docs/architecture/EXTENSION_GUIDE.md` — Pattern 2, adding a new
  Telegram command correctly.
- `docs/owner/OWNER_PANEL.md` — the Owner-only command surface built
  on this same flow.
- `docs/PHASE_V2_PHASE1_FREEZE.md` — the Language Foundation freeze
  record: full changelog, deferred items, Phase 2 checklist.
