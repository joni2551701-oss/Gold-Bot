# GoldBot Constitution — Article Index

A one-page lookup for all thirteen Articles. This is a navigation aid,
not a substitute — `docs/constitution/CONSTITUTION.md` is the single
source of truth; if this index and the Constitution ever disagree, the
Constitution wins and this file is corrected to match.

| # | Article | One line |
|---|---------|----------|
| 1 | Core Principle | Trading Engine ≠ AI Engine — AI assists, never decides. |
| 2 | Dependency Law | Dependency flows one direction only, forward through the pipeline. |
| 3 | Import Rules | `ai/` never imports `decision/`, `risk/`, or `execution/`. |
| 4 | Database Rule | Only a Repository touches the database — Handler → Service → Repository. |
| 5 | Provider Rule | An AI vendor is reached through `BaseAIProvider` only, never named above `ai/providers/`. |
| 6 | Testing Rule | Every new module ships with unit, isolation, and regression tests. |
| 7 | Reuse Principle | Before writing a new module: does this already exist? Search first, build second. |
| 8 | Change Management Law | Constitution → Architecture → Roadmap → Policy → Audit → Code, always in that order. |
| 9 | Version Compatibility Law | A LOCKed Foundation's name, path, import, and public API never change — only additive extension. |
| 10 | Owner Override Law | Every critical module answers to the Owner through the Telegram Owner Panel. |
| 11 | Foundation Reuse Law | Foundation/Manager/Contract/Model/Capability/Registry — the mandatory TASK 0 checklist. |
| 12 | Architecture Evolution Law | Every phase reports its own New/Extended/Reused table. |
| 13 | Future First Principle | Every Architecture accounts for all five target platforms, even the ones with no code yet. |

## By theme

**What the AI layer may and may not do** — Articles 1, 3, 5.

**How code depends on code** — Articles 2, 3, 4.

**How a phase is planned and executed** — Articles 6, 7, 8, 11.

**How the system stays stable as it grows** — Articles 9, 10, 12, 13.

## Related

- `docs/constitution/CONSTITUTION.md` — the full text.
- `docs/constitution/AMENDMENTS.md` — when each Article was added and
  why.
