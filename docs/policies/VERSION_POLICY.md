# Version Policy

The operational face of Constitution Article 9 (Version Compatibility
Law), scoped to how a phase's *output* is versioned rather than how a
LOCKed module's internals stay stable.

## Two kinds of phase

**Additive-within-version** — the default. A phase extends existing
Foundation (new method, new field, new Capability, new package that
passed the Article 11 Reuse Audit with all six "no"). This does not
require a version-number change; `docs/roadmap/VERSIONS.md`'s current
entry absorbs it.

**Version-boundary change** — a phase that would break a LOCKed
module's public API, remove a capability, or change a documented
behavior a user or Owner already depends on. This requires the same
STOP → AUDIT → Director Decision protocol as any other Constitution
conflict (Article 8) before it proceeds, and — if approved — an
explicit new entry in `docs/roadmap/VERSIONS.md` marking the boundary.

## Compatibility check, per phase

Before a phase is reported done, its Freeze document confirms: does
any existing import path, public method signature, or documented
Owner command behavior differ from before this phase started? If yes,
was that change explicitly Director-approved as a version-boundary
change? If it was not, it is a Constitution Article 9 violation, not a
routine change.

## Related

- `docs/constitution/CONSTITUTION.md` Article 9.
- `docs/policies/FOUNDATION_POLICY.md` — the LOCKed-module Stability
  rule this policy's compatibility check enforces.
- `docs/roadmap/VERSIONS.md`.
