# GoldBot Constitution v2.0 — Stage 0: Constitution Audit

Status: **AUDIT ONLY**. Per the Director's Stage 0 task, no code was
written, no repository file other than this one was changed, and
nothing described here has been implemented. This document reviews
Phase 1 through Phase 6 Freeze and reports findings for Director
review. Where this audit identifies a gap, tension, or stale
document, it is *flagged*, not fixed.

Method: this audit combines (a) direct reading of the governing
documents — `docs/constitution/CONSTITUTION.md`,
`docs/constitution/AMENDMENTS.md`, all five files in
`docs/architecture/`, `docs/roadmap/VERSIONS.md`,
`docs/telegram/TELEGRAM_ARCHITECTURE.md`, `docs/owner/OWNER_PANEL.md`,
and `docs/policies/DEVELOPMENT_POLICY.md` /
`docs/policies/DOCUMENTATION_POLICY.md` — with (b) four scoped,
grounded inventories: Trading Core (`context/`, `core/`, `data/`,
`decision/`, `execution/`, `lifecycle/`, `risk/`, `signals/`,
`strategies/`), the AI ecosystem (`ai/` and its 30 subpackages plus
`assistant/`, `voice/`, `knowledge/`, `learning/`, `broadcast/`,
`media/`, `translation/`), Database/Infrastructure (`database/`,
`monitoring/`, `configuration/`, `backtesting/`, `analytics/`,
`performance/`, `features/`, `contracts/`), and a full categorization
of all 264 files under `docs/`.

---

## Executive Summary

GoldBot already has most of the raw material a "Constitution v2.0"
would need: the 12-Article `docs/constitution/CONSTITUTION.md`
(amended once, Phase 62.1a), an 11-file `docs/policies/` set, and a
5-file `docs/architecture/` set. The real gap is not "write a
constitution from nothing" — it is four separate problems this audit
surfaces:

1. **Staleness.** Several documents that Directors and Workers treat
   as authoritative describe a pre-Phase-6.2 or pre-Phase-6.3 system.
   `docs/telegram/TELEGRAM_ARCHITECTURE.md` still says several
   callback families are unwired (false since Phase 6.2).
   `docs/roadmap/VERSIONS.md` stops before Phase 3 (Registration
   Wizard) and never mentions Phase 4, 5, 5.1, 6.0–6.3, or Phase 6
   Freeze at all — an entire platform layer's history is undocumented
   in the one file whose job is to record version history.
   `docs/owner/OWNER_PANEL.md` undercounts `telegram/owner/` by 8
   files. `ai/README.md` self-contradicts and is frozen at Phase
   61.7. `docs/README.md`, the master doc index, is missing 96 of 264
   files under `docs/` (36%) — everything from Phase 63 onward.

2. **Undisclosed layering.** Three real import relationships exist in
   the codebase today that no architecture document currently
   describes correctly: `risk/` (three files) imports `database/`
   directly, contradicting `risk/README.md`'s own "No dependency on
   database/" claim; `core_layer/emergency/emergency_manager.py` imports
   `database.*` directly, undocumented anywhere; and `voice/` runs a
   second, independent live integration against the OpenAI REST API,
   entirely outside `ai/providers/`/`ai/runtime/ai_service.py`, in
   apparent tension with Article 5's text. None of these are proposed
   fixes here — they are flagged for Director decision.

3. **Coverage gaps in the architecture docs.** `monitoring/` (13
   files), `configuration/` (8 files), `backtesting/` (9 files),
   `analytics/` (11 files), and `performance/` (3 files) are real,
   substantial packages with zero mention in
   `ARCHITECTURE_MASTER.md` or `MODULE_DEPENDENCIES.md`.
   `configuration/runtime_feature_manager.py` is a built feature-flag
   engine that, by its own README's admission, is never called from
   `core/pipeline.py` or any handler — wired to nothing.

