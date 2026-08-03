# GoldBot — Branch Synchronization & Telegram Live Runtime Verification — Audit

Governed by `docs/constitution/CONSTITUTION.md`. This is a direct
follow-on to the GitHub Secrets / Environment Configuration Audit and
the GoldBot Core Telegram Runtime Activation Alpha phase — both
confirmed the Telegram runtime code itself is correct; this audit
answers a different question the Director raised: **is the tested
code actually what runs in the real environment?**

## TASK 0 — Repository State Audit

| Branch | Latest commit | Date | Total commits | Status |
|---|---|---|---|---|
| `main` | `7af7ddc` | 2026-07-12 | 54 | Stale — pre-dates this session's current architecture |
| `claude/code-analysis-optimization-pwfo3q` | `a323d18` | 2026-07-20 | 183 | Active — every phase in `docs/roadmap/VERSIONS.md` lives here |

`origin/main...origin/claude/code-analysis-optimization-pwfo3q`:
**4 commits unique to `main`, 133 commits unique to `claude`.**

**Which branch is production?** `.github/workflows/trading_bot.yml`
already pins `ref: claude/code-analysis-optimization-pwfo3q` explicitly,
with its own comment: *"GoldBot v0.1 stable ... currently lives on
this branch, not on the default branch -- pin explicitly so scheduled
runs execute the real pipeline instead of the old skeleton main.py."*
This was a deliberate decision made in an earlier phase, not an
oversight discovered here — but it had never been written down outside
that one workflow-file comment, which is why the Director's concern
("hozir GoldBot eski main.py'ni ishlatib qolganmi?") was a reasonable
thing to re-verify rather than assume.

**Answer: `claude/code-analysis-optimization-pwfo3q` is already the
de facto production branch.** GitHub Actions checks it out explicitly
for the scheduled pipeline; `main` is not read by any CI/CD path.

## TASK 1 — Diff Audit

The 4 commits unique to `main` are trivial filename-casing fixes
(`liquidity_strategy.py`, `strategy_manager.py`, `ai_analyzer.py`
renames) — no functional content, safe to disregard for this audit's
purpose.

The 133 commits unique to `claude` are not an incremental diff on top
of a compatible base — `main` is a structurally different snapshot:

| Area | `main` | `claude` (this branch) |
|---|---|---|
| `main.py` | Imports `DecisionEngine`/`RiskManager`/`ExecutionEngine` directly; own docstring calls Data/Context/Signal/AI layers "TODO" | Imports `core.pipeline.TradingPipeline` (the current, real orchestrator) |
| `telegram/polling.py` | **Does not exist** | The Telegram Runtime Activation Alpha's own entry point |
| `telegram/owner/` | **Does not exist** | 22 files (Owner Telegram Panel) |
| `monitoring/` | 3 files (`__init__.py`, `performance.py`, `signal_monitor.py`) | 8+ files (`models.py`, `system_monitor.py`, `market_monitor.py`, `decision_logger.py`, `error_monitor.py`, extended `signal_monitor.py`, ...) |
| `configuration/`, `database/` | Early/partial | Full feature-registry, runtime-feature, monitoring-repository layers |

`core/` itself is not exempt from this divergence — `main`'s `core/`
predates `core/pipeline.py`, `core_layer/emergency/`, `core/guards/`,
`core/secrets.py`'s current shape, and more. There is no way to bring
just the three named Telegram Runtime commits (`71f4073`, `ee0799b`,
`a323d18`) onto `main` without first bringing over the ~130 commits
they structurally depend on — a cherry-pick of just those three would
fail immediately (missing files) or, if forced through conflict
resolution, produce a `main` with the new Telegram files bolted onto
an incompatible, pre-`TradingPipeline` core.

## Decision (Director, this session)

Presented three options; Director selected: **formalize
`claude/code-analysis-optimization-pwfo3q` as the production branch,
do not touch `main`.** Rationale: this matches what `trading_bot.yml`
already does in practice, carries zero risk (no branch state changes),
and a full `main` sync (133 commits landing on a shared branch at
once) would be a large, separately-scoped migration decision with its
own risk profile — not something to fold into a routine
verification task.

This audit documents that decision. `README.md` and
`docs/DEPLOYMENT.md` are updated (this phase) to state the production
branch explicitly, closing the gap that let this question arise in
the first place.

## TASK 3 — Telegram Runtime Entry Point Audit

Confirmed (already documented in
`docs/PHASE_TELEGRAM_RUNTIME_AUDIT.md`, re-verified here): the only
entry point is `python -m telegram.polling`, consistent across
`deploy/systemd/goldbot-polling.service`, `docker-compose.yml`,
`Dockerfile`'s own comment, and `docs/DEPLOYMENT.md`. **Not**
`main.py`, **not** a GitHub Actions workflow (no workflow runs
`telegram.polling` — `trading_bot.yml` only runs `main.py` on a
schedule; `ci.yml` only runs tests), **not** currently deployed to any
VPS/container (no VPS exists yet, per every prior phase's own
documented scope).

## TASK 4 — main.py Audit

`main.py` (on `claude/code-analysis-optimization-pwfo3q`, the branch
that matters): `grep -n "telegram" main.py` shows exactly one match —
a log-message string ("N telegram message(s)") — and zero import of
`telegram.polling`. `main.py` never starts the inbound bot listener
and never imports it; the only Telegram touchpoint is outbound
delivery via `telegram.notifier.Notifier` → `telegram.bot.TelegramBot`
(a separate `Bot` instance from `telegram.polling`'s, confirmed in
that module's own docstring). No mixing between the one-shot pipeline
and the long-running listener — matches
`docs/ARCHITECTURE.md`'s System Overview exactly. Already documented;
no doc gap found requiring a new note here.

## TASK 5 — Local Telegram Simulation

Re-run for this audit (`route_message()` with a synthetic `/start`
update, no real network):

```
Telegram update -> polling.py's dispatcher -> command_router.route_message()
    -> handlers.start_handler() -> UserService.register_user()
    -> 'Profile created.'
```

Confirmed working end-to-end on `claude/code-analysis-optimization-pwfo3q`.

## TASK 6 — Owner Startup Notification

Already built and tested in the prior Telegram Runtime Activation
Alpha phase (commit `a323d18`): `telegram/polling.py`'s
`_notify_owner_startup()` sends the "🟢 GoldBot Online" message to
`TELEGRAM_OWNER_ID` once polling starts, format documented in
`docs/TELEGRAM_RUNTIME.md`. No change needed this phase — re-verified
via the existing `tests/telegram/test_polling.py` suite (31 tests
covering this exact function).

## TASK 7 — GitHub Actions

`a323d18` (the commit containing all of TASK 2/4/5/6's runtime code)
already returned `conclusion: success` on run `29758281781`, confirmed
in the prior phase's Final Report. This audit's own doc-only changes
(TASK 1/1-formalization below) get their own fresh CI run as part of
this phase's Commit Protocol.

## Conclusion

No code defect was found anywhere in the Telegram runtime — every
prior audit's findings hold. The actual gap was informational: which
branch is "real" was never written down outside one workflow-file
comment. This phase closes that gap via documentation only; `main`
remains untouched, `core/`/`decision/`/`risk/`/`execution/`/
`strategies/`/`signals/` remain untouched (this phase adds no code,
only docs).
