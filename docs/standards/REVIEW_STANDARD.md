# Review Standard

What a review — Director review of a Worker's completed phase, or a
Worker's own pre-commit self-check — actually verifies, checklist
form.

## Constitution compliance

- No forbidden import introduced (`ai/` → `decision/`/`risk/`/
  `execution/`, or any other row in `docs/architecture/IMPORT_RULES.md`'s
  Forbidden table).
- No LOCKed module's name, path, import path, or public API changed
  (Article 9) unless explicitly Director-approved as a version-boundary
  change.
- The trading pipeline (`core/pipeline.py`, `decision/`, `risk/`,
  `execution/`, `strategies/`) has zero diff, unless the brief
  explicitly named it in scope.

## Foundation Reuse Audit (Article 11) was actually followed

Not just claimed — checkable: does the diff introduce a new top-level
package, manager, or registry where an existing one could have been
extended? If so, does the phase's audit document explain why steps 1–6
of the checklist were all "no"?

## Scope discipline

- Does the diff match what the brief's TASKs actually asked for, or
  does it carry an uninstructed refactor, rename, or cleanup alongside
  it?
- Is every new file's existence traceable to a specific TASK?

## Test and documentation completeness

- Every new module has a test (Article 6).
- Every new top-level package has a `README.md`.
- Every doc's **Related** section points to what governs it and what
  it governs (`docs/standards/DOCUMENTATION_STANDARD.md`).

## Freeze document present and honest

- Built / Not built / Constitution compliance / New-Extended-Reused
  table (Article 12) all present.
- "Not built" section is not empty by omission — it names what the
  brief's own Strict Rules excluded.

## Reporting language

No "Complete"/"Validated"/"All checks passed" before GitHub Actions
confirms `success` for the exact commit (`CLAUDE.md`'s Reporting
language rule).

## Related

- `docs/policies/DIRECTOR_POLICY.md`.
- `docs/policies/FOUNDATION_POLICY.md`.
- `docs/standards/TEST_STANDARD.md`, `docs/standards/DOCUMENTATION_STANDARD.md`.