4. **No Telegram UI Constitution content exists yet.** The Director's
   Stage 0 scope explicitly wants Reply Keyboard Primary Navigation,
   Coming Soon Policy, and Menu Stability Principle codified.
   Phase 6 Freeze's Stage 5 already produced a first draft of this
   under the name "GoldBot UI Stability Principle" (see
   `docs/PHASE6_FREEZE.md`), but it lives in a Freeze document, not in
   the Constitution, and is not yet an Article.

None of this blocks Constitution v2.0 — on the contrary, it means
Constitution v2.0's real job is narrower and more tractable than "write
everything": *consolidate what exists, backfill the Telegram UI
Constitution content that doesn't exist yet, resolve or explicitly defer
the three layering findings, and refresh the stale documents it
depends on.* Recommendations at the end of this document propose that
scope split.

---

## 1. Architecture Review

### 1.1 What already exists

`docs/architecture/` holds five files, all internally consistent with
each other in intent even where individually stale:

- `ARCHITECTURE_MASTER.md` — the system layer diagram plus per-layer
  CAN/CANNOT tables for Context, Strategy, Signal, Decision, Risk,
  Execution, TradeMonitor, Telegram, AI, and the Senior Trading AI
  Foundation. Current through Phase 63.0 only.
- `MODULE_DEPENDENCIES.md` — a detailed dependency table, strong for
  the AI subpackage ecosystem (21+ subpackages through Phase 65.2),
  thin for the Trading Core section, and contains one factual error
  (see 1.3 below).
- `IMPORT_RULES.md` — allowed/forbidden import tables operationalizing
  Constitution Article 3.
- `EXTENSION_GUIDE.md` — two patterns for adding new code (Pattern 1:
  new AI capability; Pattern 2: new Telegram command). There is no
  Pattern 3 for "add a new Reply Keyboard section," despite that being
  exactly the kind of change Phase 6.0–6.3 made four times.
- `MONITORING.md` — exists, and (per the docs-categorization
  inventory) is itself one of the files missing from `docs/README.md`'s
  index.

Also relevant but stored outside `docs/architecture/`:
`docs/trading/TRADING_ARCHITECTURE.md` (architecture-named, wrong
directory — a structural inconsistency, not a content problem), and
five historical/superseded top-level files (`ARCHITECTURE.md`,
`ARCHITECTURE_AUDIT.md`, `ARCHITECTURE_READINESS_REVIEW.md`,
`ARCHITECTURE_RULES.md`, `DEPENDENCY_MAP.md`) that `docs/README.md`
already annotates as historical/superseded — no action needed on
those, they are correctly labeled.

### 1.2 Coverage gap: five packages absent from the architecture docs

`monitoring/` (13 files), `configuration/` (8 files),
`backtesting/` (9 files), `analytics/` (11 files), and
`performance/` (3 files) are real, non-trivial packages with their own
READMEs, but none of them appear in `ARCHITECTURE_MASTER.md`'s layer
diagram or in `MODULE_DEPENDENCIES.md`'s table. This is a genuine
documentation gap, not a code problem — the packages themselves are
internally documented (each has its own README), they are simply
missing from the *system-wide* architecture picture a Constitution
would need to reference.

`configuration/runtime_feature_manager.py` deserves specific note: its
own README states it is a working runtime feature-toggle engine that
is never actually called from `core/pipeline.py` or any Telegram
handler. It exists, is tested in isolation, and is wired to nothing —
worth the Director's attention as either a completion task or an
explicit "reserved, not yet wired" designation.

### 1.3 Factual error found in `MODULE_DEPENDENCIES.md`

The table's entry for `trade_monitoring_layer/paper_trading/paper_trade_monitor.py` lists its
dependencies as `decision/`, `risk/`, `core/`. Direct inspection shows
the file only imports `trade_monitoring_layer.paper_trading.paper_trade` and
`trade_monitoring_layer.paper_trading.trade_state` — none of the three listed packages. This is a
factual inaccuracy in an authoritative document, not a design
question; flagged for correction whenever `MODULE_DEPENDENCIES.md` is
next revised.

### 1.4 Inter-document inconsistency: `core/pipeline.py`'s composition-root exception

