# TASK-CORE-001 — GoldBot Core Foundation Audit & Canonical Migration

Branch: `claude/collaboration`. Priority: CRITICAL. **AUDIT ONLY — no
code changed, no module deleted, no refactoring started** (verified:
this task produces only this document). Governed by `TASK-GOV-001.md`
Laws 1–12 and the Owner's Final Instruction ("refactoring emas... audit
natijasida tayyorlangan Migration Proposal keyingi TASK-CORE-002 uchun
yagona asos bo'ladi").

## 0. Authority-document discrepancy (flagged first — Owner should note)

The brief names five Master Documents as authority. **Only one exists:**

| Named authority | Status |
|---|---|
| `01_Ecosystem_Architecture.md` | ✅ `docs/architecture/01_Ecosystem_Architecture.md` |
| `02_Repository_Structure.md` | ❌ NOT FOUND |
| `03_Module_Contracts.md` | ❌ NOT FOUND |
| `04_Data_Flow_Contracts.md` | ❌ NOT FOUND |
| `05_Development_Standards.md` | ❌ NOT FOUND |

The `docs/architecture/` numbered family is `01_Ecosystem_Architecture`
+ `02_Data_Layer` … `11_Infrastructure` (the TASK-GOV-004 restructure) —
NOT the `02_Repository_Structure`/`03_Module_Contracts`/… names the
brief assumes. Rather than block this audit, it was run against the
authority that **does** exist and covers the same ground: `01_Ecosystem
_Architecture.md`, `03_GoldBot_Core.md`, and the Constitution-governed
set (`docs/constitution/CONSTITUTION.md`, `docs/architecture/
ARCHITECTURE_MASTER.md`, `LAYER_CONTRACT.md`, `MODULE_DEPENDENCIES.md`,
`DATA_FLOW.md`, `IMPORT_RULES.md`). **Recommendation:** a future
governance task creates the four missing documents (or the brief is
updated to reference the existing names). Not created here — this task
is Core audit, not doc authoring.

## 1. Repository Audit (Core modules)

| Dir | .py files | README |
|---|---|---|
| `core/` | 35 | ✗ none |
| `context/` | 20 | ✓ |
| `strategies/` | 21 | ✓ |
| `signals/` | 19 | ✓ |
| `decision/` | 8 | ✓ |
| `risk/` | 4 | ✓ |
| `monitoring/` | 14 | ✗ none |
| `features/` | 3 | ✓ |
| `assets/` | 6 | ✓ |
| `lifecycle/` | 5 | ✓ |
| `backtesting/` | 10 | ✗ none |
| `execution/` | 9 | ✓ |

No top-level `analysis/`, `confluence/`, `market_engine/`, or `signal/`
directory exists (confirmed). README gap: `core/`, `monitoring/`,
`backtesting/` have none — flagged for the Migration Proposal (§10).

## 2. Architecture Mapping (10 engines → real modules)

| Ecosystem Engine | Real module(s) | Exists as its own module? |
|---|---|---|
| Market Engine | `data/` (fetch) + `context/candle.py`/`market_structure.py` | **No** — absorbed (data/ + context/) |
| Context Engine | `context/context_orchestrator.py` (+ detectors) | ✅ Yes |
| Analysis Engine | `context/` detectors (Wyckoff/Regime/Session) + `signals/signal_quality.py` | **No** — absorbed |
| Strategy Engine | `strategies/strategy_manager.py` | ✅ Yes |
| Confluence Engine | inside each `strategies/*.py` + `signals/signal_quality.py` | **No** — absorbed |
| Decision Engine | `decision/decision_engine.py` | ✅ Yes |
| Risk Engine | `risk/risk_manager.py` | ✅ Yes |
| Signal Engine | `signals/signal_engine.py` | ✅ Yes |
| Monitoring | `monitoring/` | ✅ Yes |
| Simulation | `backtesting/` + `execution/simulator/` | ✅ Yes (named differently) |

Verified: no `class MarketEngine`/`AnalysisEngine`/`ConfluenceEngine`
anywhere in Core (grep: none). This matches `01_Ecosystem_Architecture.md`
§21 Conflict 1 (kept as "Accepted as Future Architecture" — the diagram
is the target; three of its engine boxes are responsibilities absorbed
into other modules today, not separate modules).

