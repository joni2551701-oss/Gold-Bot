# GoldBot Architecture Audit (Phase A1)

Complete per-module architecture audit ahead of v0.3.5. Design/
documentation only — nothing in `core/`, `data/`, `context/`,
`strategies/`, `signals/`, `ai/`, `decision/`, `risk/`, `execution/`,
`monitoring/`, `database/`, or `telegram/` was modified to produce
this document. Every claim below was verified by reading the actual
source this phase (imports grepped, functions read, tests run) — not
assumed from earlier phases' reports.

## How to read this document

Each module gets: Purpose, Responsibilities, Dependencies (real,
grepped), Public interfaces, Future expansion points, Problems found,
Missing abstractions. "Problems found" and "Missing abstractions" are
observations only — see `docs/v0.3.5_SPECIFICATION.md` for what to do
about them, and Section "Architecture Improvement Recommendations"
below (Task 5) for Current/Problem/Recommended/Benefits/Risk/Priority
treatment of the significant ones.

---

## core/

**Purpose**: cross-cutting infrastructure — pipeline orchestration,
logging, secrets. The only package every other layer (indirectly) sits
under.

**Responsibilities**: `core/pipeline.py`'s `TradingPipeline` wires
every layer into one `run()` cycle; `core_layer/logger/logger.py` gives every
module one consistent `setup_logger(name)`; `core/secrets.py` is the
single read path for every environment variable.

**Dependencies**: `pipeline.py` imports from `data/`, `context/`,
`signals/`, `ai/`, `decision/`, `risk/`, `telegram/`, `database/` —
by design, the one file allowed to import from every layer.
`logger.py`/`secrets.py` import nothing project-local.

**Public interfaces**: `TradingPipeline(symbol, interval).run()`,
`setup_logger(name)`, `Secrets().<PROPERTY>`.

**Future expansion points**: none documented beyond what
`docs/ARCHITECTURE.md` already states.

**Problems found**:
- **No `core/README.md`.** Every other layer with runtime code has
  one (see Documentation Audit); `core/` — arguably the single most
  important module, since it's the orchestrator — does not, and isn't
  even on `CLAUDE.md`'s or `docs/DEVELOPMENT_RULES.md`'s list of
  READMEs to read before a change.

**Missing abstractions**: none found. `core/` is small and its three
files each do exactly one thing.

---

## data/

**Purpose**: market data fetch and normalization.

**Responsibilities**: `twelve_data_client.py` talks to the Twelve Data
API; `market_data.py`'s `MarketDataNormalizer` validates/de-duplicates
candles into the pipeline's `Candle` shape.

**Dependencies** (grepped): imports `core/` only, project-internal.
No `context/`, `strategies/`, `signals/`, `ai/`, `decision/`, `risk/`,
`database/`, or `telegram/` import — correctly isolated as the
bottom-most layer.

**Public interfaces**: `MarketDataNormalizer.get_normalized_candles(symbol, interval)`.

**Future expansion points**: `data_layer/market_memory/data_cache.py` (`SmartDataCache`)
and `data_layer/live_data/session_filter.py` (`is_trading_time()`) are built but
unwired — see Documentation Audit / prior-phase findings, unchanged
this phase.

**Problems found**: none new. `twelve_data_client.py`'s `XAUUSD` →
`XAU/USD` symbol-formatting logic is documented as an example in its
own docstring, not a hardcoded restriction — the client itself is
symbol-generic (relevant to Folder Structure Review's multi-asset
question).

**Missing abstractions**: no retry/backoff policy around the Twelve
Data HTTP call visible from the module surface (out of this audit's
scope to assess further — not one of the seven roadmap items named in
Task 3).

---

## context/

**Purpose**: pure Smart Money Concepts (SMC) market-structure
detection — swings, structure classification, BOS/CHoCH, liquidity,
order blocks, FVGs, AMD cycles.

**Responsibilities**: nine files, each a narrow, independently
testable detector; `context_orchestrator.py`'s `ContextEngine` /
`build_context_snapshot()` runs them all in sequence and assembles one
immutable `ContextSnapshot`.

**Dependencies** (grepped): imports `core/` and `data/` (for `Candle`)
only. No `strategies/`, `signals/`, `ai/`, `decision/`, `risk/`,
`database/`, `telegram/` import.

**Public interfaces**: `build_context_snapshot(candles) ->
ContextSnapshot`. `ContextSnapshot`'s field list (see below) is a
"stable contract" per its own docstring.