`core/pipeline.py` imports from `ai/`, `telegram/`, and `database/` —
which on its face crosses several layers described elsewhere as
forbidden. One existing document explains this as a deliberate
"composition root" exception (the pipeline is what wires the layers
together, so it is allowed to import all of them). `IMPORT_RULES.md`,
however, states a blanket "`core/` → anything: forbidden" rule with no
carve-out for the composition root. The exception is real and
intentional, but it is not written into the one document
(`IMPORT_RULES.md`) whose entire purpose is to be the operational
source of truth for import legality. Flagged as an inter-document
inconsistency, not a code violation.

### 1.5 `EXTENSION_GUIDE.md`'s missing Pattern 3

Phase 6.0 through 6.3 added four new sections to the Reply Keyboard
system (Main, Settings, Admin, Owner submenus) using a pattern that
was worked out ad hoc each time rather than following a documented
template. `EXTENSION_GUIDE.md` has patterns for "new AI capability"
and "new Telegram command" but nothing for "new Reply Keyboard
section" — the exact shape of change this session's own Phase 6 work
repeatedly made. This is a real gap for a Constitution v2.0's UI
Constitution / Extension Guide content to close.

---

## 2. Telegram Review

### 2.1 Current, accurate documentation

Phase 6 Freeze's own document (`docs/PHASE6_FREEZE.md`) is the
freshest and most accurate single source for the Telegram layer as it
exists today: full Reply Menu state diagram, navigation diagram,
translation coverage, and the frozen target Reply Menu layout (Home /
Signals / Chart(Coming Soon) / AI Assistant(Coming Soon) /
News(Coming Soon) / Calendar(Coming Soon) / Academy(Coming Soon) /
Premium / Profile / Settings / Help). This is the right document to
anchor a Constitution v2.0 Telegram Constitution section on, rather
than rewriting anything from scratch.

### 2.2 Stale: `docs/telegram/TELEGRAM_ARCHITECTURE.md`

This document still states that `risk_*`, `timeframe_*`, `strategy_*`,
and `notifications_*` callbacks are "recognized but not yet wired to a
handler." This has been false since Phase 6.2, when
`callback_router.py`'s `_handle_setting()` wiring was completed and
committed (`dfb73e3`). The document also contains no mention of the
Registration Wizard (Phase 3), the Reply Keyboard Navigation system
(Phase 5/5.1/6.0–6.3), or Phase 6 Freeze at all. This is the most
Director-visible staleness finding in this audit, because it is the
one document most likely to be consulted by name when someone asks
"how does Telegram routing work" — and it currently describes a system
state that predates roughly five phases of shipped work.

### 2.3 Stale: `docs/owner/OWNER_PANEL.md`

States "19 files" under `telegram/owner/`. Actual count (per the
Database/Infra inventory) is 27 — the document predates Phase B.0's
additions (e.g. `monitoring_commands.py`).

### 2.4 Reply Keyboard as Primary Navigation — already the de facto rule, not yet an Article

Phase 6.3's retirement of the inline Navigation Controller
(`telegram/navigation.py`, deleted outright) in favor of
`telegram/reply_keyboard_manager.py` already establishes Reply
Keyboard as the system's sole navigation mechanism in practice. No
inline navigation menus remain; inline keyboards are used only for
pickers (settings toggles, etc.), consistent with what the Director's
Stage 0 scope asks the UI Constitution to state as a rule. This is a
case where the codebase already enforces the rule the Constitution
would write down — the audit finds no violation, only the absence of
the rule's text in a governing document.

### 2.5 "Coming Soon" policy — drafted once, not yet canonical

Phase 6 Freeze's Stage 5 documented which Reply Menu entries are
"Coming Soon" (Chart, AI Assistant, News, Calendar, Academy) and
introduced the "GoldBot UI Stability Principle" (Reply Menu is
permanent navigation; unfinished features render as Coming Soon
placeholders; the menu is not redesigned each time a new module ships)
as a proposal, not as an adopted Constitution Article. This is a
direct match for the Director's Stage 0 request and is ready to be
promoted essentially as-is.

---

## 3. Trading Review

### 3.1 Existing Constitution coverage

