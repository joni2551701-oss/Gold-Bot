# Platform Documentation Policy

Introduced by PLATFORM-001 (Platform Foundation & Collaboration
Infrastructure). States the section list every Platform module's own
documentation uses, per the Director's explicit brief, and reconciles
it against the repo-wide standards that already govern documentation
(`docs/DOCUMENTATION_STANDARD.md`, `docs/standards/DOCUMENTATION_STANDARD.md`,
`docs/policies/DOCUMENTATION_POLICY.md`) rather than forking a
competing rule set (Constitution Article 7/11's reuse-first
requirement).

## Required sections

Every Platform module (`platforms/`, and any future Platform
implementation module) gets a doc — either its own `README.md` or a
dedicated `docs/PLATFORM_<NAME>.md`, matching this repo's existing
two-tier convention (`docs/DOCUMENTATION_STANDARD.md`'s "Every module
needs a README" plus a deeper topic doc) — with these sections, in
this order:

1. **Architecture** — how the module fits the Platform Layer, what it
   depends on and is depended on by.
2. **Implementation** — what actually exists: files, classes,
   functions, real not aspirational.
3. **Testing** — what test file(s) cover it, what they verify.
4. **Known Limitations** — what this module deliberately does not do
   yet (never silently omitted).
5. **Future Improvements** — named, concrete, not a vague "more
   later" (same rule `docs/DOCUMENTATION_STANDARD.md` already states
   for "Future roadmap").
6. **Platform Impact** — which client platforms (Telegram Bot,
   Telegram Mini App, Android, iOS, Desktop) this module concerns, and
   how — this is the section unique to Platform docs, absent from the
   repo-wide standard because that standard predates the multi-client
   Platform Layer.
7. **Dependencies** — exact modules imported, per
   `docs/PLATFORM_DEPENDENCY_MAP.md`'s "be exact" rule.

## Mapping onto the existing repo-wide standard

`docs/DOCUMENTATION_STANDARD.md`'s required README sections
(Purpose/Responsibility/Input/Output/Dependencies/Forbidden
dependencies/Future roadmap/Tests) and this policy's seven sections
describe the same underlying facts at a different granularity — this
table states the correspondence explicitly so a Platform module's docs
satisfy both at once, never contradicting either:

| This policy | Repo-wide standard equivalent |
|---|---|
| Architecture | Purpose + Responsibility |
| Implementation | Responsibility (file-by-file detail) |
| Testing | Tests |
| Known Limitations | (new — repo-wide standard has no direct equivalent; closest is stating what's deliberately unimplemented in Responsibility) |
| Future Improvements | Future roadmap |
| Platform Impact | (new — Platform-specific; no repo-wide equivalent, see above) |
| Dependencies | Dependencies + Forbidden dependencies |

`docs/policies/DOCUMENTATION_POLICY.md`'s cross-cutting rules still
apply unchanged: documentation-driven, not written after the fact;
every doc ends with a **Related** section; "Honesty over completeness"
and "Corrections over silence" (`docs/standards/DOCUMENTATION_STANDARD.md`).

## Related

- `docs/DOCUMENTATION_STANDARD.md`, `docs/standards/DOCUMENTATION_STANDARD.md`,
  `docs/policies/DOCUMENTATION_POLICY.md` — the repo-wide rules this
  policy narrows for Platform modules, never contradicts.
- `docs/PLATFORM_FOUNDATION.md` — the first module doc written under
  this policy, for `platforms/`.
