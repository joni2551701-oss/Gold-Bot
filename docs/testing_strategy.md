# GoldBot Testing Strategy (Phase 52)

## Philosophy

1. **Test through the real chain, not around it.** Every test in this
   suite calls real services/repositories against a real (temporary,
   isolated) SQLite database — never a hand-mocked repository or an
   in-memory fake. The one deliberate exception is `TradingPipeline`'s
   data-fetch step (`tests/conftest.py`'s `mock_pipeline` fixture),
   stubbed only because no test run has live Twelve Data/Telegram
   network access — every other layer downstream of that one stub
   (Decision, Risk, the approve+select filter, `SignalFormatter`,
   `Notifier`, `SignalRepository`) runs real, unmodified production
   code.
2. **A passing test suite must mean the critical-bug-fix guarantees
   still hold.** `tests/integration/test_pipeline_flow.py` exists
   specifically so that "rejected/blocked/invalid-geometry signals
   never reach Telegram, and at most one Telegram message is sent per
   cycle" can never regress silently again — it was previously only
   verified by hand.
3. **Isolation over cleverness.** `tests/conftest.py`'s autouse
   `fresh_database` fixture points `config.Config.DB_PATH` at a fresh
   temp file per test function — no test can leak state into another,
   and no test can touch the real `database/goldbot.db`. Nothing in
   this suite relies on test execution order.
4. **A gap in coverage is a finding, not a failure.** This phase
   reports low-coverage areas it deliberately didn't chase (see
   `docs/testing_report.md`'s "Result" section) rather than writing
   low-value tests just to move a number.

## Directory Layout & Naming Rules

```
tests/
├── conftest.py          shared fixtures + env bootstrap (autouse)
├── test_*.py             existing flat suite (kept as-is, Phase 34-50)
├── unit/test_*.py         one module's logic in isolation, no I/O beyond
│                          what that module itself owns (e.g. RiskManager
│                          math, DecisionEngine branch matrix)
├── integration/test_*.py  multiple layers wired together (pipeline runs,
│                          route_command() end-to-end, real DB round-trips)
├── security/test_*.py     permission/secret/input-validation-focused
└── fixtures/               documentation only -- see "Fixtures" below
```

- File names: `test_<module_or_feature>.py`, snake_case, matching the
  production module it primarily covers (`test_risk_manager.py` for
  `risk/risk_manager.py`) or the feature it exercises
  (`test_pipeline_flow.py` for the full pipeline chain).
- Test function names: `test_<condition>_<expected_result>`, e.g.
  `test_invalid_buy_geometry_blocked`, `test_reject_when_ai_not_approved`.
  A reader should be able to tell what broke from the test name alone
  in a CI failure list, without opening the file.
- One behavior per test. A test that asserts five unrelated things is
  a sign it should be five tests.
- New tests for genuinely new coverage go in `unit/`/`integration/`/
  `security/`; the existing flat `tests/test_*.py` files are not
  required reading before adding a new one, but check first whether
  the scenario is already covered there (this phase found and avoided
  several would-be duplicates — see `docs/testing_report.md`).

## Fixtures

Defined once in `tests/conftest.py`, available to every test file
under `tests/` (including all subdirectories) via pytest's standard
dependency injection — request one by adding it as a test function
parameter, no import needed:

| Fixture | Returns |
|---|---|
| `fresh_database` (autouse) | Nothing — points `Config.DB_PATH` at a fresh temp file. |
| `test_user` | A registered FREE-plan `UserRecord`. |
| `premium_user` / `vip_user` | A registered user's `telegram_id` with an active PREMIUM/VIP subscription. |
| `admin_user` | A registered user's `telegram_id`, added to the `admins` table. |
| `owner_user` | The configured OWNER's `telegram_id` (`"111"`, matching `TELEGRAM_OWNER_ID`). |
| `mock_signal_candidate` | Factory: `mock_signal_candidate(signal_type=, entry=, stop_loss=, take_profit=, confidence=, strategy_name=)` -> `SignalCandidate`. |
| `mock_ai_result` | Factory: `mock_ai_result(approved=, confidence=, risk_score=, explanation=)` -> `AIAnalysisResult`. |
| `mock_pipeline` | Factory: `mock_pipeline(candidates, ai_results)` -> a real `TradingPipeline` with only the data-fetch step stubbed. |

Rules for adding a new fixture: put it in `tests/conftest.py`, give it
a name that says what it returns (not how it's built), and prefer a
factory (a fixture that returns a callable) over a fixed instance the
moment more than one test needs different parameters from it —
`mock_signal_candidate`/`mock_pipeline`/`mock_ai_result` are all
factories for exactly this reason.

## Running Tests

```
pip install -r requirements.txt pytest pyflakes pytest-cov
python -m pytest tests/                                    # full suite
python -m pytest tests/unit/                                 # one directory
python -m pytest tests/unit/test_risk_manager.py              # one file
python -m pytest tests/unit/test_risk_manager.py::test_valid_buy_geometry_passes  # one test
python -m pytest tests/ --cov=. --cov-report=term-missing    # with coverage
```

No special setup beyond installing dependencies — `conftest.py`
handles secrets and database isolation automatically for every run.

## CI Behavior

`.github/workflows/ci.yml` (`GoldBot CI`, runs on every push to
`main`/`claude/**` and every PR):

```
checkout -> setup Python 3.11 -> install deps
    -> compileall (syntax)
    -> pyflakes (lint: unused imports, undefined names, etc.)
    -> full module import sweep (every non-test .py file, catches
       circular imports and missing dependencies)
    -> pytest tests/ -v --cov=. --cov-report=term-missing
```

Any step failing fails the whole job. Coverage is **reported, not
gated** — `--cov-fail-under` is intentionally not set this phase. A
future phase can add `--cov-fail-under=70` (or per-module gates) once
the team has watched real coverage numbers over a few PRs and agreed
on where a hard floor makes sense; setting one today would be gating
on a number nobody has lived with yet.

`ci.yml` is separate from `trading_bot.yml` (the scheduled production
runner) — CI never touches live APIs or production secrets, it only
validates the code.
