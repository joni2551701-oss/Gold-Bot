# Repository Reset Plan (Planning Only — no delete/merge/rewrite/archive)

Per the Director's Repository Reset Planning order. **Nothing is merged,
deleted, rewritten, or archived by this document.** It classifies every
unmerged branch (Phase A), proposes a merge sequence (Phase B), and lists
deletions gated on those merges (Phase C). Every call is justified from
the branch's actual unmerged commits — no assumptions.

**Director status:** ✅ **APPROVED with modifications** — (1) `core-004`
→ MERGE; (2) `pwfo3q` → **REVIEW REQUIRED** (do not merge until the AI
Worker confirms the branch is no longer required); (3) **no permanent
HOLD branches** — every remaining branch is ultimately removed; any
wanted documentation/governance is **migrated into `main` first, then the
branch is deleted**. This revision reflects all three.

**Baseline:** `origin/main = 20e49a6` — the most‑advanced line (+96 over
the old DD‑002 canonical `pwfo3q`; contains the assembled
`docs/constitution/`, `ai/` (182 files incl. `ai/chart_intelligence/`),
`platforms/`, `data/memory` v1.1, etc.).

**Inventory:** 48 branches carry unmerged commits (data loss if deleted);
37 are already merged into `main` (safe to delete, zero data loss).

---

## Phase A — Classification of all 48 unmerged branches

Legend: **MERGE** = has wanted commits to bring into main · **KEEP** =
protected/pending, neither merge nor delete now · **DELETE** = obsolete/
superseded, deletable after the gate in its Reason.

