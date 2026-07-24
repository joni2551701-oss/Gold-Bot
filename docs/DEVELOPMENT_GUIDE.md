# GoldBot Development Guide (Phase A14)

Part of GoldBot's Documentation Architecture Foundation (Phase A14).
This document states the workflow every future worker or AI agent
follows when changing GoldBot — it formalizes, in one place, the
process this codebase's own Phase A1 through A13 already followed
every time. `CLAUDE.md` is the enforced, checked-in version of the
same rules; this document explains the workflow behind them for a
human or agent reading the docs, not the repository's own governance
file.

## Code change workflow

Every new piece of work follows the same six steps, in order:

```
1. Check architecture
        |
        v
2. Study the existing module
        |
        v
3. Write tests
        |
        v
4. Make the minimal change
        |
        v
5. Run regression tests
        |
        v
6. Update documentation
```

1. **Check architecture** — read `docs/ARCHITECTURE_RULES.md` (module
   boundaries), `docs/DECISION_PRINCIPLES.md` (decision ownership),
   and `docs/ARCHITECTURE.md`'s relevant phase section before touching
   any file. If the change would require crossing a boundary
   `docs/ARCHITECTURE_RULES.md` forbids, stop and reconsider the
   design rather than adding the import.
2. **Study the existing module** — read the target module's
   `README.md`, its existing tests, and what already imports it before
   writing a line of code. A quick `grep` of who calls a function is
   cheaper than a regression discovered later (`CLAUDE.md`'s "Before
   Code Changes" section states this as an enforced rule, not a
   suggestion).
3. **Write tests** — for new behavior, before or alongside the
   implementation, following the existing test directory's convention
   (`tests/<module>/test_<file>.py`, real objects, no mocking, matching
   every Phase A test file's own pattern).
4. **Make the minimal change** — implement only what the task asks.
   See "Forbidden" below.
5. **Run regression tests** — the full validation sequence:
   `python -m compileall .`, `python -m pyflakes $(git ls-files
   '*.py')`, `python -m pytest tests/` (with `--cov` on the touched
   module), a full module import sweep, and a `python main.py` smoke
   test where the change touches the pipeline. All must pass before
   a commit — not "mostly pass."
6. **Update documentation** — every module's own `docs/*.md` (see
   `docs/DOCUMENTATION_STANDARD.md`) and, if the change is
   architecturally visible, `docs/ARCHITECTURE.md`'s Data Flow diagram
   and Module Responsibilities table.

## Rule for adding a new module

Before creating any new file or package, answer these questions in
order — each gates the next:

```
Is it actually needed?
        |
        v
Does it fit the existing architecture?
        |
        v
Does an existing solution already do this?
        |
        v
Implement
```

- **Is it actually needed?** — tied to an explicit task, not a
  hypothetical future requirement (`CLAUDE.md`: "Don't design for
  hypothetical future requirements").
- **Does it fit the existing architecture?** — check
  `docs/ARCHITECTURE_RULES.md`'s module boundaries and
  `docs/ARCHITECTURE.md`'s Dependency Rules before picking where new
  code lives. Phase A10's Feature Engineering module was repositioned
  mid-roadmap specifically because its first placement (before
  Strategy) didn't fit this question's answer — see
  `docs/FEATURE_ENGINEERING.md`'s pipeline-position note for the full
  story.
- **Does an existing solution already do this?** — audit before
  writing. Every Phase A module (A10 through A13) began with an
  explicit repo-wide search for existing constants/patterns before any
  code was written (see each phase's own doc's "Pre-implementation
  audit" section, e.g. `docs/ASSET_INTELLIGENCE.md`,
  `docs/CONFIGURATION_MANAGEMENT.md`) — this is "reuse first, duplicate
  never," not "duplicate now, deduplicate later."
- **Implement** — only after the three questions above are answered,
  and only the minimal shape the task actually asks for.

## Forbidden

A worker does not, without the user's explicit, separate approval for
that specific change:

- ❌ **A large refactor.** A bug fix doesn't need surrounding cleanup;
  a foundation phase doesn't need a big migration (`CLAUDE.md`
  Restrictions).
- ❌ **An unnecessary dependency.** A new package/library, or a new
  cross-layer import that `docs/ARCHITECTURE_RULES.md` doesn't already
  allow.
- ❌ **A new framework.** Adopting a new testing framework, ORM,
  web framework, etc. outside what this codebase already uses.
- ❌ **Breaking the existing structure.** Existing public method
  signatures (`RiskManager.evaluate()`, `TradingPipeline.run()`,
  `UserRepository.get_user()`, etc.) stay stable unless a task
  explicitly asks for a signature change (`CLAUDE.md` Restrictions).

Trading-critical files (`strategies/`, `signals/`, `risk/risk_manager.py`,
`decision/decision_engine.py`, `execution/`) additionally require
explicit approval for *any* change, not just a large one — see
`CLAUDE.md`'s Trading Safety section.

## Reporting

Every completed change ends with an explicit report, not just "done":
what changed, what was reused vs. newly built (and why), test/coverage
numbers, and an explicit list of what was *not* touched — the same
format every Phase A closing report in this repository's commit
history already follows.
