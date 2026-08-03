# Phase 61.1.1 — AI Foundation Corrections

A deliberately small, corrections-only phase — no new capability, no
new provider, no pipeline/decision/risk/execution touch. Closes two
foundation gaps found in Phase 61.1's own post-completion audit and
finishes the Prompt Lifecycle the Director asked for. Full reuse
audit: `docs/PHASE61_1_1_FOUNDATION_CORRECTIONS_AUDIT.md`.

## TASK 2 — Cache Freshness Correction

**Problem**: `ai/cache/`'s `CacheKey.context_hash` (Phase 61.1) was a
caller-chosen hash over an arbitrary payload — nothing tied it to one
canonical identity for "which market/context moment does this cache
entry answer for." Two failure modes were possible: a caller hashing
something that doesn't actually change between two genuinely different
market moments (stale cache), or a caller accidentally including a
timestamp so identical content never matches its own earlier cache
entry (cache miss every time).

**Fix**: `AIContext` (`ai/context/context_snapshot.py`) gained
`snapshot_id` — computed exclusively inside
`ai_layer.ai_engine.context.context_builder.build_ai_context()`, never by a caller,
never via `datetime.now()`/`uuid.uuid4()`. It is a deterministic
SHA-256 (reusing `ai_layer.ai_engine.cache.cache_policy.compute_context_hash()`, not a
second hash implementation) over the built context's own `to_dict()`
output with `built_at` removed — the one field that would otherwise
make identical inputs produce different ids. `CacheKey` gained a sixth
required field, `snapshot_id`. `ai/cache/cache_policy.py` gained
`build_cache_key_from_context(ai_context, capability, provider_name,
prompt_version, context_hash=None)` — the blessed construction path,
which raises `ValueError` if `ai_context.snapshot_id` is `None`
(an `AIContext` never built through `build_ai_context()`).

Verified directly (`tests/ai/context/test_snapshot_identity.py`):
identical content produces identical `snapshot_id` even when
`built_at` differs; different content produces a different
`snapshot_id`; a directly-constructed `AIContext()` has
`snapshot_id=None` and `build_cache_key_from_context()` refuses it.

**Freshness chain, now documented in `ai/cache/cache_policy.py` and
`docs/AI_PROVIDER_FOUNDATION.md`**: Snapshot identity (content-derived,
via `snapshot_id`) -> Cache freshness (a cache hit is only possible for
a genuinely matching snapshot) -> TTL (`CachePolicy.default_ttl_seconds`,
300s default — the hard ceiling even when content hasn't changed).

## TASK 3 — Prompt Lifecycle

`ai/prompts/prompt_registry.py` gained `PromptLifecycleState`
(ACTIVE/DEPRECATED/ARCHIVED) as a field on `PromptVersionRecord`,
defaulting to ACTIVE on `register()` — fully backward compatible with
every Phase 61.1 test. New methods `deprecate()`/`archive()`/
`state_of()`. `set_active()` and `rollback()` both now refuse to
select a DEPRECATED or ARCHIVED version (`tests/ai/test_prompt_lifecycle.py`
verifies both paths) — a retired version stays visible in
`list_versions()` (history is never deleted) but can never again
become the active one. `PromptManager` itself is untouched.

## TASK 4 — Provider Documentation Correction (no code change)

`docs/AI_PROVIDER_FOUNDATION.md` gained a "Provider Preference vs
Provider Health" section, spelling out that `ProviderStatus` (owner
intent) and `ProviderHealth` (observed reality) are independent axes,
with the exact Preferred -> Offline -> Fallback -> Recovered ->
Preferred-again worked example the Director asked for, and an
explicit statement that no automatic demotion of `ProviderStatus`
occurs — recovery looks automatic only because nothing ever took
PREFERRED away during the outage. No file under `ai/providers/` or
`ai/router/` changed.

## What did not change

`core/`, `decision/`, `risk/`, `execution/`, `strategies/`,
`signals/`, `learning/` — untouched. No new AI capability, no new
provider, no real AI API, no change to `ai/router/router.py`'s
selection algorithm (the router was not touched this phase at all —
TASK 2/3 are entirely in `ai/context/`, `ai/cache/`, `ai/prompts/`).

## Tests added

`tests/ai/context/test_snapshot_identity.py` (9 tests),
`tests/ai/test_prompt_lifecycle.py` (11 tests) — 20 new tests total.

## Acceptance criteria confirmed

- Reuse Audit completed and documented
  (`docs/PHASE61_1_1_FOUNDATION_CORRECTIONS_AUDIT.md`).
- Cache freshness is now determined by a canonical `snapshot_id`.
- `snapshot_id` is produced by the AI Context Builder; a caller cannot
  construct one (`build_cache_key_from_context()` raises `ValueError`
  otherwise).
- Prompt Lifecycle (ACTIVE, DEPRECATED, ARCHIVED) is implemented.
- A DEPRECATED (or ARCHIVED) prompt is never selected by `set_active()`
  or `rollback()`.
- `docs/AI_PROVIDER_FOUNDATION.md` explains the ProviderStatus vs.
  ProviderHealth distinction explicitly, with a worked example.
- Trading Pipeline and the AI Router's selection algorithm are
  unchanged.
- No real AI Provider API was added.
