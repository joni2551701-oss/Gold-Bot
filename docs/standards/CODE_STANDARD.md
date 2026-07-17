# Code Standard

Concrete, file-level conventions this codebase already follows,
written down so a new Worker Brief doesn't have to rediscover them by
reading ten existing files.

## Constructor injection

Every constructor argument is optional with a real, working default —
never a hand-rolled mock is required to test a class in isolation.
This is the pattern `AIService(sleep_fn: Optional[Callable] = None)`,
every Manager (`PersonaManager(registry: Optional[Dict] = None)`),
and every repository already use. A new class that requires a caller
to construct three collaborators before it can be instantiated is a
standard violation, not a style preference.

## Comments

No comments unless the *why* is genuinely non-obvious — a hidden
constraint, a workaround for a specific bug, a subtle invariant. A
comment that restates what a well-named function already says is
noise, not documentation. This codebase's docstrings state the
module's *purpose*; they do not narrate the task or phase that added
it (that belongs in the commit message and the phase's Freeze doc, not
in code that outlives the phase).

## Error handling at boundaries only

Validate and handle errors where data enters the system (an external
API response, a Telegram message, a config value) — not defensively at
every internal call site where the type is already guaranteed by the
caller. `MarketDataNormalizer`'s `ExternalAPIError` handling and
`ai/providers/runtime_errors.py`'s typed exception hierarchy
(`ProviderTimeoutError`, `ProviderRateLimitError`, …) are the model.

## No duplicate logic

Before writing a helper, `grep` for one that already does this
(Constitution Article 7/11). `ai/audit/provider_stats.py`'s three
separate extensions (Phase 61.1, 61.3, 61.6) rather than three
competing stats modules is the standing example.

## Minimal diff

A bug fix does not carry a refactor. A foundation phase does not carry
a migration. If a change grows past what the brief asked for, stop and
report rather than push through (`CLAUDE.md`'s own Restrictions
section; `docs/policies/DEVELOPMENT_POLICY.md`'s Minimalism section).

## Related

- `docs/policies/DEVELOPMENT_POLICY.md`.
- `docs/architecture/DESIGN_PATTERNS.md`, `docs/architecture/NAMING_CONVENTIONS.md`.
- `/CLAUDE.md` — the top-level Engineering Governance this standard
  makes concrete.