**Future expansion points**: `context_config.py` line 12 explicitly
names "future additions such as volume, HTF bias, session detection"
— the only place in the entire codebase HTF bias is mentioned at all,
and it's a comment, not a field or a function.

**Problems found**:
- `ContextSnapshot` has **no HTF-bias field, no session field, no
  market-regime field** — confirms these aren't just "unused," they
  don't exist as data at the context layer at all (see Foundation Gap
  Analysis).
- Test coverage is uneven: `context_orchestrator.py` 95%,
  `context_config.py` 100%, but `amd.py` 30% (lowest in the whole
  repo), `bos.py`/`choch.py` 51%, `market_structure.py` 59%,
  `candle.py` 47%. The core structure-detection math — the foundation
  every strategy and the (currently-planned) HTF/Wyckoff work would
  sit on — is the least-tested code in the project.

**Missing abstractions**: no Wyckoff phase classifier (Accumulation/
Markup/Distribution/Markdown/Spring/UTAD) — `amd.py`'s
Accumulation-Manipulation-Distribution cycle detector uses overlapping
vocabulary (`ACCUMULATION`/`MANIPULATION`/`DISTRIBUTION` in
`AmdEventType`) but is a distinct, narrower SMC concept, not a Wyckoff
engine — see Foundation Gap Analysis Task 3.

---

## strategies/

**Purpose**: independent signal-candidate generation, one file per SMC
methodology.

**Responsibilities**: `liquidity_strategy.py`, `fvg_strategy.py`,
`amd_strategy.py` each turn `ContextSnapshot` data into
`SignalCandidate` objects; `strategy_manager.py`'s `StrategyManager`
runs all three and concatenates the results.

**Dependencies** (grepped): `context/` (for `ContextSnapshot`) and —
**`signals/`** (`from signals.models import SignalCandidate,
SignalType` in all three strategy files). This is a real,
package-level dependency in the "wrong" direction relative to the
documented Data Flow diagram (Strategies sits above Signal Generation
in `docs/ARCHITECTURE.md`) — see Dependency Map and "Architecture
Improvement Recommendations" below.

**Public interfaces**: `StrategyManager().run_all_strategies(context)
-> List[SignalCandidate]`.

**Future expansion points**: none documented — no README exists for
this module at all (see Documentation Audit).

**Problems found**:
- **No `strategies/README.md`.** Also absent from both `CLAUDE.md`'s
  and `docs/DEVELOPMENT_RULES.md`'s "read before a change" README
  lists — this is the layer that would gain a fourth entry
  (Wyckoff Strategy) under v0.3.5's roadmap, and it currently has zero
  documented Purpose/Flow/Input/Output contract.
- Lowest test coverage of the whole strategy chain:
  `liquidity_strategy.py` 36%, `amd_strategy.py` 37%,
  `fvg_strategy.py` 44%. `strategy_manager.py` itself is 100% covered
  (it's a thin loop), but the actual per-methodology logic is
  under-tested.

**Missing abstractions**: no shared "strategy interface"/ABC —
`StrategyManager.__init__` hardcodes a Python list of three concrete
classes rather than a registered/pluggable interface. Fine at 3
strategies; the natural place a future Wyckoff strategy (or session-
based strategy) would need to slot in without `strategy_manager.py`
growing an ad hoc if/else.

---

## signals/

**Purpose**: the `SignalCandidate` data contract and strategy-output
aggregation.

**Responsibilities**: `models.py` defines `SignalCandidate`/
`SignalType`; `signal_engine.py`'s `SignalEngine` calls
`StrategyManager.run_all_strategies()` and returns the result list
unchanged (`signal_engine.py` is 9 lines).

**Dependencies** (grepped): `context/` and — **`strategies/`**
(`signal_engine.py` imports `strategies.strategy_manager.StrategyManager`).
Combined with the previous section: `strategies` imports
`signals.models`, and `signals.signal_engine` imports
`strategies.strategy_manager`. **This is a real, two-way, package-
level circular dependency.** It does not crash today (Python resolves
it because the exact submodules involved — `signals/models.py` and
`strategies/strategy_manager.py` — don't import each other directly,
only their sibling submodules do), but the two packages are mutually
dependent, which `docs/ARCHITECTURE.md`'s stated one-directional
"Strategies → Signal Generation" flow does not disclose.

**Public interfaces**: `SignalEngine().generate_candidates(context) ->
List[SignalCandidate]` (per `signals/README.md`; re-confirmed against
`signal_engine.py`).

**Future expansion points**: none documented beyond aggregation.

**Problems found**: the circular dependency above. Currently latent,
not actively breaking anything (100% test coverage on both files
involved), but fragile — a future change that makes either package
import the *other's* orchestration module directly (not just its
models) would produce a real `ImportError`.

