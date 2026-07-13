# GoldBot Testing Report (Phase 52)

Audit of the test suite as it stood before this phase, the gaps
found, and what this phase added to close them.

## 1. Current State (Before This Phase)

- 9 files under `tests/`, flat (no subdirectories), `tests/conftest.py`
  holding one autouse fixture (`fresh_database`) plus the env-var
  bootstrap for the 5 required secrets.
- `python -m pytest tests/` collected **52 tests**, all passing.
- No `pytest.ini`/`pyproject.toml`/`setup.cfg` — pytest runs on pure
  defaults.
- No coverage measurement (`pytest-cov` not installed).
- `.github/workflows/ci.yml` already ran `compileall` → `pyflakes` →
  a full module import sweep → `pytest tests/ -v` on every push/PR
  (Phase 47.1) — the CI shape this phase's Task 10 asks for already
  existed.

### Coverage baseline (measured this phase, `pytest-cov`, whole repo)

```
TOTAL   3668 statements, 1828 missed, 50%
```

## 2. Gaps Found

**Two files collected zero tests despite matching `test_*.py`.**
`tests/test_signal_layer.py` and `tests/test_generate_signals.py`
(Phase 17.2.1/17.2.2 legacy scripts) defined a `run_test()` function,
invoked only via `if __name__ == "__main__":`. Pytest's default
collection only picks up functions named `test_*` — `run_test` was
silently never collected. `pytest tests/test_signal_layer.py
tests/test_generate_signals.py --collect-only` confirmed: **"no tests
collected."** Not a duplicate-test problem, a *disguised zero-coverage*
problem — the files looked like working regression tests and weren't.

**Zero tests for `decision/decision_engine.py` and
`core/pipeline.py`.** Coverage: both **0%** before this phase. This is
the most consequential gap: the critical-bug-fix phase's guarantees
(REJECT/BLOCKED/invalid-geometry signals never reach Telegram; at most
one Telegram message per pipeline cycle) were only ever verified with
ad-hoc scripts run in chat during that phase — nothing in `tests/`
would have caught a regression to that fix. `signals/signal_engine.py`
was also at 0%.

**`risk/risk_manager.py` at 44% coverage, no dedicated test file.**
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

## 3. Test Plan For This Phase

Directory structure: kept all 9 existing flat files exactly as they
were (all 52 tests, zero regression risk — "working code first," per
this phase's own instruction) and added new subdirectories for new
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
and zero risk of a broken import path. All fixtures used by tests in
`tests/unit/`, `tests/integration/`, and `tests/security/` were
confirmed working on the first real test run. `tests/fixtures/` is
kept as the directory the task asked for, holding only this
explanation.

No existing test file's content changed except `test_signal_layer.py`
and `test_generate_signals.py` (rewritten, same scope, now actually
collected) and `tests/conftest.py` (extended with new fixtures,
nothing removed).

## 4. Result

- **112 tests passing** (up from 52), zero failures, zero skips.
- Coverage: **50% → 68%** whole-repo; **70%** across the
  task-prioritized critical modules (`risk/`, `decision/`,
  `telegram/`, `database/`, `core/`, `signals/`, `ai/` combined) —
  meets the stated 70% minimum.
- `core/pipeline.py`: 0% → **100%**.
- `decision/decision_engine.py`: 0% → **100%**.
- `signals/signal_engine.py`: 0% → **100%**.
- `risk/risk_manager.py`: 44% → **82%**.
- `telegram/handlers.py`: 24% → **48%**.

Deliberately left low (LOW priority, per this phase's own
prioritization — network-dependent entry points, not pure logic):
`telegram/polling.py` (0%, long-running process entry point),
`telegram/result_handler.py` (0%, no caller wires it yet — dead code
per the Phase 48 audit), `telegram/notifier.py` (56%, the untested
remainder is real Telegram API/event-loop plumbing that would need
network mocking beyond this phase's scope).
