# GoldBot Testing (Strategy + Report)

Merged from `docs/testing_strategy.md` and `docs/testing_report.md`
(Phase 56 documentation consolidation) into the single `TESTING.md`
this project's final documentation structure calls for. Content is
unchanged from the two source documents except for this note and the
"Current State" section immediately below, which brings the test
count current — the rest of this document (Sections 1-4 under
"Testing Report" and everything under "Testing Strategy") is the
original Phase 52 material and intentionally keeps its original
phase-relative numbers as a historical record; see
`docs/v0.3_final_audit.md` for the authoritative current-state numbers.

## Current State (Phase 56)

```
176 tests passing (up from 112 at the end of Phase 52)
```

Growth since Phase 52's snapshot below: `tests/performance/` (+12,
Phase 53), `tests/security/test_secret_security.py` +
`test_permission_security.py` + `test_database_security.py` (+18,
Phase 54), `tests/ai/` (+26, Phase 55). Directory layout, fixture
rules, and CI behavior described below are unchanged since Phase 52
and still accurate.

---

# Testing Report (Phase 52 — original)

Audit of the test suite as it stood before Phase 52, the gaps found,
and what that phase added to close them.

## 1. Current State (Before Phase 52)

- 9 files under `tests/`, flat (no subdirectories), `tests/conftest.py`
  holding one autouse fixture (`fresh_database`) plus the env-var
  bootstrap for the 5 required secrets.
- `python -m pytest tests/` collected **52 tests**, all passing.
- No `pytest.ini`/`pyproject.toml`/`setup.cfg` — pytest runs on pure
  defaults.
- No coverage measurement (`pytest-cov` not installed).
- `.github/workflows/ci.yml` already ran `compileall` → `pyflakes` →
  a full module import sweep → `pytest tests/ -v` on every push/PR
  (Phase 47.1) — the CI shape Phase 52's Task 10 asked for already
  existed.

### Coverage baseline (measured in Phase 52, `pytest-cov`, whole repo)

```
TOTAL   3668 statements, 1828 missed, 50%
```

## 2. Gaps Found (Phase 52)

**Two files collected zero tests despite matching `test_*.py`.**
`tests/test_signal_layer.py` and `tests/test_generate_signals.py`
(Phase 17.2.1/17.2.2 legacy scripts) defined a `run_test()` function,
invoked only via `if __name__ == "__main__":`. Pytest's default
collection only picks up functions named `test_*` — `run_test` was
silently never collected. `pytest tests/test_signal_layer.py
tests/test_generate_signals.py --collect-only` confirmed: **"no tests
collected."** Not a duplicate-test problem, a *disguised zero-coverage*
problem — the files looked like working regression tests and weren't.

**Zero tests for `decision_layer/decision_engine/decision_engine.py` and
`core/pipeline.py`.** Coverage: both **0%** before Phase 52. This was
the most consequential gap: the critical-bug-fix phase's guarantees
(REJECT/BLOCKED/invalid-geometry signals never reach Telegram; at most
one Telegram message per pipeline cycle) were only ever verified with
ad-hoc scripts run in chat during that phase — nothing in `tests/`
would have caught a regression to that fix. `signal_layer/signal_engine/signal_engine.py`
was also at 0%.

**`risk_layer/risk_engine/risk_manager.py` at 44% coverage, no dedicated test file.**
The geometry-validation logic (the actual fix from the critical-bug
phase) had no direct unit test — only indirectly touched wherever
another test happened to construct a `RiskResult`.

**Several real Telegram commands had no `route_command()`-level
test.** `/settings` and `/notifications` (and
`telegram/notification_service.py` entirely) had **zero** test
coverage anywhere in the suite. `/profile`, `/history`, `/subscription`
were only exercised indirectly (service-layer calls, not through the
actual command router). `telegram/handlers.py` was at 24% coverage.

**Handler-level argument validation was untested.** `tests/test_user.py`
tested `UserService.change_risk()`/`change_language()`/etc. directly,
bypassing `telegram/handlers.py`'s own argument-allowlist validation
(e.g. `/risk 99` being rejected, `/language XX` being rejected) —
that validation branch had zero coverage.

**"Missing secret" code paths were never exercised.**
`tests/conftest.py`'s autouse setup always provides all 5 secrets (as
fake-but-present values) for every test — meaning `core/secrets.py`'s
`raise ValueError` path, and every caller's graceful-degradation path
(`TwelveDataClient`, `TelegramBot`, `MarketDataNormalizer`,
`is_owner()`), had never actually been driven by a test.

**No reusable fixtures beyond `fresh_database`.** Every test file
duplicated its own inline `UserService().register_user(...)` /
`SubscriptionRepository().create_subscription(...)` setup.

**Phase 50's 6 new indexes had no existence check.** Nothing verified
`idx_users_status`, `idx_signals_created_at`, etc. actually get
created.

**No coverage measurement.** No tool installed, no baseline number,
no visibility into which modules were actually exercised.

## 3. Test Plan (Phase 52)

