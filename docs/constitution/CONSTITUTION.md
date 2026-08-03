# GoldBot Constitution

**Status: In force from Phase 62.0 onward.** This is the single
highest-authority governance document in this repository. Every
Worker Brief, every Director instruction, and every code change from
this point forward is subordinate to it.

**Mandatory reading order**: any agent (human or AI) about to make a
change to this repository reads this document *before* reading the
task brief that brought them here. If a task brief conflicts with an
Article below, the agent stops and returns the conflict to the
Director for review — it does not resolve the conflict itself, and it
does not proceed with the conflicting instruction.

This document does not replace `CLAUDE.md`'s own Engineering
Governance (architecture layering, the Commit Protocol, Trading
Safety rules) — it sits above it as the *why*; `CLAUDE.md` remains the
*how*. Where the two overlap, they agree; where `CLAUDE.md` is silent,
this document governs.

---

## Article 1 — Core Principle

**Trading Engine ≠ AI Engine.**

GoldBot has exactly one system that decides whether a trade signal is
approved, rejected, or held: the pipeline running
`core/pipeline.py → decision/decision_engine.py → risk/risk_manager.py`.
This system is deterministic, rule-based, and fully auditable. It does
not consult the AI layer to make its decision.

The AI layer (`ai/`) exists to **help humans understand** what the
Trading Engine is doing — explain, summarize, analyze, educate. Per
`CLAUDE.md`'s own pipeline order (`signals/ -> ai/ -> decision/`),
`core/pipeline.py` calls `AIAnalyzer.analyze()` and passes its
`AIAnalysisResult` into `decision.decision_engine.DecisionEngine` as
one advisory input alongside the deterministic signal/risk factors —
this is real and intended, not a violation. What never happens, under
any configuration: the AI layer itself calling
`decision.decision_engine.DecisionEngine`, calling
`risk.risk_manager.RiskManager`, triggering execution, or triggering a
Telegram send (`ai/interfaces.py`'s `AIAnalyzerInterface` docstring
states this contract for any future provider). The Decision Engine
reads the AI's answer; the AI layer never acts on it.

> AI yordam beradi. AI qaror bermaydi.
> (AI assists. AI does not decide.)

This is not a temporary limitation to be lifted once the AI is "good
enough." It is a permanent architectural boundary. A future phase may
give the AI more to explain, more context to reason over, or a richer
voice — it will never give the AI a vote.

## Article 2 — Dependency Law

**Dependency flows in one direction only: forward through the
pipeline, never backward.**

`CLAUDE.md`'s own architecture section already states the full order:

```
data → context → strategies → signals → ai → decision → risk →
telegram → database
```

A later stage may receive/reference a **type or data value** produced
by an earlier stage (the concrete case: `decision/` importing
`AIAnalysisResult` from `ai.ai_analyzer` to accept it as a parameter —
see Article 1). An earlier stage must never import from, call, or
depend on a later stage. `core/` sits beneath this entire chain — every
stage may depend on it, and it depends on nothing else.

The Telegram/Service/Database slice of this same chain follows the
identical rule:

```
telegram → services → database
```

Correct:

```
data → context → strategies → signals → ai → decision → risk → telegram → database
telegram → services → database
```

Incorrect, and forbidden under any circumstance:

```
core → any other layer
ai → decision, ai → risk, ai → execution, ai → telegram, ai → database
decision → telegram, risk → telegram, strategies → telegram
database → telegram (in the reverse direction — a repository exposing
    itself to a specific handler's concerns, rather than the handler
    calling through a service, is still a violation even without a
    literal Python import)
```

This Article generalizes the rule `CLAUDE.md` already states: at
every layer boundary in this codebase, forward-only, no exceptions,
no "just this once." "Forward" always means further along the chain
above — never toward Telegram, never toward the database, never
toward the trading decision or execution from a layer that precedes
it.

## Article 3 — Import Rules

**AI never imports the Trading Decision layers.**

`ai/` (every file under it, no exceptions) must never `import` from:

```
decision/
risk/
execution/
```

This is verified mechanically, not just by convention: a grep sweep
for `from decision`, `from risk`, `from execution` (and their
`import` forms) under `ai/` must return zero results at the end of
every phase. This has been true since Phase 61.0's own isolation
audit and is re-verified at the close of every AI-touching phase
since (61.1 through 61.7). It stays true forever.

