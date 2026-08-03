# translation/

Phase 63.0 (Senior Trading AI Foundation), TASK 6. Foundation only.

## What this package is

- `models.py` — `Language` (UZ/RU/EN), `TranslationRequest`,
  `TranslationResult`.
- `language_registry.py` — static catalog of the three supported
  languages.
- `translation_manager.py` — `TranslationManager.translate()`, always
  returns a cleanly rejected `TranslationResult` this phase.

## What this package is not

No Google Translate, no DeepL, no Gemini/OpenAI translation call
anywhere in this package (Rule 4). `translate()` never echoes or
fabricates a translated string — a rejected result honestly says so.

## Related

- `ai/persona/persona.py`'s `language_style` field and
  `ai/explanation/explanation_output.py`'s `language` field both carry
  a plain language-code string today, not yet validated against this
  package's registry — a future phase may wire that check in.
