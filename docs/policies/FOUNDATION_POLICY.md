# Foundation Policy

The operating detail behind Constitution Article 9 (Version
Compatibility Law) and Article 11 (Foundation Reuse Law).

## What "LOCKed" means

A package or module is LOCKed when the phase that built it has a
Freeze document (`docs/PHASE*_FREEZE.md` or equivalent) that declares
it closed. Every phase's Freeze document lists exactly what is now
LOCKed. Confirmed LOCKed as of this policy's writing:

- Phase 62.x — Constitution & Runtime Foundation
  (`ai/runtime/`, `ai/providers/`, `ai/router/`).
- Phase 63.0 — Senior Trading AI Foundation
  (`ai/persona/`, `ai/content/content_types.py`'s `ContentType`,
  `ai/explanation/explanation_output.py`, `broadcast/`, `media/`,
  `translation/`, `telegram/owner/broadcast_commands.py`,
  `ai/capabilities/capability.py`'s four Phase 63.0 members).

## The Foundation Reuse Audit (Article 11 checklist)

Before any new module is written, every Worker Brief's `TASK 0`
answers, in order:

1. Foundation — does a package for this already exist?
2. Manager — does a manager class for this already exist?
3. Contract — does a request/result/output dataclass for this already
   exist?
4. Model — does a data model for this already exist?
5. Capability — does a `Capability` enum member for this already
   exist?
6. Registry — does a static registry/catalog for this already exist?

Any "yes" forbids a new module for that concern; the answer is
extension, governed by the Stability rule below. All six "no" permits
a new module, and the audit document states why.

## The Stability rule for a LOCKed module

Extension is always permitted. What is never permitted on a LOCKed
module without an explicit, dedicated Director instruction:

- moving or renaming its file/package;
- changing or removing an existing public class, function, or method
  signature;
- breaking an existing import path.

Permitted without special approval: a new method, a new optional
field with a safe default, a new `Capability`/enum member, extended
documentation. This is exactly the shape of change
`ai/audit/provider_stats.py` went through three times (Phase 61.1,
61.3, 61.6) and `ai/router/routing_rules.py` went through once per new
`Capability` (Phase 62.2, 63.0) — additive, never a move or a rename.

## Related

- `docs/constitution/CONSTITUTION.md` Articles 7, 9, 11.
- `docs/architecture/EXTENSION_GUIDE.md` — the concrete "how to add
  work without violating an Article" walkthrough.
