# GoldBot V1.0 — Production Readiness Checklist

Distilled from `docs/PHASE_V1_AUDIT.md`'s TASK 12 (Production
Readiness Audit) and related findings, for the Director's VPS
deployment go/no-go decision. GoldBot is a semi-automatic signal bot
(Telegram delivery only — no live order execution exists), which
significantly narrows what "production-ready" needs to mean for V1.

## Ready today

| Item | Status | Evidence |
|---|---|---|
| Single production entry point (`main.py`) | Ready | `docs/PHASE_V1_AUDIT.md` TASK 0 |
| Secrets never hardcoded, env-only via `core/secrets.py` | Ready | TASK 8 |
| Production `DEBUG=False` default | Ready | TASK 8 |
| No inbound ports / firewall needed (Telegram long-polling) | Ready | TASK 12 |
| systemd units for polling + pipeline + healthcheck + failure alert | Ready | `deploy/systemd/*` |
| Auto-restart on crash (`Restart=always`, `RestartSec=5`) | Ready | `deploy/systemd/goldbot-polling.service` |
| CI (pyflakes/compileall/pytest/smoke) runs on every push to this branch | Ready | `.github/workflows/ci.yml` |
| Scheduled pipeline + Owner Snapshot Reporter cron workflows | Ready | `.github/workflows/trading_bot.yml`, `owner_snapshot.yml` |
| DB self-heals on missing file (fresh `CREATE TABLE IF NOT EXISTS`) | Ready | TASK 7 |
| Documented Ubuntu/VPS setup procedure | Ready | `docs/production_setup.md` |

## Gaps (documented, not blocking a manually-operated launch)

| Item | Gap | Recommendation |
|---|---|---|
| Database backup | No automated retention/rotation — manual `cp`/`sqlite3 .backup` only | Add a cron-based backup script before extended unattended operation |
| Database corruption recovery | A corrupted (not missing) DB file crashes the process | Add a `PRAGMA integrity_check` + recreate-on-corruption path in a future phase |
| Dockerfile | No `USER` directive — container runs as root | Add non-root `USER` if the Docker path is promoted from secondary to primary |
| Docker Compose path | Never build-tested end-to-end in this project's history (self-disclosed) | Verify before relying on Docker as the primary deployment path |
| CD to VPS | No automated deploy workflow — deployment is a manual, documented procedure | Acceptable for a closed-beta launch; automate later if cadence increases |
| Architecture docs | `MODULE_DEPENDENCIES.md` is stale relative to current `ai/` subpackage count; `monitoring<->telegram` and `analytics<->learning` bidirectional dependencies undocumented | Documentation-sync follow-up, no code change needed |

## Not applicable at V1 (no live execution exists)

Order reject/timeout/reconnect/duplicate-order/restart-recovery for a
*real broker* are not applicable — `execution/` is confirmed
simulator-only, with no MT5/broker integration anywhere in the
codebase. This is by design (CLAUDE.md: "wiring it up is itself a
change requiring explicit approval, not a routine addition") and is
correctly, honestly labeled throughout the code (no function claims to
place a real order while silently no-op'ing).

## Recommendation

**Ready for a manually-operated VPS deployment / closed beta**, with
the gaps above tracked as Known Issues (see `docs/PHASE_V1_FREEZE.md`)
rather than launch blockers. The one item worth prioritizing before
extended unattended operation is database backup automation — the
current manual-only backup story is the single item most likely to
cause real data loss if neglected.
