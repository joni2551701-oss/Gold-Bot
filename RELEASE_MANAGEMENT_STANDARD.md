# Release Management Standard — Director Order No. 020

## Module Reuse Justification

No existing file in this repository governs how a release moves from
planning through production and end-of-life. `CLAUDE.md` covers the
per-change commit protocol (staging, lint, tests, one push), which is
a *change-level* process; this order defines a *release-level*
lifecycle that spans many changes, has its own stages, its own
mandatory fields, and its own approval gate at Production. Neither
`ARCHITECTURE.md`, `RFC_STANDARD.md`, nor `ADR_STANDARD.md` covers
this — an RFC gets a change approved, an ADR records why a decision
was made, neither tracks a release through Alpha/Beta/RC/Production/
Maintenance/Hotfix/EOL. Per the Module Reuse Principle, steps 1 and 2
were both "no," so a new root-level file is justified.

## Release Lifecycle

Stages, in order, each with its entry/exit criterion:

1. **Planning** — Entry: a release scope is proposed (features,
   fixes, or both) and has enough Worker/Director agreement to start
   estimation. Exit: scope, target version number, and rough timeline
   are agreed and recorded.

2. **Development** — Entry: Planning has produced an agreed scope.
   Exit: all planned code changes for the release are written and
   individually pass their own commit-protocol validation (per
   `CLAUDE.md`).

3. **Internal Testing** — Entry: Development is complete for the
   release scope. Exit: the full automated test suite
   (`pytest tests/`) passes against the assembled release, with no
   known regression left open.

4. **QA** — Entry: Internal Testing has passed. Exit: manual/
   scenario-based verification of the release's behavior (not just
   automated tests) is complete and any findings are triaged.

5. **Alpha** — Entry: QA has passed. Exit: the release has run in a
   restricted, low-risk setting long enough to surface issues that
   only appear outside unit/integration testing, with no blocking
   issue open.

6. **Beta** — Entry: Alpha is stable. Exit: the release has been
   exposed to a wider (but still controlled) audience/scenario set
   with no blocking issue open.

7. **Release Candidate** — Entry: Beta is stable and no further
   scope changes are expected. Exit: an RC build exists that is
   feature-frozen, fully tested, and ready for Director review; this
   is as far as Worker Authority extends without explicit approval.

8. **Production** — Entry: explicit Director approval of the
   Release Candidate (see Worker Authority below — this is a hard
   gate). Exit: the release is live and being used/monitored under
   normal operating conditions.

9. **Maintenance** — Entry: a release is in Production. Exit: the
   release is superseded by a newer Production release or moves to
   End of Life.

10. **Hotfix** — Entry: a critical defect is found in a Production
    release that cannot wait for the next full release cycle. Exit:
    the hotfix passes the same commit protocol and Internal Testing
    bar as a normal change, and is deployed with its own version
    bump (PATCH-level, see Version Numbering below).

11. **End of Life** — Entry: a release is formally retired, whether
    replaced or deprecated. Exit: the release is no longer maintained
    or supported; this is recorded in the release's own notes.

## Per-Release Mandatory Fields

Every release must record, verbatim from Director Order No. 020:

- Version Number
- Scope
- Features
- Breaking Changes
- Migration Guide
- Test Summary
- Performance Summary
- Security Review
- Known Issues
- Rollback Strategy
- Release Notes

If `GOLDBOT_DEVELOPMENT_STANDARD.md` exists and defines a Rollback
Strategy standard, a release's Rollback Strategy field references
that standard rather than redefining rollback mechanics from scratch.

## Release Checklist

All items below are required before any Production release — no
exceptions:

- [ ] Architecture Validation
- [ ] Engineering Validation
- [ ] Development Validation
- [ ] Regression Test
- [ ] Performance Test
- [ ] Security Review
- [ ] Documentation Review
- [ ] CHANGELOG
- [ ] Director Approval

## Worker Authority

The Worker prepares Release Candidates, runs tests, writes Release
Notes, and prepares Known Issues — all of this is within Worker
Authority and needs no pre-approval. **Worker Authority stops at
Release Candidate.** Production Release requires explicit Director
approval, full stop, no exception — the same hard-gate language that
governs the RFC and ADR approval gates in `RFC_STANDARD.md` and
`ADR_STANDARD.md`.

## Version Numbering

This project uses semantic versioning: `MAJOR.MINOR.PATCH`. This is a
convention note, not a new mandate beyond what Director Order No. 020
specified — it is consistent with the repo's prior tag attempt
(`goldbot-v1.0.0`). `MAJOR` for breaking changes, `MINOR` for
backward-compatible feature additions, `PATCH` for backward-compatible
fixes, including Hotfixes released against a Maintenance-stage
version.