Constitution v1's Articles already state the core Trading Constitution
rules the Director's Stage 0 scope asks for: Article 1 (AI assists,
never decides), Article 2 (forward-only Dependency Law: Data → Context
→ Strategy → Signal → AI → Decision → Risk → Telegram), Article 3
(import rules — `ai/` may never import `decision/`, `risk/`, or
`execution/`). The Trading Core inventory's Article 3 grep across
`context/`, `core/`, `data/`, `decision/`, `execution/`, `lifecycle/`,
`risk/`, `signals/`, `strategies/` found **zero violations** of the
forward-only pipeline direction or of the AI-never-imports-execution
rule. The pipeline's dependency direction is intact.

### 3.2 Finding: `risk/` imports `database/` directly (undisclosed)

`risk_layer/risk_engine/risk_manager.py`, `risk_layer/risk_engine/account_state_tracker.py`, and
`risk_layer/risk_validator/duplicate_checker.py` import directly from
`database/*_repository.py` modules — real, module-level imports, not
`TYPE_CHECKING`-only. This contradicts `risk/README.md`'s own explicit
statement that risk/ has "No dependency on database/", and it is not
reflected in `MODULE_DEPENDENCIES.md`'s table. The import chain dates
to a specific, named patch: "Phase V1.0.1: Risk Management Hardening
Patch."

This is not cleanly an Article 4 violation (Article 4's
Handler→Service→Repository rule is written for the Telegram side); it
sits in a gap between Article 2 (Dependency Law, which describes the
seven-layer pipeline but says nothing explicit about a Risk→Database
edge) and `IMPORT_RULES.md` (which likewise has no explicit rule
either permitting or forbidding this edge). This audit flags it as a
**real, undocumented layering fact requiring a Director decision** —
either the Dependency Law / IMPORT_RULES.md should be amended to
explicitly permit Risk → Database (documenting reality), or the
dependency should be redesigned to route through a service layer
(a code change, out of scope for this audit). No fix is proposed here.

### 3.3 Finding: `core_layer/emergency/emergency_manager.py` imports `database/` directly (undisclosed)

Same shape of finding as 3.2, in a different module: real,
module-level `database.*` imports from `core_layer/emergency/`, not
documented anywhere. Flagged alongside 3.2 as the same class of issue
— likely warranting the same Director decision (amend the Dependency
Law to acknowledge it, or treat it as a target for future
refactoring).

### 3.4 Composition root exception

See 1.4 above — `core/pipeline.py`'s own cross-layer imports are a
known, intentional exception (it is the layer that wires everything
together) but are not written into `IMPORT_RULES.md`'s blanket rule.
Same finding, cross-referenced here because it touches the Trading
Core directly.

### 3.5 No violations found in Strategy/Signal/Decision boundaries

The Trading Core inventory confirms: `strategies/` never places
orders, `signals/` and `context/` are consumed read-only by later
layers, `decision/` is the only layer that produces an
APPROVE/REJECT/NO_TRADE verdict, and `execution/` (still intentionally
inert — no live MT5 order calls exist) never performs its own market
analysis. These match Constitution v1's existing Trading Constitution
language exactly; no gap found here.

---

## 4. Database Review

### 4.1 Existing coverage

`docs/DATABASE.md` (top-level) documents the schema, and Article 4
already states the Handler→Service→Repository→Database rule, which
the Trading Core and Database/Infra inventories both confirm is
enforced today (no direct `telegram/handlers.py` → `database/` calls
found).

### 4.2 No migration or rollback tooling exists

`database_layer/database_manager/models.py` performs ad hoc, idempotent
`CREATE TABLE IF NOT EXISTS` / `ALTER TABLE` statements on every
repository construction. `database/migrations/` exists as a directory
but is an empty placeholder containing only a README describing a
*future* migration scheme — no automated migration or schema-rollback
tooling exists today, for 17 tables across 17 repositories. This is a
real, material gap the Director's "Migration, Rollback, Versioning"
Database Constitution scope calls out by name; today the answer is
"not built yet," which the Constitution should state plainly rather
than imply otherwise.