**Missing abstractions**: none beyond what's noted above.

---

## ai/

**Purpose**: advisory-only AI evaluation layer.

**Responsibilities**: `ai_analyzer.py`'s `AIAnalyzer.analyze()` is the
one function `core/pipeline.py` calls. Everything else in `ai/`
(`interfaces.py`, `memory/`, `prompts/`, `profiles/`, `journal/`,
`analyzer/`, `ai_prompt.py`, `confidence_model.py`, `trade_journal.py`)
is foundation, not wired into the pipeline.

**Dependencies** (grepped): `context/` (for `ContextSnapshot`) and
`core/` only. No `database/`, `telegram/` import — correct per
`docs/ARCHITECTURE.md`'s Dependency Rules.

**Public interfaces**: `AIAnalyzer().analyze(signal, context) ->
AIAnalysisResult`.

**Future expansion points**: `ai/interfaces.py`'s
`AIAnalyzerInterface` is the documented contract a future real
provider (Phase 55) must implement; `docs/AI_ARCHITECTURE.md` covers
this in full.

**Problems found** — the single most consequential finding in this
entire audit:
- **`AIAnalyzer.analyze()` is a hardcoded, permanent-reject stub.**
  Read in full this phase: it always returns `AIAnalysisResult(approved=False,
  confidence=0.0, risk_score=1.0, explanation="AI Analyzer initialized.
  Pending heuristic integration.")` — regardless of the signal or
  context passed in. `decision/decision_engine.py`'s `evaluate()`
  hard-gates on `ai_analysis.approved`: if `False`, the action is
  always `REJECT`, unconditionally. **This means the production
  pipeline, in its current state, structurally cannot produce an
  APPROVE decision, ever** — not a bug, a known and repeatedly-
  documented limitation (`docs/v0.3_RELEASE_NOTES.md`'s Known
  Limitations, `docs/AI_ARCHITECTURE.md`), but worth restating
  plainly here because it is the actual root blocker behind Phase
  59's "Real Market Validation" scans producing zero approved signals
  by construction, independent of market conditions or any other
  layer's correctness.
