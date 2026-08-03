# GoldBot AI Architecture (Phase 55)

Audit of `ai/` as it stood before this phase, what this phase added,
and the resulting structure. This phase is **foundation only** — no
real AI trading decision exists anywhere in this codebase, before or
after this phase.

## Part 1 — Pre-Phase-55 Module Audit

| File | Currently used in production? | Purpose |
|---|---|---|
| `ai/ai_analyzer.py` | **Yes** — imported by `core/pipeline.py`, `decision_layer/decision_engine/decision_engine.py`, `decision_layer/decision_engine/models.py`, `platform_layer/telegram/signal_formatter.py`, and `tests/conftest.py` (5 importers). | `AIAnalyzer.analyze()` is the production entry point `TradingPipeline` calls. Currently a permanent-reject stub — always returns `approved=False, confidence=0.0, risk_score=1.0` with an explanatory string. Documented as intentional in the README and the Phase 48 audit ("Heuristic scoring logic will be implemented in Phase 6.0.1") — this is the single highest-impact pre-existing finding this repository's audit history has surfaced, and it is unchanged by this phase (explicitly forbidden: "signal approve/reject AI orqali" / "existing pipeline flow o'zgarishi"). |
| `ai/confidence_model.py` | No external importer besides `ai/ai_prompt.py` (within `ai/` itself). | `evaluate_confidence()` — a deterministic technical scoring function reading `SignalCandidate.context_refs` (a field no strategy currently populates — the Phase 48 audit noted this makes the function a documented no-op today, always returning a 0 score, by design until a future phase wires `context_refs`). |
| `ai/ai_prompt.py` | No external importer at all. | `build_prompt()` — a Gemini-specific prompt + JSON-schema builder, tightly coupled to `SignalCandidate`/`ContextSnapshot`/`ConfidenceResult`. Fully built, never called by `AIAnalyzer` or anything else. |
| `ai/trade_journal.py` | No importer anywhere (confirmed by a repo-wide grep, including tests). | `TradeJournalEntry`/`create_journal_entry()` — a complete, type-safe trade-outcome record model. Never written to by anything (no `PerformanceTracker`, no repository). |

**Duplicate responsibility check**: none found. Each file has exactly
one job and none overlaps another's — `ai_analyzer.py` is the
pipeline-facing entry point, `confidence_model.py` is a scoring
helper `ai_prompt.py` alone consumes, `ai_prompt.py` is a
Gemini-specific request builder, `trade_journal.py` is an unrelated
persistence-record shape for a future outcome-tracking feature. The
one real issue found is not duplication but **disconnection**:
`confidence_model.py` and `ai_prompt.py` are fully built but neither
is called by `ai_analyzer.py` — the stub bypasses both entirely rather
than using them and returning a low/zero score. That's a Phase
6.0.1-scope wiring decision, not something this foundation phase
changes.

**Dependencies**: `ai/` depends on `context/` (for `ContextSnapshot`)
and `signals/` (for `SignalCandidate`) — never on `database/` or
`telegram/` (confirmed by grep, zero matches). `decision_layer/decision_engine/models.py`
depends on `ai/ai_analyzer.py` for `AIAnalysisResult` — the one
place outside `ai/` that reaches into it for a type, not a call.

## Part 2 — New Folder Structure

```
ai/
├── __init__.py
├── ai_analyzer.py          <- UNCHANGED, still the canonical
│                              implementation (see "Migration
│                              Decision" below)
├── confidence_model.py     <- UNCHANGED
├── ai_prompt.py            <- UNCHANGED
├── trade_journal.py        <- NOW a compatibility shim (see below)
├── interfaces.py           <- NEW (Part 3)
│
├── analyzer/
│   ├── __init__.py
│   └── ai_analyzer.py      <- NEW: re-exports ai/ai_analyzer.py
│
├── memory/
│   ├── __init__.py
│   └── context_memory.py   <- NEW (Part 4)
│
├── prompts/
│   ├── __init__.py
│   └── prompt_manager.py   <- NEW (Part 5)
│
├── profiles/
│   ├── __init__.py
│   └── user_profile.py     <- NEW (Part 6)
│
└── journal/
    ├── __init__.py
    └── trade_journal.py    <- MOVED here (real implementation)
```

### Migration Decision (why some files moved and some didn't)

This phase's spec is explicit: *"Katta migration qilinmasin ...
Agar move qilish riskli bo'lsa: faqat structure tayyorlansin."* Each
existing file was evaluated individually against that rule, using the
same import-site grep as Part 1's audit table above:

