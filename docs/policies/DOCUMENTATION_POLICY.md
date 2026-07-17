# Documentation Policy

**Documentation-driven, not documentation-after.** A module's
contract is written down before or alongside the code that implements
it — the Constitution → Architecture → Roadmap → Policy → Audit → Code
order (`docs/policies/DEVELOPMENT_POLICY.md`) already puts
documentation ahead of code by construction.

## What every new module needs

- A `README.md` if it is a new top-level package (the convention
  `ai/persona/README.md`, `broadcast/README.md`, `media/README.md`,
  `translation/README.md` already follow).
- A docstring-level statement of *why*, when it is a new module rather
  than an extension (Article 7's "why steps 1 and 2 were both no").
- An entry in the relevant layer doc
  (`docs/architecture/ARCHITECTURE_MASTER.md`'s System Overview table,
  or the specific `docs/ai/`, `docs/telegram/` file) if it changes
  what that layer CAN or CANNOT do.

## Cross-referencing convention

Every doc in this project ends with a **Related** section linking to
the documents that govern it above and the documents that build on it
below. This is not decorative — it is how a reader (or a future
Worker) finds the full context for a single file without needing a
search. New docs preserve this convention.

## What every phase needs

A Freeze document (`docs/policies/RELEASE_POLICY.md`'s Freeze
Protocol) and, when the phase touches AI, an audit document
(`docs/PHASE*_AUDIT.md`) stating what TASK 0 found already real versus
genuinely missing.

## No fabricated documentation

A doc never claims a capability is live when it is foundation-only.
Phase 63.0's own docs are the model: `docs/AI_BROADCAST_FOUNDATION.md`'s
"What none of this does yet" section is as load-bearing as its "What
exists" section.

## Related

- `docs/constitution/CONSTITUTION.md` Article 6 (tests) and Article 12
  (the Freeze table this policy's "every phase needs" section
  references).
- `docs/policies/DEVELOPMENT_POLICY.md`.