### 4.3 PostgreSQL readiness — documented, not started

`docs/DATABASE.md` has a genuine "PostgreSQL Readiness" section (not
fabricated) describing what a future Postgres conversion would need.
No conversion work has been done. This matches what the Director's
scope asks the Database Constitution to state as a forward-looking
item — the groundwork is written, the work itself is future.

### 4.4 Registration, Users, Signals, Journal, Analytics, Audit Trail

Covered by existing schema documentation and the Database/Infra
inventory's table-by-table pass; no undocumented tables or orphaned
repositories were found. No findings beyond 4.2/4.3 in this area.

---

## 5. AI Review

### 5.1 Existing coverage

`docs/ai/AI_ARCHITECTURE.md` (distinct from the stale top-level
`docs/AI_ARCHITECTURE.md`, which is correctly labeled historical in
`docs/README.md`) is current and accurate. Article 1 (AI assists,
never decides) and Article 5 (Provider Rule: one AI vendor contract,
`BaseAIProvider`/`ProviderResult`, vendor names confined to
`ai/providers/` + `ai/runtime/ai_service.py`) are both well-specified
in Constitution v1 already.

The AI-ecosystem inventory's Article 3 grep (AI layer never importing
`decision/`, `risk/`, or `execution/`) across all 30 `ai/` subpackages
plus `assistant/`, `voice/`, `knowledge/`, `learning/`, `broadcast/`,
`media/`, `translation/` found **zero violations**. AI remains
advisory-only in every subpackage checked.

### 5.2 Finding: `voice/` runs an independent OpenAI integration outside the Provider Rule

`voice/provider_adapters/openai.py` and `voice/stt/providers/openai.py`
make real, live HTTP calls directly to OpenAI's REST API. This sits
entirely outside `ai/providers/` and `ai/runtime/ai_service.py` — it
is a second, independent vendor integration. Read literally, Article
5's text ("vendor names confined to `ai/providers/` +
`ai/runtime/ai_service.py`") is violated by this. `voice/README.md`
argues this is "a different concern" (speech-to-text vs. text
generation/analysis) and therefore not subject to the same rule, but
that argument is not written into Article 5 itself — Article 5 as
currently worded does not carve out an STT exception.

This is the single most significant Article-level tension found in
this audit. It genuinely requires a Director decision between two
paths, neither of which this audit recommends: (a) amend Article 5 to
explicitly scope the Provider Rule to text-generation/analysis
providers, carving out STT/voice as a documented exception, or (b)
unify voice's OpenAI calls to route through the same
`BaseAIProvider`/`ProviderResult` contract as every other vendor call,
which would be a real code change.

### 5.3 Documentation staleness in the AI cluster

- **`ai/README.md`** (the package's own top-level README, distinct
  from the current `docs/ai/AI_ARCHITECTURE.md`) is severely stale:
  internally self-contradictory, narrative frozen at Phase 61.7, no
  mention of anything from Phase 62 through 66.8, and does not mention
  the `assistant/` or `voice/` packages at all despite both existing
  and being substantial. This is the single most out-of-date document
  found anywhere in the AI cluster.
- `docs/roadmap/AI_EVOLUTION.md` — noted by the AI-ecosystem inventory
  as also lagging behind the most recent phases, though less severely
  than `ai/README.md`.
- `docs/README.md`'s index is missing 17 of 24 `ai/` subsystem docs
  (`AI_VOICE.md`, `AI_CHART_INTELLIGENCE.md`, `AI_MEDIA.md`,
  `AI_TRADING_ANALYST.md`, `AI_CONTENT.md`, `AI_TRADE_JOURNAL.md`,
  `AI_COACHING.md`, `AI_LEARNING.md`, `AI_RESEARCH.md`,
  `AI_REASONING.md`, `AI_PERFORMANCE.md`, `AI_PORTFOLIO.md`,
  `AI_BROADCAST.md`, `AI_CONVERSATION.md`, `AI_PERSONAL_ASSISTANT.md`,
  `AI_STRATEGY.md`, `AI_INTELLIGENCE_PIPELINE.md`).

