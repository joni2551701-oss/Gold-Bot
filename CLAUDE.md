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

## After Code Changes

1. Run `python -m compileall .` — must pass.
2. Run `python -m pytest tests/` — must pass, including whatever you
   just touched.
3. Check imports — `python -m pyflakes $(git ls-files '*.py')` must
   report nothing; also worth a full module import sweep (see
   `.github/workflows/ci.yml` for the exact command) to catch a
   circular import.
4. Report changed files — every response should end with an explicit
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
