# Documentation Standard

The concrete, file-level companion to `docs/policies/DOCUMENTATION_POLICY.md`.

## Every doc's shape

1. A one-line title.
2. A first paragraph stating which Constitution Article (or Policy)
   governs it, and what it is (or is not) a substitute for.
3. Body sections with real module paths and file names — never a
   description of an idealized structure that doesn't match the repo.
4. A closing **Related** section linking to what governs this doc and
   what builds on it.

## Every module README's shape

A new top-level package's `README.md` (see `ai/persona/README.md`,
`broadcast/README.md` for the model) states: what the package is for,
what it explicitly does not do yet (if foundation-only), and which
Constitution Article/Policy governs it.

## Honesty over completeness

A doc states a capability is foundation-only, not-yet-wired, or a
known gap explicitly — it never implies more than the code actually
does. `docs/AI_BROADCAST_FOUNDATION.md`'s "What none of this does yet"
section and `docs/owner/OWNER_PANEL.md`'s "Honest gaps" section are the
model. This is not optional polish — a doc that overstates a
capability is a Documentation Policy violation, the same severity as a
missing test.

## Corrections over silence

When a phase's audit finds an existing doc states something the real
code contradicts, the doc is corrected as part of that phase's work
(with a note explaining the correction), not left standing.
`docs/architecture/MODULE_DEPENDENCIES.md`'s `knowledge/` location
note and `docs/architecture/DATA_FLOW.md`'s AI-stage-ordering
correction are both real examples from this project's own history.

## Related

- `docs/policies/DOCUMENTATION_POLICY.md`.
- `docs/constitution/CONSTITUTION.md` Article 6, Article 7.
