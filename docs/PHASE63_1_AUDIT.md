# Phase 63.1 — AI Explanation Intelligence Foundation: TASK 0 Audit

**Status: STOP — awaiting Director Decision on one finding below before
TASK 1+ proceeds.** Per Constitution Article 8 (Change Management Law):
a brief conflicting with an already-verified Article is not resolved
by the Worker unilaterally.

## Foundation Reuse Audit

| Component | Exists? | Real file(s) |
|---|---|---|
| Explanation contract | ✅ Yes | `ai/explanation/explanation_output.py` (`ExplanationOutput`, Phase 63.0), `ai/explanation/explanation_engine.py` (`ExplanationEngine`, Phase 61.3) |
| Persona | ✅ Yes | `ai/persona/persona.py`, `persona_registry.py`, `persona_manager.py` — **one** registered persona today (`SENIOR_TRADING_AI`), not three |
| Content type | ✅ Yes | `ai/content/content_types.py`'s `ContentType`, `ai/content/content_schema.py` |
| Capability | ✅ Yes | `ai/capabilities/capability.py`'s `Capability.EXPLANATION` already exists and already has a real `AIService.ask()` mapping |
| Provider system | ✅ Yes | `ai/providers/` — 4 real vendors (Gemini/OpenAI/Claude/Grok) + `base_provider.py` |
| Runtime | ✅ Yes | `ai/runtime/ai_service.py`'s `AIService.ask()`, production-wired since Phase 62.2 |
| Memory | ✅ Yes | `ai/memory/context_memory.py`, `memory_runtime.py` (Phase 61.3) |
| Knowledge | ✅ Yes (top-level, not `ai/knowledge/`) | `knowledge/` — 6 categories, 26 entries (Phase 61.3) |

**Rule applied**: every component above already exists. Per this
brief's own TASK 0 rule ("mavjud bo'lsa — yangi modul yozilmaydi,
kengaytiriladi"), no new top-level package or duplicate contract is
created anywhere in this phase — every TASK below extends an existing
file or adds a new file inside an already-existing package.

## Documents referenced in TASK 0 that do not exist

`docs/AI_EXPLANATION_FOUNDATION.md` — not present in the repository.
No prior phase created it under that name; the real, closest
equivalent is `docs/ai/AI_PIPELINE.md` (Phase 62.1c) and
`ai/explanation/explanation_output.py`'s own module docstring (Phase
63.0). Not treated as a blocking gap — TASK 9 of this brief already
asks for `docs/ai/AI_ARCHITECTURE.md` and `docs/roadmap/AI_EVOLUTION.md`
updates, which cover this ground.

## Critical finding — STOP, requires Director Decision

**TASK 2's proposed input types cannot be implemented as literally
specified without violating Constitution Article 3.**

The brief's TASK 2 names the `AI Explanation Engine`'s input as:

```
TradeContext
DecisionResult
RiskResult
MarketContext
```

Verified against the real codebase:

- **`TradeContext` does not exist anywhere in this repository** — no
  class by this name in any package. It is not a real type to import.
- **`DecisionResult`** is real — `decision_layer/decision_engine/models.py`/`decision_layer/decision_engine/decision_engine.py`.
- **`RiskResult`** is real — `risk_layer/risk_engine/risk_manager.py`.
- **`MarketContext`** is real — `ai/interfaces.py` (already `ai/`-owned,
  no conflict).

`docs/architecture/IMPORT_RULES.md`'s Forbidden table states this with
"no exceptions" language, twice:

```
ai/* (any file, no exceptions) → decision/*   — forbidden
ai/* (any file, no exceptions) → risk/*       — forbidden
```