`ai/` importing `signals/` or `context/` for **type definitions only**
(e.g. `SignalCandidate`, `SignalSchema`, `MarketContext`) is the one
standing exception, and it is narrow: a handful of specific,
already-audited files (`ai/ai_analyzer.py`, `ai/ai_prompt.py`,
`ai/confidence_model.py`, `ai/journal/trade_journal.py`,
`ai/explanation/explanation_engine.py`, `ai/context/context_snapshot.py`,
`ai/context/context_builder.py`) import a *data shape* from
`signals/`, never a decision, never a risk calculation, never an
execution call. A new such import is not automatically exempt —
adding one requires the same audit discipline as any other new
cross-layer import (see Article 7).

`decision/` importing `ai/` is the one sanctioned exception in this
direction, and it is exactly as narrow as it sounds: `decision/models.py`
and `decision/decision_engine.py` import `AIAnalysisResult` from
`ai.ai_analyzer` — a **type only**, to accept the AI's analysis as a
parameter — per Article 1 and `CLAUDE.md`'s own `signals/ -> ai/ ->
decision/` ordering. `decision/` never imports `ai/router/`,
`ai/providers/`, `ai/runtime/`, or calls into `AIService.ask()`
itself; the actual invocation of `AIAnalyzer.analyze()` belongs to
`core/pipeline.py`'s own orchestration, which then hands the result to
`decision/`. `risk/` and `execution/` import nothing from `ai/` at
all today, and have no sanctioned reason to.

## Article 4 — Database Rule

**No module touches the database directly except a Repository.**

```
Handler → Service → Repository → Database
```

`telegram/handlers.py` never imports `database.*` or `core.pipeline`
directly — this is already stated and enforced in `telegram/handlers.py`'s
own module docstring, and it generalizes here: **any** module that
needs persisted data goes through a `database/*_repository.py` module,
never raw SQL, never a direct `sqlite3`/ORM call from a service,
handler, or AI module.

Services (`telegram/*_service.py`) own business logic. Repositories
(`database/*_repository.py`) own SQL only. A business rule inside a
repository file is a Constitution violation — with the handful of
pre-existing, already-documented exceptions listed in
`docs/SECURITY.md`/`docs/AUDIT_REPORT.md`. No new exceptions are
added without Director approval.

## Article 5 — Provider Rule

**An AI provider is reached through exactly one contract.**

```
BaseAIProvider
      |
ProviderResult
```

Every real AI vendor integration (`ai/providers/gemini_provider.py`,
`openai_provider.py`, `claude_provider.py`, `grok_provider.py`)
implements `ai/providers/base_provider.py`'s `BaseAIProvider` and
returns a `ProviderResult`. No code outside `ai/providers/` and
`ai/runtime/ai_service.py` ever references "Gemini," "OpenAI,"
"Claude," or "Grok" by name, calls a vendor SDK directly, or branches
on which vendor is active. A vendor's own name never appears above
`ai/providers/` — not in `telegram/`, not in `ai/router/`, not in any
capability, tool, or command.

Swapping, adding, retiring, or re-ordering a vendor is a change
confined entirely to `ai/providers/` (the provider file itself,
`provider_registry.py`, `provider_capabilities.py`) plus `ai/router/
routing_rules.py`'s declared candidate order. Nothing above the
provider boundary is ever touched to change which vendor answers a
given capability.

## Article 6 — Testing Rule

**Every new module ships with tests. No exceptions.**

A new module is not complete without:

- **Unit tests** — the module's own logic, in isolation, with every
  dependency injectable and fake-able (the "every constructor argument
  optional, defaults to a fresh real instance" convention this
  codebase already uses everywhere).
- **Isolation tests** — proof the module respects Article 2/3's
  dependency and import boundaries where relevant (an AST/grep sweep
  for a new `ai/` module; a layering check for anything else).
- **Regression tests** — proof the module's introduction did not
  change the behavior of anything that already existed. The mandatory
  Commit Protocol's own `pytest tests/` full-suite run *is* this
  check — a full suite that stays green after a change is the
  regression guarantee.

A module without tests does not merge, regardless of how urgent the
task that produced it felt.

## Article 7 — Reuse Principle

**Before writing a new module, ask: does this already exist?**

This is `CLAUDE.md`'s own Module Reuse Principle, restated here as a
constitutional Article because it is load-bearing enough to deserve
that status. Before creating any new file, package, or top-level
class/function, answer in order, stopping at the first "yes":

1. **Does this already exist somewhere in the repo?** — search first,
   build second.
2. **Can an existing module be extended** (a new method, a new
   optional field, a new function in an existing file) **without
   breaking its current contract?** — Phase 61.6 and 61.7's own
   history is the model: `ai/audit/provider_stats.py` was extended
   three separate times (Phase 61.1 TASK 8, 61.3 TASK 9, 61.6 TASK 4)
   rather than replaced or duplicated once.
3. **Only if both are "no": create a new module**, and its own
   docstring states why steps 1 and 2 were both "no." This is not
   optional documentation — a new module without this justification
   is itself a Constitution violation.

Reuse is the default outcome, not the exception. A new top-level
package is the highest-cost option available and should be rare.

## Article 8 — Change Management Law

**Every change to this repository follows the same order: Constitution
→ Architecture → Roadmap → Policy → Audit → Code.**

A Worker Brief is read against this Constitution before it is acted
on (see the mandatory reading order stated at the top of this
document). If a brief conflicts with an Article, the Worker stops,
documents the conflict, and returns it to the Director — it does not
resolve the conflict itself and does not proceed with the conflicting
instruction (**STOP → AUDIT → Director Decision**, the protocol this
Article formalizes; in force in practice since Phase 62.0, made a
standing law here). A Director message that carries no `TASK 0…N`
breakdown, Strict Rules, and Acceptance Criteria is guidance or
roadmap vision, not an executable brief — the Worker acknowledges it
without changing code or creating files until an explicit brief
arrives (the pattern already followed for the Phase 62.1 proposal
itself before this Article existed).

Every executable brief's own `TASK 0` is an audit of current code
against the brief's assumptions — never a rebuild from a blank
assumption. `docs/PHASE62_2_RUNTIME_AUDIT.md` and
`docs/PHASE63_0_FOUNDATION_AUDIT.md` are the model: state what already
exists, what is a genuine gap, and implement only the gap.

## Article 9 — Version Compatibility Law

**A LOCKed Foundation's name, location, import path, and public API
do not change.**

A module is LOCKed when its own Freeze document (a `docs/PHASE*_FREEZE.md`
or equivalent) declares the phase that built it closed — for example
Phase 62.x (Constitution & Runtime Foundation) and Phase 63.0 (Senior
Trading AI Foundation), both LOCKed at the Director's explicit
confirmation. Once LOCKed:

- the module's file path and package name do not move or get renamed;
- an existing public class, function, or method signature does not
  change shape or get removed;
- an existing import path (`from ai.persona.persona import Persona`,
  `from broadcast.models import BroadcastRequest`, etc.) keeps
  resolving exactly as it does today.

What remains allowed on a LOCKed module: adding a new method, adding
a new optional field, adding a new `Capability`/enum member, and
extending its documentation. This is the same shape of change Phase
61.1/61.3/61.6 already made three separate times to
`ai/audit/provider_stats.py` (Article 7's own worked example) —
additive, never a rename or a moved file. A change that would break
this Article on a LOCKed module requires the same STOP → AUDIT →
Director Decision protocol as a Constitution conflict (Article 8), not
a routine Worker judgment call.

## Article 10 — Owner Override Law

**A critical module answers to the Owner through the Telegram Owner
Panel, not through a hidden default.**

Every module this Constitution treats as safety- or control-critical —
emergency state (`core_layer/emergency/`), runtime lifecycle
(`ai/runtime/runtime_manager.py`), feature toggles
(`configuration/runtime_feature_manager.py`), broadcast/media/
translation intent (`broadcast/`, `media/`, `translation/`) — exposes
its control surface through `telegram/owner/*_commands.py`, gated by
`telegram/owner/security.py`'s `require_role()`/`log_owner_action()`
(Article 4's Handler → Service → Repository chain applies here too: an
Owner command never reaches into a repository directly).

An Owner command may legitimately be foundation-only — returning a
clear "not implemented" rather than a fabricated result — while its
backend wiring awaits separate Director approval (the standing pattern
`telegram/owner/broadcast_commands.py` established in Phase 63.0). What
is never acceptable is a critical module with **no** Owner-facing
surface at all, or one whose real state can diverge from what the
Owner Panel reports.

## Article 11 — Foundation Reuse Law

**Before writing a new module, a Foundation Reuse Audit is mandatory,
not advisory.**

This is Article 7's Reuse Principle made into a checkable procedure.
Every Worker Brief's `TASK 0` answers, for the capability the brief is
about to build:

1. Does a **Foundation** for this already exist (a package like
   `ai/persona/`, `broadcast/`, `ai/content/`)?
2. Does a **Manager** for this already exist (`PersonaManager`,
   `BroadcastManager`, `RuntimeManager`, …)?
3. Does a **Contract** for this already exist (a dataclass like
   `ExplanationOutput`, `ContentRequest`, `BroadcastRequest`)?
4. Does a **Model** for this already exist?
5. Does a **Capability** for this already exist
   (`ai/capabilities/capability.py`'s `Capability` enum)?
6. Does a **Registry** for this already exist (`provider_registry.py`,
   `persona_registry.py`, `media_registry.py`, …)?

If any answer is yes, a new module is forbidden for that concern — the
existing one is extended (Article 9 governs how, if it is LOCKed).
Only when every answer is no may a new module be created, and its own
docstring or its phase's audit document states why steps 1–6 were all
"no" (Article 7's existing requirement, now scoped to this explicit
six-item checklist).

## Article 12 — Architecture Evolution Law

**Every phase reports its own New / Extended / Reused shape.**

A phase's Freeze document includes this table, filled in with the real
count for that phase (module = a new `.py` file; manager = a class
whose name ends `Manager`/`Engine`/`Service` at the phase's top level;
model = a dataclass/enum; contract = a request/result/output
dataclass meant to cross a boundary; registry = a `build_*_registry()`
static catalog):

| Item | New | Extended | Reused |
|------|-----|----------|--------|
| Modules | | | |
| Managers | | | |
| Models | | | |
| Contracts | | | |
| Registries | | | |

This is not decorative — it is the Constitution's own KPI for Article
11 taking effect. Its intended trend, stated for the record: as
GoldBot's Foundation matures, each new phase's **New** column should
shrink and its **Reused** column should grow. A phase whose table shows
the opposite trend is the mechanical trigger for a STOP → AUDIT →
Director Decision review of whether Article 11 was actually followed.

---

## Article 13 — Future First Principle

**Every Architecture accounts for every target platform, even before
that platform has a single line of code.**

Ratified following ADR-001 (`communication/decisions/ADR-001.md`):
GoldBot Platform is not built around Telegram Bot with other clients
bolted on later — Telegram Bot is one client among five, sitting below
a Shared Platform Layer alongside Telegram Mini App, Android, iOS, and
Desktop. An Architecture document that designs only for whichever
platform happens to be `LIVE` today (per `platforms/platform_registry.py`)
repeats the exact mistake this Article exists to prevent: a Navigation
(or any other Platform component) built Telegram-first would require
rewriting for every platform that comes after it.

**In force**: from Navigation (TASK-002B) onward, every Platform
Architecture document states, for every component it defines, its
compatibility with all five platforms — Telegram Bot, Telegram Mini
App, Android, iOS, Desktop — using `platforms/capability_model.py`'s
existing `SupportStatus` contract (`SUPPORTED`/`NOT_SUPPORTED`/`PLANNED`,
the latter two always carrying a `reason`). A platform having zero
code today is not a reason to omit it from the compatibility statement
— it is a reason the `reason` field says so honestly (see
`platforms/cross_platform_checker.py`'s existing validation rule,
already built for exactly this purpose in TASK-001).

**Does not require writing platform code today.** This Article governs
Architecture (design), not Implementation — it does not authorize or
require building an Android/iOS/Desktop client now, and it does not
relax Article 11's Reuse Audit or Article 8's Change Management order.
It only requires that the design account for all five from the start,
so a later platform's real requirements surface as "already considered,
now implemented" rather than "not designed for, now a rewrite."

---

## Amendment process

This Constitution changes only by explicit Director instruction,
delivered the same way any Worker Brief is delivered, and only as its
own dedicated phase (never as a side effect of an unrelated task). A
Worker never amends this document on its own initiative, no matter
how well-reasoned the change seems in the moment. `docs/constitution/AMENDMENTS.md`
is the running log of every amendment made under this process,
including Phase 62.1a (Articles 8 through 12) and TASK-002B's own
amendment (Article 13).

## Related documents

- `docs/constitution/ARTICLES.md` — a one-page index of all thirteen
  Articles above, for quick lookup without reading the full text.
- `docs/constitution/AMENDMENTS.md` — the amendment history: which
  phase added which Article, and why.
- `docs/policies/DIRECTOR_POLICY.md` — the Director/Worker operating
  model this Constitution's Article 8 formalizes.
- `docs/policies/FOUNDATION_POLICY.md` — Article 9 and Article 11's
  day-to-day operating detail (what "LOCKed" and "Reuse Audit" look
  like in a real Worker Brief).
- `docs/architecture/ARCHITECTURE_MASTER.md` — the full system layer
  diagram and per-layer responsibility (what each layer CAN and
  CANNOT do), the practical expression of Article 1 and Article 2.
- `docs/architecture/MODULE_DEPENDENCIES.md` — the real, current
  per-module dependency map, the living proof Article 2/3 hold today.
- `docs/architecture/IMPORT_RULES.md` — the allowed/forbidden import
  table, Article 3 made checkable line-by-line.
- `docs/architecture/EXTENSION_GUIDE.md` — how to add new work without
  violating any Article above.
- `CLAUDE.md` — the Engineering Governance document (Commit Protocol,
  layer list, Trading Safety hard rules) this Constitution sits above.
