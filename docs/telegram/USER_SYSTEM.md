# GoldBot — User System

Governed by `docs/constitution/CONSTITUTION.md` Article 4. Verified
directly against `database_layer/user_repository/user_repository.py`, `platform_layer/telegram/user_service.py`,
and `ai/access/permissions.py`.

## Correction to an earlier brief's assumption

A single linear chain (`NEW → FREE → PREMIUM → VIP → BANNED`) does not
match the real code — the codebase deliberately keeps two independent
axes, per `platform_layer/telegram/user_service.py`'s own docstring ("deliberately
separate from..."):

```
Lifecycle status   NEW → ACTIVE → BANNED
                    (database_layer/user_repository/user_repository.py — set_lifecycle_status(),
                     ban_user(), count_by_status(); a BANNED user is
                     never silently reactivated by activity tracking)

Subscription/role   FREE → PREMIUM → VIP   (+ ADMIN, OWNER — not
                    subscription tiers, granted separately)
                    (ai/access/permissions.py's AIRole enum, ordered
                     highest-to-lowest privilege: OWNER > ADMIN > VIP
                     > PREMIUM > FREE)
```

A user's lifecycle status and subscription tier move independently —
a `BANNED` user can still technically hold a `VIP` plan record; access
checks consult both axes, not one linear scale.

## Where each axis is enforced

- **Lifecycle status** — `platform_layer/telegram/handlers.py` checks BANNED status
  (best-effort) before normal command handling; `UserService.ban_user()`/
  `activate_user()` are the only ways to change it.
- **Subscription/role** — `ai/access/subscription_policy.py` maps a
  subscription `plan` string (`FREE`/`PREMIUM`/`VIP`) to an `AIRole`,
  failing closed to `AIRole.FREE` on any missing or unrecognized value
  — never an unearned entitlement. `AccessControl`'s `OWNER`/`ADMIN`
  gain every `Capability` automatically; `VIP`/`PREMIUM`/`FREE` are
  listed per-capability in the permission matrix.

## Related

- `docs/OWNER_PERMISSIONS.md` — the full permission matrix.
- `docs/telegram/COMMAND_SYSTEM.md` — which command tier a role can
  reach.
- `docs/policies/AI_POLICY.md`.
