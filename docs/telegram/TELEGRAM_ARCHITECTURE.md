# GoldBot — Telegram Architecture

Governed by `docs/constitution/CONSTITUTION.md` Article 2 and 4. This
document is the real, current Telegram dispatch flow — verified
directly against `telegram/command_router.py`, not assumed.

## Flow

```
Telegram (incoming update)
      |
   Router          telegram/command_router.py
      |
 Permission       telegram/permissions.py (+ telegram/owner/owner_roles.py for Owner commands)
      |
   Handler         telegram/handlers.py (or telegram/owner/<domain>_commands.py)
      |
   Service         telegram/*_service.py
      |
  Repository       database/*_repository.py
      |
   Database
```

## Dispatch mechanism (real, not illustrative)

`telegram/command_router.py` resolves a command to its handler
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

`_call_handler()` (`telegram/command_router.py:117`) invokes the
resolved handler with `telegram_id`, `username`, and `args`; the
`contact_handler` path (phone-number contact sharing) is the one
special-cased call in the router that bypasses the generic
`getattr` lookup, since it responds to a Telegram contact message
rather than a text command.

## Layer boundaries (Constitution Article 4)

- `telegram/handlers.py` never imports `database.*` or `core.pipeline`
  directly — stated in the file's own module docstring, enforced by
  the codebase's layering discipline.
- Handlers call services (`telegram/*_service.py`); services call
  repositories (`database/*_repository.py`); repositories own SQL
  only.
- Owner commands (`telegram/owner/*.py`) follow the identical flow,
  gated additionally by `owner_roles.py` before the handler runs. See
  `docs/owner/OWNER_PANEL.md` for the full section-by-section map of
  what lives under `telegram/owner/`.

## Where AI enters this flow

A Telegram handler may call `ai/runtime/ai_service.py`'s `AIService.ask()`
to obtain an explanation for already-decided pipeline output (e.g.
`telegram/owner/ai_commands.py`, `runtime_commands.py`). This is a
Service-layer call like any other — the AI's response is content to
display, never a decision that changes what the Handler does next.
See `docs/constitution/CONSTITUTION.md` Article 1.

## Related documents

- `docs/architecture/MODULE_DEPENDENCIES.md` — Telegram's place in the
  full system dependency map.
- `docs/architecture/EXTENSION_GUIDE.md` — Pattern 2, adding a new
  Telegram command correctly.
- `docs/owner/OWNER_PANEL.md` — the Owner-only command surface built
  on this same flow.