- `ai/ai_prompt.py` and `ai/confidence_model.py` are fully built,
  0% test coverage, imported by nothing (re-confirmed by grep this
  phase) — but this is already documented as intentional
  (`docs/AI_ARCHITECTURE.md`'s own audit table), not a new finding.

**Missing abstractions**: none beyond the (already-planned, Phase 55)
gap between `AIAnalyzerInterface` and a real implementation.

---

## decision/

**Purpose**: blends signal confidence and AI confidence into one
final trade verdict.

**Responsibilities**: `decision_engine.py`'s `DecisionEngine.evaluate()`
— re-read in full this phase (see `docs/v0.3.5_SPECIFICATION.md`'s
Decision Engine audit answer for the exact formula).

**Dependencies** (grepped): `ai/` (for `AIAnalysisResult`, via
`TYPE_CHECKING` only — see below) and `signals/` (also
`TYPE_CHECKING`-only). No `database/`, `telegram/`, `risk/` import.

**Public interfaces**: `DecisionEngine(config: DecisionConfig).evaluate(signal,
ai_analysis) -> TradeDecision`.

**Future expansion points**: `DecisionConfig`'s `min_confidence`/
`approve_confidence` thresholds are the one thing `CLAUDE.md`'s
Trading Safety rules name explicitly as requiring approval to change.

**Problems found**:
- **`DecisionResult` (a second, separate result dataclass with a
  `risk_score` field) is defined in `decision_engine.py` but never
  instantiated or imported anywhere else in the codebase** — confirmed
  by a full-repo grep this phase. Dead code; `evaluate()` actually
  returns `TradeDecision` (a different class, in `decision/models.py`),
  not `DecisionResult`. Not flagged for removal here (out of this
  phase's no-code-change scope) — flagged for v0.3.5 cleanup
  consideration.
- The confidence formula is a flat, unweighted 50/50 average of
  `signal.confidence` and `ai_analysis.confidence` — see Decision
  Engine Audit answer in `docs/v0.3.5_SPECIFICATION.md` for the full
  answer to "weightlar to'g'rimi? HTF bias qo'shilganmi? strategy
  score mavjudmi?".

**Missing abstractions**: no separate "Technical Score" input distinct
from `SignalCandidate.confidence` (which is computed upstream, inside
each strategy, and arrives at `DecisionEngine` as one opaque number) —
see Foundation Gap Analysis, Signal Quality Score.

---

## risk/

**Purpose**: SL/TP geometry and stop-loss-distance validation; sizing
suggestion only — never executes.

**Responsibilities**: `risk_manager.py`'s `RiskManager.evaluate()` —
unchanged since the critical notification-safety fix (commit
`3fe94cf`), re-confirmed this phase.

**Dependencies** (grepped): `decision/` (for `TradeDecision`,
`DecisionAction`) and `signals/`. No `database/`, `telegram/` import.

**Public interfaces**: `RiskManager(config: RiskConfig).evaluate(decision) ->
RiskResult`.

**Future expansion points**: none beyond what `risk/README.md`
already states — this is explicitly the layer `CLAUDE.md` names as
requiring approval to change (geometry/stop-loss validation and sizing
formulas).

**Problems found**: none new this phase.

**Missing abstractions**: none found relevant to Task 3's roadmap
items.

---

## execution/

**Purpose**: inert scaffolding for a future MT5/broker integration.

**Responsibilities**: `execution_engine.py`, `signal_lifecycle.py` —
neither is imported by `core/pipeline.py`, `main.py`, or anything else
outside `execution/` itself (re-confirmed by grep this phase: zero
external importers).

**Dependencies** (grepped): `risk/` (`execution_engine.py` imports
`RiskResult`) — a forward-looking type dependency only, not a live
call.

**Public interfaces**: none reachable at runtime.

**Future expansion points**: wiring this up is itself a change
requiring explicit approval per `CLAUDE.md`'s Trading Safety rules —
correctly still true, unchanged this phase.

**Problems found**: none new. 0% test coverage, consistent with being
fully inert.

**Missing abstractions**: n/a — this module is deliberately a stub.

---

## monitoring/

**Purpose**: signal observation / performance statistics reading — not
wired into any live command.

**Responsibilities**: two files with **different** isolation
postures, which is itself a finding:
- `signal_monitor.py`'s own docstring states an explicit isolation
  contract: "No SignalState / execution.signal_lifecycle import, no
  execution.*, no database.*, no telegram.*, no logger, no MT5." True
  for this file, re-confirmed by grep.
- `performance.py` **does** import `database.signal_repository.SignalRepository`
  directly (re-confirmed this phase) — a real database dependency
  that `signal_monitor.py`'s stated contract does not apply to, and
  that no README documents (`monitoring/README.md` doesn't exist —
  see Documentation Audit).

**Dependencies** (grepped): `core/` (logger) and `database/`
(`performance.py` only).

**Public interfaces**: none reachable at runtime — zero external
importers of either file (re-confirmed by grep this phase, same as
`execution/`).

**Future expansion points**: `signal_monitor.py`'s docstring names "a
future event contract" for signal-state monitoring; nothing
equivalent is stated for `performance.py`.

**Problems found**:
- **No `monitoring/README.md`.**
- The package-level isolation claim ("no database.*") is only true for
  one of its two files, and this inconsistency is not documented
  anywhere.
- 0% test coverage on both files.

**Missing abstractions**: n/a — inert, same posture as `execution/`.

---

## database/

**Purpose**: SQLite persistence — the only place SQL is written.

**Responsibilities**: seven `*_repository.py`/`*_models.py` pairs plus
`database.py` (connection lifecycle, `Database.init_db()`),
`models.py` (idempotent schema init), and `signal_record.py` (the
persistence-identity wrapper `core/pipeline.py` uses to save a
pipeline result).

**Dependencies** (grepped): `config`, `core/` (expected, cross-
cutting) — and **`signals/`, `decision/`, `risk/`** via
`database/signal_record.py` specifically (`from signals.models import
...`, `from decision.models import TradeDecision`, `from
risk.risk_manager import RiskResult`). No `*_repository.py` file
imports any of these — the rule "`database/*_repository.py` never
imports `telegram/`" in `docs/ARCHITECTURE.md` is true and unaffected,
but that rule's scope (repositories only) does not cover
`signal_record.py`, which reaches three layers "up" relative to the
documented Data Flow diagram's ordering (Signal → AI → Decision →
Risk → Telegram → Database) to borrow their types for a persistence
wrapper. See Dependency Map and Architecture Improvement
Recommendations.

**Public interfaces**: one repository class per table
(`SignalRepository`, `UserRepository`, `SubscriptionRepository`,
`FeedbackRepository`, `AdminRepository`), each CRUD-shaped.

**Future expansion points**: `database/migrations/README.md`'s
foundation for a future versioned-migration script, unchanged.

**Problems found**:
- The upward type-dependency in `signal_record.py`, above.
- **No automated signal-outcome tracking.** `SignalRepository.update_signal_result()`
  exists and is idempotent/well-tested (92% coverage on
  `signal_record.py`), but its only caller in the entire codebase is
  `telegram/result_handler.py` — a manual, user-reported Telegram
  command. Nothing in `execution/`, `monitoring/`, or anywhere else
  checks live price against a stored `entry`/`stop_loss`/`take_profit`
  to determine WIN/LOSS/BE automatically. "Result" as a database field
  exists; "result" as a computed fact does not. This is the concrete
  finding behind the roadmap's "Phase 59 Signal Lifecycle" step (see
  Foundation Gap Analysis, Task 6).

