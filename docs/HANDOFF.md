# GoldBot — Handoff

What a future session, agent, or human needs to pick up Platform work
without re-deriving what this phase already established. Written at
the close of the Platform Documentation phase
(see `docs/CURRENT_PHASE.md` for the formal freeze record).

## Branch state

`claude/trading-ai-arch-review-tgszrz` is based on
`claude/code-analysis-optimization-pwfo3q` (the production branch),
plus one documentation-only commit (`bdf44a2`) on top. It is **not**
based on `main` — `main` is a stale, pre-`TradingPipeline` snapshot
(58 commits) that no CI/CD path reads; the real, 216+-commit codebase
lives on `claude/code-analysis-optimization-pwfo3q`
(`docs/PHASE_BRANCH_SYNC_AUDIT.md`). Do not use `main` as an
architectural reference for any future work on this branch.

## Role split in force

- **Core** — Trading Engine & AI (`context/`, `strategies/`,
  `signals/`, `decision/`, `risk/`, `ai/`, `core/pipeline.py`). Frozen
  for the Platform role; changes require a dedicated Director task.
- **Platform** (this role) — Product Experience & Platform Foundation
  (`telegram/`, the four platform-facing `database/` tables — `users`,
  `subscriptions`, `feedback`, `admins` — and `translation/`).

## Where to start reading

1. `docs/CURRENT_PHASE.md` — what just closed, what's authorized next.
2. `docs/PLATFORM_ARCHITECTURE.md` — dispatch flow, permission model,
   subscription behavior, navigation system, localization, dashboard,
   the pipeline/Platform process boundary, reserved future modules.
3. `docs/PLATFORM_MODULE_MAP.md` — file-by-file responsibility for
   every `telegram/` and `telegram/owner/` file, the platform database
   tables, and `translation/`.
4. `docs/PLATFORM_DEPENDENCY_MAP.md` — exactly what the Platform Layer
   may and must never import, and why.
5. `docs/TECHNICAL_DEBT.md` — one open, deliberately-unfixed item
   (`main`'s broken `owner_snapshot.yml`).

These four are new; they sit alongside (and cross-reference, not
duplicate) the pre-existing `docs/telegram_layer.md`,
`docs/telegram/TELEGRAM_ARCHITECTURE.md`, `docs/commands_reference.md`,
and `docs/owner/OWNER_PANEL.md`, which remain the authoritative
low-level references.

## What is true about the Platform Layer today (short version)

- Reply Keyboard is the sole navigation mechanism (six sections: Main,
  Settings, Admin, Owner, Profile, Signals); inline keyboards are used
  only for real value choices (Language, Settings pickers), never
  screen navigation. Reply Menu layout is **frozen** — a future module
  gets a reserved slot / "Coming Soon" placeholder, never a menu
  redesign, per Director decision recorded in `docs/PHASE6_FREEZE.md`.
- Subscription platform (`FREE`/`PREMIUM`/`VIP`) has no billing wired
  — `/upgrade` is a static "coming soon" reply, `expires_at` is unused.
- No dedicated `telegram/owner/subscription_commands.py`,
  `risk_commands.py`, or `backup_commands.py` exists yet — those
  concerns live in adjacent files today; this is an honest, documented
  gap (`docs/owner/OWNER_PANEL.md`), not something to fix without a
  task naming it.
- The scheduled pipeline's own Telegram broadcast bypasses the
  Platform Layer's per-user access model entirely (fixed
  `TELEGRAM_CHAT_ID`, no `NotificationService`/`SignalAccessService`
  consulted) — a deliberate scope boundary, not a bug to close as
  Platform work.
- A large set of Reply-Keyboard-reserved modules (Chart, AI Assistant,
  Economic Calendar, News, Academy, Portfolio, Trade Journal, Market
  Scanner, Community, Marketplace) have real backend foundations
  elsewhere in the codebase but zero Telegram entry point — expected
  state per this codebase's "Foundation first, Integration later"
  phased model, not a regression.

## Open items

- `docs/TECHNICAL_DEBT.md`'s one entry: `main`'s `owner_snapshot.yml`
  references code deleted from production
  (`monitoring/run_snapshot.py`). No action authorized; do not fix
  without a dedicated Director task naming it.
- No merge of `main` ↔ production branch is planned before
  Constitution v2 / the documentation-system work referenced in the
  Director's roadmap concludes — that is an organizational decision,
  not an implementation task.

## Verification trail for this phase

- Commit `bdf44a2` — the four Platform docs + technical debt entry.
- `ci.yml` run #148 — `success`.
- `git diff --cached --stat` at commit time showed only `.md` files;
  no file under `core/`, `decision/`, `risk/`, `execution/`,
  `strategies/`, `signals/`, `context/`, `ai/`, or `database/` schema
  files was modified.

## Related

- `docs/CURRENT_PHASE.md` — this phase's formal freeze record and exit
  criteria.
- `docs/changelog/CHANGELOG.md` — permanent changelog entry for this
  phase.
