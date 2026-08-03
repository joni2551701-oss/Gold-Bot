# GoldBot — Owner Flow

Governed by `docs/constitution/CONSTITUTION.md` Article 10 (Owner
Override Law). This is a one-page flow-diagram summary — the full
command inventory (which file covers System/AI/Provider/Broadcast/
Analytics/Emergency, and which sections are honest gaps) already lives
in `docs/owner/OWNER_PANEL.md` and remains the source of truth. Per
Constitution Article 7/11, this document adds the flow-level detail
`OWNER_PANEL.md` doesn't spell out on its own — the audit/notification
steps — rather than duplicating the inventory.

## The flow

```
Command                (a Telegram message from the Owner)
   ↓
Permission Check       platform_layer/telegram/owner/owner_roles.py — require_role()
   ↓
Audit Log               platform_layer/telegram/owner/security.py — log_owner_action()
   ↓
Execution                 the command's own platform_layer/telegram/owner/<domain>_commands.py
                           handler → the domain's Manager/Service/Repository
   ↓
Notification               platform_layer/telegram/owner/runtime_notifications.py (for
                           runtime/cost-protection events) or the command's
                           own direct reply — not every command produces a
                           separate notification
```

This is the same Handler → Service → Repository chain every Telegram
command follows (`docs/architecture/TELEGRAM_FLOW.md`), with two
Owner-specific additions Article 10 requires: the Permission Check is
mandatory before the handler runs, and the Audit Log step records
*who did what* independent of the command's own business logic.
`/runtime_restart` (Phase 62.2) is the first real caller of this exact
Permission → Audit → Execution sequence.

## Critical modules and their Owner surface

Per Article 10, a module this Constitution treats as safety- or
control-critical exposes a control surface through this flow, even
when that surface is foundation-only (a clear "not implemented" is
compliant; a missing surface is not):

| Critical module | Owner surface |
|---|---|
| `core_layer/emergency/` | `platform_layer/telegram/owner/emergency_commands.py` |
| `ai/runtime/runtime_manager.py` | `platform_layer/telegram/owner/runtime_commands.py` |
| `configuration/runtime_feature_manager.py` | `platform_layer/telegram/owner/control_commands.py` |
| `broadcast/`, `media/`, `translation/` | `platform_layer/telegram/owner/broadcast_commands.py` (foundation-only, Phase 63.0 — every command returns `NOT IMPLEMENTED` honestly) |

## Related

- `docs/architecture/TELEGRAM_FLOW.md` — the general Telegram flow
  this is a variant of.
- `docs/owner/OWNER_PANEL.md` — the full Owner command inventory,
  section by section.
- `docs/policies/OWNER_POLICY.md` — the day-to-day operating rule this
  flow implements.