## 3. Module Responsibility Report

Full per-engine Responsibility / Input / Output / Dependencies /
Forbidden already exists and is authoritative in
`docs/architecture/ARCHITECTURE_MASTER.md` (Per-Layer Responsibility)
and `LAYER_CONTRACT.md` — not restated here (Reuse First / Constitution
Article 7). Core-audit summary:

| Module | Purpose | Provider (reads from) | Consumer (read by) | Public entry |
|---|---|---|---|---|
| `context/` | Stateless SMC structure detection → `ContextSnapshot`/`ContextSnapshotSchema` | `data/` | strategies/, signals/, decision/(HTF type), market/(schema) | `context_orchestrator.build_context_snapshot` |
| `strategies/` | 3 SMC methodologies → `List[SignalCandidate]` | context/ | signals/ | `strategies.strategy_manager.StrategyManager` |
| `signals/` | Candidate contract, quality grade, explainability, schema; STEP-08 `SignalManager` parallel pipeline | context/, strategies/ | decision/(types), pipeline | `signals.signal_engine.SignalEngine` |
| `decision/` | Weighted APPROVE/REJECT/NO_TRADE; STEP-09 `decision_manager` parallel | signals/, context/(HTF), `ai.ai_analyzer.AIAnalysisResult` (type) | risk/, pipeline | `decision.decision_engine.DecisionEngine` |
| `risk/` | Geometry/SL validation + sizing; last gate | decision/ | pipeline | `risk.risk_manager.RiskManager` |
| `monitoring/` | Health/error/resource/risk/signal/performance/system observers | many (observes) | telegram owner cmds | per-monitor classes |
| `features/` | Standardization layer (`MarketFeatures`) | context/signals output | future AI/ML | `features.feature_engine` |
| `assets/` | Asset metadata registry | config | future multi-asset | `assets.asset_registry` |
| `lifecycle/` | Strategy/paper-trade lifecycle metadata | decision/risk | future | `lifecycle/*` |
| `backtesting/` | Replay chain over context→…→risk (Simulation) | all Core (unmodified) | analytics/owner | `backtesting.backtest_engine` |
| `execution/` | Intentionally INERT (no MT5 order calls); `execution/simulator/` fills for backtest only | risk/ | (none live) | `execution.execution_engine` (inert) |
| `core/` | Orchestration (`pipeline.py`), guards, gateway, errors, logger, secrets, emergency | all | main.py | `core.pipeline.TradingPipeline` |

## 4. Layer Boundary Report

Rule (Owner): Core → Data Layer ALLOWED; Core → Application Services /
Platform / Telegram / UI FORBIDDEN.

