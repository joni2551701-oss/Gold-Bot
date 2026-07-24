# Audit System

How GoldBot records who did what, and how a future Owner Mode's
runtime state will eventually be modeled (Phase 59.6: Audit &
Observability Foundation). Companion to `docs/OWNER_PERMISSIONS.md`
(who is allowed to act) and `docs/FEATURE_REGISTRY.md` (what can be
toggled).

## Scope

Observation only. Per the Director's own framing: *"Bu bosqichda bot
hali hech narsani boshqarmaydi. Faqat kuzatadi."* (In this phase the
bot doesn't control anything yet — it only observes.) Nothing here
changes `strategies/`, `decision/`, `risk/`, `execution/`,
`context/`, `signals/`, any Telegram handler, or `core/pipeline.py`.

## System State (`core/system_state.py`)

```python
class SystemState(Enum):
    RUNNING = "RUNNING"
    VALIDATION = "VALIDATION"
    MAINTENANCE = "MAINTENANCE"
    PANIC = "PANIC"
    READ_ONLY = "READ_ONLY"
```

`SystemStateRecord(state, changed_at, changed_by=None, reason=None)`
and its factory `create_system_state_record()` are the only pieces
built in this phase — an immutable record of *one* state transition.
There is no mutable "current state" holder yet, and nothing in
`core/pipeline.py` reads `SystemState` — a future, separately-approved
phase (Phase 59.9, per the Director's own roadmap) would add the
actual store and wire the pipeline's stages to check it before
running.

## Audit Log (`database/audit_log_repository.py`)

A real, persisted, append-only table — `AuditLogRepository.log_action(
actor, action, target=None, result="SUCCESS", details=None)` records
one entry; there is no update or delete method, matching an audit
log's own purpose (a record that can't be quietly edited after the
fact). `get_recent(limit=50)` and `get_by_actor(actor)` read it back,
newest first.

```
2026-07-15
owner
ENABLE_PROVIDER
BITGET
SUCCESS
```

maps to `log_action(actor="owner", action="ENABLE_PROVIDER",
target="BITGET", result="SUCCESS")`.

**Nothing calls `log_action()` automatically yet.** No owner command
in `telegram/owner/` is wired to log its own actions — that wiring
(making every real owner action actually write an entry) is future
work, the same "foundation, not full wiring" posture every module in
this phase follows.

## Relationship to the rest of Phase 59.6

```
core/system_state.py (TASK 1)        -- system-wide mode vocabulary
database/audit_log_repository.py (TASK 2) -- who did what, persisted
        |
        v
telegram/owner/owner_roles.py (TASK 3)     -- who is allowed to act
        |
        v
configuration/feature_registry.py (TASK 4) -- what can be toggled
configuration/feature_dependency_validator.py (TASK 5) -- is a toggle combination valid
        |
        v
database/config_snapshot_repository.py (TASK 6) -- point-in-time rollback capture
```

Per the Director's own roadmap, this is the last "observe only" layer
before Phase 59.7 (Runtime Feature Toggle), Phase 59.8 (Owner
Dashboard), and Phase 59.9 (Emergency Layer — where `SystemState`,
`/panic`, `/maintenance` etc. actually control `Pipeline`/`Decision`/
`Execution` for the first time).
