# GoldBot — AI Knowledge

Governed by `docs/constitution/CONSTITUTION.md` Article 7. `knowledge/`
(Phase 61.3 TASK 3) is a **top-level package**, a sibling of `ai/`, not
`ai/knowledge/` — confirmed by directory listing, the same correction
`docs/architecture/MODULE_DEPENDENCIES.md` and `docs/ai/AI_ARCHITECTURE.md`
already both state. It has zero dependencies — a pure static catalog.

## The six categories

```
knowledge/
  examples.py     worked examples
  faq.py          frequently-asked-question entries
  psychology.py   trading psychology reference
  risk.py         risk-management reference
  smc.py          Smart Money Concepts reference
  wyckoff.py      Wyckoff method reference
  registry.py     lookup / category-filter / search over all six
  models.py       the entry shape every category returns
```

26 entries across the six categories as of Phase 61.3. `registry.py`
is the only way any other module reads this package — `lookup()`,
filtering by category, and free-text `search()`.

## What it is not

Not AI-generated — every entry is static, authored content, the same
posture `ContentType.EDUCATION` (Phase 63.0) will eventually draw on
when a future phase wires content generation to a real source. This
package is that source's most likely first input, not itself a
generator.

## Related

- `docs/PHASE61_3_INTELLIGENCE_FREEZE.md` — TASK 3, where this was
  built.
- `docs/architecture/NAMING_CONVENTIONS.md` — why this is a new
  top-level package rather than `ai/knowledge/`.
