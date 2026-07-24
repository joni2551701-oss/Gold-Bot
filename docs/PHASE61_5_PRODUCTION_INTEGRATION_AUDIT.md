# Phase 61.5 — AI Production Integration Foundation: Reuse Audit (TASK 0/1)

Self-initiated audit, following this session's own established
discipline (every Phase 61.x TASK 1 opens with a reuse audit before any
code is written), matching `docs/PHASE61_4_PRODUCT_CONTROL_AUDIT.md`'s
structure. Phase 61.5 is the first phase in the entire 61.x arc that
does **real live-wiring** (TASK 3/4), so this audit also resolves two
open design questions before implementation starts.

## TASK 1 — Real Provider Expansion

Confirmed pattern to replicate exactly, via `ai/providers/gemini_provider.py`
(Phase 61.2 TASK 3) and its test file
`tests/ai/providers/test_gemini_provider.py`:

- `BaseAIProvider` subclass, `session`/`secrets` both injectable
  constructor args (`session or requests`, `secrets or Secrets()`).
- `health_check()` overridden to report "usable key configured",
  never a real network call.
- One private `_generate()` (or per-provider equivalent) that every
  text capability (`analyze`/`chat`/`explain`) routes through; the API
  key travels only in a request header, never the URL/query string,
  never appears in an exception message.
- `vision()`/`image()`/`voice()` raise `NotImplementedError` — no
  multimodal support yet, matches `BaseAIProvider`'s own contract.
- On failure: `requests.exceptions.Timeout` -> `ProviderTimeoutError`;
  other `requests.exceptions.RequestException` -> `ProviderUnavailableError`;
  HTTP 429 -> `ProviderRateLimitError`; HTTP >=400 ->
  `ProviderUnavailableError`; unexpected JSON shape ->
  `ProviderInvalidResponseError`. All four already exist in
  `ai/providers/runtime_errors.py` — reused unmodified.
- `core/secrets.py` already carries `OPENAI_API_KEY`/`CLAUDE_API_KEY`/
  `GROK_API_KEY` as optional secrets (Phase 61.2 TASK 2) — no secrets
  change needed for this task.

Per-vendor REST shape (publicly documented API contracts, each vendor's
own OpenAI-compatible-or-native chat-completion endpoint):

| Provider | Endpoint | Auth header | Request body | Response text path |
|---|---|---|---|---|
| OpenAI | `POST /v1/chat/completions` | `Authorization: Bearer <key>` | `{"model":..., "messages":[{"role":"user","content":prompt}]}` | `choices[0].message.content` |
| Claude (Anthropic) | `POST /v1/messages` | `x-api-key: <key>` + `anthropic-version` header | `{"model":..., "max_tokens":..., "messages":[{"role":"user","content":prompt}]}` | `content[0].text` |
| Grok (xAI) | `POST /v1/chat/completions` | `Authorization: Bearer <key>` | same OpenAI-compatible shape | `choices[0].message.content` |

`ai/providers/placeholder_providers.py`'s `OpenAIProvider`/
`ClaudeProvider`/`GrokProvider` are removed from that file once
replaced (same precedent as Gemini's placeholder removal in Phase
61.2 — "No duplicate logic", `CLAUDE.md`). `LocalLLMProvider` stays a
placeholder — out of this phase's scope, no brief item names it.
`ai/providers/provider_registry.py`'s three entries are repointed the
same way the `gemini` entry was repointed in Phase 61.2.

## TASK 2 — Router Intelligence (⚠️ most cautious)

`ai/router/router.py`'s own docstring already documents the exact
invariant the Director's brief asks to preserve: `provider_metrics()`
"is read-only ... it never calls or is influenced by `route()`".
`route()`'s current selection order (capability matrix -> provider
status -> health) is untouched by this phase. `ProviderScore` is
therefore a **new, separate, read-only analytics function** (same
shape as `ai/audit/provider_stats.py`'s existing `rank_providers()`,
Phase 61.3 TASK 9) — composing health + cost + latency + success-rate
into one score for owner-facing display only. No change to `route()`
itself, no new parameter threading a score into it.

## TASK 3 — Telegram Owner AI Dashboard Integration

Confirmed via `telegram/command_router.py`: dispatch is
`getattr(handlers_module, f"{command}_handler")`, driven entirely by
membership in `telegram/commands.py`'s `COMMANDS`/`OWNER_COMMANDS`/
`ADMIN_COMMANDS` dicts. **No change needed to `command_router.py`
itself.** This task is exactly two additive edits:

1. `telegram/commands.py`'s `OWNER_COMMANDS` dict gains five new
   entries: `ai_status`, `ai_provider`, `ai_cost`, `ai_usage`, and a
   new `ai_health` (the brief's fifth command — not yet built in
   `telegram/owner/ai_commands.py`; TASK 3 adds it there, following
   the same `AICommandResult`-returning shape as the other five).
