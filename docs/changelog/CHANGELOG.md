# GoldBot — Changelog

Governed by `docs/constitution/CONSTITUTION.md` Article 12. One entry
per version-relevant phase, in the Director's requested format:
Version / Changes / Architecture Impact. No calendar date is recorded
per entry — this repository does not track one per phase; `git log`
against the phase's own commit is the exact record when needed.
`docs/changelog/PHASE_HISTORY.md` is the flat phase-by-phase list this
document adds Architecture Impact detail to for the phases most worth
elaborating on.

## v0.4.7 / Phase 61.7 — AI Runtime Integration

**Changes**: `RuntimeManager`, `ProviderCircuitBreaker`, `RuntimeProfile`,
`EventBus` wired into `AIService.ask()`'s real control flow.
`/runtime_status`, Runtime Self Check.

**Architecture Impact**: `AIService` became the single real
orchestration point for every AI request — no code path calls a
provider directly anymore.

## Phase 62.0 — Constitution & Architecture

**Changes**: `docs/constitution/CONSTITUTION.md` (Articles 1–7), full
`docs/architecture/` set (`ARCHITECTURE_MASTER.md`,
`MODULE_DEPENDENCIES.md`, `IMPORT_RULES.md`, `EXTENSION_GUIDE.md`),
`docs/roadmap/`, Owner/Telegram/AI architecture docs.

**Architecture Impact**: GoldBot gained a written, supreme governance
document for the first time. Every subsequent phase reads it first.

## Phase 62.2 — AI Runtime Integration Completion

**Changes**: Runtime-unhealthy audit trail, exponential retry backoff,
structured `error_type` on `PROVIDER_FAILED`, `/runtime_restart`/
`/runtime_provider`, AI Cost Protection (daily cost/token ceiling →
`DEGRADED` + Owner alert).

**Architecture Impact**: Closed the last 5 gaps between "AI Runtime
exists" and "AI Runtime is production-wired." No new architecture —
unification of what Phase 61.7 already built.

## Phase 63.0 — Senior Trading AI Foundation

**Changes**: `ai/persona/` (new), `ai/content/content_types.py`'s
`ContentType` (extended, not duplicated), `ai/explanation/explanation_output.py`
(new), `broadcast/`/`media/`/`translation/` (three genuinely new
top-level packages, foundation-only), four new `Capability` members.

**Architecture Impact**: AI Media Platform foundation created. Trading
pipeline zero diff. No real broadcast/media/translation API call
anywhere — contract-first, exactly as `docs/PHASE63_0_FREEZE.md`
declares.

## Phase 62.1 (a–d) — Governance System

**Changes**: Constitution Articles 8–12; `docs/policies/` (11 files);
`docs/architecture/` flow/pattern/naming docs (7 files) +
`docs/standards/` (6 files); `docs/ai/`/`docs/telegram/`/`docs/trading/`
documentation (14 files); `docs/VISION.md`, roadmap restructure,
`docs/changelog/` (this document + 2 siblings).

**Architecture Impact**: Zero code changed across all four sub-phases.
GoldBot gained a five-layer governance system (Constitution →
Architecture → Roadmap → Director Policy → Operational Standards) and
a full technical documentation base for `ai/`, `telegram/`, and
`trading/` — the "architecture memory" this phase's own closing note
names as its purpose.

## Platform Documentation Phase — Senior Platform Engineer Role Assignment

