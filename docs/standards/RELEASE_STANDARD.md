# Release Standard

The concrete, step-by-step companion to `docs/policies/RELEASE_POLICY.md`.

## Before a phase is releasable

1. Every TASK in the Worker Brief has a corresponding change in the
   diff, or an explicit note in the Freeze document explaining why it
   was skipped/deferred.
2. `docs/standards/COMMIT_STANDARD.md`'s full sequence has run clean
   for the exact commit being released.
3. The phase's Freeze document exists and includes Article 12's
   New/Extended/Reused table.
4. `docs/roadmap/VERSIONS.md` is checked: does this phase's scope
   belong to the version already in progress, or does it cross a
   version boundary (`docs/policies/VERSION_POLICY.md`)? If the
   latter, was that explicitly Director-approved?

## GitHub Actions is the actual gate

A phase is not released until the specific commit's GitHub Actions run
reports `success`. A local-only green run is "Local validation
passed. Waiting for GitHub Actions confirmation," not a release.

## After release

- `docs/README.md`'s Phase History section gets the new Freeze
  document's entry in the same commit or the very next one — an index
  gap is a standard violation, not a cosmetic miss (the exact gap this
  phase's own TASK 0 found and fixed for Phase 62.2/63.0).
- If the release closes out a version row in `docs/roadmap/VERSIONS.md`,
  that row's status updates in the same pass.

## Related

- `docs/policies/RELEASE_POLICY.md`.
- `docs/standards/COMMIT_STANDARD.md`.
- `docs/roadmap/VERSIONS.md`.