This is not the same category as the seven pre-existing `signals/`/
`context/` type-only import sites (Article 3's one standing exception)
— that exception is narrow, already-audited, and explicitly does
**not** extend to `decision/` or `risk/` under any circumstance. Unlike
the Phase 62.1b/62.1c findings (which were factual corrections to a
brief's sketch — e.g. the real pipeline stage order, the real provider
roster), this one is a **hard architectural boundary**, the exact one
`CLAUDE.md`'s Trading Safety section and Constitution Article 1 exist
to protect: "Never bypass Risk Manager," "AI never imports the Trading
Decision layers." A new `ai/explanation/explanation_builder.py` that
imports `decision_layer.decision_engine.models.DecisionResult`/`risk_layer.risk_engine.risk_manager.RiskResult`
directly would be a Constitution Article 3 violation on its first
line, mechanically caught by this project's own standing grep sweep
(`docs/architecture/IMPORT_RULES.md`'s "Mechanical verification"
section) at the close of this very phase.

### Proposed resolution (not yet applied — awaiting Director Decision)

Build `ExplanationBuilder` to accept **already-extracted values**, not
`decision/`/`risk/` objects:

```
ExplanationBuilder.build(
    signal_direction: str,           # "BUY" / "SELL" / "NO_TRADE"
    decision_action: str,            # "APPROVE" / "REJECT" / "NO_TRADE"
    final_confidence: float,         # DecisionResult.confidence, already 0.0-1.0
    ai_confidence: float,            # DecisionResult.ai_confidence
    lot_size: float,                 # RiskResult.lot_size
    risk_reward: float,              # RiskResult's own computed ratio
    entry: float, stop_loss: float, take_profit: float,
    market_context: MarketContext,   # ai/interfaces.py's own type — no conflict
    persona: Optional[Persona] = None,
    reasons: Optional[List[str]] = None,  # from SignalExplanation.reasons, already ai/-legal via signals/ type-only exception
) -> ExplanationOutput
```

The caller that assembles these primitive values from a real
`DecisionResult`/`RiskResult` is `core/pipeline.py` (the one place in
this codebase already permitted to see every layer's output — the
exact role it already plays for `AIAnalyzer.analyze()`), never
`ai/explanation/` itself. This mirrors the one sanctioned pattern
already on record: `decision_layer/decision_engine/models.py` accepting `AIAnalysisResult`
as a **value** while never importing `ai/router/`/`ai/providers/`/
`ai/runtime/` — the same value-not-object-import shape, just crossing
the boundary in the other direction.

This phase does **not** wire `core/pipeline.py` to actually call
`ExplanationBuilder` — that would be live integration, out of scope
for a Foundation phase per this brief's own "AI qaror qabul qilmaydi"
framing and the standing "foundation first, wiring is separately
approved" posture every phase since 63.0 has used. `ExplanationBuilder`
is built and tested with directly-constructed primitive arguments,
exactly like `ai/content/content_adapter.py`'s `ContentEngine` was
built and tested without `core/pipeline.py` ever calling it.

## Requesting Director Decision on

1. **Approve the primitive-values interface above** for
   `ExplanationBuilder`, replacing the brief's literal
   `TradeContext`/`DecisionResult`/`RiskResult` parameter list — the
   only way TASK 2 can proceed without a Constitution Article 3
   violation.
2. Confirm `TradeContext` was a planning shorthand, not a real type to
   create — no new type by that name is added anywhere (creating one
   would itself need its own Reuse Audit against `MarketContext`/
   `AIContext`, which already cover this ground).
3. Confirm TASK 4's Persona Integration proceeds using the one real
   persona (`SENIOR_TRADING_AI`) rather than the three named in the
   brief (Trader Analyst / Education / Professional Research), which
   do not exist in `persona_registry.py` today — adding two more is a
   permitted additive change to an existing registry (Article 9) but
   was not explicitly requested by TASK 4's own "yangi persona
   yaratish yo'q."

TASK 1, 3, 5, 6, 7, 8, 9, 10 have no equivalent conflict and are ready
to proceed once the above is resolved.

## Related

- `docs/constitution/CONSTITUTION.md` Article 3, Article 8.
- `docs/architecture/IMPORT_RULES.md` — the Forbidden table this
  finding is checked against.
- `docs/PHASE63_0_FOUNDATION_AUDIT.md` — the prior phase's own Reuse
  Audit, same discipline applied here.
