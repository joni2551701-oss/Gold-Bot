# Engineering Language Policy

The authoritative policy for the language of GoldBot's engineering
artifacts: source code, documentation, commit messages, ADRs, READMEs,
and naming. It is governed by `docs/constitution/CONSTITUTION.md`, sits
within Engineering Governance v1.1 (GOV-008 / ORDER-019), and formalizes
a convention this repository has followed in practice from its first
commit but never written down (confirmed genuinely new — no existing
policy named a language convention, per `docs/GOVERNANCE_REVIEW_001.md`).

**Director decision point, surfaced not buried**: the GOV-008 brief
explicitly offered the option to keep internal project documents in
Uzbek instead of English. This policy is written with **English** as
the official engineering language for all repository artifacts, because
that matches 100% of the repository's existing evidence (every file
under `docs/`, every code comment, and every commit message to date is
English) and GOV-008's own acceptance criterion is zero contradiction
with existing evidence. The Director may override this to Uzbek (or
another language) for internal documentation as an explicit, recorded
decision — doing so would require re-authoring the existing English
governance corpus and is therefore a deliberate, separately-scoped
choice, not a silent default. Absent that override, English stands.

## 1. Purpose

To make the language of engineering artifacts explicit and consistent,
so tooling (search, grep, diff, linters), any future contributor, and
every AI or human Worker operate against one predictable convention —
and so the distinction between *repository artifacts* (English) and the
*Director–Worker conversation* (unrestricted) is never ambiguous.

## 2. Official Engineering Language

**English** is the official engineering language for every artifact
committed to the repository. This is a description of existing practice
made binding, not a new imposition.

The **Director–Worker conversation** (briefs, reviews, verdicts,
discussion) is explicitly **not** governed by this policy and may be in
any language — this entire project's Director communication has been in
Uzbek, and that is unaffected. Conversation is never a repository
artifact.

## 3. Documentation Language

- All documentation committed to the repository (`docs/`,
  `communication/`, README files, ADRs, changelogs) is English.
- (Override clause, per §preamble: if the Director elects Uzbek for
  internal documentation, this section is the one that changes, and the
  existing corpus is migrated as its own task.)

## 4. Code Language

- All source code is English: identifiers, string literals used
  internally, and inline text. User-facing strings are the exception
  (§12) — they follow the product's localization approach, not this
  engineering rule.

## 5. Variable Naming

- Variables are English, descriptive, and follow the repository's
  existing style (`docs/standards/CODE_STANDARD.md`) — `snake_case` for
  Python locals/functions, no transliteration, no non-ASCII identifiers.

## 6. Class Naming

- Classes are English `PascalCase`, named for what they are
  (`RiskManager`, `NavigationCore`, `PlatformRegistry`) — matching the
  existing codebase convention.

## 7. Function Naming

- Functions/methods are English `snake_case`, named for what they do
  (`evaluate`, `has_sufficient_permission`, `build_default_registry`) —
  matching existing practice.

## 8. Comment Policy

- Comments are English and explain *why*, not *what*, only where the
  reason is non-obvious (`docs/standards/CODE_STANDARD.md`'s
  comment-density rule); this policy governs their *language*, not
  whether a comment should exist.

## 9. Commit Message Language

- Commit messages are English — summary line and body — matching every
  commit in this repository's history and the `docs/standards/COMMIT_STANDARD.md`
  shape (which this policy references for format and governs only for
  language).

## 10. ADR Language

- Architecture Decision Records (`communication/decisions/ADR-XXX.md`)
  and their `docs/changelog/DECISION_LOG.md` entries are English —
  matching ADR-001 through the current ADR.

## 11. README Language

- Every `README.md` (top-level, per-package, and the `communication/`
  folder READMEs) is English.

## 12. Exception Rules

The following are **not** governed by the English rule:

- **The Director–Worker conversation** — unrestricted (§2).
- **User-facing content** — Telegram bot messages, notifications, and
  any end-user text follow the product's own localization approach
  (multilingual support), which is a **product** concern owned by the
  Platform layer / `translation/`, not an engineering-language concern.
  This policy never dictates the language a *user* sees.
- **Quoted external content** — a third-party error message, a cited
  document, or test data may appear verbatim in its original language
  where quoting it accurately requires that.

Any exception beyond these three is a Director decision, recorded — not
a Worker's to grant.

## 13. Compliance

- **Constitution** — consistent with all Articles; introduces no
  conflict. Supremacy applies.
- **Existing evidence** — zero contradiction: every current repository
  artifact is already English (the acceptance criterion for this
  policy).
- **Governance v1.1** — no contradiction with any role/collaboration/
  policy document; `docs/standards/CODE_STANDARD.md` and
  `COMMIT_STANDARD.md` are referenced for *style/format*, this policy
  governs only *language*, so no duplication.
- **`translation/` and the product localization approach** — respected:
  user-facing multilingual content is explicitly carved out (§12).

## 14. References

- `docs/constitution/CONSTITUTION.md` — the supreme document.
- `docs/standards/CODE_STANDARD.md`, `COMMIT_STANDARD.md` — the
  style/format standards this policy governs the language of.
- `docs/GOVERNANCE_REVIEW_001.md` — confirmed no prior language policy
  existed (this is genuinely new).
- `docs/governance/roles/Platform_Worker.md`, `translation/` — the
  owner of the user-facing localization the §12 exception defers to.
- `communication/task_queue/GOV-PACKAGE-001.md` — this package's ticket.
