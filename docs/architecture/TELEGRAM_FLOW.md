# GoldBot — Telegram Flow

Governed by `docs/constitution/CONSTITUTION.md` Article 2 and 4. This
is a one-page summary for the `docs/architecture/` flow-diagram family
(`SYSTEM_LAYERS.md`, `DATA_FLOW.md`, `AI_FLOW.md`, this document,
`OWNER_FLOW.md`). It does not re-derive the full mechanism —
`docs/telegram/TELEGRAM_ARCHITECTURE.md` already documents that in
detail, verified directly against `telegram/command_router.py`, and
remains the source of truth. Per Constitution Article 7/11, this file
extends the flow-diagram family rather than duplicating that content.

## The flow

```
User
   ↓
Command Router      telegram/command_router.py
   ↓
Permission           telegram/permissions.py
   ↓
Handler                telegram/handlers.py (or telegram/owner/<domain>_commands.py)
   ↓
Service                  telegram/*_service.py
   ↓
Repository                database/*_repository.py
   ↓
Response
```

Dispatch is by name convention (`getattr(handlers, f"{command}_handler")`),
not a hand-written table — see
`docs/telegram/TELEGRAM_ARCHITECTURE.md`'s "Dispatch mechanism" section
for the exact lookup and the Phase 61.7 naming mistake it once caught.

## Owner is a variant of this same flow, not a separate one

```
Owner
   ↓
Permission Check      telegram/owner/owner_roles.py
   ↓
Audit Log               telegram/owner/security.py (log_owner_action())
   ↓
Execution                 the Owner command's own handler → service/manager
   ↓
Notification               telegram/owner/runtime_notifications.py, where applicable
```

See `docs/architecture/OWNER_FLOW.md` for this variant in detail —
Article 10 (Owner Override Law) governs it specifically.

## Related

- `docs/telegram/TELEGRAM_ARCHITECTURE.md` — the full, verified
  dispatch mechanism this summary points to.
- `docs/architecture/OWNER_FLOW.md` — the Owner-specific variant.
- `docs/owner/OWNER_PANEL.md` — the full Owner command inventory.
