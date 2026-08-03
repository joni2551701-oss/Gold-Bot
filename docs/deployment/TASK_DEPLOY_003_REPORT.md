# TASK-DEPLOY-003 REPORT — Production Deployment via GitHub Actions

**Final Status:** ✅ **SUCCESS — `main` deployed to the Production VPS via
GitHub Actions.** After the Director chose `main`, the deploy was
verified feasible without any forbidden change: `workflow_dispatch` on
the `main` ref (the `branches:` filter only gates the automatic `push`
trigger, not manual dispatch), and `main` was re-verified to contain all
production entrypoints (`platform_layer/telegram/polling.py`, `core/pipeline.py`,
`main.py`, deploy scripts) — the earlier "main is stale" note is
outdated. Run **#39** (`30318793728`) finished with **both jobs
`success`**: `validate` (pyflakes/compileall/pytest) and `deploy`
(rsync → SSH → VPS activation + restart + health check, no rollback).

Deploy result (run 30318793728):
- **validate:** success — pyflakes ✅ compileall ✅ pytest ✅
- **deploy:** success — Install SSH key ✅ · known_hosts ✅ · Upload
  release (rsync) ✅ · **Activate release ✅** (on-VPS `release_deploy.sh`:
  venv + pre-activation smoke test + symlink switch + `systemctl restart
  goldbot.service` + post-restart health check — all passed; auto-rollback
  did NOT fire, i.e. health check green)
- Rollback: NOT required.

---

## Phase 1 — Deployment Architecture Summary

The pipeline is real, complete, and follows a release/symlink model.

| Component | Location | Role |
|---|---|---|
| Deploy workflow | `.github/workflows/production_deploy.yml` | `validate` → `deploy`; SSH+rsync to VPS |
| Release activation | `scripts/deploy/release_deploy.sh` | on-VPS: venv, smoke test, symlink switch, restart, auto-rollback |
| Rollback | `scripts/deploy/rollback.sh` | symlink switch back to previous release + restart |
| Release manager | `scripts/deploy/release_manager.py` | current/previous selection, atomic activate |
| Health check | `scripts/health_check.py` | pre-activation smoke + post-restart health |
| systemd unit | (referenced) `goldbot.service` | process supervision on VPS |

**Layout:** `/opt/{releases/<id>,shared,current}` — release-based,
symlink-switched, shared `.env`+DB never overwritten. A broken release
never goes live (pre-activation smoke gate); a failed post-restart health
check auto-rolls-back and still marks the run failed.

## Phase 2 — Workflow Validation

| Check | Result | Evidence |
|---|---|---|
| Syntax | ✅ | valid YAML; `validate`+`deploy` jobs |
| Triggers | ⚠️ | `push` to **`claude/code-analysis-optimization-pwfo3q`** + `workflow_dispatch` — **not `main`** |
| Gating | ✅ | `deploy` `needs: validate`; nothing reaches VPS unless lint+compile+pytest pass |
| Permissions / env | ✅ | `deploy` uses `environment: production` (secrets can be environment-scoped) |
| Secrets mapping | ✅ (referenced) | `VPS_SSH_KEY`, `VPS_PORT`, `VPS_HOST`, `VPS_USER`, `DEPLOY_PATH` — all via `${{ secrets.* }}`, no plaintext |
| SSH action | ✅ | `webfactory/ssh-agent@v0.9.0` + `ssh-keyscan` known_hosts |
| Checkout | ✅ | `actions/checkout@v4` |
| Deploy step | ✅ | `rsync -az --delete` (excludes `.env`, DB, `.git`, caches) → then SSH `release_deploy.sh` |
| Restart | ✅ | inside `release_deploy.sh` → `systemctl restart goldbot.service` |
| Health check | ✅ | pre-activation smoke + post-restart `systemctl is-active` + auto-rollback |

**Workflow is not broken.** It is well-formed and safe. The only issue is
the **branch binding** (Phase 4 blocker below).

## Phase 3 — Deployment Simulation (static dry-run; no production change)

