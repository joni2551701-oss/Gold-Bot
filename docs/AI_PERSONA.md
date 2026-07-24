# GoldBot — AI Persona

Phase 63.0 (Senior Trading AI Foundation), TASK 1. Foundation only.

## What exists

`ai/persona/` — pure identity data, no behavior:

- `persona.py` — the `Persona` dataclass: `name`, `role`, `tone`,
  `language_style`, `disclaimer`, `system_identity`.
- `persona_registry.py` — `build_persona_registry()`, a static catalog
  (one entry this phase: `SENIOR_TRADING_AI`).
- `persona_manager.py` — `PersonaManager`, a read-only lookup over the
  registry (`get()`, `get_active_persona()`, `all()`).

## The one registered persona

```
name:            Senior Trading AI
role:            Explains GoldBot's already-decided trading signals
                 and market context to a human reader.
tone:            calm, professional, data-driven
language_style:  concise, no hype, no guaranteed-profit language
disclaimer:      Educational content only, not financial advice.
                 Past performance does not guarantee future results.
system_identity: goldbot-senior-trading-ai-v1
```

## What this is not (Rule 5)

- `Persona` never builds a prompt.
- `PersonaManager` never calls `AIService` or any provider.
- Nothing in `ai/prompts/`, `ai/runtime/`, `ai/content/`, or
  `ai/explanation/` reads this package yet.

A future, separately-approved phase decides how (or whether) a
`Persona`'s fields feed into a real prompt template — this phase only
establishes the identity contract.

## Related

- `docs/PHASE63_0_FOUNDATION_AUDIT.md` — why this is a new package
  (no existing identity/persona module to extend).
- `docs/PHASE63_0_FREEZE.md` — what this phase built and did not build.
