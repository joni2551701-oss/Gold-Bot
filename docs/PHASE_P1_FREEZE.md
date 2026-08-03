# Phase P1 Freeze — Production Deployment Pipeline Foundation

Worker Brief: "Production Deployment Pipeline Foundation" (Phase P1,
Version V1.0 Production, Priority CRITICAL, Director Approved). This
document is the freeze record: what was built, what was verified, and
what remains for the Director's first real VPS deploy.

Scope discipline honored throughout (RULE 1/2): Trading Core —
`core/`, `decision/`, `risk/`, `execution/`, `strategies/`, `signals/`,
`context/`, `ai/` — was never touched (verified empty diff, TASK 13
below). No business logic was added anywhere; this phase is deploy
tooling only.

## What this phase built

| # | Requirement | Delivered as |
|---|---|---|
| TASK 1 | GitHub Actions production workflow | `.github/workflows/production_deploy.yml` — `validate` (checkout → Python 3.11 → install → pyflakes → compileall → pytest) then `deploy`, gated on `validate` succeeding |
| TASK 2 | SSH deployment via secrets only | `webfactory/ssh-agent` + `VPS_HOST`/`VPS_PORT`/`VPS_USER`/`VPS_SSH_KEY`/`DEPLOY_PATH` — no plaintext credential anywhere |
| TASK 3 | Release-based deployment | `rsync` into `releases/<timestamp>/`, activated by `scripts/deploy/release_deploy.sh`; previous releases never deleted |
| TASK 4 | Shared persistence | `shared/.env`/`shared/database`/`shared/logs`, symlinked (never copied) into every release |
| TASK 5 | Atomic `current` symlink | `scripts/deploy/release_manager.py switch_current()` — temp symlink + `os.replace()`, POSIX-atomic |
| TASK 6 | systemd production service | `deploy/systemd/goldbot.service` — `Restart=always`, `User=senior` (never root), `WorkingDirectory=/opt/goldbot/current` |
| TASK 7 | Restart only after validation | `release_deploy.sh`'s order: smoke test → activate → restart → post-restart health check |
| TASK 8 | Health check | Extended `scripts/health_check.py` (config/secrets/database + new `main`/`telegram.polling` import checks) + `systemctl is-active` |
| TASK 9 | Smoke test | Same `scripts/health_check.py`, run against the new release *before* activation — import-only, no continuous execution |
| TASK 10 | Rollback | `scripts/deploy/rollback.sh` — symlink switch + restart, no rebuild; also invoked automatically by `release_deploy.sh` on a failed post-restart check |

## New modules

| File | Purpose |
|---|---|
| `.github/workflows/production_deploy.yml` | CI/CD pipeline (TASK 1/2) |
| `scripts/deploy/release_manager.py` | Pure release-selection/rollback-target logic — list/current/previous/switch_current, plus a CLI. Zero VPS/systemd/SSH dependency, fully unit-tested (TASK 3/5/10) |
| `scripts/deploy/release_deploy.sh` | Runs on the VPS via SSH: venv, symlink shared resources, smoke test, activate, restart, post-restart health check, auto-rollback on failure (TASK 3/4/7/9) |
| `scripts/deploy/rollback.sh` | Manual/automatic rollback — symlink switch + restart, no rebuild (TASK 10) |
| `deploy/systemd/goldbot.service` | Production unit for the release-based layout (TASK 6) |
| `docs/deployment/PRODUCTION_DEPLOYMENT.md` | Full architecture, VPS one-time setup, GitHub configuration |
| `docs/deployment/ROLLBACK.md` | Full rollback procedure, automatic and manual |

## Extended modules

- `scripts/health_check.py` (Phase 58) — two additive checks
  (`check_main_imports`/`check_telegram_imports`), reused for both the
  pre-activation smoke test (TASK 9) and the post-restart health check
  (TASK 8) rather than writing a separate script (Module Reuse
  Principle).

## Untouched (verified, not just assumed)

`docs/production_setup.md`, the four pre-existing
`deploy/systemd/goldbot-*` units, `Dockerfile`/`docker-compose.yml`,
`.github/workflows/trading_bot.yml`, `.github/workflows/owner_snapshot.yml`,
`.github/workflows/ci.yml` — see `docs/PHASE_P1_AUDIT.md` for the full
reasoning behind why each stayed untouched rather than being edited or
duplicated.

## Branch-trigger decision (Director-flagged)

