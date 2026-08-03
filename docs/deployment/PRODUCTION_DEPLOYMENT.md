# GoldBot — Production Deployment (Phase P1)

Worker Brief: "Production Deployment Pipeline Foundation" (Phase P1,
Version V1.0 Production, Priority CRITICAL, Director Approved). This
document covers the release-based, GitHub-Actions-driven deployment
path this phase introduced. It is deliberately separate from
`docs/production_setup.md` (Phase 58), which remains correct for the
older, direct-install `/opt/goldbot` layout — see
`docs/PHASE_P1_AUDIT.md` section 4 for why the two are not merged.

After this phase, **deploy only happens through GitHub Actions.**
Neither the Director nor the Worker deploys to the VPS by hand.

## Architecture

```
push to main  OR  workflow_dispatch (ref: main)   [production path]
    |   (as of TASK-CICD-001 both triggers name main -- the automatic
    |    push filter and manual dispatch deploy the same branch)
    v
GitHub Actions: production_deploy.yml
    |
    +-- validate job: checkout -> Python 3.11 -> install deps
    |                  -> pyflakes -> compileall -> pytest
    |                  (deploy job never runs if this fails)
    |
    v
    deploy job: rsync the checked-out tree over SSH into
                $DEPLOY_PATH/releases/<timestamp>/
    |
    v
    SSH: scripts/deploy/release_deploy.sh $DEPLOY_PATH <release_id> goldbot
         (runs ON the VPS, shipped as part of the release itself)
    |
    +-- create venv, pip install -r requirements.txt (per-release, isolated)
    +-- symlink shared/.env, shared/database/goldbot.db, shared/logs into the release
    +-- pre-activation smoke test (scripts/health_check.py) --
    |       FAILS -> abort here, `current` and the live service untouched
    +-- atomic switch: current -> releases/<release_id>  (scripts/deploy/release_manager.py)
    +-- systemctl restart goldbot.service
    +-- post-restart health check (scripts/health_check.py + systemctl is-active) --
            FAILS -> automatic rollback to the previous release (scripts/deploy/rollback.sh),
                     workflow run still marked failed
```

## VPS filesystem layout

```
/opt/
├── releases/
│   ├── 20260721101500/          # one full, self-contained checkout + its own venv/
│   ├── 20260721180912/
│   └── ...                       # never deleted automatically -- always keeps the previous release for rollback
├── shared/
│   ├── .env                      # real secrets, chmod 600, created once manually -- never overwritten by a deploy
│   ├── database/goldbot.db       # the runtime SQLite file, symlinked (as this one file) into every release
│   └── logs/                     # foundation per logs/README.md, symlinked into every release
├── current -> releases/20260721180912/   # atomic symlink, the only thing that changes on deploy
└── backups/                      # for your own backup rotation, see docs/DEPLOYMENT.md's Backup section
```

RULE 3/4 compliance: a deploy **never** writes directly into `current`
— it builds an entirely new `releases/<id>/` directory, and only
switches the `current` symlink once that new release has passed its
smoke test. `shared/.env`, `shared/database/goldbot.db`, `shared/logs`
are never copied or overwritten by any deploy step — every release
only symlinks to them.

### `database/` — package vs. runtime data (do not confuse the two)