### 5.4 `learning/` vs. `ai/learning/` — distinct, already cross-referenced

Top-level `learning/` (Phase 60.6/60.7, deterministic trade-outcome
pattern analysis) and `ai/learning/` (Phase 66.3, AI
vocabulary/topic-mastery tracking) are unrelated concepts that happen
to share a directory name. Both packages' own docs already
cross-reference each other as "reviewed but not reused" — this is
correctly disclosed today, not a finding requiring action, but worth
naming explicitly in the Constitution so a future Worker doesn't
assume they're duplicates and try to merge them.

### 5.5 No autonomous execution found

Consistent with Article 1 and the Director's Stage 0 scope item "No
autonomous execution": no AI-layer code calls the Risk Manager,
triggers a Telegram send, or performs an execution action directly, in
any of the 30+ subpackages inventoried. This matches
`ai/interfaces.py`'s `AIAnalyzerInterface` contract as documented.

---

## 6. UI Review

(Reply Menu / Settings / Profile / Signals / Chart / Coming Soon /
Navigation consistency / Localization / Button naming / Emoji rules)

### 6.1 Current state

Phase 6 Freeze's Stage 2–6 output (`docs/PHASE6_FREEZE.md`) is the
authoritative, current description of the full Reply Menu system:
state diagram, every Main↔submenu transition, translation coverage
(111 keys after Phase 6 Freeze's Stage 9 cleanup, EN/UZ/RU complete,
zero missing/duplicate/unused), and the frozen target layout. This
review found no discrepancy between that document and the live code
in `translation/ui_catalog.py` or `telegram/reply_keyboard_manager.py`.

### 6.2 Button naming / emoji rules — implicit, not written down

The current Reply Menu consistently uses a
`{emoji}{Label}` / `{emoji}{Label}(Coming Soon)` pattern across every
menu tier, but no document states this as a rule — it is a pattern a
Worker would have to infer by reading `translation/ui_catalog.py`
directly. This is a small, concrete gap a UI Constitution section
could close cheaply.

### 6.3 No Pattern 3 in `EXTENSION_GUIDE.md`

Repeated from 1.5: adding a new Reply Keyboard section has no
documented template today, despite being done four times across Phase
6.0–6.3. Flagged once here for the UI Constitution's benefit
specifically.

---

## 7. Future Platform Review

### 7.1 Existing reservation table

Phase 6 Freeze's Stage 6 already produced a Future Module Reservation
table (Reserved / Purpose / Entry Point / Reply Menu Position /
Status) for 16 modules: Chart, AI Assistant, AI Analyst, Economic
Calendar, News Center, Academy, Analytics, Portfolio, Trade Journal,
Trade Replay, Market Scanner, Notifications Center, Community,
Marketplace, Settings, Premium.

### 7.2 Gap against the Director's fuller Stage 0 list

The Director's Stage 0 scope names a longer list, including several
modules absent from the Phase 6 Freeze table: **Voice Assistant,
Marketplace** (already present), **Copy Trading, Broker Center,
Automation, Cloud Sync, Multi Device, API Center, Plugin System,
Developer Mode**, plus an open-ended "...". None of these have a
Reserved/Purpose/Entry Point/Reply Menu Position/Status row anywhere
yet. This is a straightforward extension of an existing table, not a
new concept — flagged as a concrete to-do for whichever phase actually
writes Constitution v2.0's Future Platform Constitution section.

### 7.3 Related existing package: `contracts/`

`contracts/` (10 `.md` interface-spec files, no code) already exists
as a form of "reserved module" specification pattern — worth the
Constitution cross-referencing rather than inventing a second
convention for the same purpose.

---

## 8. Development Review

(Version Policy, Freeze Policy, Review Policy, Audit Policy, Testing
Policy, Commit Policy, CI Policy, Rollback Policy, Production Policy)

### 8.1 All nine already exist as individual policy documents

