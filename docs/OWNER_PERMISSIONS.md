# Owner Permissions

The Owner Mode role hierarchy foundation (Phase 59.6: Audit &
Observability Foundation, TASK 3). Companion to `docs/AUDIT_SYSTEM.md`.

## Two separate permission systems — read this before touching either

**`telegram.permissions.PermissionLevel`** (`OWNER`/`ADMIN`/`USER`,
pre-existing) is **live**: `telegram/command_router.py`'s
`_PERMISSION_RANK` and `_required_level()` gate every real command the
bot routes today. Do not add values to this enum casually — it is
load-bearing production code.

**`telegram.owner.owner_roles.OwnerRole`** (`OWNER`/`SUPER_ADMIN`/
`ADMIN`/`VIEWER`, new this phase) is a **separate, not-yet-wired**
hierarchy, built specifically for the future Owner Mode dashboard
(Phase 59.8). It never imports or modifies `PermissionLevel`, and no
owner command checks it yet.

| | `PermissionLevel` | `OwnerRole` |
|---|---|---|
| Status | Live, gates real commands today | Foundation only, not checked anywhere |
| Values | OWNER / ADMIN / USER | OWNER / SUPER_ADMIN / ADMIN / VIEWER |
| Source of truth | `core.secrets.Secrets.TELEGRAM_OWNER_ID` + `admins` table (existence only) | Same owner ID + `admins` table's `role` column (value now classified) |

## `resolve_owner_role(telegram_id, admin_repository=None) -> OwnerRole`

```python
if is_owner(telegram_id):          # same telegram.permissions.is_owner()
    return OwnerRole.OWNER
# else looks up admins.role via AdminRepository.get_admin()
#   role == "SUPER_ADMIN"  -> OwnerRole.SUPER_ADMIN
#   role == anything else (row exists) -> OwnerRole.ADMIN
#   no row at all           -> OwnerRole.VIEWER
```

Never raises — a lookup failure fails closed to `VIEWER`, the same
posture `telegram.permissions.is_admin()` already uses.

### Reused, not duplicated

`admins.role` (`database/admin_models.py`'s `AdminRecord.role`) has
existed since Phase 37/45 as a free-text column, defaulting to
`"ADMIN"` on `AdminRepository.add_admin()`. It was never actually
classified into a tier before this phase — `resolve_owner_role()` is
the first place its value is read and interpreted. Setting
`role="SUPER_ADMIN"` via `AdminRepository.add_admin(telegram_id,
role="SUPER_ADMIN")` already works today (the column always accepted
any string); nothing new was added to the schema.

## What this phase does NOT do

- Does not add a per-command minimum-`OwnerRole` check anywhere.
- Does not change what any existing command actually requires (still
  governed entirely by `PermissionLevel`/`OWNER_COMMANDS`/
  `ADMIN_COMMANDS`).
- Does not add a `VIEWER`-specific read-only enforcement — the name
  states intent, nothing in this codebase restricts a `VIEWER` from
  anything yet.

Wiring real per-command `OwnerRole` checks into a future Owner
Dashboard (Phase 59.8) is explicitly out of scope here.
