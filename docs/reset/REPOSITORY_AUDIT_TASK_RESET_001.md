# TASK-RESET-001 — Repository Audit & Cleanup Report

**Status:** Audit + Classification COMPLETE. **No merge/delete executed yet
— awaiting Director confirmation of the destructive plan** (see §7).
**Snapshot:** `origin/main = dc1761c` · 81 non-main remote branches · fetched
with `--prune`.

Consolidates all TASK-RESET-001 read-only deliverables (Branch Inventory,
Main Comparison, Classification). Merge/Delete/Final reports are filled in
§6 only after the Director authorizes execution.

---

## 1. Executive summary

- **81** remote branches exist besides `main` — the exact
  parallel-branch sprawl the Branch Management Policy was written to end.
- **34** are fully contained in `main` (`ahead=0`) — their code is
  already merged; deleting them loses nothing.
- **47** carry unique unmerged commits (`ahead>0`) — mostly **other
  workers'** recent branches. Deleting these *would* destroy work, so
  none is auto-classified DELETE.
- `origin/main` advanced independently during this task
  (`5618ade → dc1761c`) and **already contains `ai/foundation/`** — so
  some "unique" commits are likely **content-duplicates** of main under
  different SHAs (the duplicate-work problem). Content-level equivalence
  must be confirmed per branch before any of them is called redundant.
- **I did not create 80 of these 81 branches.** Per policy (Rule 11 +
  Rule 10) and safety, mass irreversible deletion of other workers'
  branches is presented for Director decision, not executed unilaterally.

---

## 2. Branch Inventory (81 + main)