**Missing abstractions**: an automatic outcome-evaluation service —
named but not built anywhere in this codebase today.

---

## telegram/

**Purpose**: the Telegram product layer — routing, permissions,
handlers, services, presentation.

**Responsibilities**: `polling.py` is the long-running inbound
listener; `command_router.py` → `handlers.py` → `*_service.py` →
`database/*_repository.py` is the enforced call chain
(`telegram/handlers.py` never imports `database/*`/`core/pipeline.py`
directly, re-confirmed by grep this phase); `signal_formatter.py`/
`notifier.py` are the pipeline's outbound path.

**Dependencies** (grepped): `ai/`, `decision/`, `risk/`, `signals/` —
all four, but exclusively from `signal_formatter.py`
(`from signals.models import SignalCandidate`, `from
ai.ai_analyzer import AIAnalysisResult`, `from decision.models import
TradeDecision`, `from risk.risk_manager import RiskResult`). Unlike
`database/signal_record.py`'s case above, this is architecturally
consistent with the documented Data Flow diagram — Telegram sits
downstream of AI/Decision/Risk, so importing their result types to
format a message is expected, not an inversion. `database/` is also
imported, but only from `telegram/*_service.py` files, never
`handlers.py` — correct per the stated rule.

**Public interfaces**: one `*_service.py` class per product surface
(`UserService`, `SubscriptionService`, `AdminService`,
`FeedbackService`, `SignalService`, `SignalAccessService`,
`NotificationService`).

**Future expansion points**: none beyond what `telegram/README.md`
states.

**Problems found**: `telegram/handlers.py` is 53% covered — the
lowest of any file with an external caller in the whole product layer
(345 statements, 163 uncovered) — and `telegram/polling.py` (0%,
expected — a long-polling loop) and `telegram/result_handler.py` (0%,
**not obviously expected** — it's a pure function processing a
Telegram command's result-reporting logic, not a blocking loop, and
its only caller path (the manual result-reporting command) has no
test coverage at all despite being the *only* path that ever populates
`signal_status`/`result` beyond `"NEW"`).

**Missing abstractions**: none beyond what's listed above.

---

## Architecture Improvement Recommendations (Task 5)

Recommendations only — **nothing below has been implemented.**

### 1. `strategies/` ↔ `signals/` circular package dependency

- **Current**: `strategies/*.py` imports `signals.models`;
  `signals/signal_engine.py` imports `strategies.strategy_manager`.
- **Problem**: a two-way package dependency the architecture docs
  don't disclose. No runtime failure today (the specific submodules
  involved don't cross-import each other), but any future change that
  makes either package's orchestration module reach into the other's
  orchestration module (not just its models) produces a real
  `ImportError`. Fragile, easy to trip on without noticing during a
  routine change.
