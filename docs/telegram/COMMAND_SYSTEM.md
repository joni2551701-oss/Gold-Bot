# GoldBot — Command System

Governed by `docs/constitution/CONSTITUTION.md` Article 2/4. The
dispatch mechanism itself (Router → Permission → Handler → Service →
Repository) already lives in `docs/telegram/TELEGRAM_ARCHITECTURE.md`
(full detail) and `docs/architecture/TELEGRAM_FLOW.md` (summary) — this
document does not repeat it. What it adds: the real command catalog,
`platform_layer/telegram/commands.py`'s three dicts, verified directly against the
file.

## The three command tiers

```
COMMANDS          (17 entries) — any user: start, help, profile,
                   settings, language, risk, strategy, timeframe,
                   signal, history, status, about, plan, subscription,
                   upgrade, notifications, feedback
ADMIN_COMMANDS    (13 entries) — admin, stats, users, userinfo,
                   vipinfo, broadcast, system, feedbacks, plus 5
                   read-only ai_* informational commands, owner
OWNER_COMMANDS    (19 entries) — everything ADMIN_COMMANDS implies
                   plus addadmin/removeadmin, doctor, and the full
                   runtime/* family (runtime, runtime_events,
                   runtime_metrics, runtime_status, runtime_check,
                   runtime_restart, runtime_provider)
```

## Dual-listed commands are not a bug

`platform_layer/telegram/commands.py`'s own docstring states the rule directly: the
five `ai_*` informational commands plus `system`/`broadcast`/`owner`
appear in **both** `OWNER_COMMANDS` and `ADMIN_COMMANDS` because
`command_router._required_level()` checks `ADMIN_COMMANDS` first —
dual membership means "ADMIN or OWNER," not "OWNER only." `doctor` and
the entire `runtime_*` family are OWNER-only by deliberate contrast
(Phase 61.6 TASK 6's own reasoning): they expose internal
lifecycle/event/metrics detail the read-only `ai_*` commands don't.

## Related

- `docs/telegram/TELEGRAM_ARCHITECTURE.md` — the dispatch mechanism.
- `docs/architecture/TELEGRAM_FLOW.md` — the short flow summary.
- `docs/owner/OWNER_PANEL.md` — what each Owner command's handler
  actually does, section by section.
