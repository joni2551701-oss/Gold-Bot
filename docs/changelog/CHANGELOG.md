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
(`telegram/keyboards.py`/`telegram/reply_keyboard_manager.py`), the
unwired foundation `platforms/navigation_model.py`/`menu_registry.py`
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

## Related

- `docs/changelog/PHASE_HISTORY.md` — the flat, complete phase list.
- `docs/changelog/DECISION_LOG.md` — the reasoning behind the
  load-bearing decisions in the phases above.
