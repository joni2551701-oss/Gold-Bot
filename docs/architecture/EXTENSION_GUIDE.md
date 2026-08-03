# GoldBot — Extension Guide

Governed by `docs/constitution/CONSTITUTION.md`, especially Article 7
(Reuse Principle). This is the practical "how do I add X without
violating the Constitution" reference for the two most common kinds
of new work in this codebase: a new AI capability, and a new
Telegram command.

Before starting either pattern below, apply Article 7's three-step
audit: does this already exist? can an existing module be extended?
only if both are "no," create something new.

## Pattern 1 — Adding a new AI capability

1. **Capability enum** — add the new capability to
   `ai/capabilities/` (the existing `Capability` enum). Do not create
   a parallel enum elsewhere.
2. **Permission matrix** — extend the existing permission mapping in
   `ai/access/` / `ai/capabilities/` so the new capability has an
   explicit allow/deny per role. A capability with no matrix entry is
   a bug, not an implicit-deny.
3. **Provider support** — confirm which providers under `ai/providers/`
   support the new capability via `provider_capabilities.py`; do not
   branch on vendor name anywhere outside `ai/providers/` (Constitution
   Article 5).
4. **Route it** — if the new capability needs specific candidate
   ordering, add it to `ai/router/routing_rules.py`. Never modify
   `ai/router/router.py`'s own selection logic to special-case a
   capability — routing rules are data, not code changes to the
   router itself.
5. **Test** — unit test for the capability's own logic, an isolation
   test confirming no forbidden import was introduced (Article 3), a
   regression run of `pytest tests/` (Article 6).
6. **Document** — update `ai/README.md` and, if the capability changes
   what `AIService.ask()` can do, `docs/AI_RUNTIME_FLOW.md`.

This never requires touching `decision/`, `risk/`, or `execution/` —
if a capability seems to need one of those, it is not an AI
capability; stop and raise it with the Director (Constitution
Article 1).

## Pattern 2 — Adding a new Telegram command

1. **Command file** — add the command's name to the relevant list in
   `platform_layer/telegram/commands.py` (e.g. `OWNER_COMMANDS`) rather than creating
   a new command registry.
2. **Permission** — declare who may run it in `platform_layer/telegram/permissions.py`.
3. **Service** — implement the business logic in the appropriate
   `telegram/*_service.py` or, for Owner-only tooling, a file under
   `platform_layer/telegram/owner/*.py`. If the command needs data, the service calls
   a `database/*_repository.py` — never raw SQL in the service, never
   a handler touching the database directly (Constitution Article 4).
4. **Handler** — add `<command>_handler()` to `platform_layer/telegram/handlers.py`
   (or the owner module it belongs to), matching the exact
   `getattr(handlers, f"{command}_handler")` dispatch convention
   `platform_layer/telegram/command_router.py` already uses. A handler name that
   doesn't match this pattern is silently never called — verify the
   name before writing tests, not after (this exact mistake was
   caught and fixed once already, in Phase 61.7).
5. **Test** — a handler test (dispatch reaches the right service), a
   service test (business logic in isolation), and a regression run.
6. **Document** — add the command to the relevant `telegram/README.md`
   or `docs/owner/OWNER_PANEL.md` section if it's an Owner command.

## What never changes for either pattern

- No new top-level package for a single capability or command — it
  belongs inside an existing package (`ai/*`, `platform_layer/telegram/owner/*`), per
  Constitution Article 7's "a new top-level package is the
  highest-cost option and should be rare."
- No AI capability or Telegram command reaches into `decision/`,
  `risk/`, or `execution/` directly, ever, regardless of how
  convenient a shortcut looks in the moment (Constitution Article 1
  and 3; `CLAUDE.md` Trading Safety rules).
- Every new module ships with tests before it is considered complete
  (Constitution Article 6).

## Related documents

- `docs/constitution/CONSTITUTION.md` — the Articles this guide
  operationalizes.
- `docs/architecture/IMPORT_RULES.md` — what imports the new code is
  allowed to use.
- `docs/ai/AI_ARCHITECTURE.md` — the real `ai/` package map to orient
  Pattern 1 within.
- `docs/telegram/TELEGRAM_ARCHITECTURE.md` — the real Telegram
  dispatch flow to orient Pattern 2 within.
