# Development Policy

**Documentation First.** No code is written until the documents above
it agree.

```
Constitution
    ↓
Architecture
    ↓
Roadmap
    ↓
Policy
    ↓
Audit
    ↓
Code
```

## What each step means in practice

**Constitution** — read `docs/constitution/CONSTITUTION.md` before the
task brief that brought you here (its own mandatory reading order). If
the brief conflicts with an Article, stop (`docs/policies/DIRECTOR_POLICY.md`'s
conflict-handling section).

**Architecture** — read `docs/architecture/ARCHITECTURE_MASTER.md` and
the relevant layer's own doc (`docs/ai/AI_ARCHITECTURE.md`,
`docs/telegram/TELEGRAM_ARCHITECTURE.md`, the module's own `README.md`)
before changing that layer.

**Roadmap** — check `docs/roadmap/VERSIONS.md` and
`docs/roadmap/AI_EVOLUTION.md` to confirm the work belongs at this
point in the sequence, not a future phase pulled forward.

**Policy** — this document and its siblings under `docs/policies/`
govern *how* work proceeds (testing, security, release, foundation
stability) independent of *what* is being built.

**Audit** — every executable brief's `TASK 0` is a Foundation Reuse
Audit (Article 11) against the real, current code — never an
assumption about what "probably" exists.

**Code** — only after the five steps above agree does implementation
start, and even then scoped to the brief's genuine gaps (Article 7),
never a rebuild of what audit found already real.

## Minimalism

`CLAUDE.md`'s own restriction stands unmodified by this policy: no
unnecessary refactor, no duplicate logic, no speculative abstraction.
A bug fix does not need surrounding cleanup. A foundation phase does
not need a big migration. If a change looks like it is growing past
"minimal," the Worker stops and reports instead of pushing through.

## Related

- `docs/constitution/CONSTITUTION.md` Article 8 — Change Management
  Law.
- `docs/policies/FOUNDATION_POLICY.md` — the Reuse Audit and Stability
  Principle referenced above.
- `docs/policies/TESTING_POLICY.md` — the validation gate between Code
  and a reportable "done."
