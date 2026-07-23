# GoldBot — Current Phase

Living pointer to whatever phase is presently open. Updated at the
close of each phase to reflect the phase that just froze and, where
known, what's authorized to start next. `docs/changelog/CHANGELOG.md`
and `docs/changelog/PHASE_HISTORY.md` are the permanent record; this
document is only ever the current tip.

## Phase: Platform Documentation (Senior Platform Engineer role assignment)

**Status: FROZEN.** Type: Documentation-only phase — no source code
change, no refactor, no new architecture, confirmed by
`git diff --cached --stat` showing only `.md` files across every
commit in this phase.

### Scope authorized by the Director

1. Re-point the Worker's designated branch
   (`claude/trading-ai-arch-review-tgszrz`) from the stale `main`
   snapshot onto the production branch
   (`claude/code-analysis-optimization-pwfo3q`).
2. Produce Platform Layer documentation: `docs/PLATFORM_ARCHITECTURE.md`,
   `docs/PLATFORM_MODULE_MAP.md`, `docs/PLATFORM_DEPENDENCY_MAP.md`.
3. Log the known-broken `main`-branch `owner_snapshot.yml` workflow as
   a technical debt entry — no fix applied (Director decision: legacy
   synchronization work, out of scope).
4. On CI success: update `docs/HANDOFF.md`, `docs/changelog/CHANGELOG.md`,
   `docs/CURRENT_PHASE.md` (this document), and freeze this phase's
   documentation.

### Exit criteria (all met)

| Criterion | Result |
|---|---|
| Branch re-pointed to production, zero commits lost | ✅ confirmed (`main..old-branch` diff was empty before the reset) |
| Trading Core zero-diff | ✅ every commit this phase touched only `docs/` |
| Technical debt recorded, not modified | ✅ `docs/TECHNICAL_DEBT.md` |
| Platform documentation created | ✅ `docs/PLATFORM_ARCHITECTURE.md`, `docs/PLATFORM_MODULE_MAP.md`, `docs/PLATFORM_DEPENDENCY_MAP.md` |
| CI confirmation | ✅ `ci.yml` run #148, commit `bdf44a2`, conclusion `success` |
| Changelog updated | ✅ `docs/changelog/CHANGELOG.md`, "Platform Documentation Phase" entry |
| Handoff prepared | ✅ `docs/HANDOFF.md` |

### Role boundary reaffirmed by this phase

Per the Director's role assignment: **Core** (Trading Engine & AI —
`context/`, `strategies/`, `signals/`, `decision/`, `risk/`, `ai/`,
`core/pipeline.py`) and **Platform** (Product Experience & Platform
Foundation — `telegram/`, platform-facing `database/` tables,
`translation/`) now carry separate responsibility. This phase touched
Platform only; Trading Core was read for reference (to confirm the
Platform Layer's own dependency boundaries) but never for modification.

## Next

Platform is ready to receive new implementation tasks (not
documentation) once the Director assigns one. Until a dedicated
Director task says otherwise, Trading Core, Decision Engine, Risk
Manager, and Signal/Context Engine remain off-limits to this role.

## Related

- `docs/HANDOFF.md` — what a future session/agent needs to continue
  Platform work without re-deriving this phase's findings.
- `docs/changelog/CHANGELOG.md` — this phase's permanent changelog
  entry.
- `docs/PLATFORM_ARCHITECTURE.md`, `docs/PLATFORM_MODULE_MAP.md`,
  `docs/PLATFORM_DEPENDENCY_MAP.md` — this phase's deliverables.
- `docs/TECHNICAL_DEBT.md` — the one open item this phase recorded.
