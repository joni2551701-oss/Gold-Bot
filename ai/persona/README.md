# ai/persona/

Phase 63.0 (Senior Trading AI Foundation), TASK 1. Foundation only.

## What this package is

Pure identity data for GoldBot's AI voice — `Persona` (name, role,
tone, language_style, disclaimer, system_identity), a static catalog
of known personas (`persona_registry.py`), and a read-only lookup
(`persona_manager.py`).

## What this package is not

- It does not build a prompt.
- It does not call `AIService` or any provider.
- It is not read by `ai/prompts/`, `ai/runtime/`, or any content
  generator yet.

A future, separately-approved phase decides how (or whether) a
`Persona`'s fields feed into a real prompt template.

## Files

- `persona.py` — the `Persona` dataclass.
- `persona_registry.py` — `build_persona_registry()`, the static
  catalog (one entry this phase: Senior Trading AI).
- `persona_manager.py` — `PersonaManager`, injectable read-only lookup
  over the registry.

## Related

- `docs/AI_PERSONA.md` — the phase-level documentation.
- `docs/PHASE63_0_FOUNDATION_AUDIT.md` — why this package is new
  (Module Reuse Principle: no existing persona/identity module
  existed to extend).