- **Recommended architecture**: move `SignalCandidate`/`SignalType`
  (currently in `signals/models.py`) to a location both packages can
  depend on without depending on *each other* — e.g. a `signals/`
  package split into `signals/models.py` (imported by `strategies/`)
  and `signals/signal_engine.py` (imports `strategies/`, not the
  reverse). This is almost the current layout already; the fix is
  narrower than it sounds — `strategies/*.py` already only needs
  `signals.models`, never `signals.signal_engine`. The dependency is
  circular at the *package* level only because Python packages are
  imported as a whole in dependency-map tooling; at the *module* level
  it is already one-directional. **Recommendation: no file move
  needed — document the module-level (not package-level) dependency
  rule explicitly in `docs/ARCHITECTURE.md`**, i.e. "`strategies/`
  depends on `signals/models.py` only, never `signals/signal_engine.py`;
  `signals/signal_engine.py` depends on `strategies/strategy_manager.py`."
  A documentation fix, not a code migration.
- **Benefits**: removes a currently-invisible fragility; a future
  contributor reading `docs/ARCHITECTURE.md` would know exactly which
  submodule boundary must never be crossed.
- **Migration risk**: none (this recommendation is documentation-only).
- **Priority**: MEDIUM.

### 2. `database/signal_record.py`'s upward type dependency

- **Current**: `database/signal_record.py` imports `SignalCandidate`/
  `SignalType` from `signals.models`, `TradeDecision` from
  `decision.models`, `RiskResult` from `risk.risk_manager`, to type a
  persistence wrapper.
- **Problem**: `docs/ARCHITECTURE.md`'s Data Flow diagram places
  Database last, after Telegram; `database/`'s only stated dependency
  rule is "`database/*_repository.py` never imports `telegram/`" —
  silent on this file, which reaches three layers up (past Telegram)
  to borrow types.
- **Recommended architecture**: this is very likely the *correct*
  design already (a persistence record legitimately needs to know the
  shape of what it's persisting), so the recommendation is **not** to
  restructure the import — it's to make the existing Dependency Rules
  section in `docs/ARCHITECTURE.md` state this exception explicitly,
  the same way it already states the `telegram/*_service.py`-only
  database-import rule. An undocumented exception looks identical to
  an accidental violation to the next auditor; a documented one does
  not.
- **Benefits**: closes the gap between what the docs claim
  ("never depend upward") and what the code actually and reasonably
  does.
- **Migration risk**: none (documentation-only).
- **Priority**: LOW.

### 3. `monitoring/`'s inconsistent isolation contract

- **Current**: `signal_monitor.py` states (and honors) a strict
  "no database.*" isolation contract in its own docstring;
  `performance.py`, in the same package, directly imports
  `database.signal_repository.SignalRepository` with no equivalent
  statement anywhere.
- **Problem**: a future contributor reading `signal_monitor.py`'s
  docstring could reasonably assume the *package* is isolated from
  `database/`, when only one of its two files actually is.
- **Recommended architecture**: `monitoring/README.md` (currently
  missing — see Documentation Audit) should state the real, per-file
  posture rather than let one file's docstring stand in for the whole
  package.
- **Benefits**: prevents a future contributor from either (a) wrongly
  assuming `monitoring/` as a whole can't reach `database/`, or (b)
  wrongly assuming `performance.py`'s existing database access sets a
  precedent that `signal_monitor.py` should follow.
- **Migration risk**: none (documentation-only).
- **Priority**: LOW.

### 4. `decision/decision_engine.py`'s dead `DecisionResult` class

- **Current**: `DecisionResult` (with a `risk_score` field) is defined
  but never instantiated or imported anywhere in the codebase;
  `evaluate()` returns `TradeDecision` instead.
- **Problem**: dead code sitting directly beside the class that *is*
  used, in the single most safety-critical file in the project
  (`CLAUDE.md` names `decision_engine.py`'s thresholds as requiring
  explicit approval to touch) — a future reader could plausibly
  mistake `DecisionResult.risk_score` for a real, wired-in input to
  the decision formula, when the formula (see Foundation Gap Analysis)
  actually has no separate risk-score input at all.
- **Recommended architecture**: remove `DecisionResult` in a future,
  explicitly-approved cleanup pass (out of scope for this
  documentation-only phase) — or, if a future risk-score-weighted
  decision formula is intentionally planned, keep it but add a
  docstring stating so and connect it to a real code path.
- **Benefits**: removes a source of confusion in the codebase's most
  safety-sensitive file.
- **Migration risk**: low — confirmed zero external references this
  phase, so removal (when explicitly approved) would not break any
  caller. Still requires the explicit approval `CLAUDE.md` mandates
  for any change to `decision/decision_engine.py`.
- **Priority**: LOW.
