# AI Production Integration Foundation (Phase 61.5)

The sixth v0.4 AI Core phase, and the first to do real live-wiring.
Where 61.0-61.4 built the AI Core and its product-control layer, all
strictly foundation ("real, tested, documented, never registered into
a live handler"), 61.5 registers real commands into
`platform_layer/telegram/commands.py`/`platform_layer/telegram/handlers.py` and wires a real user
registration flow through `platform_layer/telegram/polling.py`. Full reuse audit:
`docs/PHASE61_5_PRODUCTION_INTEGRATION_AUDIT.md` (TASK 0/1).

## TASK 1 — Real Provider Expansion

`ai/providers/openai_provider.py`, `claude_provider.py`,
`grok_provider.py` — each replaces the corresponding placeholder in
`ai/providers/provider_registry.py`, following
`ai/providers/gemini_provider.py`'s exact pattern (Phase 61.2 TASK 3):
`session`/`secrets` both injectable, `health_check()` reports "usable
key configured" without a network call, one private `_generate()`
every text capability routes through, `vision()`/`image()`/`voice()`
raise `NotImplementedError`. API key travels only in a request header
(`Authorization: Bearer` for OpenAI/Grok, `x-api-key` for Claude),
never the URL, never an exception message. `core/secrets.py` already
carried `OPENAI_API_KEY`/`CLAUDE_API_KEY`/`GROK_API_KEY` as optional
secrets (Phase 61.2 TASK 2) — no secrets change needed.
`ai/providers/placeholder_providers.py`'s corresponding three classes
were removed (same precedent as Gemini's Phase 61.2 removal —
CLAUDE.md's "No duplicate logic"); `local_llm` stays the one
remaining placeholder.

## TASK 2 — Router Intelligence (⚠️ most cautious)

`ai/router/provider_score.py` (new) — `ProviderScore` composes health
(`ai.providers.provider_health.ProviderHealthTracker`) + success rate
+ latency + cost (`ai.audit.provider_stats.ProviderStats`) into one
0.0-1.0 score, weighted health-first. `score_providers()` ranks an
explicit provider-name list best-first. **`ai/router/router.py` is
unmodified** — `AIRouter.route()` does not import, call, or otherwise
consume `provider_score.py`, matching `router.py`'s own pre-existing
docstring invariant ("`provider_metrics()` ... never calls or is
influenced by `route()`"). Recommendation/analytics/owner-view only,
per the Director's explicit "❌ Router avtomatik provider
almashtirmaydi" constraint.

## TASK 3 — Telegram Owner AI Dashboard Integration (live wiring)

`platform_layer/telegram/commands.py`'s `OWNER_COMMANDS` gained five entries:
`ai_status`, `ai_provider`, `ai_cost`, `ai_usage`, `ai_health`.
`platform_layer/telegram/handlers.py` gained the matching five `{command}_handler`
functions, each calling the corresponding `platform_layer/telegram/owner/
ai_commands.py` function (built Phase 61.4 TASK 3) — the first live
callers those functions have ever had. No change to
`platform_layer/telegram/command_router.py` itself: dispatch is registry-driven
(`getattr(handlers, f"{command}_handler")`), confirmed by TASK 0's own
audit. `platform_layer/telegram/owner/ai_commands.py` gained a sixth function,
`ai_health()`, formatting `provider_score.score_providers()`'s
ranking. Every handler relies on `ai_commands.py`'s own
`Optional[...] = None` defaults to construct its `ai/` objects — no
new `ai/` import in `platform_layer/telegram/handlers.py` itself beyond the six
`ai_commands` functions. `ai_cost`/`ai_usage` are called with an empty
`provider_stats`/`user_usage` dict — no live `ai/audit/` data source
exists yet (no live `AIService` call happens anywhere in this phase
either), so they honestly report zero/"no usage" rather than
fabricating history.

## TASK 4 — User Registration Integration (live wiring)

Real `/start` → Phone Share Button → Phone Hash → `UserRecord` →
Trial Check → FREE account flow:

- `platform_layer/telegram/keyboards.py` gained `phone_share_keyboard()` — the first
  `ReplyKeyboardMarkup` in this codebase (every prior keyboard is
  `InlineKeyboardMarkup`, which cannot request a contact).
  `platform_layer/telegram/command_router.py`'s `_KEYBOARD_BY_COMMAND["start"]` now
  points at it (repurposed from `language_keyboard` — language
  selection is unaffected, still fully available via its own
  `/language` mapping).
- `platform_layer/telegram/polling.py`'s dispatcher gained one conditional: a message
  with `.contact` populated routes to the new
  `platform_layer.telegram.command_router.route_contact()` instead of
  `route_message()` (a contact-share message has `.text is None`, so
  `route_message()` would have silently resolved it to "Unknown
  command").
- `platform_layer/telegram/handlers.py` gained `contact_handler()`, calling the new
  `platform_layer.telegram.user_service.UserService.register_phone()`.
- `register_phone()`: hashes the phone number immediately via
  `core_layer.secrets.phone_hash.hash_phone_number()` (the raw string never outlives
  the method call), checks reuse via `ai.access.identity_checker.
  is_phone_reused_by_another_account()` against
  `UserRepository.get_users_by_phone_hash()`'s result, persists the
  hash unconditionally, and — only if not reused and no trial has
  started yet — persists `trial_started_at` (a new, additive
  `UserRecord`/`users`-table column, same migration convention as
  `phone_hash`) and reports trial status via
  `ai.access.trial_manager.trial_status_from_started_at()` (new: a
  stateless extraction of `TrialManager.status_of()`'s own math, so
  this database-persisted caller doesn't duplicate it).
- **`role` is not a new column.** It is already fully derivable from
  `platform_layer.telegram.permissions.is_owner()`/`is_admin()` (config-driven) and
  `SubscriptionRecord.plan` (already persisted) — exactly what
  `ai.access.permission_service.resolve_ai_role()` (Phase 61.4 TASK 2)
  already takes. A fourth persisted role would duplicate existing
  state.
- **The raw phone number is never persisted** — same invariant Phase
  61.4 TASK 4 established, re-verified by this phase's own tests.

## TASK 5 — AI Content Intelligence Foundation

`ai/capabilities/capability.py` gained four members
(`AI_MARKET_REPORT`/`AI_WEEKLY_OUTLOOK`/`AI_NEWS_ANALYSIS`/
`AI_SCRIPT_GENERATION`) — extended in place (Module Reuse Principle
step 2), not a duplicate "ContentType" enum; `Capability` is already
this codebase's one vocabulary for "what can AI be asked to do."
Additive and safe: `AccessControl`'s `OWNER`/`ADMIN` matrix entries are
`frozenset(Capability)` (every current member), so console operators
gain access automatically; `VIP`/`PREMIUM`/`FREE` list members
explicitly and do not gain these four until a future phase opts them
in. `ai/router/routing_rules.py` and
`ai/providers/provider_capabilities.py` both gained matching entries
(same text-generation-provider candidate shape as `ANALYSIS`/
`EXPLANATION`).

`ai/content/` (new top-level package under `ai/`):
- `content_types.py` — `CONTENT_CAPABILITIES` (which four `Capability`
  values are content-shaped) + `content_title()`.
- `content_schema.py` — `ContentRequest`/`ContentResult`, composing
  existing foundation types (`Capability`/`AIContext`/`AIRole`), same
  convention `ai/runtime/runtime_request.py` established.
- `content_adapter.py` — `ContentEngine.generate()` wraps
  `ai/runtime/ai_service.py`'s `AIService.ask()` unmodified, exact
  same pattern `ai/explanation/explanation_engine.py`'s
  `ExplanationEngine` established (Phase 61.3 TASK 7). **Foundation
  only**: none of the four content capabilities has an entry in
  `AIService`'s `_CAPABILITY_METHOD` dispatch table yet (same
  pre-existing gap `SUMMARY`/`EDUCATION`/`MEMORY`/`TOOL_CALLING`/
  `VIDEO`/`DOCUMENT` already have), so `generate()` always receives a
  cleanly rejected `RuntimeResponse` today — never a fabricated
  answer.

## TASK 6 — Broadcast Preparation Interface

`ai/content/broadcast_output.py` (new) — `BroadcastReadyContent` +
`prepare_broadcast()`, a contract-only adapter from an accepted
`ContentResult` to the shape a future broadcast layer would consume.
`prepare_broadcast()` returns `None` for any non-accepted result
(every result today) rather than fabricating broadcast-ready content.
No real streaming/voice/video/scheduling/send logic — explicitly
deferred to a future v0.5 Product Media Layer / Phase 62.x Owner
Broadcast Foundation, per the Director's own decision.

## Addendum — Director review response

The Director reviewed a mid-flight log snapshot of this phase and
requested three verifications plus two new foundation commands before
closing. All five are addressed here:

1. **ProviderScore stays read-only.** Re-confirmed: `ai/router/router.py`
   is unmodified this phase; `test_provider_score.py`'s own
   `test_score_providers_never_calls_or_imports_router_route()`
   inspects `provider_score.py`'s source directly to assert neither
   `AIRouter` nor `.route(` appears in it.
2. **`ai_health()` enriched.** Now shows per-provider Latency/Success/
   Requests/Tokens/Today's Cost/Failures alongside the existing score
   ranking — all reused from `ai.audit.provider_stats.ProviderStats`'s
   existing fields, no new metric. A provider with no call history
   reports "N/A" per field, never a fabricated number.
   `ai_status()`/`ai_provider()`'s own inline online/current-provider
   calculations were extracted into two new public helpers
   (`ai_runtime_online()`/`current_provider_for()`) so `/owner` reuses
   them directly instead of parsing formatted message text.
3. **Permission-tier tests added**
   (`tests/telegram/test_ai_command_permission_matrix.py`): FREE
   denied, ADMIN allowed on every read-only AI/dashboard command,
   OWNER allowed on all of them plus the OWNER-only `/doctor`, and an
   unknown command (`/ai_abc`) reports "Unknown command." **Scope
   note**: `ai_disable`/`ai_enable`/`ai_limit` (built Phase 61.4 TASK 3)
   remain **not** live-wired this phase — TASK 3's original brief named
   exactly five commands (`ai_status`/`ai_provider`/`ai_cost`/
   `ai_usage`/`ai_health`); wiring three more mutating commands was not
   in that scope and is flagged here rather than silently added.
   `ai_status`/`ai_provider`/`ai_cost`/`ai_usage`/`ai_health`/`owner`
   were additionally added to `ADMIN_COMMANDS` (dual membership with
   `OWNER_COMMANDS`, same precedent as the pre-existing `system`/
   `broadcast` commands) since they are read-only information, not
   mutations — `doctor` stays OWNER-only (exposes internal subsystem
   reachability).
4. **`/owner`** (new) — `platform_layer/telegram/owner/dashboard.py`'s
   `get_owner_summary()`: a compact panel (System/AI/Provider/Users/
   Premium/Signals Today/Win Rate/Cost Today/Emergency), composing
   `AdminService`, the new `ai_runtime_online()`/`current_provider_for()`
   helpers, `ai_cost()`, two new repository methods
   (`SubscriptionRepository.count_by_plan()`,
   `SignalRepository.count_signals_today()`/
   `get_closed_signals_today()`), `analytics.strategy_report.compute_win_rate()`,
   and `core_layer.emergency.emergency_manager.EmergencyManager`. Every
   section degrades to "N/A" independently on failure — never raises,
   never fabricates.
5. **`/doctor`** (new) — `get_doctor_report()`: nine subsystem checks
   (Database/AI/Market Data/Telegram/Scheduler/Providers/Learning/
   Cache/Audit), each a cheap reachability probe or an existing status
   field, never a live network call. "Scheduler" is honestly reported
   "N/A" — GoldBot's own scheduling is external (cron/GitHub Actions),
   so no in-process object exists to check.

Neither `/owner` nor `/doctor` touches `decision/`/`risk/`/`execution/`
— both are pure read/reachability reporting.

## Isolation re-verification (TASK 7)

AST-based import sweep (`ast.walk()` over every `.py` file under
`ai/`), re-run at the end of this phase:

| Target | Import sites found |
|---|---|
| `decision/` | **0** |
| `risk/` | **0** |
| `execution/` | **0** |
| `strategies/` | **0** |
| `database/` | **0** |
| `telegram/` | **0** |
| `signals/` | 7 (unchanged from Phase 61.4 — no new site this phase, including `ai/content/`) |
| `context/` | 6 total, unchanged from Phase 61.4 (including `ai/content/`) |

`ai/content/` specifically: zero imports of `signals/`, `context/`,
`decision/`, `risk/`, `execution/`, `database/`, `telegram/` — it
never produces or influences a trading signal.

`platform_layer/telegram/user_service.py` and `platform_layer/telegram/owner/ai_commands.py`
(outside `ai/`, this phase's live-wiring surface) both import `ai/`
directly — the same relationship every `platform_layer/telegram/owner/*.py` module
has always had to its own domain (consuming `ai/`'s already-computed
output, never the reverse).

## Not wired

Real content generation (no `AIService` runtime mapping for the four
`AI_*` capabilities), Router Intelligence auto-switching (`route()`
unmodified by design), and real Broadcast delivery are all still out
of scope.

## Tests

1959 tests total (up from 1879 at the start of this phase), zero
regressions in the pre-existing suite. Two pre-existing tests were
updated to reflect TASK 1's real behavior change (`openai`/`claude`
providers no longer fabricate a successful placeholder response) and
TASK 5's new `Capability` members (`test_every_capability_has_a_routing_rule`
already asserted "every declared `Capability`", so it required no
logic change once `routing_rules.py` covered the four new members).

## Deliberately out of scope (Director's own decision)

Streaming, YouTube automation, Voice engine, Video generator,
Hologram, TikTok/Twitch integration, adaptive autonomous routing —
none built this phase.
