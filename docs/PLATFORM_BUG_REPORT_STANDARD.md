# Platform Bug Report Standard

Introduced by PLATFORM-001, per the Director's explicit instruction:
a bug is never reported as just "bug fixed" — every one uses this
exact eight-field format. Confirmed during PLATFORM-001's own research
pass that no dedicated bug-report template existed anywhere in this
repo before this document (the closest relative,
`docs/standards/REVIEW_STANDARD.md`, is a phase-review checklist, not
a per-bug format) — genuinely new, not a duplicate.

`communication/issues/TEMPLATE.md` mirrors this format field-for-field
so filing a bug ticket doesn't require opening two files; this
document is the canonical definition.

## Fields

1. **Problem** — what is observed, concretely: an input, an action,
   the actual (wrong) output. Not a summary — the specific case.
2. **Root Cause** — the verified mechanism producing the wrong
   behavior, not a guess. If not yet verified, the status field says
   so rather than fabricating a cause.
3. **Current Code** — the relevant existing code: file path + line
   range, or a short quote, so the reader doesn't have to hunt for it.
4. **Correct Architecture** — what the code should do, stated against
   this repo's own architecture rules (`docs/ARCHITECTURE_RULES.md`,
   `docs/PLATFORM_DEPENDENCY_MAP.md`, or the relevant Constitution
   Article) — not just "it should work," a specific rule reference.
5. **Correct Code** — the proposed fix: a diff, or a description
   precise enough to implement from without further investigation.
6. **Regression Risk** — what could break if this fix is applied, and
   which existing tests already cover that risk (or don't).
7. **Tests** — which test(s) already cover this area; which new
   test(s) this fix adds.
8. **Status** — Open / In Progress / Fixed / Won't Fix (with reason).
   Never silently closed without one of these four.

## Where this is used

- `communication/issues/ISSUE-XXXX.md` — every ticket in that folder
  uses this exact format.
- Any bug fix reported in a Platform end-of-task report (see the
  Director's own Report Format, restated in `docs/PLATFORM_CHANGELOG.md`)
  that touches a bug, not just a feature, includes this format inline
  rather than a one-line "fixed X."

## Related

- `communication/issues/README.md`, `communication/issues/TEMPLATE.md`
  — the ticket-folder application of this format.
- `docs/standards/REVIEW_STANDARD.md` — the adjacent, but distinct,
  phase-review checklist.