This repository has a naming collision that matters here: `database/`
is **both** a Python package (`database_layer/database_manager/database.py`,
`database/*_repository.py` — real application source, imported as
`from database.database import Database`) **and**, per `config.py`'s
`DB_PATH`, the directory the runtime SQLite file (`goldbot.db`) lives
in. A deploy must ship the package (it's application code) while never
overwriting the data file (RULE 4). Concretely:

- `releases/<id>/database/*.py` — real files, `rsync`'d fresh with
  every release, exactly like any other source directory.
- `releases/<id>/database/goldbot.db` — a symlink to
  `shared/database/goldbot.db`, the one persistent copy, reused by
  every release.

`rsync`'s exclude is therefore scoped to `database/*.db`, not
`database` — excluding the whole directory would silently drop the
Python package itself, breaking every `from database...` import in the
release (this was a real bug caught during the first end-to-end VPS
deploy verification; see `docs/PHASE_P1_FREEZE.md`'s Known Limitations
section for the incident).

## One-time VPS setup (manual, before the first deploy)

1. Create the directory skeleton and a dedicated non-root user (e.g.
   `senior`, matching `deploy/systemd/goldbot.service`'s `User=`):
   ```bash
   sudo useradd -r -m -d /opt/goldbot senior   # or your actual deploy user
   sudo mkdir -p /opt/{releases,shared/database,shared/logs,backups}
   sudo chown -R senior:senior /opt/goldbot
   ```
2. Create `/opt/goldbot/shared/.env` **manually**, with real secret
   values, `chmod 600` — see `.env.example` for the variable list.
   `release_deploy.sh` refuses to deploy if this file is missing; it
   never creates or writes it.
3. Install the systemd unit once:
   ```bash
   sudo cp deploy/systemd/goldbot.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable goldbot.service
   ```
   (`goldbot-healthcheck.service`/`.timer` and
   `goldbot-notify-failure@.service` from Phase 58 can be reused
   as-is for periodic health monitoring and crash alerts — adjust
   their `WorkingDirectory=`/`EnvironmentFile=`/`ExecStart=` to the
   `current`/`shared` paths above if you want them to track the
   release-based layout too.)
4. Grant the deploy user passwordless sudo **scoped to systemctl on
   this one unit** — the deploy scripts run `sudo systemctl restart
   goldbot.service`, never a broader command:
   ```
   # /etc/sudoers.d/goldbot-deploy
   senior ALL=(root) NOPASSWD: /usr/bin/systemctl restart goldbot.service, /usr/bin/systemctl is-active goldbot.service
   ```
5. Ensure the deploy user's SSH key (the private half of
   `VPS_SSH_KEY`) is authorized for that user
   (`~senior/.ssh/authorized_keys`).

## GitHub configuration

**Production deploys run against `main`, via either an automatic push to
`main` or a manual `workflow_dispatch` on the `main` ref.** `main` is the
sole production branch; it holds the full production surface
(`platform_layer/telegram/polling.py`, `core/pipeline.py`, `main.py`, `scripts/deploy/`).
To deploy manually: GitHub → Actions → *GoldBot Production Deployment* →
**Run workflow** → branch **`main`** (or API `workflow_dispatch` with
`ref: main`). The first `main` deploy was verified in TASK-DEPLOY-003
(run #39, commit `61bbcb5`, both jobs green).

As of **TASK-CICD-001** (CI/CD migration to `main`),
`.github/workflows/production_deploy.yml`'s `push:` `branches:` filter
names **`main`** — so the automatic and the manual (`workflow_dispatch`)
paths deploy the same branch, with no divergence. The legacy
`claude/code-analysis-optimization-pwfo3q` auto-trigger has been removed;
no workflow deploys or runs from the development branch any longer. The
workflow reads exactly five repository secrets, all pre-configured per the
Phase P1 brief — no plaintext credential appears anywhere in the workflow
file or the deploy scripts:

| Secret | Used for |
|---|---|
| `VPS_HOST` | SSH target hostname/IP |
| `VPS_PORT` | SSH port |
| `VPS_USER` | SSH login user (should match `goldbot.service`'s `User=`) |
| `VPS_SSH_KEY` | Private key, loaded via `webfactory/ssh-agent`, never echoed |
| `DEPLOY_PATH` | The VPS-side base path (`/opt/goldbot` in the examples above) |

## What a deploy actually does, end to end

1. `validate` job: pyflakes, `compileall`, full `pytest tests/` —
   **the deploy job does not run at all if any of these fail.**
2. `deploy` job computes a release id (`date -u
   +%Y%m%d%H%M%S`), `rsync`s the checked-out tree (excluding `.git`,
   `__pycache__`, `database/*.db`, `.env`, `logs`, `venv` — the
   `database` Python package itself ships with every release, see
   above) into `$DEPLOY_PATH/releases/<id>/`, then SSHes in and runs
   `scripts/deploy/release_deploy.sh` — see the Architecture diagram
   above for what that script does on the VPS side.
3. Every decision about which release is "current"/"previous" is
   pure Python (`scripts/deploy/release_manager.py`), independently
   unit-tested (`tests/deploy/test_release_manager.py`) without
   needing a VPS at all.

## Smoke test / health check (TASK 8/9)

Both reuse the same, single script: `scripts/health_check.py` (Phase
58, extended this phase with two more checks — see its own updated
docstring). Never runs `main.py`'s real pipeline or
`platform_layer.telegram.polling`'s real listener — only imports the two entry-point
modules and confirms config/secrets/database are reachable. Exit 0
healthy, exit 1 otherwise.

- **Pre-activation** (TASK 9): run against the *new* release, before
  `current` is switched — a failure here means the release never goes
  live, and the previously-running release keeps serving traffic
  uninterrupted.
- **Post-restart** (TASK 8): run against `current` after
  `goldbot.service` restarts — a failure here triggers the automatic
  rollback described below.

## Rollback (TASK 10)

See `docs/deployment/ROLLBACK.md` for the full procedure — summary:
`scripts/deploy/rollback.sh $DEPLOY_PATH goldbot [release_id]` switches
`current` back (to the immediately-previous release by default, or an
explicit one) and restarts the service. **No rebuild** — the target
release's `venv` is already installed from when it was originally
deployed.

## Known limitations (disclosed, not silently claimed as solved)

- **Never tested against a real VPS.** This sandbox has no `systemd`,
  no real SSH target, and no VPS — every script here is verified by
  `bash -n` syntax checking, pure-Python unit tests
  (`scripts/deploy/release_manager.py`'s logic), and careful manual
  review, not an actual end-to-end deploy. The Director/operator's
  first real deploy is the first true end-to-end verification. This
  mirrors `docs/production_setup.md`'s own disclosed gap for the
  Phase 58 systemd units.
- **No release retention/pruning.** `releases/` grows by one directory
  per deploy, forever — no automatic cleanup exists (RULE 5 requires
  keeping the previous release for rollback; a retention policy that
  prunes anything older than N releases would be a reasonable, small
  follow-up, but is not implemented here to avoid ever deleting a
  release a rollback might still need).
- **`shared/.env` bootstrap is manual by design** — a deploy script
  writing real secret values would mean secrets pass through CI logs
  or the repository checkout; this phase deliberately requires the
  file to already exist on the VPS.
