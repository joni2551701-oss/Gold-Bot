# GoldBot — Rollback Procedure (Phase P1, TASK 10)

Release-based deployment (see `docs/deployment/PRODUCTION_DEPLOYMENT.md`)
keeps every previously-deployed release on disk under
`$DEPLOY_PATH/releases/`, specifically so a rollback never needs to
rebuild anything — it is always just a symlink switch plus a service
restart.

## Automatic rollback

`scripts/deploy/release_deploy.sh` already does this for you on a
failed deploy: if the post-restart health check fails, it calls
`rollback.sh` itself and switches `current` back to whatever release
was live immediately before this deploy. The GitHub Actions run still
ends in failure (so the Director/operator knows something went wrong),
but the live service recovers to the last known-good release
automatically, without anyone needing to SSH in.

## Manual rollback

If you need to roll back for a reason the automated health check
wouldn't catch (a runtime regression only visible under real traffic,
for example), SSH to the VPS and run:

```bash
# Roll back to the release immediately before the current one:
/opt/goldbot/current/scripts/deploy/rollback.sh /opt/goldbot goldbot

# Or roll back to a specific, known-good release id:
/opt/goldbot/current/scripts/deploy/rollback.sh /opt/goldbot goldbot 20260721101500
```

(Substitute `/opt/goldbot` with your actual `DEPLOY_PATH` if
different.)

## What rollback does — and does not — do

**Does:**
1. Determines the target release — either the one you named, or
   whatever `scripts/deploy/release_manager.py previous` resolves to
   (the release immediately before `current` in the sorted release
   list).
2. Atomically switches the `current` symlink to that release
   (`scripts/deploy/release_manager.py activate`).
3. Restarts `goldbot.service`, which now runs the rolled-back
   release's code (`WorkingDirectory=/opt/goldbot/current` never
   changes — only what `current` points at does).
4. Verifies `systemctl is-active goldbot.service` afterward and exits
   non-zero if the restart didn't actually come up healthy.

**Does not (RULE 5 — "No rebuild"):**
- Reinstall dependencies. The target release's `venv/` is exactly
  what it was when that release was originally deployed and passed
  its own smoke test.
- Delete or modify any `releases/<id>/` directory — rollback never
  removes anything, including the release you're rolling back *away*
  from (so you can roll forward again later by re-running a deploy,
  or by calling `rollback.sh ... <that release id>` directly).
- Touch `shared/.env`, `shared/database`, or `shared/logs` — these are
  never release-specific, so a rollback changes nothing about them.

## If there is nothing to roll back to

`rollback.sh` fails loudly (`no previous release available to roll
back to`, exit 1) rather than doing anything destructive when:
- Zero or one release exists under `releases/`.
- `current` already points at the oldest known release (there is
  nothing further back in history to fall back to).

In either case, the fix is a fresh, forward deploy (push to the
production branch, or `workflow_dispatch` the production workflow),
not a rollback.

## Verifying a rollback succeeded

```bash
systemctl status goldbot.service
journalctl -u goldbot.service --since "5 minutes ago"
/opt/goldbot/current/venv/bin/python /opt/goldbot/current/scripts/health_check.py
```

The last command is the same script the deploy pipeline itself uses
(TASK 8) — exit 0 means config/secrets/database/imports are all
healthy on whichever release `current` now points at.