Directory structure: kept all 9 existing flat files exactly as they
were (all 52 tests, zero regression risk — "working code first," per
that phase's own instruction) and added new subdirectories for new
coverage only:

```
tests/
├── conftest.py                      (extended, not replaced)
├── test_access.py                   (existing, unchanged)
├── test_admin.py                    (existing, unchanged)
├── test_database.py                 (existing, unchanged)
├── test_feedback.py                 (existing, unchanged)
├── test_generate_signals.py         (rewritten: run_test() -> real test_* functions)
├── test_signal.py                   (existing, unchanged)
├── test_signal_layer.py             (rewritten: run_test() -> real test_* functions)
├── test_subscription.py             (existing, unchanged)
├── test_user.py                     (existing, unchanged)
├── unit/
│   ├── test_risk_manager.py         (new -- geometry, distance, APPROVE-gate)
│   └── test_decision_engine.py      (new -- APPROVE/REJECT/NO_TRADE matrix)
├── integration/
│   ├── test_pipeline_flow.py        (new -- the 4 critical-bug-fix regression cases)
│   ├── test_database_flow.py        (new -- index existence, idempotency, basic perf)
│   └── test_telegram_flow.py        (new -- /profile /settings /history /subscription
│                                      /notifications /users via route_command())
├── security/
│   ├── test_secrets.py              (new -- missing token/API key handled)
│   └── test_input_validation.py     (new -- invalid command args, empty feedback)
└── fixtures/                        (see Note below)
```

(Phase 53-55 later added `tests/performance/`, `tests/security/test_secret_security.py`
/`test_permission_security.py`/`test_database_security.py`, and
`tests/ai/` on top of this — see each phase's own commit for detail;
the directory-layout *rules* below stayed the same throughout.)

**Note on `tests/fixtures/`:** the reusable fixtures (`test_user`,
`premium_user`, `vip_user`, `admin_user`, `owner_user`,
`mock_signal_candidate`, `mock_pipeline`, `mock_ai_result`) live in
`tests/conftest.py`, not in `tests/fixtures/*.py`. This was a
deliberate choice, not an oversight: there is no `tests/__init__.py`
in this repo (and adding one to make `tests.fixtures.factories`
dotted-importable everywhere is itself a structural change with its
own risk), while pytest's `conftest.py` mechanism auto-shares fixtures
with every test file under `tests/` — including these new
subdirectories — via dependency injection, with zero import wiring
and zero risk of a broken import path. `tests/fixtures/` is kept as
the directory the task asked for, holding only this explanation.

## 4. Result (Phase 52)

- **112 tests passing** (up from 52), zero failures, zero skips.
- Coverage: **50% → 68%** whole-repo; **70%** across the
  task-prioritized critical modules (`risk/`, `decision/`,
  `telegram/`, `database/`, `core/`, `signals/`, `ai/` combined) —
  met the stated 70% minimum.
- `core/pipeline.py`: 0% → **100%**.
- `decision_layer/decision_engine/decision_engine.py`: 0% → **100%**.
- `signal_layer/signal_engine/signal_engine.py`: 0% → **100%**.
- `risk_layer/risk_engine/risk_manager.py`: 44% → **82%**.
- `telegram/handlers.py`: 24% → **48%**.

Deliberately left low at the time (LOW priority, per Phase 52's own
prioritization — network-dependent entry points, not pure logic):
`telegram/polling.py` (0%, long-running process entry point),
`telegram/result_handler.py` (0%, no caller wires it yet — dead code
per the Phase 48 audit), `telegram/notifier.py` (56%, the untested
remainder is real Telegram API/event-loop plumbing that would need
network mocking beyond that phase's scope).

---

# Testing Strategy (Phase 52 — original)

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
4. **A gap in coverage is a finding, not a failure.** Report low-
   coverage areas deliberately not chased (see "Result" above) rather
   than writing low-value tests just to move a number.

## Directory Layout & Naming Rules

```
tests/
├── conftest.py             shared fixtures + env bootstrap (autouse)
├── test_*.py                existing flat suite (kept as-is, Phase 34-50)
├── unit/test_*.py            one module's logic in isolation, no I/O beyond
│                             what that module itself owns (e.g. RiskManager
│                             math, DecisionEngine branch matrix)
├── integration/test_*.py     multiple layers wired together (pipeline runs,
│                             route_command() end-to-end, real DB round-trips)
├── security/test_*.py        permission/secret/input-validation-focused
├── performance/test_*.py     timing/regression-guard tests (Phase 53)
├── ai/test_*.py               AI foundation shape checks, no real AI call (Phase 55)
└── fixtures/                  documentation only -- see "Fixtures" below
```

- File names: `test_<module_or_feature>.py`, snake_case, matching the
  production module it primarily covers (`test_risk_manager.py` for
  `risk_layer/risk_engine/risk_manager.py`) or the feature it exercises
  (`test_pipeline_flow.py` for the full pipeline chain).
- Test function names: `test_<condition>_<expected_result>`, e.g.
  `test_invalid_buy_geometry_blocked`, `test_reject_when_ai_not_approved`.
  A reader should be able to tell what broke from the test name alone
  in a CI failure list, without opening the file.
- One behavior per test. A test that asserts five unrelated things is
  a sign it should be five tests.
- New tests for genuinely new coverage go in `unit/`/`integration/`/
  `security/`/`performance/`/`ai/`; the existing flat `tests/test_*.py`
  files are not required reading before adding a new one, but check
  first whether the scenario is already covered there.

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
gated** — `--cov-fail-under` is intentionally not set. A future phase
can add `--cov-fail-under=70` (or per-module gates) once the team has
watched real coverage numbers over a few PRs and agreed on where a
hard floor makes sense; setting one before that would be gating on a
number nobody has lived with yet.

`ci.yml` is separate from `trading_bot.yml` (the scheduled production
runner) — CI never touches live APIs or production secrets, it only
validates the code.