### A1 — MERGE (wanted code into main)
| Branch | Commits | Decision | Reason |
|---|---|---|---|
| `feature/core-004-current-price-integration` | +2 | **MERGE** | Approved Current Price Phase 1 (CI #362/#363 green); the wanted production feature. Clean FF into main. |
| `claude/code-analysis-optimization-pwfo3q` | +4 | **REVIEW REQUIRED** (Mod 2) | `TASK-AI-000/000A/001` AI Foundation Activation + Constitution v2.0 Stage‑0 audit — the **ACTIVE AI Foundation** track's work. **Do not merge** until the AI Worker confirms the branch is no longer required (is the AI Worker still developing on it, or are its wanted commits already elsewhere?). After that review: MERGE wanted commits → then the branch joins the deletion set (Mod 3, no permanent HOLD). |

### A2 — MIGRATE‑THEN‑DELETE (no permanent HOLD — Mod 3)
These are not deleted immediately, but they are **not** permanent HOLD
branches either: their wanted material is migrated into `main`, then the
branch is deleted.
| Branch | Commits | Decision | Reason & resolution |
|---|---|---|---|
| `claude/trading-ai-arch-review-tgszrz` | +3 | **MIGRATE‑THEN‑DELETE** | DD‑005/DD‑006 governance + TASK‑002F audit; the **Governance Reconciliation is DEFERRED by DD‑073**. Resolution: when that reconciliation runs, migrate the wanted governance records into `main` (per the accepted Governance Reconciliation Plan — DD‑006's substance may be dropped, DD‑005's Navigation freeze migrates as an MA record), **then delete the branch**. No permanent HOLD. |
| `feature/gb-ai-constitution-v1` | +21 | **REVIEW → MIGRATE‑THEN‑DELETE** | 21 commits of AI Constitution docs [Draft]. AI‑track review: confirm whether its content is already in main's `docs/constitution/` (AI chapters exist). Migrate anything wanted into `main`, **then delete**. |

### A3 — MVP chain (DELETE conditional — see gate)
| Branch | Commits | Decision | Reason |
|---|---|---|---|
| `feature/gb-data-layer-mvp-v1` | +1 | **DELETE (gated)** | MVP data layer — superseded by v1.1/production (accepted TASK‑CORE‑003). |
| `feature/gb-strategy-engine-mvp-v1` | +2 | **DELETE (gated)** | MVP strategy (naive momentum) — superseded by `signals/`+`strategies/`. |
| `feature/gb-signal-builder-mvp-v1` | +3 | **DELETE (gated)** | MVP signal builder — superseded by `signals/`. |
| `feature/gb-telegram-delivery-mvp-v1` | +9 | **DELETE (gated) — preserve docs first** | MVP telegram + Current Price (migrated via core‑004). **BUT its +9 also carries the reconciliation analysis** (`docs/architecture_reconciliation/`, `docs/mvp_release/`) — decide whether to preserve those in main before deleting (they document the whole reconciliation decision). |
| **Gate for A3** | | | (1) Current Price merged via `core-004`; **(2) Director's explicit MVP retirement approval** — the prior order kept the MVP "Reference Only until retirement approval." The Reset arguably lifts that hold; confirm before deleting. |

### A4 — DELETE (obsolete/superseded docs‑draft working branches)
| Branch(es) | Commits | Decision | Reason |
|---|---|---|---|
| `feature/gb-chart-const-batch-01 … -25` (25 branches) | +2…+7 | **DELETE** | Draft working branches for the Chart Constitution identifier migration. Main already has the assembled `docs/constitution/` + `ai/chart_intelligence/`. Obsolete working branches (same lifecycle as the platform‑const batches already merged). |
| `feature/gb-core-spec/api/datamodel/statemachine/implementation/unit-test/integration-test/security-test/review-release/production-handoff-v1` (10) | +1 each | **DELETE** | Docs‑only `[Draft]` chapter sets superseded by the assembled Core docs + real implementation in main. |
| `feature/gb-core-dcr-system-v1` | +5 | **DELETE / REVIEW** | Carries `CORE-DCR-###` governance records — verify they're in main's `docs/constitution/DIRECTOR_RULINGS_REGISTER.md` before delete; if present → DELETE. |
| `feature/chart-engine-vision` | +1 | **DELETE** | Concept draft; chart work is in main (`ai/chart_intelligence/`). |
| `feature/gb-media-constitution-v1` | +1 | **DELETE / REVIEW** | Media Constitution [Draft]; main has `media/` code but no media‑constitution doc found — confirm the doc isn't wanted, then DELETE. |
| `feature/gb-platform-dcr-migration` | +2 | **DELETE** | Platform ruling‑identifier migration + freeze confirm; superseded by main's governance. |
| `feature/master-task-phase2` | +1 | **DELETE** | Obsolete Phase‑2 master planning doc. |

### A5 — Already merged (37 branches, incl. `archive/*`)
**DELETE — zero data loss.** Their commits are ancestors of `main`
(verified via `git branch -r --merged origin/main`), so dropping the refs
loses nothing. Includes `archive/main-pre-v1`, `archive/claude-code-analysis`,
`archive/claude-trading-ai` (all merged).

---

## Phase B — Merge sequence (only when authorized; nothing merged here)

```
1. feature/core-004-current-price-integration → main     (Current Price; approved; clean FF, +2)
        ↓  CI green + (operator) VPS/live-smoke
2. Migrate wanted docs/governance into main BEFORE any deletion (Mod 3):
     - reconciliation analysis (docs/architecture_reconciliation/, docs/mvp_release/)
       from feature/gb-telegram-delivery-mvp-v1, if retained;
     - the Governance Reconciliation content from claude/trading-ai-arch-review-tgszrz
       (when the DD-073-deferred reconciliation runs).
        ↓
3. [REVIEW REQUIRED — Mod 2] claude/code-analysis-optimization-pwfo3q:
     merge its AI-Foundation commits into main ONLY after the AI Worker
     confirms the branch is no longer required.
```

Each merge: reason above; verify CI green before the next. Step 3 is
gated on AI‑Worker confirmation; step 2's governance migration is gated on
the DD‑073‑deferred reconciliation. Nothing here is executed by this plan.

---

## Phase C — Deletion list (authorized ONLY after Phase B + validation)

Delete in tiers, each after its precondition:

- **Tier 1 — immediate‑safe (no data loss):** the **37 merged branches**
  incl. `archive/*`. Precondition: none (already in main).
- **Tier 2 — MVP chain (A3):** the 4 `feature/gb-*-mvp-v1`. Precondition:
  Current Price merged (Phase B‑1) **and** Director MVP‑retirement approval
  **and** the reconciliation docs preserved if wanted.
- **Tier 3 — obsolete drafts (A4):** the 25 chart‑const + 10 core‑*‑v1 +
  chart‑engine‑vision + media‑constitution + platform‑dcr‑migration +
  master‑task‑phase2 (+ core‑dcr‑system after its rulings are confirmed in
  main). Precondition: the per‑branch verifications noted in A4.
- **Tier 4 — migrate‑then‑delete (A2, Mod 3 — no permanent HOLD):**
  `claude/trading-ai-arch-review-tgszrz` and `feature/gb-ai-constitution-v1`
  are deleted **after** their wanted governance/docs are migrated into
  `main`. `pwfo3q` is deleted **after** the Mod‑2 AI‑Worker review (its
  wanted AI‑Foundation commits merged first). None of these remains as a
  standing branch.

**End state:** only `main` remains, plus **temporary** `feature/<task>`
branches that follow `main → feature → CI → merge → delete`. No
`claude/*`, `archive/*`, `governance/*`, old `feature/*`, or `recovery/*`
branch persists (Mod 3). A long‑lived branch exists only with explicit
Director approval.

---

## Blockers / notes for the Director (no assumptions)

1. **VPS / Telegram / live‑smoke validation (Reset Phase 1–2 gates) cannot
   be done from this environment** (no egress). They remain operator steps;
   cleanup should follow them, as ordered.
2. **Branch deletion is irreversible** — this plan never deletes an
   unmerged branch before its wanted commits are in `main`.
3. **Three prior orders intersect this reset** — now resolved by the
   Director's modifications: the **MVP‑keep** hold (A3) is lifted on
   explicit MVP‑retirement approval (after Current Price merges); the
   **deferred governance reconciliation** (A2 `claude/trading-ai`) ends in
   migrate‑then‑delete, not a permanent HOLD (Mod 3); the **AI track**
   (`pwfo3q`, `gb-ai-constitution`) is REVIEW‑gated on AI‑Worker
   confirmation (Mod 2), then migrate‑then‑delete.
4. **Nothing executed.** Plan APPROVED with modifications; deletion
   authorized only per Phase C after the required merges + validation. The
   first safe, no‑data‑loss executable steps on your go: merge `core-004`
   → main, then Tier‑1 deletion of the 37 already‑merged branches.
