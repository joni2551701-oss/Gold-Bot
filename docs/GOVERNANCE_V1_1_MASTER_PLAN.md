# GOVERNANCE_V1_1_MASTER_PLAN

**Task**: GOV-PLAN-001 (ORDER-013), Critical priority, Planning only.
**Type**: Master Plan only. No governance document is created by this
task (beyond this plan itself). No existing Constitution, Law, Policy,
ADR, or Standard is changed. No repository implementation, branch
operation, or GitHub settings change is performed. This document is the
sole deliverable; each of the 9 planned documents becomes its own
future, separately-issued, separately-reviewed, separately-Frozen task.

**Naming note (flagged before anything else, per the No Silent
Decisions Policy)**: the Director's own note says the Director will
"launch TASK-001 through TASK-009" for the 9 documents once this plan
is approved. **`TASK-XXX` is already a reserved, in-use prefix** in
this repository — `communication/task_queue/QUEUE.md`'s Platform Tasks
track already owns `TASK-001` (Platform Foundation) through `TASK-005`
(Notification Center). Reusing bare `TASK-001`..`TASK-009` for the 9
Governance v1.1 documents would collide with that existing sequence
and create real ambiguity about which `TASK-001` a reference means.
This plan proposes **`GOV-001` through `GOV-009`** instead — consistent
with this session's own established convention of giving each distinct
work track its own prefix (`TASK-XXX` Platform, `DEVOPS-XXX`
Engineering, `GOVERNANCE-REVIEW-XXX` whole-governance audit, `REPO-XXX`
repository engineering, `GOV-PLAN-001` this very planning task) — and
maps 1:1 onto the Director's own 1–9 ordering below. Flagged explicitly
rather than silently substituted.

---

## Writing Order

The Director's own 1–9 listing is also the correct dependency order —
no document needs to be written out of this sequence:

```
Roles                                    Policies                              Standard
GOV-001 Director.md                      GOV-005 Repository_Policy.md         GOV-009 Git_Workflow_Standard.md
   ↓                                          ↓
GOV-002 Core_Worker.md                   GOV-006 Branch_Policy.md
   ↓                                          ↓
GOV-003 Platform_Worker.md                GOV-007 Branch_Protection_Policy.md
   ↓                                          ↓
GOV-004 Collaboration_Rules.md           (GOV-008 Engineering_Language_Policy.md —
   ↓                                       no dependency on any other document;
   └──────────────┬────────────────────────  safe to write at any point in this
                   ↓                          sequence, kept in the Director's
              GOV-009 depends on              stated position by default)
              GOV-006 + GOV-007
```

Rationale: `GOV-002`/`GOV-003` (Core/Platform Worker) each need `GOV-001`
(Director) to exist first, since both roles are defined partly by their
relationship to the Director. `GOV-004` (Collaboration Rules) needs all
three role documents to exist before it can describe how they interact.
`GOV-006` (Branch Policy) needs `GOV-005` (Repository Policy) for its
general repo-governance framing. `GOV-007` (Branch Protection) needs
`GOV-006` to exist, since protection rules attach to specific branches
`GOV-006` defines. `GOV-009` (Git Workflow Standard) needs both `GOV-006`
and `GOV-007`, since day-to-day git mechanics depend on knowing which
branches exist and how they're protected. `GOV-008` (Engineering
Language Policy) is the one document with zero dependency on any other
— it could be written first, last, or anywhere between without
breaking anything; it stays in position 8 only because that is where
the Director placed it and there is no reason to move it.

## Cross-Document Dependency Map

