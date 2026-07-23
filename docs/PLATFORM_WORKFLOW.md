# Platform Workflow — "Architecture First"

Director-mandated, effective from TASK-002 (Navigation) onward: the
Platform Worker never writes code first. Every implementation task
follows this exact sequence — no step skipped, no step reordered.

## The 10 steps

1. **Analysis** — understand what already exists and what the task
   actually requires. No design, no code.
2. **Architecture** — propose how it should be built: shape, contracts,
   where it sits relative to existing modules (Module Reuse Principle,
   Constitution Article 11).
3. **Implementation Plan** — concrete files, functions, tests, in
   enough detail to execute without further investigation.
4. **Approval Check** — the Director reviews steps 1–3 before any code
   is written. This is the gate; skipping it is the one thing this
   workflow exists to prevent.
5. **Implementation** — write the code, exactly per the approved plan.
6. **Tests** — unit/isolation coverage, per Constitution Article 6.
7. **Documentation** — per `docs/PLATFORM_DOCUMENTATION_POLICY.md`.
8. **CI** — `pyflakes`/`compileall`/`pytest`/`python main.py`, pushed,
   confirmed `success` before anything is called "Completed"
   (`CLAUDE.md`'s existing reporting-language rule, unchanged).
9. **Freeze** — a closing record for the task (mirrors this repo's
   existing `*_FREEZE.md` convention, e.g. `docs/PHASE6_FREEZE.md`).
10. **Next Task** — pulled from `communication/task_queue/QUEUE.md`,
    never "what's next?" asked of the Director, unless the next task
    itself requires a Director brief (a new, not-yet-scoped module).

## Relationship to Constitution Article 8

Article 8 (Change Management Law) already states the whole-codebase
order: Constitution → Architecture → Roadmap → Policy → Audit → Code,
with STOP → AUDIT → Director Decision on conflicts. This workflow is
that same principle applied at task granularity for the Platform role
— it does not replace Article 8, it is Article 8's discipline made
concrete for a single Platform task instead of a whole phase.

## When a task is split into sub-tasks

A module the Director judges high-risk (e.g. Navigation, TASK-002) may
be split so each of the 10 steps — or a natural group of them — becomes
its own sub-task with its own Approval Check, rather than one task
running all 10 steps unreviewed. `communication/task_queue/TASK-002.md`
is the first example: 002A (Analysis) stops and waits for Director
review before 002B (Architecture) starts, and so on. Not every task
needs this split — the Director decides per-task whether the risk
justifies it.

## No Silent Decisions Policy

See `communication/decisions/README.md` — the specific trigger
conditions requiring a `PROPOSED-DECISION-XXXX.md` ticket and Director
sign-off before Implementation (step 5) begins.

## Universal UI Abstraction (ADR-001)

No Platform component is ever written as:

```
Telegram Callback → Business Logic
```

It is always:

```
Platform UI → Navigation Layer → Application Layer → Business Logic
```

This follows directly from `communication/decisions/ADR-001.md`:
GoldBot Platform is a Shared Platform Layer serving five equal clients
(Telegram Bot, Telegram Mini App, Android, iOS, Desktop), not Telegram
Bot with everything else bolted on later. Skipping the Navigation/
Application layers to call business logic straight from a Telegram
handler is exactly the shortcut that would need undoing once a second
platform exists.

## Future First Principle (Constitution Article 13)

Every Architecture step (step 2) states, for every component it
defines, its compatibility with all five target platforms — using
`platforms/capability_model.py`'s existing `SupportStatus` contract —
even for platforms with zero code today. See Article 13's full text
for what this does and does not require.

## Future Expansion section (mandatory in every Architecture document)

Every Architecture-step deliverable also ends with (immediately before
Director Questions):

```
## Future Expansion

AI Impact
...
Education Impact
...
Marketplace Impact
...
Enterprise Impact
...
Scalability
...
Migration Risk
...
```

Each line is a real, honest statement — "not applicable today, no such
concept exists yet" is a valid, complete answer; a speculative feature
is never invented to fill a blank. This forces every Architecture
decision to consider GoldBot's v1.0 Platform direction and beyond, not
only the task in front of it (per Director instruction, TASK-002B
review).

## Director Questions section (mandatory in every Architecture document)

Every Architecture-step deliverable (step 2's output) ends with:

```
## Director Questions

Question 1
...
Question 2
...
```

or, if nothing needs a Director decision:

```
## Director Questions

None.
```

This lets the Director see immediately, at the end of any Architecture
document, exactly where a decision is needed — without reading the
whole document to find it.

## Freeze Checklist (mandatory — defines what step 9, "Freeze," means)

A task is not "Completed" — regardless of what its own status line
says — until every box below is checked, in its own
`communication/task_queue/TASK-XXX(X).md` record:

```
Freeze Checklist
□ CI Passed
□ Tests Passed
□ Documentation Updated
□ ADR Updated (if required)
□ Constitution Impact Reviewed
□ Public Contracts Reviewed
□ Backward Compatibility Checked
□ No Silent Decisions
□ Director Approval
□ Freeze Applied
```

"ADR Updated (if required)" and "Constitution Impact Reviewed" are
allowed to be checked as *not applicable* — stated as such, never
silently skipped. Once every box is checked, that task is Frozen (per
`docs/PLATFORM_WORKFLOW.md`'s wider meaning of the word: it is never
reopened for refactoring or new features — only for a critical bug, a
security issue, a Director-approved ADR, or a future, separately
authorized Migration Task, per `communication/decisions/ADR-005.md`'s
own precedent).

## CI Supersession Rule (ADR-009 — what "CI Passed" means on the Freeze Checklist)

`ci.yml`'s `concurrency: cancel-in-progress: true` means a push
arriving before an in-flight run finishes cancels that run — this is
not a code failure, and does not by itself block a task. "CI Passed"
on the Freeze Checklist is satisfied when:

1. The prior run's only fate was cancellation-by-supersession (never
   a real failure), and
2. A later run — on the same tree, or the same tree plus only a
   non-functional change (e.g. a documentation fix) — completed with
   `success`.

That later `success` is the task's official CI validation, regardless
of which run number a task's own brief happened to name first. See
`communication/decisions/ADR-009.md` for the TASK-002D precedent this
formalizes.

## Related

- `docs/constitution/CONSTITUTION.md` Article 8, Article 11.
- `communication/task_queue/README.md` — how tasks and sub-tasks are
  tracked.
- `communication/decisions/ADR-009.md` — the CI Supersession Rule's
  full record.
- `communication/decisions/ADR-005.md` — the Migration Task rules that
  govern any future change to a Frozen task's content.
- `communication/decisions/README.md` — the No Silent Decisions Policy.
