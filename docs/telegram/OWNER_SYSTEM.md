# GoldBot — Owner System

Governed by `docs/constitution/CONSTITUTION.md` Article 10 (Owner
Override Law). The full, real 12-section command inventory already
lives in `docs/owner/OWNER_PANEL.md`; the Permission → Audit →
Execution → Notification sequence already lives in
`docs/architecture/OWNER_FLOW.md`. This document adds one thing
neither provides: the Director's own six-group "Senior Trading AI
Control Center" framing, mapped onto the real, existing sections
rather than re-deriving them.

## The six control groups, mapped to real sections

```
Owner
 ├── AI Control          → OWNER_PANEL.md "AI" section (ai_commands.py, runtime_commands.py, runtime_notifications.py)
 ├── Runtime Control      → the runtime_* half of the same "AI" section (Phase 61.6/61.7/62.2)
 ├── User Control          → OWNER_PANEL.md "Users" section (owner_roles.py)
 ├── Broadcast Control      → OWNER_PANEL.md "Broadcast" section (runtime_notifications.py's queue; live delivery loop is the still-open v0.7 gap) + telegram/owner/broadcast_commands.py (Phase 63.0, foundation-only, NOT IMPLEMENTED)
 ├── Emergency Control       → OWNER_PANEL.md "Emergency" section (emergency_commands.py, core/emergency/)
 └── Analytics               → OWNER_PANEL.md "Analytics" section (performance/report/dataset/feature/fundamental/learning commands)
```

`OWNER_PANEL.md`'s own table has 12 sections, not 6 — this six-group
view is a coarser lens for orientation purposes; `System`,
`Provider`, `Subscription`, `Trading`, `Risk`, `Decision`, and
`Backup` fold into the six groups above by adjacency (e.g. `Provider`
and `System` both live conceptually under a broader "Runtime/AI
Control" umbrella) rather than getting their own top-level branch
here.

## Related

- `docs/owner/OWNER_PANEL.md` — the authoritative, full section-by-section
  inventory.
- `docs/architecture/OWNER_FLOW.md` — the Permission → Audit →
  Execution → Notification sequence every group's commands follow.
- `docs/policies/OWNER_POLICY.md`.
