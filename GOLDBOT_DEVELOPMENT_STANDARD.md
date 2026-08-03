# GoldBot Development Standard (GDS)

Status: CANONICAL — established by Director Order No. 017.

This is a new root-level document rather than an extension of an existing one because, per the Module Reuse Principle's own test (does an existing module cover this? / can an existing module be extended without breaking its contract?), the answer to both was "no" for a repo-wide day-to-day coding/workflow standard: `CLAUDE.md` is governance and commit protocol, `ARCHITECTURE.md` is structural/layer definition, and neither one is "how the Worker writes code, tests it, and ships it" — so a third, distinct root document is justified and is the minimal correct answer (one new file, not a new package).

## Relationship to existing rules

GDS does not override, replace, or re-litigate anything already frozen in this repository — per Director Order No. 017's own instruction, "Yangi standartlar mavjud qoidalarga zid bo'lmasligi kerak" (new standards must not conflict with existing rules). Specifically:

- **`CLAUDE.md`** remains the source of truth for the 11-step Commit Protocol, the Trading Safety boundaries (Risk Manager, AI advisory-only, no direct DB access from Telegram handlers), and Worker Authority / Director Order No. 016. GDS-010 and GDS-011 below map onto that protocol; they do not add a second, competing one.
- **GEL-001 ("One Module = One Package")** remains the rule for what documentation set each module package carries (`README.md`, `CONTRACTS.md`, `MODULE_MAP.md`, `IMPLEMENTATION.md`, `ROADMAP.md`, `WORK_LOG.md`, `CHANGELOG.md`, a sequence diagram) and that `tests/` stays centralized under `tests/`, not duplicated per module. GDS-002 and GDS-007 below reuse this set verbatim rather than inventing new per-module files.
- **`ARCHITECTURE.md`** remains the source of truth for the Layer Direction Rule (`data_layer -> context_layer -> indicator_layer -> strategy_layer -> signal_layer -> ai_layer -> decision_layer -> risk_layer -> execution_layer -> trade_monitoring_layer -> ...` down to `database_layer`, per its Repository Philosophy section) and the 17-layer canonical structure. GDS-008 below operationalizes that rule; it does not redraw the layer diagram.
- **`DIRECTOR_DECISIONS.md`** remains the single append-only decision log (WAR/WDR/MIR/RAR/GEL/DD/Order entries). GDS references it; it is not duplicated here.

Where GDS adds anything new (Definition of Done, Risk Assessment levels, Rollback Strategy, Module Health Score, Technical Debt Standard, Module Status Lifecycle, Dependency Graph Standard, AI Knowledge Base / Lessons Learned Standard), it is new *process*, not new *architecture* — it tells the Worker how to apply the existing rules consistently, sprint over sprint, module over module.

---

## GDS-001 — Coding Standard

**Purpose.** Keep code readable and consistent across 17 Layers written by different sessions of the same Worker over time, without inventing a house style disconnected from what is already in the repo.

**Scope.** All `.py` files under any `*_layer/` package, `core_layer/`, `database_layer/`, `database/`, and `platform_layer/`.

**Mandatory Rules.**
- Type hints on public function/method signatures (parameters and return type), matching the existing style in `risk_layer/risk_engine/risk_manager.py` (`@dataclass(frozen=True)` configs, `Optional[...]` for nullable fields) and `decision_layer/decision_engine/decision_engine.py` (`TYPE_CHECKING`-guarded imports for types only needed at type-check time).
- Naming: `snake_case` for functions/variables/modules, `PascalCase` for classes and `Enum`s (e.g. `DecisionAction`, `DecisionType`), `UPPER_SNAKE_CASE` for module-level constants (e.g. `_BLOCKING_EMERGENCY_STATES`, `DEFAULT_DUPLICATE_WINDOW_SECONDS`). A leading underscore marks module-private constants/helpers, as already used in `risk_manager.py`.
- Docstrings and comments are WHY-only, not WHAT — restate the existing CLAUDE.md convention. A comment explains a decision or a hazard ("defense in depth for any direct caller ... that reaches RiskManager.evaluate() without going through PipelineGuard"), never narrates the next line of code.
- Imports are absolute, from the Layer root down (`from risk_layer.risk_engine.account_state_tracker import AccountStateTracker`, `from core_layer.logger.logger import setup_logger`), matching the post-migration import style already used across the repo. No relative imports (`from .foo import bar`) in Layer code.
- `@dataclass(frozen=True)` for value objects that represent a decision, config, or result (`RiskConfig`, `DecisionResult`) — immutability is the default for anything that crosses a Layer boundary.

**Forbidden Practices.**
- No bare `except:` — catch a named exception or `Exception` explicitly (see GDS-003).
- No new relative imports, no wildcard imports (`from x import *`).
- No comments that just restate the line below them.
- No untyped public function signatures in new code.

**Example.** `risk_layer/risk_engine/risk_manager.py`'s `_BLOCKING_EMERGENCY_STATES` tuple and its accompanying WHY comment (why `WARNING` is excluded, why this exists even though `PipelineGuard` already gates earlier) is the model to follow for any new module-level constant that encodes a business rule.

