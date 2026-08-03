# AI_ARCHITECTURE_REVIEW.md — TASK-AI-001 Foundation Architecture Review

Status: review of the `ai/foundation/` package against the Director's
mandated Architecture Rules: Clean Architecture, SOLID, Separation of
Concerns, Dependency Inversion, Future First, Reuse First.

## Clean Architecture

The Foundation is a pure inner layer: value objects and interfaces at
the centre (`interfaces.py`, `context.py`, `lifecycle.py`), stateful
collaborators around them (`registry.py`, `factory.py`, `session.py`,
`runtime.py`), and one composition root (`manager.py`). Nothing in the
Foundation performs I/O, network, or persistence; nothing imports a
framework or an outer layer. `self_check.py` is the only entry point
and depends inward only.

## SOLID

- **S (Single Responsibility):** each module owns exactly one concern —
  Registry holds, Factory builds, Session tracks sessions, Runtime
  tracks state, Manager orchestrates. No module does two of these.
- **O (Open/Closed):** new AI capabilities extend the Foundation by
  *implementing `AIComponent`* and registering — no Foundation code
  changes to add one. New lifecycle consumers subclass
  `LifecycleComponent`.
- **L (Liskov):** `AIComponent` refines `LifecycleComponent` without
  weakening it; `DummyAIComponent` is substitutable anywhere an
  `AIComponent` is expected (the Manager treats it purely through the
  interface).
- **I (Interface Segregation):** two small interfaces — a component
  that only needs lifecycle implements `LifecycleComponent`; one that
  is also a registrable AI capability implements the slightly larger
  `AIComponent`. Nothing is forced to implement methods it does not use.
- **D (Dependency Inversion):** `AIManager`, `FoundationRegistry`, and
  `FoundationFactory` depend on the `AIComponent`/`LifecycleComponent`
  abstractions, never on `DummyAIComponent` or any concrete class. The
  Dummy is injected (registered), not imported by the Manager.

## Separation of Concerns

Interfaces vs. implementations vs. orchestration are in separate
files. Lifecycle vocabulary (`lifecycle.py`) is separate from the
runtime that uses it (`runtime.py`). Session state (`session.py`) is
separate from the context value it carries (`context.py`).

## Dependency Inversion & Future First

The Foundation is the stable *base*: it imports only its own
abstractions + stdlib, so future components (and, in a later task, the
existing `ai/` managers) depend on the Foundation, not the reverse.
This is deliberately the inverse of wiring the Manager to today's
concrete `ProviderManager`/`SessionManager`/`RuntimeManager` — those
would drag their own dependencies (including `core_layer.logger.logger`) inward and
couple the base to the present. The Foundation is built for what comes
next, not retrofitted to what exists.

## Reuse First — and why some reuse is by-pattern

Reuse First was applied, but under this task's hard dependency rule
("Foundation may depend only on other Foundation modules inside `ai/`",
"no dependency to Core") two proven `ai/` designs are reused *by
pattern* rather than by import, because importing them would pull in
`core_layer.logger.logger`:

- `lifecycle.py` reuses the transition-validated state-machine model of
  `ai/runtime/runtime_state.py` (`RuntimeState` + `is_valid_transition`).
- `session.py` reuses the in-memory create/get/close manager pattern of
  `ai/session/session_manager.py`, extended with `restore_session`.

Where reuse was possible without any forbidden dependency it was taken
directly: the Foundation defines each concept once and every collaborator
reuses that single definition (e.g. one `LifecycleState`, one
`HealthReport`, one `FoundationContext` shared across the package).

## Duplicate-name discipline (carried over from TASK-AI-000A)

Every Foundation class name was collision-checked repo-wide before use.
Notably `FoundationContext` (not `AIContext`, which already exists at
`ai_layer.ai_engine.context.context_snapshot.AIContext`) and `FoundationRuntimeStatus`
(not `RuntimeStatus`) avoid reintroducing the duplicate-name hazard the
previous task removed.

## Assessment

The package satisfies all six mandated Architecture Rules. The one
deliberate trade-off — pattern-reuse instead of import-reuse for the
lifecycle/session models — is forced by the Foundation→Core
prohibition and is the correct call: it keeps the base layer
genuinely dependency-free, which is what makes it a *foundation*.