2. `telegram/handlers.py` gains five `{command}_handler` functions,
   each: (a) resolve `is_owner` via the existing
   `telegram.permissions.is_owner()` check (same guard every other
   `telegram/owner/*.py`-backed handler already uses), (b) construct
   the real `ai/` objects (`ProviderManager`, `ProviderHealthTracker`,
   `CapabilityManager`, `UsageLimiter`, `provider_stats`/
   `user_usage` dicts) the same way other owner-command handlers
   construct their own service objects, (c) call the corresponding
   `telegram/owner/ai_commands.py` function, (d) send
   `result.message` back to the chat. This is the first phase where
   these `ai/` objects are constructed from a live handler rather than
   only from a test.

## TASK 4 — User Registration Integration: two open design questions, resolved

**(a) `trial_status` persistence.** `ai/access/trial_manager.py`'s
`TrialManager` (Phase 61.4 TASK 5) is deliberately in-memory-only —
correct for that phase's foundation-only posture, wrong for this
phase's real persistence requirement. Per the Module Reuse Principle
(extend before creating new): `TrialManager.status_of()` already
contains the exact pure calculation needed
(`started_at + duration` vs `now` -> `active`/`expires_at`); this task
extends `trial_manager.py` in place with a stateless function
(`trial_status_from_started_at(started_at, duration, now)`) that both
the existing in-memory `status_of()` and a new persisted caller can
share — no new module. Persistence itself follows the exact
`phone_hash` precedent from Phase 61.4 TASK 4: `UserRecord` gains
`trial_started_at: Optional[str] = None` (ISO string, same convention
as `last_activity`), `database/models.py`'s `_migrate_users_schema()`
gains one more additive `ALTER TABLE` column, `UserRepository` gains
`set_trial_started_at()`. `role` is **not** a new column: it is
already fully derivable from existing persisted facts — `telegram.
permissions.is_owner()`/`is_admin()` (config-driven) and
`SubscriptionRecord.plan` (already persisted by
`database/subscription_repository.py`) — exactly the two inputs
`ai/access/permission_service.py`'s `resolve_ai_role()` (Phase 61.4
TASK 2) already takes. Adding a fourth `role` column would duplicate
state that already exists and could drift from it — CLAUDE.md's "No
duplicate logic".

**(b) Contact-message routing.** `telegram/polling.py`'s single
catch-all `@dispatcher.message()` handler forwards every message to
`route_message()`, which only reads `message.text` (a contact-share
message has `message.contact` populated, `message.text is None` —
today this silently falls through to "Unknown command"). This task
adds a new, narrow code path: a `route_contact()` function (mirrors
`route_message()`'s shape: resolve `telegram_id`, extract
`message.contact.phone_number`, call the registration flow), and one
new conditional in `polling.py`'s dispatcher — `if message.contact is
not None: route_contact(...); return` before the existing text-command
path. `telegram/keyboards.py` gains one new `ReplyKeyboardMarkup` +
`KeyboardButton(request_contact=True)` keyboard (`phone_share_keyboard()`)
— the first use of `ReplyKeyboardMarkup` in this codebase; every
existing keyboard in that file is `InlineKeyboardMarkup`, a
structurally different aiogram type for a structurally different
purpose (requesting contact data vs. carrying callback data), so this
is an addition, not a change to any existing keyboard function.

The raw phone number never touches `UserRepository`: `route_contact()`
computes `core.phone_hash.hash_phone_number(contact.phone_number)`
immediately, passes only the hash onward, and the raw string is not
retained in any variable that outlives the function call.

## TASK 5 — AI Content Intelligence Foundation

Confirmed via `ls ai/content` (no such directory) — a genuinely new
package, correctly justified under the Module Reuse Principle's step
3 (steps 1/2 are both "no": no existing package builds structured,
schema-typed AI output content; `ai/runtime/runtime_response.py`'s
`RuntimeResponse` is free-text only, not the structured
report/outlook/analysis shape this task's brief specifies). Builds on
`ai/runtime/ai_service.py`'s existing `AIService.ask()` — content
generation is one more `AIService` caller, same relationship
`ai/conversation/conversation_engine.py` and
`ai/explanation/explanation_engine.py` already have.

## TASK 6 — Broadcast Preparation Interface

`ai/content/broadcast_output.py` — a plain dataclass contract
(`BroadcastReadyContent` or similar), no network/scheduling/media
logic. No existing module in this codebase declares a
broadcast-shaped output contract, so this is additive to the new
`ai/content/` package from TASK 5, not a duplicate.

## TASK 7 / TASK 8

Standard closing pattern, unchanged from every prior phase: AST-based
import sweep re-run at the end (`decision/`/`risk/`/`execution/`/
`strategies/` must stay at 0 imports from `ai/`; the new `ai/content/`
package must not import any of those four either, and must not import
`database/`/`telegram/`), then `docs/AI_PRODUCTION_INTEGRATION.md` +
`docs/PHASE61_5_FREEZE.md`, then the full mandatory Commit Protocol.

## Summary of what changes vs. every prior 61.x phase

This is the first phase where `telegram/commands.py`,
`telegram/handlers.py`, `telegram/polling.py`, and
`telegram/keyboards.py` (all outside `ai/`, but the live wiring
surface) are edited with real behavior, not left foundation-only. The
Director's own explicit caveat — "har bir live wiring oldin reuse
audit va isolation check bilan qilinadi" — is satisfied by this
document for TASK 3/4 specifically; TASK 7 re-verifies isolation after
all live wiring lands.
