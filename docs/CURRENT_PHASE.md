# GoldBot — Current Phase

Living pointer to whatever phase is presently open. Updated at the
close of each phase to reflect the phase that just froze and, where
known, what's authorized to start next. `docs/changelog/CHANGELOG.md`
and `docs/changelog/PHASE_HISTORY.md` are the permanent record; this
document is only ever the current tip.

## Phase: Platform Foundation & Collaboration Infrastructure (PLATFORM-001)

**Status: IN PROGRESS.** Type: Foundation phase — new `platforms/`
package (data models, registries, a validator) and a new
`communication/` process infrastructure, plus four new docs. Zero
Trading Core diff; nothing wired into any existing `telegram/*.py`
file's live behavior. Will be marked `FROZEN` once GitHub Actions
confirms `success` on the commit closing this phase, per this
project's own reporting-language convention.

### Scope authorized by the Director

1. `platforms/` — Platform Registry, Universal Navigation model,
   Universal Menu Registry, Platform Capability System, Cross Platform
   Checker (foundation only, no live wiring).
2. `communication/` — nine collaboration folders (requests/responses/
   notifications/issues/contracts/reviews/decisions/technical_debt/
   task_queue), each with a README and template.
3. `docs/PLATFORM_DOCUMENTATION_POLICY.md`,
   `docs/PLATFORM_BUG_REPORT_STANDARD.md`, `docs/PLATFORM_CHANGELOG.md`.
4. A Platform Task Queue (`communication/task_queue/QUEUE.md`) seeded
   with the Director's own Phase 2 — Platform backlog (Navigation,
   Dashboard, Settings, Notification Center), so Platform stops asking
   "what's next?" after this task.

### Exit criteria

| Criterion | Result |
|---|---|
| `platforms/` foundation created, tested | ✅ 7 modules, `tests/platforms/` (28 tests passing) |
| `communication/` infrastructure created | ✅ 9 folders + task queue, each with README + template |
| Documentation Policy, Bug Report Standard, Platform Changelog written | ✅ `docs/PLATFORM_DOCUMENTATION_POLICY.md`, `docs/PLATFORM_BUG_REPORT_STANDARD.md`, `docs/PLATFORM_CHANGELOG.md` |
| Cross-platform policy encoded, not just described | ✅ `platforms/capability_model.py` + `platforms/cross_platform_checker.py`, both tested |
| Trading Core zero-diff | ✅ every file changed is under `platforms/`, `communication/`, `docs/`, `tests/platforms/` |
| CI passed | pending — see Status above |
| README/standard docs present for every new folder | ✅ |

### Role boundary reaffirmed by this phase

Per `docs/HANDOFF.md`'s role split: **Core** (Trading Engine & AI) is
untouched — no file under `context/`, `strategies/`, `signals/`,
`decision/`, `risk/`, `ai/`, or `core/pipeline.py` was modified.
**Platform** (Product Experience & Platform Foundation) gains its
first real implementation, still foundation-only per the Director's
own framing: infrastructure and process first, live features after.

## Previous phase

**Platform Documentation** (Senior Platform Engineer role
assignment) — FROZEN, CI `success` confirmed (`ci.yml` run #149,
commit `00e3f4a`). Full record: `docs/changelog/CHANGELOG.md`'s
"Platform Documentation Phase" entry.

## Next

`communication/task_queue/QUEUE.md` — TASK-002 (Navigation) is next,
Pending a dedicated Director brief. Until then, Trading Core, Decision
Engine, Risk Manager, and Signal/Context Engine remain off-limits to
this role.

## Related

- `docs/HANDOFF.md` — the Core/Platform role split and how to pick up
  Platform work.
- `docs/changelog/CHANGELOG.md` — the permanent phase-level record.
- `docs/PLATFORM_FOUNDATION.md` — this phase's `platforms/` module doc.
- `communication/README.md`, `communication/task_queue/QUEUE.md` —
  this phase's collaboration infrastructure and live task chain.
- `docs/TECHNICAL_DEBT.md` — the one open item from the prior phase,
  still unresolved (out of scope for this one too).