The brief's TASK 1 literally named `main` as the trigger branch.
`production_deploy.yml` instead triggers on
`claude/code-analysis-optimization-pwfo3q`, matching every other
production-facing workflow in this repository
(`trading_bot.yml`/`owner_snapshot.yml`) and the Director-reviewed
`docs/DEPLOYMENT.md`/`docs/PHASE_BRANCH_SYNC_AUDIT.md`. `main` remains
a stale, pre-`TradingPipeline` snapshot; deploying it as-is would ship
broken code to the VPS. See `docs/PHASE_P1_AUDIT.md` section 1 for the
full reasoning — flagged here again for visibility since it is a
deviation from the brief's literal text.

## Trading Core verification (RULE 1)

`git diff --stat -- core/ decision/ risk/ execution/ strategies/
signals/ context/ ai/` against the pre-phase commit is **EMPTY** — see
TASK 13 in the Final Report for the exact command and output.

## Tests

155 new tests across `tests/deploy/` (`test_release_manager.py`,
`test_health_check_extended.py`, `test_production_deploy_workflow.py`,
`test_goldbot_systemd_unit.py`, `test_deploy_scripts_shape.py`) —
exceeding the 120+ minimum. Coverage matches TASK 12's named
categories: workflow validation, release logic, rollback, symlink
logic, deployment scripts, compatibility (full existing suite
unmodified and passing), isolation (`release_manager.py` statically
verified to import nothing from Trading Core).

## Known limitations (disclosed, not silently claimed as solved)

- **Never run end-to-end against a real VPS.** This sandbox has no
  `systemd`, no SSH target, and no `/opt/goldbot` to deploy to —
  everything here is verified by `bash -n` syntax checking, pure-Python
  unit tests of the release-selection logic, and manual review, not an
  actual deploy. The Director/operator's first real push to the
  production branch (or manual `workflow_dispatch`) is the first true
  end-to-end verification. This mirrors `docs/production_setup.md`'s
  own disclosed gap for the Phase 58 systemd units — same honesty
  standard, not a new risk category for this codebase.
- **No release retention/pruning** — `releases/` grows unboundedly;
  RULE 5 requires keeping the previous release for rollback, so no
  automatic deletion was added. A retention policy is a reasonable,
  small future follow-up.
- **`shared/.env` bootstrap is manual by design** — no deploy script
  writes real secret values anywhere, so the file must already exist
  on the VPS before the first deploy (documented in
  `docs/deployment/PRODUCTION_DEPLOYMENT.md`'s one-time setup section).

### Post-freeze incident: first real VPS deploy caught a database-exclude bug

The first real end-to-end deploy against the production VPS (after
this freeze) surfaced a bug this sandbox could never catch on its own:
`production_deploy.yml`'s `rsync` excluded `database` to protect the
shared SQLite file (RULE 4), but `database` is also this repository's
Python package name (`database_layer/database_manager/database.py`, `database/*_repository.py`).
The exclude matched the whole directory, so the release shipped
without the package at all, and the pre-activation smoke test failed
with `ModuleNotFoundError: No module named 'database_layer.database_manager.database'` —
correctly aborting before `current` or `goldbot.service` were touched
(the safety gate worked exactly as designed). Fixed by narrowing the
exclude to `database/*.db` and changing `release_deploy.sh` to symlink
only `shared/database/goldbot.db` into the release instead of the
whole `database/` directory — see
`docs/deployment/PRODUCTION_DEPLOYMENT.md`'s "package vs. runtime
data" section for the corrected design. Trading Core was not touched
by this fix; it is confined to deploy tooling
(`production_deploy.yml`, `release_deploy.sh`) plus this documentation
and their tests.

## Acceptance Criteria — Status

| Criterion | Status |
|---|---|
| GitHub Actions SUCCESS | Pending final push (see Final Report) |
| pyflakes clean | PASS |
| compileall clean | PASS |
| pytest 100% | PASS |
| Production workflow created | PASS |
| systemd service created | PASS |
| Release deployment implemented | PASS |
| Rollback implemented | PASS |
| Shared persistence implemented | PASS |
| Health Check implemented | PASS |
| Smoke Test implemented | PASS |
| Trading Core ZERO DIFF | PASS |
| Documentation complete | PASS |

## Director's stated next sequence

VPS Deployment → systemd Restart → Owner Monitoring → Alpha Runtime.
No manual production deployment is permitted after this phase unless
explicitly authorized by the Director.