`docs/policies/` holds 11 files, nine of which map directly onto the
Director's Stage 0 Development Constitution list:
`VERSION_POLICY.md`, `RELEASE_POLICY.md` (Freeze-adjacent),
`DIRECTOR_POLICY.md` (Review Policy), `TESTING_POLICY.md`,
`DEVELOPMENT_POLICY.md` (Commit/CI-adjacent), `SECURITY_POLICY.md`,
plus `AI_POLICY.md`, `BROADCAST_POLICY.md`, `FOUNDATION_POLICY.md`,
`OWNER_POLICY.md`, `DOCUMENTATION_POLICY.md` covering adjacent ground.
This audit did not find a standalone "Rollback Policy" or "Audit
Policy" document by that exact name — `docs/deployment/ROLLBACK.md`
covers rollback mechanics at the deployment level, and audit practice
is implicit in the repeated `PHASE*_AUDIT.md` convention (48 such
documents exist) rather than codified as a single named policy.

### 8.2 CLAUDE.md's Commit Protocol is the de facto Commit Policy

The repository's own `CLAUDE.md` (governance instructions for any
agent working in this repo) already specifies an 11-step mandatory
Commit Protocol (stage → pyflakes → compileall → pytest → smoke-run →
clean git status → diff review → commit → push → CI confirmation),
enforced in practice across every phase of this session's own work
(Phase 6.2, Phase 6 Freeze). This is a strong, already-working Commit
Policy; a Constitution v2.0 Development Constitution section should
reference it rather than re-derive it.

### 8.3 Phase-numbering / naming convention observations

The docs-categorization inventory found one concrete naming
inconsistency worth the Director's attention:
`FOUNDATION_FREEZE_v0.4.md` is functionally a freeze document (sits
chronologically between `PHASE60_10_FOUNDATION_AUDIT.md` and
`PHASE61_AI_FOUNDATION_AUDIT.md`) but does not follow the
`PHASE*_FREEZE.md` naming convention every other of the 44 freeze
documents follows. Also found: a duplicate filename,
`DOCUMENTATION_STANDARD.md`, exists both at the top level (Phase A14,
older) and under `standards/DOCUMENTATION_STANDARD.md` (current, the
one indexed in `docs/README.md`) — same name, two different documents,
one stale. Neither is a code issue; both are naming-hygiene items a
Development Constitution's documentation-naming rule could prevent
going forward.

### 8.4 `docs/README.md` index — the completeness gate has lapsed

`docs/README.md` is a genuinely curated (not auto-generated) index
with a stated convention: *"When adding a new document, add it here in
the same pass."* That convention is sound and matches what a
Development/Documentation Constitution should require. In practice it
has not been followed since Phase 62.1d — 96 of 264 files (36%) under
`docs/` are absent from it, concentrated in every Phase 63–66.8
audit/freeze document, 17 of 24 `ai/` subsystem docs, both
`deployment/` files, and `architecture/MONITORING.md`. This is
evidence *for* whatever documentation-completeness gate a Constitution
v2.0 Documentation Constitution section proposes — the rule already
exists in writing, enforcement is what lapsed.

---

## 9. Open Questions

Per the Director's explicit instruction, these are recorded without
being answered.

1. Should the Risk → Database and Emergency Manager → Database import
   edges (Section 3.2, 3.3) be formally added to the Dependency Law as
   permitted exceptions, or should they be refactored to route through
   a service layer instead?
2. Should Article 5 (Provider Rule) be amended to explicitly scope
   itself to text-generation/analysis AI providers, carving out
   speech-to-text as a separate, documented exception — or should
   `voice/`'s OpenAI integration be unified under
   `BaseAIProvider`/`ProviderResult`?
3. Should `core/pipeline.py`'s composition-root exception (crossing
   `ai/`/`telegram/`/`database/` imports) be written explicitly into
   `IMPORT_RULES.md`, rather than living only in prose elsewhere?
4. Should Chart become a core module, or remain a Telegram-layer
   "Coming Soon" placeholder indefinitely?
5. Should AI Assistant have its own architectural layer distinct from
   `ai/`, given `assistant/` already exists as a separate top-level
   package?
6. Should Portfolio live inside the Telegram layer or become a
   platform-level module with its own data model?
