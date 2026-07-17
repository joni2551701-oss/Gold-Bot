# Release Policy

## Freeze Protocol

Every phase closes with a Freeze document
(`docs/PHASE*_FREEZE.md` or equivalent) before it is reported as done.
A Freeze document states, at minimum:

- **Built this phase** — what shipped, per TASK.
- **Not built (honestly, not silently)** — what the brief's own Strict
  Rules explicitly excluded, so a future phase does not assume it
  exists.
- **Constitution compliance** — the specific grep/diff checks run
  (import sweeps, pipeline-diff checks) and their results.
- **New / Extended / Reused table** — Article 12's mandatory KPI.
- **Next phase recommendation** — what is separately-approved future
  work, not automatic follow-on.

## The CI gate

A phase is not "complete" until GitHub Actions reports `success` for
the exact commit being reported on. Local validation passing
(`pytest`, `pyflakes`, `compileall`, the `python main.py` smoke run) is
necessary but not sufficient — it is reported as "Local validation
passed. Waiting for GitHub Actions confirmation," never as done, until
CI confirms.

## Versioning

`docs/roadmap/VERSIONS.md` is the source of truth for what version
number a given phase belongs to. A phase does not silently jump a
version boundary (e.g. claim `v1.0` behavior while `VERSIONS.md` still
lists the project at `v0.4`) — see `docs/policies/VERSION_POLICY.md`
for how a phase decides whether it is additive-within-version or a
version-boundary change requiring explicit Director sign-off.

## Related

- `docs/constitution/CONSTITUTION.md` Article 12.
- `docs/policies/TESTING_POLICY.md` — the validation pipeline a Freeze
  depends on.
- `docs/policies/VERSION_POLICY.md`.
- `docs/roadmap/VERSIONS.md`.