| Crossing | Found? | Detail |
|---|---|---|
| Core → Data Layer (ALLOWED) | ✅ present, correct | `context/*` and `core/pipeline.py` import `data/` |
| Core → Platform | ✅ none | zero imports |
| Core → UI | ✅ none | zero imports |
| **Core → Telegram (FORBIDDEN)** | ⚠ **PRESENT** | `core/pipeline.py` imports `telegram.signal_formatter.SignalFormatter` + `telegram.notifier.Notifier` (the pipeline's delivery-boundary wiring); `monitoring/` imports `telegram.admin_service.AdminService` in 7 files (system/decision/risk/error/signal/performance/resource monitors) |
| **Core → Database (persistence)** | ⚠ **PRESENT** | `core/pipeline.py` (SignalRepository/SignalRecord), `core/emergency/emergency_manager.py`, and `monitoring/*` write/read the DB |
| Core → AI (type-only) | ⚠ present, documented | `decision/models.py` imports `ai.ai_analyzer.AIAnalysisResult` — a TYPE only (Constitution Article 1/3; `IMPORT_RULES.md`); the Decision Engine reads the AI's result value, never calls the AI layer |

**Reading of the crossings (audit judgment, not a fix):** the
`core/pipeline.py` → telegram/database crossings are the pipeline's own
delivery + persistence stages and are **documented and intentional** in
`ARCHITECTURE_MASTER.md` ("they meet only at the Telegram delivery
boundary"). They are the orchestrator wiring, not leaf-Core logic
reaching sideways. However, under the brief's strict "Core → Telegram
FORBIDDEN" rule they ARE boundary crossings and are recorded here. The
`monitoring/ → telegram/database` crossings are a monitoring
cross-cutting concern reaching up into `AdminService`/DB — the most
debatable crossings; candidate for a boundary review (§10). None is
changed by this audit.

## 5. Duplicate Report (audit only — nothing deleted)

| Checked | Finding |
|---|---|
| Duplicate Engine | None. Market/Analysis/Confluence "engines" are ABSENT (absorbed), not duplicated. |
| Duplicate Strategy logic | None found across `strategies/`. |
| Duplicate Decision logic | `decision/decision_manager.py` (STEP-09) is a **parallel, additive** manager that REUSES (does not recompute) `decision_engine.py`'s frozen verdict — documented as reuse, not a duplicate. |
| Duplicate Signal logic | `signals/manager.py` (STEP-08 `SignalManager`) is a **parallel, additive** canonical pipeline reusing `SignalSchema` — documented reuse, not a duplicate. |
| Duplicate Risk logic | None found. |

The two "parallel manager" files (STEP-08/09) are the only near-duplication
and both self-document as reuse-not-recompute. Flagged for the Migration
Proposal to confirm whether the engine and its manager should consolidate
(a later decision, not this audit's).

## 6. Dependency Report

- **Circular dependency:** none Core↔Data — `data/` imports nothing from
  `context/`/`strategies/`/`decision/`/`risk/`/`signals/`/`core.pipeline`
  (grep: zero). Forward-only, as Constitution Article 2 requires.
- **Invalid import / layer violation:** the §4 crossings (Core →
  Telegram/Database; monitoring → AdminService). These are the only
  upward/sideways imports found.
- **Hidden dependency:** `decision/models.py` → `ai.ai_analyzer` is a
  type-only import that is easy to miss in a dependency scan; recorded
  here explicitly. It is intentional and documented.
- Authoritative living dependency map: `docs/architecture/
  MODULE_DEPENDENCIES.md` / `IMPORT_RULES.md` (not restated).

## 7. Data Flow Report

**Real per-cycle order** (`docs/architecture/DATA_FLOW.md`, verified
against `TradingPipeline._log_stage()`):

```
market_data → data_quality → htf_bias → context → market_phase → signal
  → signal_quality → explainability → features → ai → decision → risk
  → signal_history → telegram_format → telegram_delivery → database
```

**Task's proposed Core flow:**
`MarketMemory → Market Engine → Context → Analysis → Strategy →
Confluence → Decision → Signal Engine`.

**Divergences (reported, per Step 7):**
1. **Source:** the real pipeline reads from `MarketDataNormalizer`
   (`data/market_data.py`), NOT `MarketMemory`. MarketMemory (MA-001) is
   built and canonical but is **not yet the pipeline's read source**
   (known gap from the Data Layer phase — TASK-ARCH-100/101).
2. **Order:** the task diagram places `Decision → Signal Engine` (signal
   last); the real flow is `signal → … → decision` (signal precedes
   decision). The task diagram omits `risk`, `data_quality`, `htf_bias`,
   `market_phase`, `features`, `ai`, and the delivery/persistence tail.
3. **Absorbed engines** (Market/Analysis/Confluence) appear as flow
   nodes in the task diagram but are not distinct stages in the real
   pipeline (they are inside `context`/`signal`/`strategy` stages).

Neither flow is "wrong" — the task diagram is target/conceptual; the
real flow is `DATA_FLOW.md`. The divergence is recorded for the
Migration Proposal, not reconciled here.

## 8. Gap Analysis (vs `01_Ecosystem_Architecture.md`)

| Engine | Present? |
|---|---|
| Context / Strategy / Signal / Decision / Risk / Monitoring | ✅ fully present, own modules |
| Simulation | ✅ present (`backtesting/` + `execution/simulator/`) |
| Market Engine | ⚠ partial — absorbed into `data/` + `context/`, no standalone module |
| Analysis Engine | ⚠ partial — absorbed into `context/` + `signals/signal_quality.py` |
| Confluence Engine | ⚠ partial — absorbed into `strategies/` + `signals/signal_quality.py` |
| MarketMemory as Core's read source | ❌ gap — Core reads `MarketDataNormalizer`, not `MarketMemory` (Data Layer phase left this unwired) |

## 9. Canonical Mapping

| Module | Status |
|---|---|
| `context/`, `strategies/`, `signals/signal_engine.py`, `decision/decision_engine.py`, `risk/risk_manager.py`, `core/pipeline.py`, `monitoring/`, `features/`, `assets/`, `backtesting/`, `execution/` (inert) | **CANONICAL** |
| `signals/manager.py` (STEP-08), `decision/decision_manager.py` (STEP-09) | **CANDIDATE FOR MIGRATION** — parallel/additive; confirm consolidation with the frozen engine |
| Market / Analysis / Confluence "Engine" | **GAP (not a module)** — CANDIDATE for a future decision on whether to promote to real modules or keep absorbed |
| Core→Telegram/DB wiring in `core/pipeline.py`, monitoring→AdminService | **CANDIDATE FOR MIGRATION** (boundary review) — not LEGACY, not DUPLICATE; a layering question |
| (none) | **LEGACY** — no Core module is legacy today |
| (none) | **DUPLICATE** — no true duplicate found |

## 10. Migration Proposal (for TASK-CORE-002 — no code here)

1. **Folder Refactoring Proposal:** add missing READMEs (`core/`,
   `monitoring/`, `backtesting/`) for parity. Decide (Owner) whether
   Market/Analysis/Confluence Engine become real modules or stay
   documented-as-absorbed (recommend: keep absorbed, per `01`'s
   "Accepted as Future Architecture" ruling — promoting them is a large
   change with no functional gain today).
2. **Module Migration Proposal:** consolidate each STEP-08/09 parallel
   manager with its frozen engine, OR formally document the two-layer
   (engine + manager) split as intended — a decision, not a rewrite.
3. **Dependency Refactoring Proposal (boundary):** the honest question
   this audit surfaces — `core/pipeline.py` and `monitoring/` import
   `telegram/` + `database/`. Options: (a) accept them as the documented
   orchestrator/delivery boundary (status quo, `ARCHITECTURE_MASTER.md`
   already sanctions the pipeline's delivery edge); (b) introduce a thin
   Core-owned "delivery port" interface so `core/pipeline.py` depends on
   an abstraction that `telegram/` implements (dependency inversion —
   removes the literal Core→Telegram import); (c) move signal
   persistence behind a Core-owned repository interface. All are
   proposals; none is executed. **Recommend (a) for the delivery edge
   (it is intentional and documented) and a focused review of the
   `monitoring/ → AdminService` crossing (the least-justified one).**
4. **Canonical Structure Proposal:** wire `MarketMemory` (MA-001) as the
   Core pipeline's read source (closes the §8 gap) — but that is a
   Data-Layer↔Core integration task with Trading-Safety implications and
   must be its own Owner-approved, test-covered task (it touches
   `core/pipeline.py`'s data source), explicitly NOT part of this audit.
5. **Missing authority docs:** create `02_Repository_Structure.md` /
   `03_Module_Contracts.md` / `04_Data_Flow_Contracts.md` /
   `05_Development_Standards.md` (§0) so the brief's named authority
   actually exists before TASK-CORE-002 relies on it.

## Handover / Status

```
TASK-ID:    TASK-CORE-001 (GoldBot Core Foundation Audit)
Status:     DONE (audit only). All 10 deliverables produced in this doc.
Findings:   7 engines real + Simulation; Market/Analysis/Confluence
            absorbed (not modules); MarketMemory not yet Core's read
            source (gap); boundary crossings Core->Telegram/Database in
            core/pipeline.py + monitoring/ (documented delivery edge +
            a monitoring cross-cut to review); decision->ai type-only
            (intentional); no circular deps; no true duplicates; 2
            parallel STEP-08/09 managers (reuse, candidate to
            consolidate); 4 of 5 named Master Documents do not exist.
No code:    verified -- 0 .py changed, 0 modules deleted, 0 refactoring.
Next:       TASK-CORE-002 executes from the §10 Migration Proposal,
            each item its own Owner-approved, test-covered task; the
            MarketMemory wiring and any boundary change touch
            core/pipeline.py and carry Trading-Safety review.
```
