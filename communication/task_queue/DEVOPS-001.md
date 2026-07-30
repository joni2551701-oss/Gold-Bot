# DEVOPS-001

**Title**: Smart CI Routing
**Track**: Engineering (separate from the Platform Tasks chain — see
`communication/task_queue/QUEUE.md`)
**Status**: ⏳ Blocked — does not start until Navigation Foundation
(TASK-002E + TASK-002F) is fully complete. Not scoped in detail yet;
this document records the Director's brief, not an Analysis-step
output.

## Objective

Split `.github/workflows/ci.yml`'s single full-regression run into
routed pipelines, so a documentation-only commit (observed taking
~2 minutes for the full 4660+-test suite, e.g. `ci.yml` run #160) no
longer pays that cost.

**Documentation Pipeline** — triggered by changes limited to
Markdown/ADR/Constitution/README/Workflow/Task Queue/Decision Log
files. Runs: Markdown validation, link validation, documentation
consistency checks only. No test suite.

**Platform Pipeline** — triggered by changes under `platforms/` or
`tests/platforms/`. Runs: Platform tests, static analysis, unit tests,
Platform validation. Does not run Trading Core tests.

**Trading Pipeline** — triggered by changes under Trading Core
(`context/`, `strategies/`, `decision/`, `risk/`, etc.). Runs: full
Trading regression, strategy/decision/risk tests.

**Full Regression** — triggered by shared infrastructure changes,
dependency updates (`requirements.txt`), workflow changes
(`.github/workflows/`), or a release candidate. Runs everything.

## Mandatory pre-start deliverables (before any workflow file changes)

Per Director instruction — design first, implementation second, no
workflow touched until all of these exist and are reviewed:

1. Current GitHub Actions map — every existing workflow, what triggers
   each one, today.
2. When each proposed pipeline would run (the trigger conditions
   above, stated precisely).
3. Which file/folder path maps to which pipeline — an explicit,
   reviewable table, not a vague description.
4. Expected time savings — measured against real recent run durations
   (e.g. `ci.yml` run #160's ~2 minutes for a docs-only change),
   not guessed.
5. Regression risk — what could slip through if a path-matching rule
   is wrong (e.g. a Trading Core change misclassified as
   documentation-only and skipping the full suite it needs).

## Depends on

TASK-002E (Navigation Tests) and TASK-002F (Navigation Freeze) — both
must be fully complete first. This is a Director-ordered sequencing
decision (Architecture First: the Navigation roadmap is not
interrupted by an unrelated Engineering track), not a technical
dependency between the two tracks.

## Notes

`.github/workflows/ci.yml` is shared CI infrastructure — every future
commit from any role runs through whatever ends up here. No change is
made without the five deliverables above reviewed and approved first.
