# GoldBot Development Rules

Engineering governance for any Claude/AI agent (or human) working in
this repository. GoldBot is a semi-automatic XAUUSD trading-signal
bot — read this before making any change, not after.

## Architecture Rules

- Respect existing layers: `data/ -> context/ -> strategies/ ->
  signals/ -> ai/ -> decision/ -> risk/ -> telegram/ -> database/`
  (see `docs/ARCHITECTURE.md` for the full diagram). A layer talks to
  the layer immediately below it, never reaches two layers down.
- No direct database access from Telegram handlers
  (`platform_layer/telegram/handlers.py`) — handlers call a service
  (`telegram/*_service.py`), services call a repository
  (`database/*_repository.py`). This is enforced today; keep it that
  way.
- Services own business logic. Repositories own SQL only — no
  business rule belongs in a `database/*_repository.py` file (a
  handful of pre-existing exceptions are documented in
  `docs/SECURITY.md`/`docs/AUDIT_REPORT.md`; don't add new
  ones).
- Keep modules isolated: `strategies/` doesn't import `telegram/`,
  `ai/` doesn't import `database/`, etc. If a change requires a new
  cross-layer import, stop and check whether that's actually correct
  before adding it.

## Before Code Changes

1. Read architecture docs — `docs/ARCHITECTURE.md`, the relevant
   module's `README.md` (`data/README.md`, `context/README.md`,
   `signals/README.md`, `decision/README.md`, `risk/README.md`,
   `execution/README.md`, `database/README.md`, `telegram/README.md`,
   `ai/README.md`), and any `docs/*.md` covering the area.
2. Check dependencies — what imports the file you're about to change,
   and what does it import. A quick `grep` before editing is cheaper
   than a regression after.