| Doc | Depends on | Existing repo documents it must reconcile with (Reuse Audit, per Constitution Article 11) |
|---|---|---|
| GOV-001 Director.md | Constitution Articles 8, 10 | `docs/policies/DIRECTOR_POLICY.md` (already informally covers much of this — its own TASK 0 must state explicitly whether Director.md extends, replaces, or sits alongside it) |
| GOV-002 Core_Worker.md | GOV-001 | `docs/HANDOFF.md`, `docs/CURRENT_PHASE.md`'s "Role boundary" section, `CLAUDE.md`'s Trading Safety rules |
| GOV-003 Platform_Worker.md | GOV-001 | `docs/HANDOFF.md`, `docs/PLATFORM_WORKFLOW.md` (must cross-reference, not restate, its 10-step process) |
| GOV-004 Collaboration_Rules.md | GOV-001, GOV-002, GOV-003 | `communication/README.md` and its 9 subfolder READMEs (must state whether Collaboration_Rules.md sits above them as role-level narrative or replaces any of them — recommend the former) |
| GOV-005 Repository_Policy.md | none | `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md`, `docs/BRANCH_FORENSICS_001.md`, `docs/PHASE_BRANCH_SYNC_AUDIT.md`, `docs/PHASE_P1_AUDIT.md`, `docs/DEPLOYMENT.md` (must state whether it supersedes or cross-references these) |
| GOV-006 Branch_Policy.md | GOV-005 | `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md` §3/§4 (direct source of the proposed branch model) |
| GOV-007 Branch_Protection_Policy.md | GOV-006 | `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md` §5 |
| GOV-008 Engineering_Language_Policy.md | none | none identified — genuinely new, no existing document covers this |
| GOV-009 Git_Workflow_Standard.md | GOV-006, GOV-007 | `docs/standards/COMMIT_STANDARD.md` (must state explicitly: complementary, not competing — COMMIT_STANDARD governs single-commit validation sequence, Git_Workflow_Standard governs branch/PR/tag mechanics) |

---

## GOV-001 — Director.md

**Purpose**: Formally define the Director role's authority,
responsibilities, and boundaries — the principal who sets mission and
priority, reviews and approves every Architecture-First deliverable,
issues ORDER-numbered decisions, and holds final Freeze sign-off.

**Scope**: What the Director does (sets intent/priority, approves
Analysis/Architecture/Implementation Plan steps before code is
written, resolves STOP → AUDIT conflicts per Article 8, authorizes
Constitution amendments as their own dedicated phase); what the
Director does not do (write code directly, bypass the Worker's
Commit Protocol, silently amend the Constitution).

**Dependencies**: Constitution Article 8 (Change Management Law),
Article 10 (Owner Override Law — for disambiguating the engineering
"Director" from the Telegram "Owner" role, which are easily confused
by name-adjacency but govern entirely different things). `docs/policies/DIRECTOR_POLICY.md`
already states most of this informally — GOV-001's own TASK 0 must run
the Foundation Reuse Audit against it and state explicitly whether
Director.md extends it, replaces it, or the two coexist at different
tiers (Role vs. Policy).

**Required Sections**: Role Definition; Authority (what only the
Director decides); Responsibilities; Boundaries (what the Director
does not do); Relationship to the Owner role (Article 10
disambiguation); Escalation Path (Article 8's STOP → AUDIT → Director
Decision, restated at the role level); Related.

**Out of Scope**: Does not define Core Worker or Platform Worker (their
own documents); does not restate `DIRECTOR_POLICY.md`'s Intelligence
Dependency Principle content unless the Reuse Audit finds it belongs
here instead; does not introduce a multi-Director model (a Part B item
in `docs/GOVERNANCE_REVIEW_001.md`, still out of scope).

**Acceptance Criteria**: The `DIRECTOR_POLICY.md` overlap question is
answered explicitly in the document itself, not left ambiguous; Director
vs. Owner is disambiguated in writing; no content contradicts Articles
8 or 10.

**Review Checklist**: Article 8/10 compliance confirmed; `DIRECTOR_POLICY.md`
relationship stated; no new authority invented beyond what this
session has already demonstrated in practice (ORDER-numbering, Freeze
approval, ADR issuance).

**Freeze Criteria**: Director-approved; `DIRECTOR_POLICY.md` overlap
resolved with no open question remaining; Constitution impact reviewed
(likely "none — Role tier, not Article tier" unless the Director
decides otherwise).

## GOV-002 — Core_Worker.md

**Purpose**: Define the Core Worker role — Trading Engine & AI layer
work (`context/`, `strategies/`, `signals/`, `ai/`, `decision/`,
`risk/`, `execution/`, `database/`), operating on its own line
(`feature/core`, per `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md`
§3 — not yet approved or implemented; see Out of Scope).

