# GoldBot Development Rules

Naming, testing, commit, and review conventions actually followed
throughout this codebase's history — this document describes existing
practice, it doesn't invent a new one. See `CLAUDE.md` for the
higher-level architecture/safety rules this document's conventions
support.

## Naming Convention

- **Files**: `snake_case.py`, matching the primary class/responsibility
  it holds (`risk_manager.py` holds `RiskManager`,
  `user_repository.py` holds `UserRepository`).
- **Classes**: `PascalCase` (`RiskManager`, `SignalCandidate`,
  `TradingPipeline`). Zero exceptions found in a full-repo audit
  (Phase 48).
- **Functions/methods**: `snake_case` (`get_user_profile()`,
  `calculate_risk()`, `evaluate()`).
- **Constants**: `UPPER_CASE` (`MAX_RISK`-style — e.g.
  `SLOW_OPERATION_THRESHOLD_SECONDS`, `DEFAULT_SYMBOL`). One
  deliberate, documented exception: `core/secrets.py`'s
  `@property`-based secret accessors (`TWELVE_DATA_API_KEY`, etc.) are
  `UPPER_CASE` methods, not constants — intentional, since callers use
  them exactly like the constant/env-var name they wrap
  (`Secrets().TWELVE_DATA_API_KEY`).
- **Logger names**: `PascalCase`, one `setup_logger("Name")` call per
  module at import time, `Name` matching the module's primary
  class/responsibility — see `docs/LOGGING.md` for the full
  hierarchy.
- **Test functions**: `test_<condition>_<expected_result>`, e.g.
  `test_invalid_buy_geometry_blocked` — a reader should be able to
  tell what broke from the test name alone in a CI failure list.

## Testing Rules

See `docs/TESTING.md` for the full policy (directory layout,
fixture rules, running tests, CI behavior). The short version:

- Test through the real chain — real services/repositories against a
  real (temporary, isolated) SQLite database, never a hand-mocked
  repository.
- One behavior per test.
- New tests for genuinely new coverage go in `tests/unit/`,
  `tests/integration/`, `tests/security/`, `tests/performance/`, or
  `tests/ai/`; check first whether the scenario is already covered in
  the existing flat `tests/test_*.py` files before adding a near-
  duplicate.
- Every change must leave `python -m pytest tests/` fully green — no
  exceptions, no "pre-existing failure, not my problem."

## Commit Rules

- One logical change per commit; the commit message states the *why*,
  not just the *what* (the diff already shows the what).
- Every commit message that touches production code states, when
  applicable, what was verified: `compileall`, `pyflakes`, `pytest`
  pass/fail counts, and `python main.py` exit code — this repository's
  commit history is itself a verification log, not just a change log.
- Never commit a secret, credential, or `.env` file — `.gitignore`
  covers `.env`, `*.db`, `*.log`, `__pycache__/`, `.pytest_cache/` (see
  `docs/SECURITY.md`'s Section 2 for the full policy and the
  full-history scan confirming this has held).

## Review Process

- Before any change: read the relevant module's `README.md`
  (`data/README.md`, `context/README.md`, `signals/README.md`,
  `risk/README.md`, `execution/README.md`, `telegram/README.md`,
  `ai/README.md`) and any `docs/*_report.md`/`docs/*_architecture.md`
  covering the area — most non-trivial questions about "why is it
  built this way" are already answered in one of these.
- After any change: run the full validation sequence
  (`compileall` → `pyflakes` → `pytest` → full module import sweep →
  `python main.py` exit code) before reporting the change as done —
  this exact sequence is what `.github/workflows/ci.yml` runs on every
  push/PR, so a change that hasn't been checked against it locally
  isn't actually verified.
- Report the change: files changed and why, test results, and
  regression risk — every phase in this project's history has ended
  with exactly this structure; keep doing it.
- If a task's scope starts requiring a "big refactor" partway through
  investigation, stop and report instead of pushing through — this is
  a repeated, explicit instruction across this project's foundation-
  hardening phases (Phase 49 cleanup, Phase 52 testing, Phase 53
  performance, Phase 55 AI foundation all state it independently), not
  a one-off preference.