3. Do not break the pipeline — `core/pipeline.py`'s
   Data→Context→Signal→AI→Decision→Risk→Telegram flow (see
   `docs/ARCHITECTURE.md`'s Data Flow diagram) must keep working
   exactly as documented; if a change touches it, re-read
   `docs/AUDIT_REPORT.md` first.
4. Add tests — `tests/` (plus `tests/unit/`, `tests/integration/`,
   `tests/security/`, `tests/performance/`, `tests/ai/`) almost
   certainly already covers the area; read the relevant test file
   before assuming behavior, and add a new test for any new behavior.
5. Run validation — see "After Code Changes" below; do this before
   reporting a change as done, not after.

## After Code Changes — Commit Protocol (mandatory)

In force from this rule's own introduction onward — added after two
separate incidents (Phase 59.9, Phase 60.0/60.1) where a post-staging
edit (fixing a `pyflakes` finding) was never re-staged before the
commit, so a commit that looked locally clean actually still failed
CI. The root cause both times was the same: `pyflakes`/tests were run
against a state that didn't match what `git commit` actually captured.
This exact order closes that gap — do not skip or reorder these
steps:

1. `git add -A` — stage everything first, before any validation.
2. `python -m pyflakes $(git ls-files '*.py')` — must report nothing.
   Run this *after* `git add -A` (step 1), not before — `git ls-files`
   only lists tracked files, so pyflakes run too early silently skips
   anything not yet staged.
3. **If step 2 changed even one line** (a lint fix, or any other
   edit) — go back to step 1 (`git add -A` again) before continuing.
   This is the loop that closes the actual bug behind both prior
   incidents: a fix made after staging is invisible to everything
   downstream until it is re-staged. Do not proceed past this step
   with any unstaged change outstanding.
4. `python -m compileall .` — must pass.
5. `python -m pytest tests/` — must pass, including whatever you just
   touched.
6. `python main.py` (or the project's own smoke-run equivalent) —
   confirm no new runtime error; compare log output shape against the
   pre-change baseline when touching anything pipeline-adjacent.
7. `git status` — **must be clean** (no unstaged/untracked changes
   remaining outside what's staged). **If it is not clean, committing
   is forbidden** — return to step 1.
8. `git diff --cached` — review exactly what is about to be
   committed, one last time.
9. Commit.
10. Push.
11. Confirm GitHub Actions reports `success` for the pushed commit
    before reporting the phase as done — see "Reporting language"
    below.

### Reporting language (mandatory)

Do not use the words **"Complete"**, **"Validated"**, **"Production
Ready"**, or **"All checks passed"** until GitHub Actions has actually
returned `success` for the exact commit being reported on. Before that
confirmation arrives, say exactly:

    Local validation passed. Waiting for GitHub Actions confirmation.

Only after CI confirms:

    GitHub Actions: SUCCESS. Phase complete.

### Pre-Commit Verification checklist (mandatory report section)

Every response that commits and pushes a change must include this
checklist, unskipped, reflecting what was actually done for that
specific commit:

    Pre-Commit Verification
    ✓ git add -A
    ✓ pyflakes
    ✓ compileall
    ✓ pytest
    ✓ python main.py
    ✓ git status clean
    ✓ git diff --cached reviewed
    ✓ GitHub Actions SUCCESS

Report changed files — every response should end with an explicit
list of what changed and why, not just "done."

## Restrictions

- No unnecessary refactor. A bug fix doesn't need surrounding
  cleanup; a foundation phase doesn't need a big migration. If a
  change looks like it's growing past "minimal," stop and report
  instead of pushing through.
- No breaking changes. Existing public method signatures
  (`RiskManager.evaluate()`, `TradingPipeline.run()`,
  `UserRepository.get_user()`, etc.) stay stable unless a task
  explicitly asks for a signature change.
- No duplicate logic. Before writing a new helper, check whether one
  already exists (this codebase has caught and removed several
  duplicates across its Phase 49/50 cleanup passes — don't reintroduce
  the pattern).
- **Module Reuse Principle** (mandatory, in force from the Phase 59
  Architecture Freeze / Phase 60.0 Architecture Audit onward — see
  `docs/PHASE59_ARCHITECTURE_FREEZE.md`'s "Design principle" section
  and `docs/PHASE60_ARCHITECTURE_AUDIT.md` for the audit that
  established it). Before creating any new module — a new file, a new
  package/folder, or a new top-level class/function in an existing
  file — answer these in order and stop at the first "yes":
  1. Does this already exist somewhere in the repo?
  2. Can an existing module be extended (a new method, a new optional
     field, a new function in an existing file) without breaking its
     current contract?
  3. Only if both are "no": create a new module, and document in its
     own docstring why steps 1 and 2 were both "no".
  Reuse is the default outcome, not the exception. A new top-level
  package is the highest-cost option and should be rare — most work
  should land as a new file inside an *existing* package
  (`platform_layer/telegram/owner/*.py`, `database/*_repository.py`-style), not a new
  top-level folder.

## Trading Safety

Never modify, without explicit approval for that specific change:
- **Signal logic** (`strategies/`, `signals/`).
- **Risk limits** (`risk_layer/risk_engine/risk_manager.py`'s geometry/stop-loss
  validation and sizing formulas).
- **Decision flow** (`decision_layer/decision_engine/decision_engine.py`'s
  confidence-blending and APPROVE/REJECT/NO_TRADE thresholds).
- **Execution rules** — `execution/` is intentionally inert (no MT5
  order calls exist yet); wiring it up is itself a change requiring
  explicit approval, not a routine addition.

Specific hard rules:
- Never bypass Risk Manager. Every signal that could reach a user
  must pass through `risk_layer.risk_engine.risk_manager.RiskManager.evaluate()` —
  no shortcut path to Telegram delivery.
- Never allow AI direct execution. The AI layer (`ai/`) is advisory
  input to `decision_layer.decision_engine.decision_engine.DecisionEngine` only — it must
  never itself approve/reject a trade, call the Risk Manager, or
  trigger a Telegram send or an execution action. See
  `ai_layer/ai_service/interfaces.py`'s `AIAnalyzerInterface` docstring for the
  contract this applies to any future AI provider.
- The full "why" behind this boundary — the REJECT/BLOCKED-signals-
  reaching-Telegram incident and its fix — is documented in
  `docs/AUDIT_REPORT.md` and `core/pipeline.py`'s own docstring. Read
  it before touching the notification-eligibility filter.

## Deployment Authority — Director Order No. 021 (Deployment Authority — Worker as Deployment/DevOps Engineer)

The Director's own framing, stated explicitly: **the Worker is not a
VPS Administrator — the Worker performs the role of Deployment
Engineer / DevOps Engineer.** This section is the authoritative
boundary on what the Worker may do unilaterally for deployment; both
`docs/DEPLOYMENT.md` and `docs/deployment/PRODUCTION_DEPLOYMENT.md`
point here rather than duplicating it.

**Phase 1 (recommended) — Semi-autonomous.** Worker may do all of:
connect to the VPS, clone/pull the repository, create a virtual
environment, install dependencies, verify `.env` (checking
presence/shape, never changing values), run migrations, run tests, run
a smoke test, create or update the systemd service, configure Nginx if
needed, check logs, start monitoring, fix errors, and prepare a
deployment report.

Worker must **NOT**, even in Phase 1:
- change production API keys,
- change DNS,
- change firewall rules, or
- enable production trading.

**Phase 2 (later, after Development is complete) — Fully autonomous,
Production-level — not yet in effect, Development must complete
first.** Worker additionally does: CI/CD-driven deploy, Blue/Green
deployment, rollback, health check, auto-restart, monitoring, hotfix
deploy, release deploy.

**Always requires Director Approval, regardless of phase** (these sit
above both Phase 1 and Phase 2 — the Worker never gets autonomous
authority over them):
- replacing a Production API Key,
- replacing the server,
- changing the VPS provider,
- a database reset,
- changing firewall policy,
- replacing an SSL certificate,
- enabling/disabling Live Trading,
- deleting production data.

**Future-state target pipeline** (recorded verbatim as the Director
specified it; this is the eventual Phase 2 flow, not the current
state):

```
Git Push → Worker → CI/CD → VPS → Deploy → Health Check → Monitoring → Report
```

## Worker Authority — Director Order No. 016 (Worker Authority Expansion)

From this order onward the Worker is the System Owner of each module it
touches — responsible for that module's quality, consistency,
extensibility, and stability, not just the task in front of it. The
overriding goal is 100% fidelity to the Canonical Architecture
documents (`ARCHITECTURE.md` and the rest of the architecture set).

**Permitted without asking the Director first** (still subject to
every other rule in this file — Trading Safety, Module Reuse
Principle, the Commit Protocol below, and MIR-001/SMR-001/GEL-001):

- Autonomous Bug Fix — find, fix, add a regression test, update the
  Changelog.
- Performance Optimization — caching, lazy loading, query/algorithm/
  memory optimization, as long as the public API and external
  behavior are unchanged.
- Internal Refactoring — split classes/functions, add helpers or
  utilities, remove duplicate logic, simplify — inside a module's
  existing boundary, never crossing a Layer contract.
- Documentation Evolution — keep README/CONTRACTS/MODULE_MAP/
  IMPLEMENTATION/ROADMAP/WORK_LOG/CHANGELOG in sync with the code.
- Test Evolution — add or update unit/integration/regression tests,
  mocks, fixtures.
- Code Quality — typing, docstrings, naming, lint, formatting, import
  cleanup.
- Dependency Cleanup — unused imports, dead code, duplicate classes/
  functions, unnecessary dependencies.
- Module Expansion — split an oversized/hard-to-manage module into
  packages/submodules/helpers/services/engines, provided the Canonical
  Architecture (Layer boundaries, ownership) is not broken.
- Backlog Management — the Worker keeps its own Critical/Major/Minor/
  Future backlog.
- Continuous Self Review — at the end of each Sprint, the Worker runs
  its own consistency, regression, architecture, and dependency
  audits; the Director receives only the final Consolidated Report.
- Development Planning — at the end of each Sprint, the Worker
  prepares next Sprint's Task/Risk/Dependency/Estimate plan.
- Autonomous Root Cause Analysis (ARCA) — every real error goes
  through Problem → Root Cause Analysis → Permanent Solution →
  Validation → Lessons Learned. Temporary fixes/workarounds are
  forbidden; apply a permanent fix wherever possible.

**Director Review is still required** whenever a change touches: Layer
Architecture, the Pipeline, Trading Logic, AI Logic, Decision Logic,
Risk Logic, a public-API breaking change, Ownership, a Canonical
Contract, or a Foundation Rule. Everything else is the Worker's
independent technical call.

**Decision Memory** — the Worker tracks every WAR/WDR/MIR/RAR/GEL/DD
decision (see `Architecture_Audit_Plan.md` and `DIRECTOR_DECISIONS.md`
at repo root). A decision approved once is never re-asked.

**Where this is recorded** (Director's own filing scheme for Order No.
016, mapped onto files that already exist per this repo's Module
Reuse Principle rather than creating new top-level docs):
- `ARCHITECTURE.md` — the unchanging system architecture (stands in
  for "01_Ecosystem_Architecture.md").
- `CLAUDE.md` (this file) — Worker operating rules and authority;
  Director Order No. 016 itself lives here.
- `DIRECTOR_DECISIONS.md` (repo root) — append-only log of every
  Director-approved decision (WAR/WDR/MIR/RAR/GEL/DD/Order).
- Each module's own `WORK_LOG.md` — that module's own completed work,
  problems, and fixes (per-module logs already exist repo-wide as of
  the GoldBot Engineering Standard v1.0 rollout).

## Governance Chain

Director Orders No. 018 (`RFC_STANDARD.md`), 019 (`ADR_STANDARD.md`),
and 020 (`RELEASE_MANAGEMENT_STANDARD.md`) sit on top of the process
already established above. The full governance chain, exactly as
described by the Director, one line each for what it governs:

1. **Architecture Standard** (`ARCHITECTURE.md`) — how the system is
   built.
2. **Engineering Standard** — how the project is engineered and
   managed.
3. **Development Standard** (`GOLDBOT_DEVELOPMENT_STANDARD.md`, GDS)
   — how code is written.
4. **RFC Standard** (`RFC_STANDARD.md`) — how large changes are
   proposed.
5. **ADR Standard** (`ADR_STANDARD.md`) — why a particular decision
   was made, preserved as permanent record.
6. **Release Management Standard** (`RELEASE_MANAGEMENT_STANDARD.md`)
   — how a product is released.

Each standard governs a distinct question and none replaces another:
Architecture answers "how is the system built," Engineering answers
"how is the project managed," Development answers "how is code
written," RFC answers "how are large changes proposed," ADR answers
"why was this particular decision made," and Release Management
answers "how is a product released."
