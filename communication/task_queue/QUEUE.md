# Platform Task Queue

Live chain. Update this file and the corresponding `TASK-XXX.md`
together whenever a status changes. Seeded from the Director's own
GoldBot Master Progress table (Phase 2 — Platform); TASK-002
(Navigation) split into sub-tasks per Director decision — Navigation
is treated as the highest-risk Platform module, so it is staged
through the full "Architecture First" workflow
(`docs/PLATFORM_WORKFLOW.md`) one step at a time.

```
TASK-001   Platform Foundation & Collaboration Infrastructure   Completed
    ↓
TASK-002   Navigation                                           In Progress
    ├── TASK-002A  Navigation Analysis                          Delivered, awaiting review
    ├── TASK-002B  Navigation Architecture                      Pending (needs 002A approval)
    ├── TASK-002C  Navigation Registry                          Pending
    ├── TASK-002D  Navigation Implementation                    Pending
    ├── TASK-002E  Navigation Tests                              Pending
    └── TASK-002F  Navigation Freeze                              Pending
    ↓
TASK-003   Dashboard                                             Pending
    ↓
TASK-004   Settings                                               Pending
    ↓
TASK-005   Notification Center                                     Pending
```

| Task | Title | Status |
|---|---|---|
| TASK-001 | Platform Foundation & Collaboration Infrastructure | Completed (CI `success`, `ci.yml` run #150, commit `05d05c7`) |
| TASK-002 | Navigation (parent) | In Progress |
| TASK-002A | Navigation Analysis | Delivered, awaiting Director review |
| TASK-002B | Navigation Architecture | Pending |
| TASK-002C | Navigation Registry | Pending |
| TASK-002D | Navigation Implementation | Pending |
| TASK-002E | Navigation Tests | Pending |
| TASK-002F | Navigation Freeze | Pending |
| TASK-003 | Dashboard | Pending |
| TASK-004 | Settings | Pending |
| TASK-005 | Notification Center | Pending |

## Rule change (this update)

Per Director decision: every future task (not just Navigation) follows
the mandatory 10-step "Architecture First" workflow
(`docs/PLATFORM_WORKFLOW.md`) — Analysis → Architecture →
Implementation Plan → Approval Check → Implementation → Tests →
Documentation → CI → Freeze → Next Task. A task that touches a new
public API, a folder-structure change, a broken contract, a database
schema change, or the Core↔Platform interface additionally requires a
`communication/decisions/PROPOSED-DECISION-XXXX.md` ticket and Director
approval before Implementation starts (`communication/decisions/README.md`'s
"No Silent Decisions Policy"). Internal refactoring, bug fixes, and
documentation are exempt from that specific ticket requirement.
