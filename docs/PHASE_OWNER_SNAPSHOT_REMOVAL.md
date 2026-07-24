# V2 Phase 2 — GitHub Owner Snapshot Removal

Companion record to `docs/PHASE_OWNER_SNAPSHOT_AUDIT.md`/
`docs/PHASE_OWNER_SNAPSHOT_V1_1_AUDIT.md` (the feature's own build
history — both docs are themselves deleted by this phase; this file
is the removal-side record). Superseded by
`docs/PHASE_V2_PHASE1_FREEZE.md`'s Phase 2 Checklist entry.

## Scope

Removed the GitHub Owner Snapshot Reporter (`*/15 * * * *` cron ->
`python -m monitoring.run_snapshot` -> Telegram message to the Owner),
built as a temporary substitute for `telegram.polling`'s own live
heartbeat until that runtime was deployed 24/7 — it now is (see
`docs/TELEGRAM_RUNTIME.md`), so the Alpha layer is redundant.

**Branch scope, as corrected by the Director:** this removal covers
`claude/code-analysis-optimization-pwfo3q` (feature/production branch)
only. `.github/workflows/owner_snapshot.yml` also exists on `main` —
that copy is what actually keeps the `*/15 * * * *` schedule trigger
firing (GitHub Actions `on: schedule` reads from the default branch),
since the workflow's own `checkout` step pins
`ref: claude/code-analysis-optimization-pwfo3q` for the code but the
YAML file itself must live on `main` to be scheduled at all. **The
`main` copy is untouched by this phase** — it updates automatically
once this branch is merged, per the Director's explicit instruction
not to switch branches or edit `main` directly.

## Files Deleted (17)

```
.github/workflows/owner_snapshot.yml
monitoring/snapshot_models.py
monitoring/snapshot_collector.py
monitoring/run_snapshot.py
telegram/owner/snapshot_formatter.py
telegram/owner/snapshot_sender.py
tests/monitoring/test_snapshot_models.py
tests/monitoring/test_snapshot_collector.py
tests/monitoring/test_run_snapshot.py
tests/telegram/owner/test_snapshot_formatter.py
tests/telegram/owner/test_snapshot_sender.py
tests/workflows/test_owner_snapshot_workflow.py
docs/OWNER_SNAPSHOT_REPORTER.md
docs/PHASE_OWNER_SNAPSHOT_AUDIT.md
docs/PHASE_OWNER_SNAPSHOT_FREEZE.md
docs/PHASE_OWNER_SNAPSHOT_V1_1_AUDIT.md
docs/PHASE_OWNER_SNAPSHOT_V1_1_FREEZE.md
```

## Files Edited (section removal, not deletion)

- `docs/architecture/MONITORING.md` — removed the "Owner Snapshot
  Reporter (GitHub Actions Alpha, v1.1)" section.
- `docs/DEPLOYMENT.md` — removed the "Owner Snapshot Reporter (no VPS
  needed)" section.
- `tests/deploy/test_production_deploy_workflow.py` — its docstring
  cited `tests/workflows/test_owner_snapshot_workflow.py` as a
  PyYAML-avoidance naming precedent; that file no longer exists, so
  the reference was removed from the docstring (no test logic
  changed).
- `docs/PHASE_V2_PHASE1_FREEZE.md` — Phase 2 Checklist item marked
  done, cross-referenced to this file.

## Pre-Delete Checks (Director's additional requirements)

**1. GitHub Secrets.** `owner_snapshot.yml` referenced exactly four
secrets: `TELEGRAM_BOT_TOKEN`, `TELEGRAM_OWNER_ID`,
`TWELVE_DATA_API_KEY`, `GEMINI_API_KEY`. None of the Director's named
patterns (`OWNER_SNAPSHOT_TOKEN`, `OWNER_CHAT_ID`, `OWNER_REPORT_CHAT`,
`SNAPSHOT_*`) exist anywhere in the repository. All four actual
secrets are shared with `trading_bot.yml` and/or core modules
(`core/secrets.py`, `telegram/permissions.py`, `telegram/polling.py`,
`telegram/owner/runtime_notifications.py`) — **none are
snapshot-exclusive.** No secret is deprecated or removed; none needed
to be.

**2. CI/CD.** No README badge referenced the workflow. No other
workflow file referenced `owner_snapshot.yml`. `workflow_dispatch` is
used by three other workflows too (not a snapshot-specific pattern) —
nothing to clean up here beyond the workflow file itself.

**3. Documentation (dead links/navigation/TOC).** No docs index or
TOC file linked to the 5 deleted docs. `docs/DEPLOYMENT.md` and
`docs/architecture/MONITORING.md` had live links to
`docs/OWNER_SNAPSHOT_REPORTER.md` etc. inside the sections that were
removed (handled above). `docs/PHASE_V1_FREEZE.md` and
`docs/PHASE_V1_AUDIT.md` cite `docs/PHASE_OWNER_SNAPSHOT_V1_1_AUDIT.md`
by name as a historical fact ("this gap was already disclosed in
[doc]") — these are **narrative citations of a past audit finding,
not navigation**, and were left untouched per this repo's established
convention (`docs/PHASE_P1_FREEZE.md` etc. from the Phase 2 audit)
that historical documents are never rewritten to match a later state.
Flagged explicitly for the Director below.

**4. Post-delete grep.** `grep -rl "owner_snapshot\|snapshot_formatter\|
snapshot_sender\|run_snapshot\|OwnerSnapshot"` returns **4 files**, not
0 — all narrative/historical, not functional:
`docs/V1_READINESS.md`, `docs/PHASE_P1_AUDIT.md`,
`docs/PHASE_P1_FREEZE.md`, `docs/PHASE_V1_AUDIT.md`. See the flag
below. `market_snapshot` (8 files), `config_snapshot` (6 files), and
`context_snapshot` (25 files) remain fully intact — unrelated
features, unaffected.

**5. Regression.** `pyflakes`/`compileall`/`pytest`/`python main.py`
results recorded in the Commit Protocol section of the Director report
that follows this document.

## Flag for the Director — grep 0-result requirement vs. historical preservation

The Director's Stage-4 instruction specified 0 grep results for these
terms after deletion. Four historical docs (`PHASE_P1_FREEZE.md`,
`PHASE_P1_AUDIT.md`, `V1_READINESS.md`, `PHASE_V1_AUDIT.md`) still
contain one narrative mention each, naming
`docs/PHASE_OWNER_SNAPSHOT_V1_1_AUDIT.md` as a fact about what was
true at that point in the project's history. This repo's own
established convention — confirmed by the Director during the Phase 2
audit itself — is that such documents are not rewritten after the
fact, since doing so would falsify the historical record. This
document's author judged the historical-preservation convention to
take precedence over the literal 0-result instruction and left those
four files untouched. If the Director wants those four citations
removed anyway, say so explicitly and it will be done as a follow-up
edit.