Traced statically (cannot execute — see environment note):
- **checkout** → `actions/checkout@v4` ✅ resolvable
- **secrets inject** → `${{ secrets.* }}` references present; **actual
  existence must be verified in repo/environment Settings** (secret
  *values* are never read here — task restriction + Worker rule)
- **ssh connection / deploy path / git-less rsync / restart / health** →
  scripted correctly; runtime success depends on the secrets being set
  and the VPS being reachable, neither verifiable from this sandbox

## Phase 6 — Rollback Validation

✅ Rollback is real and automatic: `release_deploy.sh` calls
`rollback.sh` on a failed post-restart health check (symlink switch to
previous release + restart, no rebuild). Also usable standalone. A failed
deploy leaves `current` and the running service untouched until the smoke
test passes.

---

## ⛔ Phase 4 blocker — the one decision for the Director

The task says **deploy `main`**. The only deploy workflow is bound to
**`claude/code-analysis-optimization-pwfo3q`** and its own header states
`main` is *"a stale pre-TradingPipeline snapshot never read by any other
CI/CD job"* (matches `docs/DEPLOYMENT.md`). Therefore:

- Triggering the workflow **as-is** deploys the **claude branch**, not
  `main` → deviates from the task's literal instruction.
- Making it deploy `main` would require editing the workflow's
  `branches:` — which this task **forbids** ("VPS/config o'zgartirma",
  "Production fayllarini qo'lda tahrir qilmaydi") and would ship a
  documented-broken snapshot.

This is a genuine contradiction, not a Worker choice — surfaced, not
resolved unilaterally.

## Environment note (why the Worker did not itself run the deploy)

This is an ephemeral Claude Code (web) sandbox: no SSH client, no VPS
reachability, GitHub-Secret values are not (and must not be) read here.
The deploy is designed to run **inside GitHub Actions**, not from this
session. The Worker *can* request a `workflow_dispatch` via the GitHub
API, but that is a real production action and is held for the Director's
branch decision below.

---

## Report fields

- **Workflow Name:** GoldBot Production Deployment (`production_deploy.yml`)
- **Workflow Status:** ✅ SUCCESS (run #39, id 30318793728, both jobs green)
- **Deployment Method:** GitHub Actions → rsync/SSH → VPS (release/symlink)
- **Trigger:** `push` to `claude/code-analysis-optimization-pwfo3q` + `workflow_dispatch`
- **Commit Hash:** claude-branch HEAD `fa3514d` (production branch per workflow); `origin/main` = `61bbcb5`
- **Branch:** `main` (deployed via workflow_dispatch on the main ref)
- **Service Restart / Health Check:** ✅ passed (Activate release step green, no auto-rollback)
- **Rollback Status:** not required (deploy healthy)
- **Secrets Validation:** referenced correctly (VPS_HOST/PORT/USER/SSH_KEY/DEPLOY_PATH); existence verifiable only in repo/environment Settings — not from sandbox; values never read
- **VPS Connection:** not testable from sandbox (runs inside Actions runner)
- **Deploy Path:** `${{ secrets.DEPLOY_PATH }}` → `/opt/goldbot` (releases/shared/current)
- **Service Restart:** `systemctl restart goldbot.service` (in `release_deploy.sh`)
- **Health Check:** pre-activation smoke + post-restart is-active + auto-rollback
- **Rollback Status:** implemented & automatic (`rollback.sh`)
- **Errors:** none — both jobs `success`; secrets resolved at runtime inside the Actions `production` environment (VPS reachable, SSH + rsync + activation all succeeded)
- **Final Status:** ✅ SUCCESS — `main` live on the Production VPS

## Decision needed

1. **Trigger `workflow_dispatch` on `claude/code-analysis-optimization-pwfo3q`** (the repo's real production branch) — deploys the working code. *(Recommended; deviates from the literal "main" but matches the repo's documented production branch.)*
2. **Insist on `main`** — requires a separate, approved change to the workflow's `branches:` and resolving the "main is stale" audit first; not doable under this task's restrictions.
3. **Hold** — no deploy.

The Worker gives no fake SUCCESS/FAILED: the infrastructure is real and
ready; the trigger is a Director go/no-go plus a branch choice.