7. Should Plugin System / Developer Mode / API Center be reserved now
   (added to the Future Module Reservation table with a Status of
   "Reserved, not started"), or left undocumented until a concrete
   proposal exists?
8. Should database migration/rollback tooling (Section 4.2) be built
   before or after Constitution v2.0 is adopted — i.e., is "no
   migration tooling exists" an acceptable state for the Constitution
   to simply document, or a gap it should mandate closing?
9. Should `docs/architecture/` gain explicit sections for
   `monitoring/`, `configuration/`, `backtesting/`, `analytics/`, and
   `performance/` as part of Constitution v2.0, or as a separate,
   later architecture-documentation phase?
10. Is `configuration/runtime_feature_manager.py` (built, tested, but
    wired to nothing) intended to be wired into `core/pipeline.py` in
    a future phase, or is it dead weight the Constitution should mark
    for removal consideration?

---

## 10. Recommendations

These are offered as scope suggestions for whatever phase actually
*writes* Constitution v2.0 (a separate, future, code/doc-touching
phase per the Director's own closing note) — not as decisions made by
this audit.

1. **Treat Constitution v2.0 as consolidation-plus-three-additions,
   not a rewrite.** Most of Architecture/Trading/Database/AI/Module
   Reuse Constitution content the Director's Stage 0 scope asks for
   already exists correctly in Constitution v1 and `docs/policies/`.
   The genuinely new material needed is: (a) a Telegram/UI
   Constitution section (Reply Keyboard Primary Navigation, Coming
   Soon Policy, Menu Stability Principle — largely transcribable from
   Phase 6 Freeze's Stage 5 draft), (b) an extended Future Platform
   Constitution section (the 16-module table plus the Director's
   additional modules from Section 7.2), (c) explicit Director
   resolution of the three layering findings (Sections 3.2, 3.3, 5.2)
   folded into either amended Articles or a new Amendment record.

2. **Refresh, don't rewrite, the four stale documents.** VERSIONS.md,
   TELEGRAM_ARCHITECTURE.md, OWNER_PANEL.md, and ai/README.md each
   need an update pass to catch up to Phase 3 through Phase 6 Freeze
   (and Phase 62–66.8 for ai/README.md) — this is bounded,
   well-scoped work, not a redesign.

3. **Restore the `docs/README.md` completeness gate** as part of
   Constitution v2.0's Documentation Constitution section — the rule
   already exists in the document's own text; what's missing is
   either enforcement (a checklist item in the Commit Protocol) or a
   lighter mechanism (e.g., a CI check that flags new files under
   `docs/` not referenced in `docs/README.md`).

4. **Correct `MODULE_DEPENDENCIES.md`'s factual error** (Section 1.3,
   `trade_monitoring_layer/paper_trading/paper_trade_monitor.py`'s listed dependencies) as a
   trivial fix whenever that document is next touched.

5. **Add a Pattern 3 to `EXTENSION_GUIDE.md`** ("new Reply Keyboard
   section") the next time any UI Constitution work is authorized —
   four real precedents (Phase 6.0–6.3) already exist to derive it
   from.

6. **Do not treat the layering findings (Sections 3.2, 3.3, 5.2) as
   bugs to silently fix.** Each is longstanding (one traces to a named
   hardening patch), each has a plausible legitimate rationale, and
   each requires a Director-level architectural decision (amend the
   rule vs. change the code) rather than a Worker judgment call.

7. **Naming hygiene** (Section 8.3): rename or reclassify
   `FOUNDATION_FREEZE_v0.4.md` to match the `PHASE*_FREEZE.md`
   convention, and resolve the duplicate `DOCUMENTATION_STANDARD.md`
   filename (retire or clearly re-label the top-level Phase A14
   version) — both zero-risk, purely-documentation cleanups suitable
   for a future Cleanup-permitted phase.

---

*This document was produced entirely from direct reading of the
repository's own documentation and source code (no fabricated
capability claims), per `docs/policies/DOCUMENTATION_POLICY.md`. No
repository file other than this one was created or modified in the
production of this audit.*