---

## GDS-002 — Testing Standard

**Purpose.** Keep test coverage centralized, discoverable, and consistent with how tests are already organized in this 5400+-test suite.

**Scope.** Everything under `tests/`.

**Mandatory Rules.**
- `tests/` stays centralized at the repository root. GEL-001 does not change this — the Director's earlier clarification stands: per-module packages get documentation files (`README.md`, `CONTRACTS.md`, etc.) under GEL-001, but never their own `tests/` directory. All tests live under the root `tests/` tree, mirroring the Layer/module structure (e.g. `tests/core/gateway/`, `tests/core/emergency/`, `tests/configuration/`, `tests/deploy/`, `tests/performance/`) rather than a `tests/` folder inside each `*_layer/` package.
- Categorize by kind, not just by module: `tests/unit/`, `tests/integration/`, `tests/security/`, `tests/performance/`, `tests/ai/` are the existing top-level kind buckets referenced in CLAUDE.md's "Before Code Changes" checklist; module-scoped subfolders (`tests/core/`, `tests/configuration/`, `tests/signals/`, `tests/strategies/`, `tests/errors/`, `tests/contracts/`, `tests/deploy/`) sit alongside them for module-specific suites. A new test belongs in the bucket matching its *kind* (unit/integration/security/performance/ai) when one applies, otherwise in the module-scoped folder.
- Naming: test files are `test_<subject>.py` (`test_service_registry.py`, `test_circuit_breaker.py`, `test_pipeline_execution_time.py`); shared non-test helpers used only by fixtures are prefixed with `_` (e.g. `tests/core/gateway/_gfakes.py`).
- Fixtures live in `conftest.py` at the narrowest scope that needs them (e.g. `tests/signals/conftest.py`, `tests/strategies/conftest.py`) rather than a single monolithic root `conftest.py`, matching current practice.
- Mocking: fake collaborators (`_gfakes.py`-style) over patching internals — prefer constructing a fake implementation of a dependency's interface over `unittest.mock.patch` on private attributes, matching `tests/core/gateway/_gfakes.py`.
- Every Autonomous Bug Fix (CLAUDE.md's Worker Authority list) adds a regression test in the same commit — no bug fix lands without one.

**Forbidden Practices.**
- No test folder nested inside a `*_layer/` package — this violates the "tests/ stays centralized" ruling above.
- No test that silently skips on failure (`pytest.mark.skip` without a tracked reason referencing a ROADMAP.md Technical Debt entry, see GDS-016).
- No new test dependency without checking `requirements.txt`/`requirements-freeze.txt` first for an existing equivalent.

**Example.** `tests/core/gateway/` holds nine `test_*.py` files (`test_core_gateway.py`, `test_dependency_graph.py`, `test_gateway_auth.py`, ...) plus a shared `_gfakes.py` — this is the template for any module that accumulates enough surface area to need multiple, kind-separated test files.

---

## GDS-003 — Error Handling Standard

**Purpose.** Make failures diagnosable and make sure a failure in one Layer cannot silently corrupt state in a downstream Layer.

**Scope.** All Layers, with extra weight on `risk_layer/`, `decision_layer/`, and anything that touches `core_layer/emergency/`.

**Mandatory Rules.**
- Raise specific, named exceptions (`ValueError`, a project-defined error type from `tests/errors/test_error_types.py`'s corresponding `errors` module) rather than a bare string-carrying `Exception`.
- Fail loud on missing required configuration — `core_layer/secrets/secrets.py`'s `Secrets.get()` raises `ValueError(f"Secret '{key}' not found in environment.")` when a required secret is absent and no default is given; this is the pattern for any required external input. Use `get_optional()`'s "return `None`, let the caller decide disabled-vs-required" pattern only when absence is a legitimate, documented state (as `OPENAI_API_KEY` is, per its own docstring), never as a way to swallow a real error.
- Emergency-state checks (`_BLOCKING_EMERGENCY_STATES` in `risk_layer/risk_engine/risk_manager.py`) are defense in depth, not the only gate — a Layer that can be called directly (by tests, by backtesting) must still enforce its own invariants even though `core_layer/pipeline/pipeline_guard.py` gates the real pipeline earlier.
- Every caught exception either re-raises, returns a typed error/rejection result (e.g. a `DecisionResult` with `DecisionType.REJECTED`), or logs at `ERROR`/`WARNING` via the standard logger (GDS-004) — never a silent `pass`.

**Forbidden Practices.**
- No bare `except:` or `except Exception: pass`.
- No swallowing an exception to "keep the pipeline running" for a Trading Safety-relevant Layer (`signals/`, `signal_layer/`, `strategy_layer/`, `risk_layer/`, `decision_layer/`) — a swallowed error there is exactly the class of incident CLAUDE.md's Trading Safety section exists to prevent.
- No new custom exception type without checking `tests/errors/` and the existing error-types module first (Module Reuse Principle applies to exception classes too).

**Example.** `Secrets.get()` in `core_layer/secrets/secrets.py` is the canonical "fail loud, no silent default" pattern; `RiskManager`'s emergency-state check is the canonical "defense in depth even for direct callers" pattern.

---

## GDS-004 — Logging Standard

**Purpose.** Standardize on the one logging pattern already used repo-wide so log output is uniform and greppable.

**Scope.** All Layers.

**Mandatory Rules.**
- Use `core_layer/logger/logger.py`'s `setup_logger(name: str = "GoldBot")` — never call `logging.getLogger(...)` directly outside `logger.py` itself. It wraps stdlib `logging`, sets `INFO` level, attaches a single `StreamHandler(sys.stdout)` with format `'%(asctime)s - %(name)s - %(levelname)s - %(message)s'`, and guards against duplicate handlers (`if not logger.handlers:`).
- Name the logger after the class/module it instruments, matching `logger = setup_logger("RiskManager")` at the top of `risk_layer/risk_engine/risk_manager.py` — module-level, one call, reused by every function/method in that file.
- Log level discipline: `INFO` for normal pipeline progress, `WARNING` for advisory/non-blocking conditions (matching `EmergencyState.WARNING`'s own "advisory only, does not block" contract), `ERROR` for anything that caused a rejection, abort, or exception.

**Forbidden Practices.**
- No `print()` for anything beyond a one-off local debugging session that never gets committed.
- No second logging setup/formatter defined in a new module — extend `setup_logger`'s existing contract if a new capability is genuinely needed (GDS-006's Module Reuse Principle applies), don't hand-roll a parallel one.
- No logging of secrets — anything sourced from `core_layer/secrets/secrets.py` must never appear in a log message (see GDS-009).

**Example.** `logger = setup_logger("RiskManager")` at module scope in `risk_layer/risk_engine/risk_manager.py`, called once, reused throughout the file — this is the pattern for every new module.

---

## GDS-005 — Performance Standard

**Purpose.** Keep the pipeline's latency and resource behavior predictable and regression-tested, without turning "performance work" into unbounded rewrites.

**Scope.** All Layers, with the Data→Context→Signal→AI→Decision→Risk→Telegram pipeline (`core/pipeline.py` / `core_layer/pipeline/`) as the primary measured path.

**Mandatory Rules.**
- Any Performance Optimization (CLAUDE.md's Worker Authority list: caching, lazy loading, query/algorithm/memory optimization) must leave the public API and external behavior unchanged — this is a hard CLAUDE.md constraint, not a GDS addition.
- Pipeline-timing-sensitive changes are checked against `tests/performance/test_pipeline_execution_time.py` — run it, don't just eyeball it.
- Prefer an existing cache/lazy-load mechanism over adding a new one (Module Reuse Principle, GDS-006) — check `core_layer/` for an existing caching utility before writing a new one.
- Database and repository calls (`database/*_repository.py`, `database_layer/`) should be measured for N+1 patterns before a Layer-crossing loop is added; batch where the existing repository already exposes a batch method.

**Forbidden Practices.**
- No performance change that alters what a caller receives or when (that's a breaking change, not an optimization — needs Director Review per CLAUDE.md's public-API rule).
- No unmeasured "this should be faster" change to a hot pipeline path — `tests/performance/` exists precisely so performance claims are checked, not assumed.

**Example.** `tests/performance/test_pipeline_execution_time.py` is the existing regression test any pipeline-path performance change must be run against, and extended (not duplicated) if a new measurable path is added.

---

## GDS-006 — Refactoring Standard

**Purpose.** Make sure refactoring never gets tangled with migration or feature work, and never reintroduces a duplicate module the Module Reuse Principle already ruled out once.

**Scope.** All Layers.

**Mandatory Rules.**
- **Stable Migration Rule (SMR-001):** if an existing module works and already matches the Canonical Architecture, its internal structure is not changed as part of a migration — internal refactoring happens only after the migration itself is complete and committed. A migration commit and a refactor commit are two different commits, never one.
- **Module Reuse Principle** (CLAUDE.md, restated here as it governs every refactor decision too): before creating a new file, package, or top-level class/function, answer in order and stop at the first "yes" — (1) does this already exist somewhere in the repo? (2) can an existing module be extended (new method, new optional field, new function in an existing file) without breaking its current contract? Only if both are "no," create something new, and document in its own docstring why steps 1 and 2 were both "no."
- Internal Refactoring under Worker Authority (CLAUDE.md's Order No. 016 list) is permitted without Director approval as long as it stays inside a module's existing boundary and never crosses a Layer contract.
- Module Expansion (splitting an oversized module into packages/submodules/helpers/services/engines) is permitted the same way, provided Layer boundaries and ownership are preserved.

**Forbidden Practices.**
- No refactor bundled into the same commit as a migration (`git mv`) or a feature change — SMR-001 forbids this explicitly, and CLAUDE.md's "No unnecessary refactor" restriction backs it up.
- No new top-level package created without having gone through both Module Reuse Principle questions first, in order, and documented the "no" answers.
- No refactor that crosses a Layer contract without Director Review (this is a Layer Architecture change, which Director Order No. 016 explicitly reserves).

**Example.** The GEL-001 rollout itself (`git mv Contracts.md CONTRACTS.md`, `git mv ModuleMap.md MODULE_MAP.md` across 178 packages, content unchanged) is the canonical SMR-001-compliant migration: pure rename, zero internal refactor, in its own dedicated commit per Layer.

---

## GDS-007 — Documentation Standard

**Purpose.** Keep every module's documentation set complete, current, and in the one place GEL-001 already defines for it.

**Scope.** Every `*_layer/` package and its sub-packages; `tests/` stays out of scope for this per-module set (see GDS-002).

**Mandatory Rules.**
- **GEL-001 ("One Module = One Package")** doc set — every module package carries exactly these files, and no others, for documentation: `README.md`, `CONTRACTS.md`, `MODULE_MAP.md`, `IMPLEMENTATION.md`, `ROADMAP.md`, `WORK_LOG.md`, `CHANGELOG.md`, and a sequence diagram (embedded in `README.md` or `MODULE_MAP.md` unless the module is complex enough to warrant its own diagram file). `DIRECTOR_DECISIONS.md` itself stays root-level only — it is not duplicated per module; a module's `WORK_LOG.md` may reference a `DIRECTOR_DECISIONS.md` entry by its ID (e.g. "per GEL-001") without copying its text.
- `tests/` for that module's code stays centralized at the repository root (GDS-002) — this is unaffected by GEL-001 and is not one of the per-module files.
- Documentation Evolution (CLAUDE.md Worker Authority) means these files are kept in sync with the code as part of the same change, not as a follow-up: a bug fix updates `CHANGELOG.md` and `WORK_LOG.md` in the same commit.

**Forbidden Practices.**
- No 9th per-module doc file invented for something that already has a home in this set (Technical Debt goes in `ROADMAP.md`, not a new `TECHDEBT.md`; dependency direction goes in `CONTRACTS.md`/`MODULE_MAP.md`, not a new `DEPENDENCIES.md` — see GDS-016 and GDS-018).
- No module-local `tests/` folder (restated from GDS-002).
- No documentation change left for "later" — a code change without its doc-set update is not Done (see the Definition of Done section below).

**Example.** The GEL-001 rollout across 14 Layers (`risk_layer`, `trade_monitoring_layer`, `execution_layer`, `decision_layer`, `signal_layer`, `strategy_layer`, `context_layer`, `media_layer`, `backtesting_layer`, `database_layer`, `core_layer`, `platform_layer`, `data_layer`, `ai_layer`) is the reference implementation of this doc set, one Layer per commit.

---

## GDS-008 — Dependency Standard

**Purpose.** Preserve the Layer Direction Rule so the pipeline stays a directed, acyclic flow and no Layer silently grows a shortcut around another.

**Scope.** All cross-module and cross-Layer imports.

**Mandatory Rules.**
- **Layer Direction Rule** (ARCHITECTURE.md's Repository Philosophy, restated concretely per the actual package names in this repo): dependencies flow strictly downward, `data_layer -> context_layer -> indicator_layer -> strategy_layer -> signal_layer -> ai_layer -> decision_layer -> risk_layer -> execution_layer -> trade_monitoring_layer -> ... -> database_layer`. A Layer imports only from the Layer(s) immediately below it (or from `core_layer`, which every Layer may use), never from a Layer above it, and never by reaching two Layers down when the Layer directly below already exposes what's needed.
- CLAUDE.md's existing Architecture Rules restate the handler-specific case of this: no direct database access from `platform_layer/telegram/handlers.py` — handlers call a `telegram/*_service.py` service, services call a `database/*_repository.py` repository. Never shortcut this chain regardless of how convenient a direct call looks.
- A genuinely new cross-Layer import (one that isn't already covered by the existing direction) requires stopping and checking whether it's correct *before* adding it — and per Director Order No. 016, any change touching Layer Architecture requires Director Review, not a unilateral Worker decision.
- Check `grep`-for-importers before changing a shared module's public surface (CLAUDE.md's "Before Code Changes" step 2) — a dependency you don't know about is the fastest way to break a downstream Layer silently.

**Forbidden Practices.**
- No import from `telegram/` inside `strategies/`/`strategy_layer/`, no import from `database/`/`database_layer/` inside `ai/`/`ai_layer/` — these are the explicit CLAUDE.md examples of a forbidden upward/sideways reach.
- No new circular import between two Layers, ever — this is a Layer Architecture violation regardless of direction.
- No silent addition of a new cross-Layer import without recording the reasoning (commit message, `WORK_LOG.md`) — if it needed a moment's thought, it needed a written reason.

**Example.** `risk_layer/risk_engine/risk_manager.py` imports downward from `decision_layer.decision_engine.models`, `signal_layer.signal_builder.models`, `core_layer.emergency.*`, `core_layer.logger.logger`, and `database_layer.trade_repository.risk_decision_repository` — every one of those is a Layer at or below `risk_layer` in the canonical order, never above it.

---

## GDS-009 — Security Standard

**Purpose.** Keep secrets, trading safety, and input validation to the standard CLAUDE.md already sets, expressed as day-to-day rules a Worker checks on every change.

**Scope.** All Layers, with `core_layer/secrets/secrets.py`, `risk_layer/`, `ai_layer/`, and `platform_layer/telegram/` under the most scrutiny.

**Mandatory Rules.**
- Secrets are read only via `core_layer.secrets.secrets.Secrets` (`Secrets.get()` for required values, `Secrets.get_optional()` for values whose absence means "this provider is disabled," per its own Phase 61.2 TASK 2 docstring) — never `os.getenv()` called directly from Layer code, never a hardcoded credential, never a `.env` file read in production (the class's own docstring: "No .env file usage for production security").
- **Never bypass Risk Manager.** Every signal that could reach a user must pass through `risk_layer.risk_engine.risk_manager.RiskManager.evaluate()` — restated verbatim from CLAUDE.md's Trading Safety section because it is the single most important security rule in this codebase.
- **Never allow AI direct execution.** `ai_layer`/`ai/` is advisory input to `decision_layer.decision_engine.decision_engine.DecisionEngine` only — it must never itself approve/reject a trade, call the Risk Manager, or trigger a Telegram send or execution action, per `ai_layer/ai_service/interfaces.py`'s `AIAnalyzerInterface` contract.
- Input validation happens at the boundary a Layer receives external input (an incoming Telegram update, an external price feed in `data_layer/`) — validate before it crosses into business logic, not after.
- Never log a secret (restated from GDS-004) — a value sourced from `Secrets.get()`/`Secrets.get_optional()` never appears in a log line, an exception message, or a `WORK_LOG.md` example.

**Forbidden Practices.**
- No shortcut path from a signal to Telegram delivery that skips `RiskManager.evaluate()` — this is exactly the incident documented in `docs/AUDIT_REPORT.md` and `core/pipeline.py`'s own docstring; read both before touching the notification-eligibility filter.
- No AI-layer code that calls into `risk_layer` or `platform_layer/telegram/` directly.
- No secret read via `os.getenv()` outside `core_layer/secrets/secrets.py` itself.

**Example.** `Secrets.OPENAI_API_KEY`'s property in `core_layer/secrets/secrets.py` — `get_optional()`-backed, returns `None` rather than raising, documented as additive so it never changes `GEMINI_API_KEY`'s existing raise-on-missing contract — is the model for adding a new optional external credential safely.

---

## GDS-010 — Development Workflow

**Purpose.** Give every change, regardless of size, the same 12-stage sequence so nothing (a test, a doc update, a validation step) gets skipped under time pressure.

**Scope.** Every code change in this repository.

**The 12 stages.**

1. **Read** — read the relevant architecture docs first: `ARCHITECTURE.md`, the target module's `README.md`, and any `docs/*.md` covering the area, per CLAUDE.md's "Before Code Changes" step 1. Skipping this is how Layer-boundary violations happen.
2. **Understand** — trace what imports the file you're about to change and what it imports (CLAUDE.md step 2), and read the existing tests for that area before assuming current behavior (CLAUDE.md step 4's "read the relevant test file before assuming behavior").
3. **Design** — decide the smallest change that satisfies the task, running it through the Module Reuse Principle (GDS-006) before any new file/class/function is even sketched, and confirming it doesn't cross a Layer contract (GDS-008).
4. **Implement** — write the change following GDS-001 (typing, naming, WHY-only comments, absolute imports) and GDS-003/GDS-004/GDS-009 (error handling, logging, secrets) as it's written, not retrofitted after.
5. **Unit Test** — add or update a unit test in the matching `tests/` bucket (GDS-002) for the specific behavior changed.
6. **Integration Test** — verify the change against `tests/integration/` (or the relevant cross-module suite) so a Layer-boundary regression is caught before commit, not in CI.
7. **Refactor** — only now, after the functional change is tested and green, apply any Internal Refactoring the change made obviously desirable (GDS-006) — never combined with the functional change itself (SMR-001's separation applies here too, not just to migrations).
8. **Documentation** — update the module's GEL-001 doc set (`README.md`/`CONTRACTS.md`/`MODULE_MAP.md`/`IMPLEMENTATION.md`/`ROADMAP.md`/`WORK_LOG.md`/`CHANGELOG.md`) per GDS-007, in the same change, not a follow-up.
9. **Validation** — this stage *is* CLAUDE.md's Commit Protocol steps 1–6: `git add -A`, `pyflakes`, `compileall`, `pytest tests/`, `python main.py` smoke check, re-loop to step 1 if anything changed. GDS does not define a second validation sequence — it points at the existing one.
10. **Commit** — this stage *is* CLAUDE.md's Commit Protocol steps 7–9: clean `git status`, review `git diff --cached`, then commit with a message that states the "why."
11. **Push** — CLAUDE.md's Commit Protocol step 10: `git push`.
12. **Review** — CLAUDE.md's Commit Protocol step 11 (confirm GitHub Actions `success` before using "Complete"/"Validated" language) plus GDS-011's self-review checklist, run before the commit is made (folded into stage 10/step 8's `git diff --cached` review, not a separate gate).

**Mandatory Rules.** All 12 stages apply to every change, including a one-line fix — the stages scale in effort, not in whether they happen. Stages 9–12 are not a rewrite of CLAUDE.md's protocol; they are this workflow's names for that protocol's existing steps.

**Forbidden Practices.** No skipping straight from Implement to Commit. No treating Documentation (stage 8) as optional for a "small" change — GDS-007 makes it mandatory in the same change.

**Example.** The GEL-001 rollout is this workflow end-to-end, one Layer at a time: Read (`Architecture_Audit_Plan.md`), Design (rename only, per SMR-001), Implement (`git mv`), Validation (pyflakes/compileall/pytest/smoke, all green, 5400/5400 each time), Commit, Push — repeated per Layer, never batched across stages.

---

## GDS-011 — Code Review Standard

**Purpose.** Give the Worker a concrete self-review checklist to run before every commit, rather than a vague "review your diff."

**Scope.** Every commit's `git diff --cached`, immediately before the commit itself.

**Mandatory Rules.** This is not a separate gate — it is what CLAUDE.md's Commit Protocol step 8 (`git diff --cached` — review exactly what is about to be committed) means in practice. Before committing, walk the staged diff against each of these:

- **Architecture Compliance** — does every changed/added import still respect the Layer Direction Rule (GDS-008)? Does nothing reach two Layers down or sideways into `telegram/handlers.py`-style forbidden paths?
- **Security** — does anything in the diff read a secret outside `core_layer/secrets/secrets.py`, log a secret, or create any path that could reach Telegram without going through `RiskManager.evaluate()` (GDS-009)?
- **Performance** — for anything touching the pipeline's hot path, was `tests/performance/test_pipeline_execution_time.py` run, and does the change avoid an unmeasured N+1 or a new unbounded loop (GDS-005)?
- **Maintainability** — does the diff pass the Module Reuse Principle test (GDS-006)? Is naming/typing/logging consistent with GDS-001/GDS-004?
- **Test Coverage** — does every new/changed behavior have a corresponding new/updated test in `tests/` (GDS-002), and does every bug fix carry a regression test?
- **Documentation** — is the module's GEL-001 doc set (GDS-007) updated in this same diff, not deferred?
- **Backward Compatibility** — does the diff change any existing public method signature (`RiskManager.evaluate()`, `TradingPipeline.run()`, `UserRepository.get_user()`, or any equivalent) without an explicit task asking for that signature change? If yes, stop — this needs Director Review, not a commit.

**Forbidden Practices.** No committing with any checklist item unresolved. No treating this checklist as optional for a "trivial" diff — trivial diffs are the fastest to check and the ones most likely to be skipped carelessly.

**Example.** Applied to a hypothetical change to `decision_layer/decision_engine/decision_engine.py`'s confidence-blending thresholds: Architecture Compliance passes (no new imports), Backward Compatibility fails the check immediately (`DecisionEngine`'s public behavior changes) — so per CLAUDE.md's Trading Safety section this halts and requires explicit Director approval before it can even reach this checklist's later items.

---

## Definition of Done (DoD)

A module or change cannot be marked **Completed** or **Stable** unless every item below is checked. This is a literal checklist — partial credit does not count as Done.

- [ ] Architecture mos (change matches ARCHITECTURE.md's Layer structure and Layer Direction Rule)
- [ ] Contracts mos (module's `CONTRACTS.md` reflects the current public surface)
- [ ] Coding Standard mos (GDS-001 typing/naming/import/comment rules followed)
- [ ] Test yozilgan (a test exists for the new/changed behavior, in the correct `tests/` bucket per GDS-002)
- [ ] Integration ishlaydi (integration tests pass; the change doesn't break the Data→Context→Signal→AI→Decision→Risk→Telegram pipeline)
- [ ] Performance tekshirildi (checked against `tests/performance/` where the change touches a measured path)
- [ ] Documentation yangilandi (GEL-001 doc set — `README.md`/`CONTRACTS.md`/`MODULE_MAP.md`/`IMPLEMENTATION.md`/`ROADMAP.md` — updated)
- [ ] WORK_LOG yangilandi (module's `WORK_LOG.md` records what was done and why)
- [ ] CHANGELOG yangilandi (module's `CHANGELOG.md` records the user/system-visible change)
- [ ] Director Decision talab qilmaydi (the change does not touch Layer Architecture, Pipeline, Trading Logic, AI Logic, Decision Logic, Risk Logic, a public-API breaking change, Ownership, or a Foundation Rule — or if it does, Director Review was actually obtained and is cited)

---

## Risk Assessment

Every change is classified into one of four levels before it is implemented. High and Critical levels require Director Review, matching Director Order No. 016's existing "Director Review Required" list — this section just gives concrete criteria for sorting a change into a level.

- **Low** — no Layer-boundary change, no Trading Safety surface touched. Examples: adding a new test, fixing a docstring, adding a `WORK_LOG.md` entry, a logging message wording fix.
- **Medium** — internal refactor or performance optimization within one module's existing boundary, behavior-preserving, no public signature change. Examples: splitting an oversized function inside `database_layer/trade_repository/`, adding a cache inside `data_layer/` that doesn't change what callers receive.
- **High** — touches a public method signature, a cross-Layer import that didn't exist before, or a non-trading-critical part of the pipeline's shape. Examples: adding a new optional field to `RiskConfig`, adding a new Layer-to-Layer call that's still Layer-Direction-compliant but new. Requires Director Review before merge.
- **Critical** — touches Signal logic (`strategies/`, `signals/`, `strategy_layer/`, `signal_layer/`), Risk limits (`risk_layer/risk_engine/risk_manager.py`'s geometry/stop-loss validation and sizing formulas), Decision flow (`decision_layer/decision_engine/decision_engine.py`'s confidence-blending and APPROVE/REJECT/NO_TRADE thresholds), or Execution wiring (`execution_layer`/`execution/`). Examples: changing `RiskManager`'s `min_risk_reward_ratio` default, changing what makes a signal eligible to reach Telegram. Requires explicit Director approval for that specific change, per CLAUDE.md's Trading Safety section — no exception, regardless of how small the diff looks.

---

## Rollback Strategy

When a change fails validation or, worse, fails after being pushed, the sequence is: **Failure -> Rollback -> Restore -> Revalidate -> Retest -> Continue.** This sequence respects CLAUDE.md's existing git safety rules — no `git push --force`, no `git reset --hard`, no skipped hooks, unless the user/Director has explicitly authorized that specific destructive action.

1. **Failure** — a validation step (pyflakes, compileall, pytest, smoke run) or a post-push CI run fails. Stop; do not layer another change on top while the failure is unresolved.
2. **Rollback** — for an uncommitted, unpushed change: discard via `git restore`/re-editing, never `git reset --hard` without explicit authorization. For a pushed, already-merged commit: use `git revert <sha>` to create a new commit undoing it — never rewrite pushed history.
3. **Restore** — bring the working tree back to the last known-good state (the pre-failure commit, or the revert commit's resulting tree) and confirm `git status` is clean.
4. **Revalidate** — re-run the full Commit Protocol (pyflakes, compileall) against the restored state to confirm it is genuinely clean, not just apparently clean.
5. **Retest** — re-run `pytest tests/` and the `python main.py` smoke check against the restored state.
6. **Continue** — only once revalidation and retesting are both green does work resume, either by re-attempting the original change with the root cause fixed (ARCA, see the AI Knowledge Base section below) or by moving to the next task.

**Forbidden Practices.** No force-push to `main`/`goldbot-v1` to "undo" a mistake. No `git reset --hard` on a shared branch without explicit authorization. No skipping straight to step 6 without steps 4–5.

---

## Module Health Score

Each module is scored 0–10 on each of 8 criteria; the sum (max 80) or the average (max 10) is the Module Health Score, used to gate the Module Status Lifecycle transitions below.

1. **Architecture** — conformance to ARCHITECTURE.md's Layer placement and Layer Direction Rule.
2. **Contracts** — accuracy/completeness of `CONTRACTS.md` against the actual public surface.
3. **Documentation** — completeness of the full GEL-001 set (`README.md`/`MODULE_MAP.md`/`IMPLEMENTATION.md`/`ROADMAP.md`/`WORK_LOG.md`/`CHANGELOG.md`).
4. **Testing** — coverage and pass rate of the module's tests under the centralized `tests/` tree.
5. **Performance** — whether the module's pipeline-relevant paths are covered by `tests/performance/` and currently pass their thresholds.
6. **Maintainability** — GDS-001 coding standard adherence, absence of duplicate logic (Module Reuse Principle compliance).
7. **Dependency** — cleanliness of incoming/outgoing dependencies per GDS-018 (no stray upward or sideways imports).
8. **Security** — GDS-009 adherence (secrets handling, Risk Manager gating, AI advisory-only boundary where applicable).

**Score-to-Lifecycle mapping** (used by the Module Status Lifecycle section below):
- 0–3 average: **Blueprint / In Development** range — not yet a candidate for Testing.
- 4–6 average: **Implemented / Testing** range — functional but not yet meeting the bar for Stable.
- 7–8 average: candidate for **Stable**, but only in combination with a fully-checked Definition of Done (score alone is necessary, not sufficient).
- 9–10 average: **Stable**, DoD complete.

A module scoring below 7 average cannot be marked Stable regardless of how complete its DoD checklist looks — the two gates (score and DoD) are both required, per the Module Status Lifecycle section's Testing→Stable transition.

---

## Technical Debt Standard

Known Issues, Technical Debt, Future Refactor ideas, and Deferred Improvements are tracked inside each module's existing `ROADMAP.md` — this is a GEL-001 doc already, reused here rather than creating a 9th per-module file, per the Module Reuse Principle.

**Standard `ROADMAP.md` subsection template** (append under a `## Technical Debt` heading, updated every Sprint):

```markdown
## Technical Debt

### Known Issues
- <issue>: <one-line description> — discovered <date/phase>, severity <Low/Medium/High>.

### Technical Debt
- <item>: <what shortcut was taken and why, at the time> — tracked since <date/phase>.

### Future Refactor
- <item>: <what could be improved, not urgent> — candidate Sprint: <sprint or "unscheduled">.

### Deferred Improvements
- <item>: <what was explicitly deferred, and the Director/Worker reasoning for deferring it>.
```

**Mandatory Rules.** Every Sprint's Continuous Self Review (CLAUDE.md's Worker Authority list) includes a pass over every touched module's `ROADMAP.md` Technical Debt section — items get added when discovered, and closed (moved to `CHANGELOG.md` with a reference back) when resolved, never silently deleted.

---

## Module Status Lifecycle

Six stages, each with a precise entry and exit criterion:

1. **Blueprint** — the module exists only as an entry in `ARCHITECTURE.md`/a Sprint plan; no package directory yet. *Exit:* an assigned Sprint task creates the package skeleton (moves to In Development).
2. **In Development** — package exists, code is being written, tests are incomplete or red. *Entry:* an assigned Sprint task (per Blueprint's exit). *Exit:* `pytest` passes for the module's existing test files and `pyflakes`/`compileall` are clean (moves to Implemented).
3. **Implemented** — functionally complete for its current scope, passes its own unit tests, but integration/performance coverage is not yet complete. *Exit:* integration tests covering this module's pipeline interactions are written and green (moves to Testing).
4. **Testing** — full test suite (unit + integration + relevant security/performance) is green; the module is under active DoD/Module-Health-Score evaluation. *Exit:* Module Health Score reaches 7+ average **and** every Definition of Done item is checked (moves to Stable). Either condition alone is insufficient.
5. **Stable** — DoD complete, Module Health Score 7+ (target 9–10), documented, in production use. *Exit:* either the module is superseded/no longer used (moves to Deprecated) or a Critical-risk change forces it back through Testing.
6. **Deprecated** — no longer part of the active architecture. *Entry:* explicit Director Review (a Layer Architecture / Ownership change per Director Order No. 016) confirming removal or replacement. Deprecated modules keep their `WORK_LOG.md`/`CHANGELOG.md` history; they are not deleted silently.

A module can move backward (Stable → Testing) if a later change drops its Module Health Score or breaks a DoD item — the lifecycle is not strictly forward-only.

---

## Dependency Graph Standard

Each module's dependency relationships are tracked as two directions, and belong inside that module's existing `CONTRACTS.md` or `MODULE_MAP.md` (GEL-001 docs, reused here rather than a new `DEPENDENCIES.md` file, per the Module Reuse Principle):

- **Incoming Dependencies ("Who Uses Me")** — every module/Layer that imports from this one.
- **Outgoing Dependencies ("Whom I Use")** — every module/Layer this one imports from.

**Standard table template** (add to `CONTRACTS.md` or `MODULE_MAP.md`):

```markdown
## Dependency Graph

### Incoming Dependencies ("Who Uses Me")
| Caller Module            | Import Path                                      | Reason                        |
|---------------------------|--------------------------------------------------|--------------------------------|
| decision_layer            | risk_layer.risk_engine.risk_manager               | signal approval gating         |

### Outgoing Dependencies ("Whom I Use")
| Dependency Module          | Import Path                                      | Reason                        |
|-----------------------------|--------------------------------------------------|--------------------------------|
| core_layer.logger           | core_layer.logger.logger.setup_logger             | standard logging               |
| database_layer.trade_repository | database_layer.trade_repository.risk_decision_repository | persisting risk decisions |
```

**Mandatory Rules.** Any change to a module's imports must keep this table in sync in the same commit (GDS-007's "same change, not a follow-up" rule applies here too) — the table must stay consistent with `MODULE_MAP.md`/`CONTRACTS.md` content generally; a stale dependency table is treated as a documentation defect, same as a stale `README.md`.

---

## AI Knowledge Base / Lessons Learned Standard

Each module's `WORK_LOG.md` carries a `## Lessons Learned` subsection. For any significant problem, this reuses CLAUDE.md's existing ARCA (Autonomous Root Cause Analysis) structure verbatim — Problem → Root Cause Analysis → Permanent Solution → Validation → Lessons Learned — rather than inventing a second, parallel template.

**Standard `WORK_LOG.md` entry template:**

```markdown
## Lessons Learned

### <short problem title> — <date/phase>
- **Problem:** <what went wrong, observed symptom>
- **Root Cause:** <the actual underlying cause, not the symptom>
- **Permanent Solution:** <the fix applied — temporary workarounds are forbidden per ARCA>
- **Validation:** <how the fix was confirmed — which tests, which commit>
- **Lessons Learned:** <what this teaches for the future — a rule, a check to add, a pattern to avoid>
```

**Mandatory Rules.** Every ARCA-qualifying incident (a real error, not a hypothetical) gets one of these entries in the affected module's `WORK_LOG.md`, in the same commit as the fix. Temporary fixes/workarounds remain forbidden, per CLAUDE.md's existing ARCA definition — this section does not loosen that.

**Example.** CLAUDE.md's own Commit Protocol preamble is itself an ARCA-style Lessons Learned entry in miniature: Problem (a commit that looked clean but still failed CI), Root Cause (a post-staging `pyflakes` fix never re-staged before commit, across two separate incidents — Phase 59.9 and Phase 60.0/60.1), Permanent Solution (the current strict "stage first, validate after, loop back to stage on any change" ordering), which is exactly the shape every module's `WORK_LOG.md` Lessons Learned entries should follow.
