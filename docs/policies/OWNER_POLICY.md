# Owner Policy

The operational face of Constitution Article 10 (Owner Override Law).

## Every critical module has an Owner surface

A module that governs safety, availability, or user-facing spend is
"critical" for this policy's purposes:
`core_layer/emergency/` (kill switch, maintenance mode),
`ai/runtime/runtime_manager.py` (AI Runtime lifecycle, cost
protection), `configuration/runtime_feature_manager.py` (feature
toggles), and — foundation-only today — `broadcast/`, `media/`,
`translation/`. Each has (or, for foundation-only modules, will have
when wired) a `telegram/owner/*_commands.py` surface.

## The command chain (Article 4 applied to Owner commands)

```
Telegram Owner command → telegram/owner/security.py
    (require_role + log_owner_action)
  → telegram/owner/*_commands.py
  → the module's own Manager
```

An Owner command never reaches into a repository directly, and every
Owner action is audited via `log_owner_action()` — the same pattern
`/runtime_restart` (Phase 62.2) established as the first real caller
of `security.py`'s role-check/audit pair.

## Foundation-only is an honest state, not a bug

`telegram/owner/broadcast_commands.py`'s four commands (Phase 63.0)
all return a clear "not implemented" rather than a fabricated result.
This is compliant with this policy: the surface exists (so the Owner
knows the command is planned and where it will live), and it does not
lie about what it can currently do.

## Related

- `docs/constitution/CONSTITUTION.md` Article 10.
- `docs/owner/OWNER_PANEL.md` — the full existing Owner Panel command
  reference.
- `docs/telegram/TELEGRAM_ARCHITECTURE.md`.
