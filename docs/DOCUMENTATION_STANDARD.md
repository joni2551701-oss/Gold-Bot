# GoldBot Documentation Standard (Phase A14)

Part of GoldBot's Documentation Architecture Foundation (Phase A14).
This document states the standard every future module's documentation
follows, so a reader can find the same information in the same shape
regardless of which module they're reading about.

## Every module needs a README

Every top-level package (`context/`, `strategies/`, `signals/`,
`features/`, `assets/`, `configuration/`, etc.) has its own
`README.md`, in the module's own directory:

```
module/
    README.md
```

This has been this codebase's own practice since Phase A2 (extended
to every module touched or added by a later phase — `context/README.md`,
`signals/README.md`, `strategies/README.md`, `features/README.md`,
`assets/README.md`, `configuration/README.md`); this document makes
it an explicit, checked standard rather than an informal habit.

## Required format

```markdown
# Module Name

## Purpose
## Responsibility
## Input
## Output
## Dependencies
## Forbidden dependencies
## Future roadmap
## Tests
```

- **Purpose** — why this module exists, in 2-4 sentences. What
  question does it answer that nothing else in the codebase already
  answers?
- **Responsibility** — what this module actually does, file by file
  if there's more than one.
- **Input** — what this module's public functions/classes take
  (types, not values) — e.g. `ContextSnapshot`, a `SignalCandidate`.
- **Output** — what this module's public functions/classes return.
- **Dependencies** — which other modules this one is allowed to
  import, per `docs/ARCHITECTURE_RULES.md`. Be exact: name the actual
  modules imported, not just "context and signals."
- **Forbidden dependencies** — which modules this one must never
  import, and why (usually a direct pointer to
  `docs/ARCHITECTURE_RULES.md`'s Module Responsibility Rules for that
  module). Stating the forbidden list explicitly, not just the
  allowed one, is what makes a later accidental import easy to catch
  in review.
- **Future roadmap** — named, explicit future extensions this module
  anticipates but does not implement — never a vague "more features
  later." Every Phase A module's docs (e.g.
  `docs/FEATURE_ENGINEERING.md`'s "Future ML usage",
  `docs/ASSET_INTELLIGENCE.md`'s "Future") follows this pattern:
  name the specific thing, name why it isn't here yet.
- **Tests** — where the module's tests live
  (`tests/<module>/test_*.py`) and what they cover, at a glance.

## Applying this to existing module READMEs

Existing module `README.md` files (written before this document
existed) use a close variant of this shape — typically
Purpose/Flow/Responsibilities/Input/Output/Dependencies/Future
Roadmap, with a `## Flow` diagram in place of (or in addition to) the
`## Forbidden dependencies` section. This document does not require
rewriting them: Phase A14 changes documentation-standard *statement*
only, not existing documentation content — see this phase's own
Acceptance Criteria ("no Python file changes, documentation layer
only"). A future module's README should include the
`## Forbidden dependencies` section explicitly; an older module's
README gaining one is a welcome, but not mandatory, cleanup for
whichever future phase next touches that module.

## Two-tier documentation

GoldBot's documentation has two tiers, and a new module's docs belong
in both:

1. **Module `README.md`** (this document's format) — lives with the
   code, answers "what does this module do."
2. **`docs/<TOPIC>.md`** — a deeper, phase-specific document for any
   module whose design required real decisions worth recording (e.g.
   `docs/FEATURE_ENGINEERING.md`, `docs/STRATEGY_LIFECYCLE.md`,
   `docs/ASSET_INTELLIGENCE.md`, `docs/CONFIGURATION_MANAGEMENT.md`) —
   answers "why does this module work this way," including
   pre-implementation audit findings, deliberate deviations from a
   brief's illustrative example, and what was reused vs. newly built.
   Not every module needs one — a module whose README fully answers
   "what" and "why" in a few paragraphs doesn't need a second document
   just to have one.

Both tiers link to `docs/ARCHITECTURE.md` (the technical reference)
and, where relevant, `docs/ARCHITECTURE_RULES.md`/
`docs/DECISION_PRINCIPLES.md` (the rule statements) — never duplicate
their content wholesale.

## Verification checklist

Before a documentation change is considered complete:

- ✅ Every file the task named actually exists at the stated path.
- ✅ Markdown renders correctly — headings nest properly, code fences
  are closed, tables have matching column counts.
- ✅ Every diagram referenced in prose is actually present.
- ✅ Every rule stated is unambiguous — a reader should not need to
  guess which module owns a decision after reading it.
