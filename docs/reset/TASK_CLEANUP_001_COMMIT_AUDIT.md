# TASK-CLEANUP-001 — Claude-branch Commit Audit

**Branch:** `claude/code-analysis-optimization-pwfo3q` · **ahead of
`origin/main`:** 13 commits (merge-base far back; `main` advanced ~100+
commits independently on other work). **Verdict up front: 0 DROP.** None
of the 13 is a duplicate of `main` — every one is unique, unmerged, and
useful. All are **MERGE**; grouped below with a safe landing order.

## Key finding — `main` has NOT superseded this work

Verified against `origin/main`:

| Refactor artifact (this branch) | State on `main` |
|---|---|
| `ai_layer/ai_service/event_bus.py` (moved out of `ai/runtime/`) | `main` LACKS it — still `ai/runtime/event_bus.py` |
| `ai_layer/ai_service/content/content_types.py` (neutral `ContentType`) | `main` LACKS it |
| `ai/foundation/` (whole package) | `main` has **no** `ai/foundation/` |
| `TradeJournalRecord` rename | `main` LACKS it — still `TradeJournalEntry` |
| `ai/content/explanation_content_adapter.py` (relocated) | `main` still has it at `ai/explanation/` |

So the TASK-AI-000A circular-dependency cleanup and the TASK-AI-001
Foundation are genuinely **missing from `main`**, not redundant.

## Per-commit classification (oldest → newest)

| # | Commit | Content | Class | Note |
|---|---|---|---|---|
| 1 | `3baae51` | Constitution v2.0 Stage 0 Audit → `docs/CONSTITUTION_V2_AUDIT.md` | **MERGE** | doc, unique |
| 2 | `4d7c0c4` | TASK-AI-000 AI Architecture Audit → `docs/ai/*` (9 files) | **MERGE** | audit docs, unique |
| 3 | `805b8d4` | TASK-AI-000A AI Cleanup → **code**: `event_bus` move, `ai_layer/ai_service/content/content_types.py`, `TradeJournalEntry→Record`, ~20 test import updates | **MERGE** | approved cleanup, not in `main`; **conflict-check needed** (main diverged) |
| 4 | `05d4024` | TASK-AI-001 AI Foundation → `ai/foundation/` (15 files) | **MERGE** | approved, not in `main` |
| 5 | `fcdfbe5` | Branch Management Policy → `docs/policies/BRANCH_MANAGEMENT_POLICY.md` | **MERGE** | permanent policy |
| 6 | `837a3a0` | Branch Management Policy Rev 1 (Rule 11) | **MERGE** | squashes with #5 |
| 7 | `effed1d` | TASK-RESET-001 report | **MERGE** | session record |
| 8 | `d4b8082` | INFRA-403 diagnosis | **MERGE** | infra note |
| 9 | `cf4538d` | INFRA-403 exhaustive layer analysis | **MERGE** | squashes with #8 |
| 10 | `fa3514d` | TASK-DEPLOY-002 report | **MERGE** | deploy record |
| 11 | `aaba1f2` | TASK-DEPLOY-003 report | **MERGE** | deploy record |
| 12 | `4a43e45` | TASK-DEPLOY-003 SUCCESS | **MERGE** | squashes with #11 |
| 13 | `e8ee06e` | **Production deploy docs reconcile** (`DEPLOYMENT.md`, `PRODUCTION_DEPLOYMENT.md`) | **MERGE (priority)** | *these must reach `main` — they document main-as-production* |

**Summary:** KEEP 0 · MERGE 13 · DROP 0.

## Grouped landing plan (recommended)

- **Group A — functional (approved code):** `4d7c0c4`, `805b8d4`,
  `05d4024` (+ `3baae51` audit). The AI cleanup + Foundation. **Highest
  scrutiny** — `main` diverged, so a merge here can conflict on shared
  `ai/` and test files; CI on the merge must pass (pyflakes/pytest).
- **Group B — governance:** `fcdfbe5`, `837a3a0` — Branch Management
  Policy (permanent).
- **Group C — session records:** `effed1d`, `d4b8082`, `cf4538d`,
  `fa3514d`, `aaba1f2`, `4a43e45` — audit/infra/deploy reports (low risk,
  docs-only).
- **Group D — production docs (priority):** `e8ee06e` — must land so
  `main`'s own `DEPLOYMENT.md` stops saying "main stale".

## How to actually land these (the Worker cannot self-merge)

This session's git-proxy allows writes to this branch only (HTTP 403 on
any push/merge to `main` — see `INFRA_403_DIAGNOSIS_TASK_INFRA_001.md`),
and no PR exists yet. So the MERGE cannot be done from here directly.
Path:

1. Open a PR: `claude/code-analysis-optimization-pwfo3q` → `main`.
2. Let CI (`ci.yml` / the deploy `validate` job) run — this is the
   conflict/regression gate for Group A especially.
3. Owner reviews + merges (Group A with care; B/C/D are low-risk docs).
4. After merge, delete the branch (remote+local) — closing TASK-RESET's
   branch-cleanup item. Deletion still needs owner/permission (git-proxy
   403 blocks it from this session).

**No merge or PR was created by this audit** — classification only, per
the task's "Natija: KEEP/MERGE/DROP".