**Changes**: Branch `claude/trading-ai-arch-review-tgszrz` re-pointed
from the stale `main` snapshot onto this production branch (Director
decision, following an Architecture Understanding Report that first
identified the two-branch divergence — see `docs/PHASE_BRANCH_SYNC_AUDIT.md`
for the underlying audit this re-point acted on). `docs/PLATFORM_ARCHITECTURE.md`,
`docs/PLATFORM_MODULE_MAP.md`, `docs/PLATFORM_DEPENDENCY_MAP.md` (new)
— dispatch flow, permission/subscription/navigation/dashboard behavior,
file-by-file responsibility map, and import boundaries for the
Telegram Platform Layer. `docs/TECHNICAL_DEBT.md` (new) — logs `main`'s
broken `owner_snapshot.yml` workflow (references
`monitoring/run_snapshot.py`, deleted by `docs/PHASE_OWNER_SNAPSHOT_REMOVAL.md`)
as a recorded, deliberately-unfixed item. Commit `bdf44a2`; CI
(`ci.yml` run #148) confirmed `success`.

**Architecture Impact**: Zero code changed. First phase run under the
Senior Platform Engineer role split (Core → Trading Engine & AI,
Platform → Product Experience & Platform Foundation) — the Platform
Layer now has its own documented architecture/module/dependency map,
separate from and cross-referencing the pre-existing
`docs/telegram_layer.md`/`docs/telegram/TELEGRAM_ARCHITECTURE.md`
detail. See `docs/CURRENT_PHASE.md` for this phase's freeze record and
`docs/HANDOFF.md` for the state a future session/agent needs to
continue Platform work.

## PLATFORM-001 — Platform Foundation & Collaboration Infrastructure

**Changes**: New `platforms/` package (`platform_model.py`,
`platform_registry.py`, `capability_model.py`, `capability_registry.py`,
`cross_platform_checker.py`, `navigation_model.py`, `menu_registry.py`)
plus `tests/platforms/` (28 tests). New `communication/` collaboration
infrastructure — nine folders (`requests/`, `responses/`,
`notifications/`, `issues/`, `contracts/`, `reviews/`, `decisions/`,
`technical_debt/`, `task_queue/`), each with a README and template;
`task_queue/QUEUE.md` seeded with the Director's own Phase 2 —
Platform backlog. New `docs/PLATFORM_DOCUMENTATION_POLICY.md`,
`docs/PLATFORM_BUG_REPORT_STANDARD.md`, `docs/PLATFORM_CHANGELOG.md`,
`docs/PLATFORM_FOUNDATION.md`. Named `platforms/` (plural), not
`platform/`, to avoid shadowing Python's own stdlib `platform` module.

**Architecture Impact**: First real Platform implementation task
(previously documentation-only). Foundation only — no live wiring into
`telegram/`'s existing commands/keyboards/handlers, zero Trading Core
diff. Establishes the shared metadata/validation layer every future
client platform (Telegram Bot, Telegram Mini App, Android, iOS,
Desktop) will register into, plus the ticket-based process
infrastructure so cross-role (Core↔Platform) collaboration and the
Platform Worker's own task queue no longer depend on a single prose
handoff document per phase. See `docs/PLATFORM_FOUNDATION.md` for the
full module doc and `docs/CURRENT_PHASE.md` for this phase's exit
criteria.

**CI**: `ci.yml` run #150, commit `05d05c7`, conclusion `success`.
Director-approved and closed.

## Governance update — "Architecture First" workflow & No Silent Decisions Policy

**Changes**: `docs/PLATFORM_WORKFLOW.md` (new) — the mandatory 10-step
sequence (Analysis → Architecture → Implementation Plan → Approval
Check → Implementation → Tests → Documentation → CI → Freeze → Next
Task) every Platform task now follows, applying Constitution Article
8's whole-codebase change-management order at task granularity.
`communication/decisions/README.md` updated with the "No Silent
Decisions Policy" and a new `PROPOSED-DECISION-XXXX.md` ticket type
(`communication/decisions/PROPOSED_DECISION_TEMPLATE.md`) — a
folder-structure change, new public API, broken contract, database
schema change, or Core↔Platform interface change requires Director
approval via this ticket before implementation; internal refactoring,
bug fixes, and documentation are exempt.

**Architecture Impact**: Zero code changed — governance only. Director
decision, prompted by Navigation (TASK-002) being judged the
highest-risk Platform module built so far (every future client
depends on getting it right).

## TASK-002A — Navigation Analysis

**Changes**: `docs/NAVIGATION_ANALYSIS.md` (new) — records the current
Telegram-specific navigation implementation
(`platform_layer/telegram/keyboards.py`/`platform_layer/telegram/reply_keyboard_manager.py`), the
unwired foundation `platform_layer/platform_service/navigation_model.py`/`menu_registry.py`
already provide, six open questions for TASK-002B to resolve, and the
constraints (Phase 6 Freeze, No Silent Decisions Policy) any future
architecture must respect. `communication/task_queue/TASK-002.md`
split into sub-tasks 002A–002F, per Director decision to stage
Navigation instead of delivering it as one task.

**Architecture Impact**: None — analysis only, no design decision made.
Awaiting Director review before TASK-002B (Navigation Architecture)
starts.

**CI**: `ci.yml` run #151, commit `0e8f89b`, conclusion `success`.

## PLATFORM-001 — Director approval and freeze; ADR-001; Constitution Article 13

**Changes**: PLATFORM-001 marked ✅ APPROVED and FROZEN (never
reopened) following CI success on both its commits (`ci.yml` runs
#150/#151). TASK-002A (Navigation Analysis) marked ✅ APPROVED.
`communication/decisions/ADR-001.md` (new) — GoldBot Platform is
architected as a Shared Platform Layer serving five equal clients
(Telegram Bot, Telegram Mini App, Android, iOS, Desktop), not Telegram
Bot with others bolted on later; also answers TASK-002A's six open
questions directly. `docs/constitution/CONSTITUTION.md` Article 13
(Future First Principle, new) — every Architecture document states its
compatibility across all five platforms, even the four with no code
today; `docs/constitution/AMENDMENTS.md`/`ARTICLES.md` updated to
match. `docs/PLATFORM_WORKFLOW.md` extended with the Universal UI
Abstraction rule (no `Telegram Callback → Business Logic` shortcuts)
and the mandatory "Director Questions" section for every Architecture
document. `docs/changelog/DECISION_LOG.md` updated with ADR-001's
permanent ledger entry.

**Architecture Impact**: Governance only, zero code changed. Reframes
every future Platform Architecture decision: Telegram is one client
among five, not the foundation. TASK-002B (Navigation Architecture)
is the first task built under this rule.

**CI**: `ci.yml` run #152, commit `8ee86ff` — pending confirmation.

## TASK-002B — Navigation Architecture

**Changes**: `docs/NAVIGATION_ARCHITECTURE.md` (new) — 13 components
(Screen Model, Navigation Graph, Route Registry, Back Stack, Deep Link
System, Permission Layer, Platform Adapter, Navigation State, Session
Navigation, Navigation Events, Screen Lifecycle, Platform Capability
Mapping, plus the Universal Navigation umbrella), each with a
cross-platform compatibility table (Constitution Article 13) and a
proposed design extending TASK-001's existing foundation
(`platform_layer/platform_service/navigation_model.py`/`menu_registry.py`/`capability_model.py`)
rather than replacing it. Ends with 6 Director Questions — no design
decision in this document is final until those are answered.

**Architecture Impact**: None yet — design only, zero code, zero API,
zero folder-structure change. Awaiting Director review before
TASK-002C (Navigation Registry) starts.

**CI**: `ci.yml` run #153, commit `8de03f3`, conclusion `success`.

## Navigation Architecture approved; ADR-002/003/004; TASK-002C authorized

**Changes**: TASK-002B marked ✅ APPROVED following Director resolution
of its 6 Director Questions — `docs/NAVIGATION_ARCHITECTURE.md`
updated with a "Director Decisions" section (Navigation Stack with no
Telegram exception; Platform Adapter touches UI only; Route Registry
is dynamic; Permission Layer runs before Navigation; Deep Link System
covers all five platforms; Navigation State lives in the Platform
Layer, never the Business Layer) and a new "Future Expansion" section
(AI/Education/Marketplace/Enterprise Impact, Scalability, Migration
Risk). Three new ADRs: `communication/decisions/ADR-002.md` (Universal
Screen Identity — one dotted ID per screen, stable across every
platform), `ADR-003.md` (a platform never creates a Screen, only calls
Navigation), `ADR-004.md` (Navigation Event Bus vocabulary — interface
only, no dispatch). All three folded into
`docs/changelog/DECISION_LOG.md`. `docs/PLATFORM_WORKFLOW.md` extended
with the mandatory "Future Expansion" section for every future
Architecture document. TASK-002C (Navigation Registry) 🟢 AUTHORIZED
under a specific rule list (no hardcode, no `telegram/` dependency, no
platform-specific code, Universal Screen ID, dynamic Registry, Event
Bus interface only, extensible for not-yet-built future modules).

**Architecture Impact**: Governance and design resolution only, zero
code changed in this entry. Sets the exact shape TASK-002C's real
implementation must follow.

## TASK-002C — Navigation Registry

**Changes**: `platform_layer/platform_service/navigation_model.py` — `is_valid_screen_id()`
(ADR-002 validator, not enforced retroactively on TASK-001's frozen
registrations) and `NavigationNode.category`/`content_type` (additive
fields, Screen Model). `platform_layer/platform_service/menu_registry.py` —
`MenuDefinition.target_bindings` (additive field, Route Registry) and
`DEFAULT_MENUS`/`build_default_menu_registry()`: a read-only mirror of
GoldBot's real, live 25 Telegram screens under Universal Screen IDs
with real `"/command"` target bindings — no fictitious AI/Education/
Marketplace/Trading entries. `platform_layer/platform_service/navigation_events.py` (new) —
`NavigationEventType`/`NavigationEvent`, the ADR-004 Event Bus
vocabulary, interface only, no dispatcher. 15 new tests
(`tests/platforms/`, 39 total). `docs/PLATFORM_FOUNDATION.md` updated
per the Documentation Policy.

**Architecture Impact**: First real Platform code since PLATFORM-001.
Zero diff to Trading Core or any `telegram/*.py` file —
`platform_layer/telegram/reply_keyboard_manager.py`'s live behavior is completely
unchanged; the Registry is a parallel, unwired mirror, per ADR-003.
Full suite: 4648 passed.

**CI**: `ci.yml` run #155, commit `4784a18`, conclusion `success`.

## TASK-002C frozen; ADR-005; Freeze Checklist; TASK-002D authorized

**Changes**: TASK-002C marked ✅ APPROVED and **Frozen** — full Freeze
Checklist recorded in `communication/task_queue/TASK-002C.md`.
`communication/decisions/ADR-005.md` (new) — Universal Screen Identity
Migration is its own, separately-scoped Migration Task: no silent
migration, frozen tasks not modified, mandatory Backward Compatibility
and Rollback plans; folded into `docs/changelog/DECISION_LOG.md`.
`docs/PLATFORM_WORKFLOW.md` extended with the mandatory **Freeze
Checklist** — the formal definition of step 9 ("Freeze"): 10 boxes
(CI Passed, Tests Passed, Documentation Updated, ADR Updated,
Constitution Impact Reviewed, Public Contracts Reviewed, Backward
Compatibility Checked, No Silent Decisions, Director Approval, Freeze
Applied) that must all be checked before a task counts as
"Completed." TASK-002D (Navigation Implementation) 🟢 AUTHORIZED with
an explicit permitted/forbidden scope
(`communication/task_queue/TASK-002D.md`). Director order recorded: no
action on PR #2 (base `main`) — not merged, closed, or reviewed; its
own separate review process.

**Architecture Impact**: Governance only, zero code changed in this
entry. TASK-002C is now permanently closed to refactoring — only a
critical bug, security issue, Director-approved ADR, or future
Migration Task can touch it again.

**CI**: `ci.yml` run #157, commit `00bc826`, conclusion `success`.

## TASK-002D — Navigation Implementation

**Changes**: `platform_layer/platform_service/navigation_core.py` (new) — `NavigationCore`
(Registry lookup + Permission Flow `Request → Permission → Navigation
→ Screen` + per-session Navigation State, a real stack with no
Telegram exception + Event Interface via `NavigationResult`/
`NavigationEvent`), `has_sufficient_permission()` (platform-agnostic
tier rank comparison). `platform_layer/platform_service/platform_adapter.py` (new) —
`PlatformAdapterBase`, an abstract interface only, no concrete
per-platform subclass. 12 new tests (`tests/platforms/`, 51 total).
`docs/PLATFORM_FOUNDATION.md` updated per the Documentation Policy.

**Architecture Impact**: First orchestration code in `platforms/` —
composes TASK-001/002C's Registry and Event contracts into a real,
tested Navigation Core, still fully unwired (no `telegram/*.py` file
imports it). Zero diff to Trading Core or any `telegram/*.py` file.
Full suite: 4660 passed.

**CI**: run #157 success (governance commit); run #158 (this commit's
own content, `b366971`) shows `cancelled` — superseded by the very
next push before it finished (GitHub's `concurrency:
cancel-in-progress: true` on `ci.yml`), not a code failure; run #159
(`8adf53b`, same tree plus one non-code line) completed `success`.

## TASK-002D architecture review; ADR-006/007/008; TASK-002E scoped

**Changes**: Director reviewed and approved TASK-002D's architecture
(Navigation Core, Platform Adapter, Tests) — status 🟡 Conditionally
Approved pending final CI confirmation (see CI note above).
`communication/decisions/ADR-006.md` (Navigation Transaction — every
Navigation operation is Start→Permission→Resolve Route→Update
Stack→Emit Events→Commit, with rollback on any stage failing),
`ADR-007.md` (Navigation Context — every screen navigation carries
`screen_id`/`session_id`/`parameters`/`source`/`timestamp`/
`navigation_reason`, not just a screen id), `ADR-008.md` (Navigation
Result — a fixed outcome vocabulary, `SUCCESS`/`BLOCKED`/`NOT_FOUND`/
`PERMISSION_DENIED`/`FAILED`/`REDIRECTED`, never a plain boolean) — all
three folded into `docs/changelog/DECISION_LOG.md`, all three
explicitly governing **future** Navigation work, not retroactively
applied to TASK-002D's own already-approved code in this cycle.
`communication/task_queue/TASK-002E.md` scoped: Navigation Validation
(stress tests, edge cases, session recovery, stack consistency,
invalid route handling, permission failures, event validation,
multi-session isolation) — Pending, starts after TASK-002D's freeze.

**Architecture Impact**: Governance only, zero code changed. Sets the
direction for Navigation's next maturity level without rewriting what
was just reviewed.

**CI**: `ci.yml` run #160, commit `954ee42`, conclusion `success` —
Director-confirmed, ADR-006/007/008 accepted.

## Engineering track established; DEVOPS-001 recorded and blocked

**Changes**: Following the observation that a documentation-only
commit (run #160) still ran the full ~2-minute, 4660+-test suite, the
Director proposed and then formalized a separate **Engineering**
roadmap (`DEVOPS-XXX`), sequenced independently from **Platform
Tasks** (`TASK-XXX`) so neither interrupts the other — the reserved
`TASK-003` (Dashboard) slot is not displaced.
`communication/task_queue/DEVOPS-001.md` (Smart CI Routing — routes CI
into Documentation/Platform/Trading/Full-Regression pipelines by
changed path) recorded with its full scope and five mandatory
pre-start deliverables (current Actions map, per-pipeline trigger
conditions, path→pipeline table, measured time savings, regression
risk); `DEVOPS-002.md`/`003.md`/`004.md` (Release Pipeline, Branch
Protection, Build Optimization) stubbed, not yet scoped.
`communication/task_queue/QUEUE.md`/`README.md` updated with the
two-track structure.

**Architecture Impact**: Roadmap organization only, zero code changed.
DEVOPS-001 is explicitly **Blocked** until Navigation Foundation
(TASK-002E + TASK-002F) is complete — no `.github/workflows/*.yml`
file is touched now or at DEVOPS-001's own start without those five
deliverables reviewed first.

**CI**: `ci.yml` run #161, commit `d3bd60e`, conclusion `success`.

## ADR-009 (CI Supersession Rule); TASK-002D frozen; TASK-002E authorized

**Changes**: `communication/decisions/ADR-009.md` (new) — a CI run
cancelled only by a superseding push (never a real failure) is
resolved by that later run's `success`, which becomes the official
validation; folded into `docs/changelog/DECISION_LOG.md` and
`docs/PLATFORM_WORKFLOW.md`'s Freeze Checklist section. Applied
immediately: TASK-002D marked ✅ **APPROVED and Frozen** — run #158's
cancellation-by-supersession is resolved by run #159's `success`, full
Freeze Checklist recorded in `communication/task_queue/TASK-002D.md`.
Navigation Foundation's pause lifted. TASK-002E (Navigation Tests /
Validation) 🟢 authorized with explicit scope (Navigation Validation,
Edge Cases, Stack Consistency, Multi-session/Permission/Event
Validation, Recovery Scenarios, Integration Validation — forbidden:
architecture redesign, contract changes, Trading Core, concrete
Platform Adapter implementation).

**Architecture Impact**: Governance only, zero code changed. Closes
the last open question from TASK-002D's review and unblocks Navigation
Foundation's final two steps.

## TASK-002E — Navigation Tests (Validation) delivered

**Changes**: `tests/platforms/test_navigation_validation.py` (new, 29
tests) — Navigation Validation, Edge Cases/Invalid Route Handling,
Stack Consistency, Multi-session Validation (20 sessions, interleaved
ops), Permission Validation (full USER/ADMIN/OWNER rank matrix),
Event Validation, Recovery Scenarios (after repeated failures),
Integration Validation (`NavigationCore` + `build_default_menu_registry()`
+ a test-only `PlatformAdapterBase` subclass composed end-to-end), and
a stress test (50 sessions × 20 ops each). `docs/PLATFORM_FOUNDATION.md`'s
Testing section updated to reflect 80 total tests
(28 PLATFORM-001 + 11 TASK-002C + 12 TASK-002D + 29 TASK-002E).

Zero changes to `platform_layer/platform_service/navigation_core.py`, `platform_layer/platform_service/platform_adapter.py`,
`platform_layer/platform_service/navigation_events.py`, or `platform_layer/platform_service/menu_registry.py` — all
Frozen contracts stayed exactly as TASK-002D left them.

**Validation finding surfaced, not fixed**: `has_sufficient_permission()`
ranks an unrecognized *required* tier at -1, so any real user tier
(rank ≥0) satisfies "≥ -1" — making the function permissive rather than
restrictive for a malformed/empty *required*-tier input specifically
(the *user*-tier direction correctly fails closed). Not exploitable
today since every `DEFAULT_MENUS` entry's `permission` is independently
validated to be exactly USER/ADMIN/OWNER. Documented in
`tests/platforms/test_navigation_validation.py` and
`docs/PLATFORM_FOUNDATION.md`; left for a future authorized fix since
`navigation_core.py` is Frozen — raised here for Director awareness
under the No Silent Decisions Policy, not self-authorized.

**Architecture Impact**: Test-depth only, zero production code changed,
zero Trading Core/`telegram/`/`.github/` diff.

## ADR-010/011 (Fail Closed Permission Policy; Security Review Layer); TASK-002E frozen; TASK-002F authorized (expanded)

**Changes**: `communication/decisions/ADR-010.md` (new) — every
permission check must fail closed on an unknown/invalid/missing/
malformed value, on either side of the comparison.
`communication/decisions/ADR-011.md` (new) — every task touching
Permission/Authentication/Authorization/Session/Navigation code must
include a Security Review section (Attack Surface, Failure Modes, Fail
Open/Fail Closed, Abuse Scenarios, Recommendations) in its report; both
folded into `docs/changelog/DECISION_LOG.md` and
`docs/PLATFORM_WORKFLOW.md`. TASK-002E marked ✅ **APPROVED and
Frozen** — full Freeze Checklist recorded in
`communication/task_queue/TASK-002E.md`. The `has_sufficient_permission()`
finding is classified by Director decision as a Potential Security
Weakness (not a routine bug) and recorded as a Security Backlog entry
in `docs/TECHNICAL_DEBT.md` — no code change applied; deferred to a
future, separately-authorized Security Task. TASK-002F re-scoped by
Director order from "Navigation Freeze" to a full **Navigation
Foundation Final Audit** (Architecture/Code/Documentation/Test/Future/
Security Audit — see `communication/task_queue/TASK-002F.md`) and
🟢 authorized to start.

**Architecture Impact**: Governance only, zero code changed. If
TASK-002F's audit succeeds, Navigation Foundation (Phase 1 of Platform
Foundation) will be declared COMPLETE and Production Ready, unblocking
DEVOPS-001.

## Related

- `docs/changelog/PHASE_HISTORY.md` — the flat, complete phase list.
- `docs/changelog/DECISION_LOG.md` — the reasoning behind the
  load-bearing decisions in the phases above.