| Prefix | Count | Notes |
|---|---|---|
| `main` | 1 | authoritative branch (`dc1761c`) |
| `archive/*` | 3 | intentional historical backups |
| `claude/*` | 2 | agent working branches (1 is this Worker's) |
| `feature/*` | 76 | task/worker feature branches |

---

## 3. Main Comparison — classification key

- **MERGED-IN** = `ahead=0`: every commit is already in `main` → code loss
  on delete = none.
- **HAS-UNIQUE** = `ahead>0`: has commits not in `main` → delete *may*
  lose work; requires review (SHA-unique ≠ content-unique).

---

## 4. Classification

### 4a. MERGED-IN → DELETE-eligible (34; code already in `main`)

`archive/*` (3) are deliberate backups → **REVIEW/KEEP**, not deleted
without Director word. The remaining **31 `feature/*`** are safe DELETE
candidates:

```
feature/bootstrap-followup            feature/gb-platform-const-batch-01
feature/candle-builder                feature/gb-platform-const-batch-02
feature/core-004-current-price-integration  feature/gb-platform-const-batch-03
feature/core-gateway                  feature/gb-platform-const-batch-04
feature/docs-price-stream-live-price  feature/gb-platform-const-batch-05
feature/event-bus                     feature/gb-platform-constitution-v1
feature/gb-const-001-vision           feature/governance-batch-1
feature/gb-const-002-mission          feature/governance-batch-2
feature/gb-const-batch-01             feature/governance-dd038-dd039
feature/gb-const-batch-02             feature/historical-bootstrap
feature/gb-const-batch-03             feature/market-data-foundation
feature/gb-const-batch-04             feature/market-memory-core
feature/gb-const-batch-05             feature/memory-reader
feature/gb-constitution-v1            feature/persistent-memory
feature/price-stream                  feature/replay-engine
feature/snapshot-infra
```

`archive/*` → **REVIEW (recommend KEEP):**
`archive/claude-code-analysis`, `archive/claude-trading-ai`,
`archive/main-pre-v1` — named backups; deletion is a Director call.

### 4b. HAS-UNIQUE → REVIEW (47; unmerged commits, mostly other workers')

None are auto-DELETE and none are auto-MERGE — each needs a Director
decision. Grouped:

| Group | Branches | ahead | Note |
|---|---|---|---|
| This Worker | `claude/code-analysis-optimization-pwfo3q` | 5 | 4 commits' content already in `main` (`ai/foundation`); only `BRANCH_MANAGEMENT_POLICY.md` is genuinely novel → **KEEP** (active) |
| Other agent | `claude/trading-ai-arch-review-tgszrz` | 3 | other worker — REVIEW |
| gb-core-* | 12 branches (`api/datamodel/dcr-system/impl/integration-test/production-handoff/review-release/security-test/spec/statemachine/unit-test` + `data-layer-mvp`) | 1–5 | recent (07-26/27), active-looking — REVIEW |
| gb-chart-const-batch-* | 25 branches (01–25) | 2–7 | near-identical pattern, likely superseded content-dupes — REVIEW (verify content) |
| gb-mvp / misc | `gb-signal-builder-mvp`, `gb-strategy-engine-mvp`, `gb-telegram-delivery-mvp`(9), `gb-media-constitution`, `gb-platform-dcr-migration`, `gb-ai-constitution-v1`(21), `chart-engine-vision`, `master-task-phase2` | 1–21 | REVIEW |

Full per-branch `ahead` counts and last-commit dates are in the raw audit
(§8 appendix note).

---

## 5. Why execution is paused here

1. **Irreversibility** — remote branch deletion cannot be undone from this
   session; 47 branches hold unmerged commits.
2. **Not this Worker's branches** — 80/81 were created by other
   workers/sessions; safety rules require surfacing, not guessing.
3. **`main` moved independently** — SHA-uniqueness overstates real unique
   *content*; calling a branch redundant needs content confirmation.
4. **Archives are intentional** — `archive/*` are backups; Rule 10 puts
   retention under the Director.
5. **Permission unknown** — pushing branch deletes / merges to `main` may
   exceed this session's git scope; to be verified at execution.

---

## 6. Merge / Delete / Final Repository Report

**Director decision (recorded):** delete the 31 merged-in `feature/*`;
KEEP `archive/*` (3); REVIEW the 47 HAS-UNIQUE (no action).

**Delete execution — BLOCKED by permissions.** All 31 deletions were
attempted (each re-guarded at `ahead=0` first) and **all 31 failed with
`HTTP 403`** from the git remote:

```
git push origin --delete feature/bootstrap-followup
→ error: RPC failed; HTTP 403 ... Everything up-to-date
git ls-remote origin feature/bootstrap-followup
→ f3f0c4f...  refs/heads/feature/bootstrap-followup   (still present)
```

This session's git credentials permit pushing to this Worker's own
branch only; they do **not** carry delete/force rights on other refs.
The agent proxy is healthy (`recentRelayFailures: []`), so the 403 is a
GitHub-side permission decision, not a network fault — retrying will not
change it. There is also no branch-delete tool in the GitHub MCP set.

**Result:** 0 deleted, 31 blocked. No local deletions were needed (the 31
are remote-only; local has just `main` + this Worker's branch). No merge
was attempted (none was authorized). **Repository is unchanged.**

**To actually delete these 31**, one of:
- the Director/owner deletes them (GitHub UI *Branches* page, or
  `git push origin --delete <name>` with owner credentials), or
- this session is granted delete scope on the repo, then re-run §7A.

## 6a. Final Repository state (current)

`main` + 3 `archive/*` (KEEP) + 2 `claude/*` (this Worker active + 1
other) + 76 `feature/*` — **81 non-main branches remain** (unchanged;
deletes blocked). Target "only main" is not reachable from this session's
permissions.

---

## 7. Proposed execution plan (needs Director GO)

- **A. Safe deletes (31 merged-in `feature/*`):** delete remote+local.
  Zero code loss (all `ahead=0`). ← recommend GO.
- **B. `archive/*` (3):** KEEP as backups (default) unless Director says
  delete.
- **C. HAS-UNIQUE (47):** Director decides per group — MERGE, DELETE, or
  KEEP. Worker will content-verify any group the Director marks before
  acting. No guessing.
- **D. This Worker's branch:** KEEP; its one novel artifact
  (`BRANCH_MANAGEMENT_POLICY.md`) is the only thing not yet in `main`.

---

## 8. Worker note

Audit is read-only and complete. I am holding before any destructive
step and requesting the Director's decision on §7 A/B/C. I will not
delete or merge another worker's branch on my own judgment.