- **`ai/trade_journal.py` → moved** to `ai/journal/trade_journal.py`.
  Zero importers anywhere (confirmed above) — moving it carries
  exactly zero production risk. The old path
  (`ai/trade_journal.py`) is kept as a thin compatibility shim
  (`from ai.journal.trade_journal import ...`) purely as a defensive,
  zero-cost safety net, not because anything currently needs it.
- **`ai/ai_analyzer.py` → NOT moved.** Five separate production
  modules import this exact path
  (`core/pipeline.py`, `decision_layer/decision_engine/decision_engine.py`,
  `decision_layer/decision_engine/models.py`, `platform_layer/telegram/signal_formatter.py`, plus
  `tests/conftest.py`). Relocating it would be precisely the "risky
  move" this phase's spec says to avoid. Instead, the compatibility
  layer runs in the *other* direction: `ai/analyzer/ai_analyzer.py`
  (the new, professional-layout path) re-exports the untouched
  original at `ai/ai_analyzer.py`. This achieves the same practical
  outcome — the new structure has a real, working module at
  `ai.analyzer.ai_analyzer` — with strictly lower risk, since not one
  existing import site changes.
- **`ai/confidence_model.py` and `ai/ai_prompt.py` → NOT moved.**
  Neither is named in this phase's target folder structure (only
  `ai_analyzer.py`, `context_memory.py`, `prompt_manager.py`,
  `user_profile.py`, and `trade_journal.py` are), so there is no
  requested destination to move them to. They stay exactly where they
  are; `docs/AI_ARCHITECTURE.md` (this file) is their audit record.

## Part 3 — Interface Foundation

`ai/interfaces.py`: `AIAnalyzerInterface` (abstract base class),
`MarketContext`, `UserContext`, `AIResponse` (frozen dataclasses). No
real AI/LLM call anywhere in this file. The existing production
`AIAnalyzer` (`ai/ai_analyzer.py`) does **not** implement this
interface yet — retrofitting it is out of scope this phase
("existing pipeline flow o'zgarishi" is forbidden). This interface is
the agreed shape a *future* v0.4+ AI Assistant Core implements against
from day one, not a retrofit of what exists today.

The interface's docstring restates the hard boundary that already
governs the production `AIAnalyzer` (unchanged, just now written down
in one place a future provider implementation will actually read): an
AI provider is advisory input to `DecisionEngine` only — it must never
itself approve/reject a trade, call `RiskManager`, or trigger
execution/Telegram delivery.

## Part 4 — Memory Foundation

`ai/memory/context_memory.py`: `ContextMemory` with `save()`/`load()`/
`clear()`, backed by a plain in-process `dict`. No database
integration (explicitly forbidden this phase), not wired into
`ai_analyzer.py`, `core/pipeline.py`, or any Telegram handler — a
future `User -> Trading History -> AI Memory -> Personal Assistant`
feature has a shape to build against, nothing more.

## Part 5 — Prompt Management Foundation

`ai/prompts/prompt_manager.py`: `PromptManager` with
`get_market_analysis_prompt(market_context)` and
`get_user_assistant_prompt(user_context)`, both returning static
template strings built from `ai.interfaces.MarketContext`/
`UserContext`. No LLM call anywhere. Deliberately built against the
new interface types rather than duplicating `ai/ai_prompt.py`'s
internal-type-coupled, Gemini-specific, signal-validation-only prompt
— see Part 1's audit table for why `ai_prompt.py` was left alone
rather than merged into this new module.

## Part 6 — User AI Profile Foundation

`ai/profiles/user_profile.py`: `AIUserProfile` (frozen dataclass) —
`telegram_id`, `experience_level`, `preferred_strategy`, `risk_style`,
`language`. No database access anywhere in this file (explicitly
forbidden this phase). Distinct from `database_layer.user_repository.user_models.UserRecord`
(the real, database-backed settings record) — `AIUserProfile` is a
lightweight, AI-facing *projection*, plus a field
(`experience_level`) that doesn't exist in the `users` table at all;
this phase does not connect the two.

## Summary

Zero real AI trading decisions exist anywhere in `ai/`, before or
after this phase. `core/pipeline.py`'s actual runtime call
(`self.ai_analyzer.analyze(candidate, context)` →
permanent-`approved=False` stub) is completely untouched. Everything
added this phase is either a new, unwired foundation file or a
compatibility shim pointing at code that already existed.
