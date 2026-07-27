# Repository Reset Plan (Planning Only — no delete/merge/rewrite/archive)

Per the Director's Repository Reset Planning order. **Nothing is merged,
deleted, rewritten, or archived by this document.** It classifies every
unmerged branch (Phase A), proposes a merge sequence (Phase B), and lists
deletions gated on those merges (Phase C). Every call is justified from
the branch's actual unmerged commits — no assumptions.

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
| `claude/code-analysis-optimization-pwfo3q` | +4 | **MERGE (AI track)** | `TASK-AI-000/000A/001` AI Foundation Activation + Constitution v2.0 Stage‑0 audit — the **ACTIVE AI Foundation** track's work. Wanted, but the merge is the **AI Worker's** call to coordinate, not a unilateral Core‑reset merge. |

### A2 — KEEP (protected / pending; do NOT delete or merge yet)
| Branch | Commits | Decision | Reason |
|---|---|---|---|
| `claude/trading-ai-arch-review-tgszrz` | +3 | **KEEP** | DD‑005/DD‑006 governance + the TASK‑002F audit; the **Governance Reconciliation is DEFERRED by DD‑073**. Deleting or migrating it is blocked until that deferred reconciliation runs. |
| `feature/gb-ai-constitution-v1` | +21 | **KEEP / REVIEW** | 21 commits of AI Constitution governance docs [Draft]. AI track is active; verify against main's `docs/constitution/` (which already has AI chapters) before any delete — an **AI‑track** decision, not this reset's. |

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
2. [AI track] claude/code-analysis-optimization-pwfo3q → main   (AI Foundation; AI-Worker coordinated)
        ↓
3. [optional] preserve reconciliation analysis docs → main
        (cherry-pick docs/architecture_reconciliation/ + docs/mvp_release/
         from feature/gb-telegram-delivery-mvp-v1, if the Director wants them retained)
```

Each merge: reason above; verify CI green before the next. `pwfo3q`
(step 2) and the KEEP branches (A2) are **not** merged by this Core reset
without the AI‑track / governance owners' sign‑off.

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
- **HOLD (not deleted by this reset):** `claude/trading-ai-arch-review-tgszrz`
  (governance reconciliation deferred), `feature/gb-ai-constitution-v1`
  and `pwfo3q` (AI track — until their merges/decisions are done).

After Tiers 1–3 and the HOLD items are resolved, only `main` (+ any
Director‑approved long‑lived branch) remains — the single source of truth.

---

## Blockers / notes for the Director (no assumptions)

1. **VPS / Telegram / live‑smoke validation (Reset Phase 1–2 gates) cannot
   be done from this environment** (no egress). They remain operator steps;
   cleanup should follow them, as ordered.
2. **Branch deletion is irreversible** — this plan never deletes an
   unmerged branch before its wanted commits are in `main`.
3. **Three prior orders intersect this reset** and need an explicit call:
   the **MVP‑keep** hold (A3), the **deferred governance reconciliation**
   (A2 `claude/trading-ai`), and the **AI‑track independence** (A1/A2
   pwfo3q + ai‑constitution). This plan holds them rather than overriding
   silently.
4. **Nothing executed.** Awaiting Director approval of this plan before any
   merge; deletion authorized only per Phase C after merges + validation.
