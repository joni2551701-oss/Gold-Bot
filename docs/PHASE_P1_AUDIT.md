# Phase P1 Audit — Production Deployment Pipeline Foundation

Worker Brief: "Production Deployment Pipeline Foundation" (Phase P1,
Version V1.0 Production, Priority CRITICAL, Director Approved). TASK 0
foundation audit: what already exists, what Phase P1 must not
duplicate, and one branch-trigger decision this document records and
flags for the Director.

## 1. `.github/workflows/`

Three existing workflows, none of them a production/CD deploy
pipeline:

| File | Purpose |
|---|---|
| `ci.yml` | Validation-only: compile/lint/test on every push/PR. Never touches production. |
| `trading_bot.yml` | Scheduled (`*/5 3-18 * * 1-5`) one-shot `python main.py` run, pinned to `ref: claude/code-analysis-optimization-pwfo3q`. This **is** GoldBot's production trading-pipeline runtime today — it runs on GitHub Actions itself, not on a VPS. |
| `owner_snapshot.yml` | Scheduled (15 min) one-shot owner status snapshot, same pinned branch. |

No existing workflow builds, SSHes to, or deploys anything to a VPS.
Phase P1's `production_deploy.yml` (TASK 1/2) is new, not a duplicate.

**Branch decision (flagged for the Director):** the brief's TASK 1
literally names `main` as the trigger branch. `docs/DEPLOYMENT.md` and
`docs/PHASE_BRANCH_SYNC_AUDIT.md` (both already Director-reviewed, in
force since the Branch Sync Brief) establish that
`claude/code-analysis-optimization-pwfo3q` — not `main` — is GoldBot's
actual production branch; `main` is a stale, pre-`TradingPipeline`
snapshot with no `platform_layer/telegram/polling.py`, never read by any existing
CI/CD job. `trading_bot.yml` and `owner_snapshot.yml` both pin the same
branch for exactly this reason. Deploying literal `main` today would
ship the stale skeleton to the VPS. This audit adopts
`claude/code-analysis-optimization-pwfo3q` as `production_deploy.yml`'s
trigger branch, matching every other production-facing workflow in
this repository, and documents the decision here and in
`docs/deployment/PRODUCTION_DEPLOYMENT.md` for visibility. If the
Director's intent was literally `main`, that requires a separate,
explicitly-scoped branch-sync phase first (133+ commits of drift) —
out of scope for a deployment-pipeline phase per RULE 2 ("No business
logic. Deploy only.").

## 2. `scripts/`

| File | Purpose | Reused by Phase P1? |
|---|---|---|
| `scripts/health_check.py` | Config loads, 3 required secrets present, database reachable (`SELECT 1`). Exit 0/1. Standalone, no side effects beyond checks. | **Yes** — extended additively (TASK 8/9) with two new checks (`main` importable, `platform_layer.telegram.polling` importable), reused both as the pre-activation smoke test and the post-restart health check. No duplicate script created. |
| `scripts/notify_failure.sh` | systemd `OnFailure=` alert to `TELEGRAM_OWNER_ID` via `curl`, independent of the Python app. | Reused unmodified — `deploy/systemd/goldbot.service` (TASK 6) wires the same `OnFailure=goldbot-notify-failure@%n.service` pattern the existing units already use. |

No `scripts/deploy/` directory exists yet — new in this phase (TASK
3/4/5/10), holding the release-selection/rollback logic. Placed as a
subdirectory of the existing `scripts/` package rather than a new
top-level directory (Module Reuse Principle).

## 3. `deployment/`

Does not exist. Not created — the brief's own target layout
(`/opt/{releases,shared,current,backups}`) is a **VPS-side**
filesystem layout, not a repository directory; nothing repository-side
needs a `deployment/` folder. `deploy/` (see below) already serves the
"deployment artifacts live here" role this repository uses.

## 4. `deploy/systemd/`

Six existing units, all built for a direct (non-release-based) install
at `/opt/goldbot` (Phase 58, `docs/production_setup.md`):

| File | Type | Targets |
|---|---|---|
| `goldbot-polling.service` | `simple`, `Restart=always` | Long-running `platform_layer/telegram/polling.py` — `WorkingDirectory=/opt/goldbot`, `ExecStart=/opt/venv/bin/python -m telegram.polling`. |
| `goldbot-pipeline.service` + `.timer` | `oneshot` + timer | `main.py` every 5 min — an *alternative* to `trading_bot.yml`, not meant to run alongside it. |
| `goldbot-healthcheck.service` + `.timer` | `oneshot` + timer | Runs `scripts/health_check.py` every 10 min. |
| `goldbot-notify-failure@.service` | `oneshot`, templated | `OnFailure=` target for the three units above; sends a Telegram alert naming the failed unit. |

None of these point at a `releases/<id>` + `current` symlink layout —
they hardcode `/opt/goldbot` directly, which RULE 3's release-based
layout cannot reuse without breaking the existing manual-install
documentation. Per Module Reuse Principle step 2 ("can an existing
module be extended without breaking its current contract?") — no:
retargeting these units' `WorkingDirectory`/`ExecStart` to
`/opt/goldbot/current` would silently change behavior for anyone who
followed `docs/production_setup.md`'s existing manual-install
instructions. Per step 3, a new, distinctly-named unit is justified:
`deploy/systemd/goldbot.service` (TASK 6) — same process
(`platform_layer/telegram/polling.py`, the long-running production process; the
trading pipeline continues to run via `trading_bot.yml` on GitHub
Actions, unaffected and not duplicated here), same `Restart=always` +
`OnFailure=` pattern as `goldbot-polling.service`, but pointed at
`/opt/goldbot/current` (the release-based, CI/CD-managed path) instead
of `/opt/goldbot` directly, and running as a named non-root user per
the brief (`senior`) instead of the existing units' implicit
"whatever user you configured" posture. The existing four
`goldbot-*.service`/`.timer` files are untouched — they remain valid
for anyone using the older manual-install path documented in
`docs/production_setup.md`; `goldbot-healthcheck.service`/`.timer` and
`goldbot-notify-failure@.service` are referenced (not copied) by the
new release-based flow's documentation, since both are install-path
agnostic once `EnvironmentFile=`/`ExecStart=` are adjusted at install
time — covered in `docs/deployment/PRODUCTION_DEPLOYMENT.md`.

## 5. `README` / `docs`

- `docs/DEPLOYMENT.md` (Phase 56) — general install/configure/run/
  backup guide, confirms the production branch (see Section 1).
- `docs/production_setup.md` (Phase 58) — VPS-specific process
  supervision, `.env.production` template, monitoring foundation.
  Explicitly scoped to the direct-install layout; Phase P1 does not
  edit this file (it stays correct for that install path) — it adds a
  new, distinctly-scoped `docs/deployment/PRODUCTION_DEPLOYMENT.md`
  for the release-based, GitHub-Actions-driven path instead of
  conflating the two.
- `Dockerfile` / `docker-compose.yml` (Phase 56) — an alternative,
  still build-untested path per `docs/production_setup.md`'s own
  disclosure. Out of scope for Phase P1 (RULE 2: deploy only, no new
  containerization work); untouched.
- No prior `docs/deployment/` directory exists — new in this phase.

## 6. Environment / secrets

- `core/secrets.py` reads plain `os.environ` (confirmed: no
  `python-dotenv`/`load_dotenv` call anywhere in the codebase) — a
  systemd `EnvironmentFile=` pointed at the real, VPS-side
  `shared/.env` is sufficient; the application needs no code change to
  pick up environment variables from that file once systemd loads it
  into the unit's process environment. `requirements.txt` itself lists
  only `aiogram`/`requests` — no `python-dotenv` dependency to justify
  adding one.
- `platform_layer/telegram/polling.py` confirmed import-safe: all top-level names are
  `def`/`async def` behind `if __name__ == "__main__":` (line 236) —
  `import telegram.polling` never starts polling, executes no network
  call, and is safe to use as a smoke-test import check.

## 7. Conclusion

Nothing in Phase P1's scope duplicates existing tooling. New surface
area: `.github/workflows/production_deploy.yml`,
`scripts/deploy/release_manager.py` (pure release-selection logic,
testable without a VPS), `scripts/deploy/release_deploy.sh`,
`scripts/deploy/rollback.sh`, `deploy/systemd/goldbot.service`,
`docs/deployment/PRODUCTION_DEPLOYMENT.md`,
`docs/deployment/ROLLBACK.md`. Extended, not duplicated:
`scripts/health_check.py` (two new checks). Untouched:
`docs/production_setup.md`, the four existing `deploy/systemd/
goldbot-*` units, `Dockerfile`/`docker-compose.yml`,
`trading_bot.yml`, `owner_snapshot.yml`, `ci.yml`.
