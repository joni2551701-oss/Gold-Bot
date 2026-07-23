# Platform Task Queue

Live chain. Update this file and the corresponding `TASK-XXX.md`
together whenever a status changes. Seeded from the Director's own
GoldBot Master Progress table (Phase 2 — Platform); TASK-002
(Navigation) split into sub-tasks per Director decision — Navigation
is treated as the highest-risk Platform module, so it is staged
through the full "Architecture First" workflow
(`docs/PLATFORM_WORKFLOW.md`) one step at a time.

```
TASK-001   Platform Foundation & Collaboration Infrastructure   ✅ Frozen
    ↓
TASK-002   Navigation                                           In Progress
    ├── TASK-002A  Navigation Analysis                          ✅ CLOSED
    ├── TASK-002B  Navigation Architecture                      ✅ APPROVED
    ├── TASK-002C  Navigation Registry                          ✅ FROZEN
    ├── TASK-002D  Navigation Implementation                    🟡 Conditionally Approved (CI confirmation pending)
    ├── TASK-002E  Navigation Tests (Validation)                 ⏳ Pending
    └── TASK-002F  Navigation Freeze                              ⏳ Pending
    ↓
TASK-003   Dashboard                                             Pending
    ↓
TASK-004   Settings                                               Pending
    ↓
TASK-005   Notification Center                                     Pending
```

| Task | Title | Status |
|---|---|---|
| TASK-001 | Platform Foundation & Collaboration Infrastructure | ✅ Frozen — never reopened |
| TASK-002 | Navigation (parent) | In Progress |
| TASK-002A | Navigation Analysis | ✅ CLOSED |
| TASK-002B | Navigation Architecture | ✅ APPROVED |
| TASK-002C | Navigation Registry | ✅ FROZEN (Freeze Checklist complete) |
| TASK-002D | Navigation Implementation | 🟡 Conditionally Approved — CI #158 cancelled (concurrency, superseded by #159 success); Director confirmation pending |
| TASK-002E | Navigation Tests (Validation) | ⏳ Pending, awaiting TASK-002D freeze |
| TASK-002F | Navigation Freeze | ⏳ Pending |
| TASK-003 | Dashboard | Pending |
| TASK-004 | Settings | Pending |
| TASK-005 | Notification Center | Pending |

## Rule change (ADR-001, this update)

Per `communication/decisions/ADR-001.md` and Constitution Article 13
(Future First Principle): GoldBot Platform is architected around a
Shared Platform Layer serving five equal clients (Telegram Bot,
Telegram Mini App, Android, iOS, Desktop), not Telegram Bot with
others added later. Every Architecture document from TASK-002B onward
states each component's compatibility across all five, and no
component is ever written as `Telegram Callback → Business Logic`
directly (`docs/PLATFORM_WORKFLOW.md`'s Universal UI Abstraction rule).

## Rule change (prior update)

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