**Scope**: Permitted modules; forbidden actions; validation
obligations (the same Commit Protocol as every other role);
interaction points with the Director and Platform Worker.

**Dependencies**: GOV-001 (Director.md must exist first — this role is
partly defined by its relationship to the Director). `docs/HANDOFF.md`
(the existing Core/Platform role-boundary document — Reuse Audit must
state whether Core_Worker.md extends it or is a new, more formal
restatement); `docs/CURRENT_PHASE.md`'s "Role boundary" section
("Core... remains untouched" — the standing rule this entire session
has operated under); `CLAUDE.md`'s Trading Safety section (signal
logic, risk limits, decision flow, execution — must be cross-referenced,
never duplicated or reworded).

**Required Sections**: Role Definition; Permitted Modules; Forbidden
Actions (no Platform-layer changes); Validation Obligations; Branch
Usage (written conditionally — see Out of Scope); Escalation (when
Core Worker needs Platform Worker's output, or vice versa — ties into
GOV-004); Related.

**Out of Scope**: Does not change any Trading Core code; does not
define the branch model itself (GOV-006's job) — this document's
Branch Usage section must be written to remain correct whether or not
`feature/core` is ever actually created, i.e. it describes intent, not
a committed-to branch name, until GOV-006 is Frozen and Repository
Migration actually executes; does not define the Director's role
(GOV-001's job).

**Acceptance Criteria**: `docs/HANDOFF.md` Reuse Audit finding stated
explicitly; zero contradiction with `CLAUDE.md`'s Trading Safety rules;
Branch Usage section explicitly conditional, not presumptive.

**Review Checklist**: `CLAUDE.md` Trading Safety cross-check; no
unauthorized branch-model assumption baked in ahead of GOV-006's own
approval.

**Freeze Criteria**: Director-approved; `docs/HANDOFF.md` relationship
resolved explicitly.

## GOV-003 — Platform_Worker.md

**Purpose**: Define the Platform Worker role — this session's own role
throughout — covering `platforms/`, `telegram/`, `communication/`, and
Platform-facing documentation, operating on its own line
(`feature/platform`, same conditional status as GOV-002's `feature/core`).

**Scope**: Mirrors GOV-002's structure exactly, for the Platform side.

**Dependencies**: GOV-001. `docs/HANDOFF.md` (same Reuse Audit
question as GOV-002, mirrored for the Platform side). `docs/PLATFORM_WORKFLOW.md`
(the existing 10-step "Architecture First" process this role has
followed throughout this session — Platform_Worker.md's Required
Sections must cross-reference this document, never restate its steps).
`docs/CURRENT_PHASE.md`'s role-boundary section.

**Required Sections**: Role Definition; Permitted Modules; Forbidden
Actions (no Trading Core changes — demonstrated repeatedly this
session via `git diff --cached --stat` checks against Trading Core
paths on every commit); Validation Obligations; Process (cross-reference
`PLATFORM_WORKFLOW.md`, do not duplicate); Branch Usage (conditional,
same posture as GOV-002); Escalation; Related.

**Out of Scope**: Does not restate `PLATFORM_WORKFLOW.md`'s 10 steps;
does not define the Core Worker's role.

**Acceptance Criteria**: Explicit `PLATFORM_WORKFLOW.md` cross-reference
rather than duplication; `docs/HANDOFF.md` relationship stated; Branch
Usage section explicitly conditional.

**Review Checklist / Freeze Criteria**: mirrors GOV-002's, applied to
the Platform side.

## GOV-004 — Collaboration_Rules.md

**Purpose**: Define exactly how Director, Core Worker, and Platform
Worker interact — task issuance, review cycles, escalation — and, once
GOV-006 exists, how work flows between `feature/core`/`feature/platform`
→ `develop` → `main`.

**Scope**: Ties together the nine existing `communication/` folders
(`requests/`, `responses/`, `notifications/`, `issues/`, `contracts/`,
`reviews/`, `decisions/`, `technical_debt/`, `task_queue/`) into one
coherent "how the three roles actually work together" narrative, which
today exists only piecemeal across `communication/README.md` and each
subfolder's own README.

**Dependencies**: GOV-001, GOV-002, GOV-003 (must exist first — this
document defines interaction between roles those documents define).
`communication/README.md` and its 9 subfolder READMEs (Reuse Audit
must state Collaboration_Rules.md sits *above* them as a higher-level
narrative — `communication/README.md` stays the folder-level index,
this document does not replace it). `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md`
§6's proposed Collaboration Model diagram (Director → Task → Core/Platform
Worker → develop → Director Review → main) — its branch-level content
is conditional on GOV-006's own approval, same posture as GOV-002/003's
Branch Usage sections.

**Required Sections**: Interaction Model (Director ↔ Core Worker ↔
Platform Worker); Task Issuance Flow; Review/Approval Flow; Escalation/
Conflict Resolution (Article 8's STOP → AUDIT → Director Decision, at
the collaboration level); Branch-Level Collaboration (conditional on
GOV-006); Related.

**Out of Scope**: Does not redefine any of the 9 `communication/`
folders' own formats (already governed by their own READMEs); does not
itself approve the branch model.

**Acceptance Criteria**: Explicit statement of relationship to
`communication/README.md`; no content restated from GOV-001/002/003,
only their interaction.

**Review Checklist / Freeze Criteria**: standard pattern (Constitution/
ADR/Workflow compliance, Director approval, no open Reuse question).

## GOV-005 — Repository_Policy.md

**Purpose**: The top-level policy governing how this repository itself
is structured and governed — default-branch meaning, production-branch
identity, when a branch is authoritative — the policy-tier home for
facts `REPO-001`/`BRANCH-FORENSICS-001` already established, so no
future engineer has to reconstruct "which branch is production" from
scattered phase-audit docs and workflow-file comments again.

**Scope**: Formalizes `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md`
§0/Q1–Q2's findings (production branch identity since 2026-07-12,
`main` as configured-but-inactive default branch) as standing policy,
not merely an audit finding.

**Dependencies**: none (first in its group, no other Governance v1.1
document precedes it). Existing documents to reconcile with:
`docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md`, `docs/BRANCH_FORENSICS_001.md`
(the facts this policy formalizes); `docs/PHASE_BRANCH_SYNC_AUDIT.md`,
`docs/PHASE_P1_AUDIT.md`, `docs/DEPLOYMENT.md` (existing docs already
recording pieces of this — Reuse Audit must state whether
Repository_Policy.md supersedes/consolidates or merely cross-references
them, per `docs/policies/DOCUMENTATION_POLICY.md`'s own no-duplication
rule); Constitution Article 9 (repo-level stability guarantees).

**Required Sections**: Default Branch vs. Production Branch (explicit,
standing distinction, correct until Migration actually executes);
Branch Authority Table; Historical Note (cross-reference the forensics
report, do not repeat its content); Change Process (how this policy
itself updates once Migration executes); Related.

**Out of Scope**: Does not define the specific new branch model
(GOV-006's job); does not perform the Migration itself; does not lift
ORDER-009's pause.

**Acceptance Criteria**: Zero contradiction with `BRANCH_FORENSICS_001.md`'s
findings; explicit stated relationship to `PHASE_BRANCH_SYNC_AUDIT.md`/
`PHASE_P1_AUDIT.md` (supersede vs. cross-reference, chosen and stated,
not left implicit).

**Review Checklist**: standard pattern, plus a live-fact check — the
repository state this document describes must match the actual current
git state at the moment of Freeze, re-verified, not assumed carried
over from `REPO-001`.

**Freeze Criteria**: Director-approved; live-fact check passed;
Reuse Audit's supersede/cross-reference choice stated.

## GOV-006 — Branch_Policy.md

**Purpose**: Ratify the actual branch model (`main` / `develop` /
`feature/core` / `feature/platform`) this repository will use once
Migration resumes — promoting `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md`
§3's proposal (or the Director's revised version of it) from "audit
report proposal" to "standing policy."

**Scope**: Each branch's purpose, who may commit to it, its
relationship to the others. Explicitly written to remain correct while
ORDER-009's pause is still in effect — this is the plan the eventual
Migration executes against, not an action taken now.

**Dependencies**: GOV-005 (general repository governance must exist
first). `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md` §3/§4
(direct source material). GOV-002/GOV-003 reference this document's
branches conditionally — GOV-006 does not depend on them.

**Required Sections**: Branch Model Diagram; Per-Branch Purpose/
Ownership; Promotion Rules (`feature/*` → `develop` → `main`);
Relationship to Repository Recovery (ORDER-010's queued item — the
Unicode filename fix should logically land before or as part of the
model's first real use) and to the still-paused Migration; Related.

**Out of Scope**: Does not itself create any branch (still forbidden
until Migration is separately authorized); does not define protection
rules (GOV-007's job).

**Acceptance Criteria**: Consistent with GOV-005; explicitly marked
"approved policy, pending implementation" for as long as ORDER-009's
pause remains in effect.

**Review Checklist / Freeze Criteria**: standard pattern; Freeze here
means the *policy* is finalized, not that the branches exist yet.

## GOV-007 — Branch_Protection_Policy.md

**Purpose**: The specific protection rules per branch (direct-push
restrictions, required review, required CI) — promoting `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md`
§5's proposal to standing policy.

**Scope**: Mirrors REPO-001 §5's table, refined as the Director
directs.

**Dependencies**: GOV-006 (protection cannot attach to branches not
yet policy-defined). GitHub's actual branch-protection feature set — a
technical constraint this policy must respect exactly, not describe
past what GitHub can actually enforce.

**Required Sections**: Protection Rules Table (per branch); Enforcement
Mechanism (GitHub branch-protection settings — described here, applied
only in a later, separately-authorized implementation step); Exception
Process (for a rare, explicit Director override); Related.

**Out of Scope**: Does not enable any protection itself (forbidden
without separate authorization); does not define CI pipeline content
(`.github/workflows/*.yml` remains untouched without its own explicit
authorization, per `CLAUDE.md`'s standing rule).

**Acceptance Criteria**: Consistent with GOV-006; zero direct edit to
any `.github/workflows/*.yml` file.

**Review Checklist / Freeze Criteria**: standard pattern, plus an
explicit note that Freeze here means the policy is finalized — not
that protection is enabled on any branch.

## GOV-008 — Engineering_Language_Policy.md

**Purpose**: Formalize the language convention this repository already
follows in practice but has never written down: code, comments,
commit messages, and documentation are English-only; the Director-Worker
conversational exchange may be in any language (this entire session's
own Director messages have been Uzbek) but every artifact committed to
the repository is English — matching 100% of existing evidence across
this repository's full history and every commit made this session.

**Scope**: Language of code/comments/docstrings; language of commit
messages; language of documentation (`docs/`, `communication/`).
Explicitly out of scope: the Director-Worker conversational channel
itself, which is never repository content and is not something an
engineering policy governs.

**Dependencies**: none — the one document in this set with zero
dependency on any other; no existing document was found that already
covers this (genuinely new, confirmed during `GOVERNANCE-REVIEW-001`'s
full read of all 11 existing policies — none named a language
convention).

**Required Sections**: Scope of Applicability; The Standard (English,
with its evidence base — `CLAUDE.md`, every file under `docs/`, every
commit message to date); Non-Governance Exception (Director-Worker
conversation is unrestricted); Rationale (searchability, tooling
compatibility, matching this repository's own established practice);
Related.

**Out of Scope**: Does not restrict the Director's own language choice
in conversation; does not touch user-facing Telegram bot content
language (a distinct, product-level question belonging to
`translation/`'s Phase 63.0 foundation, not engineering governance).

**Acceptance Criteria**: Zero contradiction with existing evidence (no
repository content anywhere is in a language other than English);
explicit non-governance-exception stated for the Director's own
communication.

**Review Checklist / Freeze Criteria**: standard pattern; trivial to
Freeze given zero existing contradiction to reconcile.

## GOV-009 — Git_Workflow_Standard.md

**Purpose**: The Standard-tier document operationalizing GOV-006 and
GOV-007 into day-to-day git mechanics — branch naming, PR title/
description convention, merge-vs-rebase policy, and a tagging
convention that directly closes the "zero tag strategy, zero rollback
anchor" gap both `REPO-001` and `BRANCH-FORENSICS-001` independently
found.

**Scope**: Everything about actually using git under the new model —
distinct from `docs/standards/COMMIT_STANDARD.md`, which governs the
validation sequence for a single commit (pyflakes → compileall →
pytest → smoke run → push → CI), not branch/PR/tag mechanics.

**Dependencies**: GOV-006, GOV-007 (day-to-day mechanics depend on
knowing which branches exist and how they're protected). `docs/standards/COMMIT_STANDARD.md`
(explicit cross-reference required — Reuse Audit must state clearly
these two Standards are complementary, not competing, since both touch
"how we commit").

**Required Sections**: Branch Naming Convention; PR Convention (title/
description — an opportunity to fix the "both existing PRs share one
generic auto-generated title" finding from `REPO-001`, if the Director
wants PR hygiene formalized); Merge Strategy (merge/squash/rebase, and
why); Tagging Convention (closing the rollback-anchor gap); Relationship
to `COMMIT_STANDARD.md`; Related.

**Out of Scope**: Does not restate `COMMIT_STANDARD.md`'s validation
sequence; does not enable branch protection itself.

**Acceptance Criteria**: Explicit `COMMIT_STANDARD.md` cross-reference,
not duplication; tagging convention section directly addresses the
rollback-anchor gap by name.

**Review Checklist / Freeze Criteria**: standard pattern.

---

## Common Review Checklist Pattern (applies to all 9, stated once here to avoid repeating it 9 times)

Every one of GOV-001 through GOV-009's own future Freeze Checklist
includes, at minimum: Constitution/ADR/Workflow compliance reviewed;
the specific Reuse Audit question named in its own Dependencies section
above answered explicitly (not left ambiguous); no other existing
Constitution Article, Law, Policy, ADR, or Standard modified; Director
Approval; Freeze Applied — mirroring the same Freeze Checklist shape
`docs/PLATFORM_WORKFLOW.md` already established for Platform Tasks,
reused here rather than inventing a second checklist format.

## Governance v1.1 Freeze Sequencing

Per the Director's own note: each of GOV-001 through GOV-009 is
written, reviewed, and Frozen individually — Governance v1.1 as a
whole is declared Frozen only once all 9 are individually Frozen, not
before. This Master Plan does not itself Freeze anything; it is the
plan those 9 future Freezes are checked against.

## Exit Criteria (from ORDER-013, confirmed met)

- Writing order for all 9 documents is explicit (see Writing Order,
  above) — matches the Director's own 1–9 listing exactly.
- Each document's purpose and boundaries are explicit (see GOV-001
  through GOV-009 above — each has its own Purpose, Scope, Dependencies,
  Required Sections, Out of Scope, Acceptance Criteria, Review
  Checklist, Freeze Criteria).
- Each document is ready to be issued as its own separate task — every
  section above is written at brief-level detail, adaptable directly
  into an executable Director Brief per Constitution Article 8 /
  `docs/policies/DIRECTOR_POLICY.md`'s "what makes a brief executable"
  rule (Objective, TASK 0 Reuse Audit question, Strict Rules/Out of
  Scope, Acceptance Criteria all present for each).
- The Director can launch GOV-001 through GOV-009 in sequence without
  further clarification — each entry states exactly what exists today
  that the future task must reconcile with, removing the need for a
  fresh audit pass before each one starts.

## Related

- `docs/GOVERNANCE_REVIEW_001.md` — the whole-governance audit whose
  Part B findings this plan draws on (missing `PLATFORM_POLICY.md`,
  missing Engineering Workflow document, etc. — none of which
  duplicate the 9 documents planned here).
- `docs/REPO_001_REPOSITORY_ENGINEERING_MIGRATION.md`,
  `docs/BRANCH_FORENSICS_001.md` — the source material GOV-005/006/007/009
  formalize into policy/standard form.
- `docs/constitution/CONSTITUTION.md` Article 8, Article 11 — the
  ordering and Reuse Audit discipline this plan itself follows.
- `communication/task_queue/QUEUE.md` — where each GOV-00X task will be
  tracked once issued, on its own track, distinct from `TASK-XXX`.
