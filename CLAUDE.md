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
  (`telegram/handlers.py`) — handlers call a service
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
  (`telegram/owner/*.py`, `database/*_repository.py`-style), not a new
  top-level folder.

## Trading Safety

Never modify, without explicit approval for that specific change:
- **Signal logic** (`strategies/`, `signals/`).
- **Risk limits** (`risk/risk_manager.py`'s geometry/stop-loss
  validation and sizing formulas).
- **Decision flow** (`decision/decision_engine.py`'s
  confidence-blending and APPROVE/REJECT/NO_TRADE thresholds).
- **Execution rules** — `execution/` is intentionally inert (no MT5
  order calls exist yet); wiring it up is itself a change requiring
  explicit approval, not a routine addition.

Specific hard rules:
- Never bypass Risk Manager. Every signal that could reach a user
  must pass through `risk.risk_manager.RiskManager.evaluate()` —
  no shortcut path to Telegram delivery.
- Never allow AI direct execution. The AI layer (`ai/`) is advisory
  input to `decision.decision_engine.DecisionEngine` only — it must
  never itself approve/reject a trade, call the Risk Manager, or
  trigger a Telegram send or an execution action. See
  `ai/interfaces.py`'s `AIAnalyzerInterface` docstring for the
  contract this applies to any future AI provider.
- The full "why" behind this boundary — the REJECT/BLOCKED-signals-
  reaching-Telegram incident and its fix — is documented in
  `docs/AUDIT_REPORT.md` and `core/pipeline.py`'s own docstring. Read
  it before touching the notification-eligibility filter.
