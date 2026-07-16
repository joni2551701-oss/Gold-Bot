# Phase 61.1.1 — AI Foundation Corrections: Reuse Audit

TASK 1 of the Phase 61.1.1 Worker Brief. Audits `ai/cache/`,
`ai/context/`, `ai/prompts/`, `docs/`, `tests/` before any code is
written — same discipline as every prior phase's TASK 1.

## Where `CacheKey` is created today

`ai/cache/cache_policy.py`'s `CacheKey` (frozen dataclass, five
fields: `capability`, `context_version`, `provider_name`,
`prompt_version`, `context_hash`) is constructed directly by whatever
caller wants a cache entry — there is no factory function today, only
the bare dataclass constructor. `context_hash` is produced by
`compute_context_hash(context_payload: dict)`, but that function
accepts *any* JSON-serializable dict — nothing ties it to a specific
canonical representation of an `AIContext`. In `tests/ai/cache/test_response_cache.py`,
the test helper `_make_key()` calls `compute_context_hash({"symbol": "XAUUSD"})`
directly — an arbitrary, test-chosen payload, exactly the pattern the
Director's audit flagged as the risk: nothing stops two different
callers from hashing two different subsets of the same real context
and landing on different cache entries for what should be the same
snapshot, or from hashing something that never changes between two
genuinely different market moments.

## Does a Context Snapshot ID exist today?

No. `ai/context/context_snapshot.py`'s `AIContext` (as of Phase 61.1
TASK 7) has `schema_version`/`context_version` — both static
strings describing the *shape* of the context, not the *content* of
one particular built instance. Nothing on `AIContext` identifies "this
specific snapshot" versus "another snapshot built from different
underlying data." `build_ai_context()` in `ai/context/context_builder.py`
stamps `built_at=datetime.now(timezone.utc)` — a real timestamp, but
one that changes on every call even when given byte-identical inputs,
so it cannot serve as a content-freshness identifier (using it directly
for cache-key purposes would guarantee a cache miss on every single
call, one of the two failure modes the Director's brief explicitly
forbids: "yoki har safar cache miss").

**Conclusion**: TASK 2's `snapshot_id` cannot be `built_at` and cannot
be a fresh `datetime.now()`/`uuid.uuid4()` call at cache-key-construction
time (per the brief's own explicit prohibition) — it must be a
**deterministic function of the AIContext's own content**, so that two
calls to `build_ai_context()` with identical inputs at different real
times produce the *same* `snapshot_id` (enabling a legitimate cache
hit), while two calls with different inputs (different market summary
text, different signal, etc.) produce *different* `snapshot_id`s
(preventing the stale-serve the Director described). `built_at` stays
in `AIContext` for its existing "when was this built" purpose, unused
for freshness.

## Reuse found: `compute_context_hash()`

`ai/cache/cache_policy.compute_context_hash()` already is exactly the
deterministic, order-independent SHA-256 hashing function TASK 2
needs — `ai/context/context_builder.py` should call it directly to
derive `snapshot_id` from a canonical payload built from `AIContext`'s
own already-existing fields (excluding `built_at`), rather than
reimplementing hashing a second time. This is a one-directional import
(`ai/context/` -> `ai/cache/`) with no cycle: `ai/cache/cache_policy.py`
only imports `ai/capabilities/capability.py`, never `ai/context/`.

## What lifecycle does Prompt Registry use today?

None. `ai/prompts/prompt_registry.py`'s `PromptVersionRecord` (Phase
61.1 TASK 5) has no state field at all — every registered version is
implicitly always selectable via `set_active()`, and `rollback()` will
happily move the active pointer to *any* earlier-registered version
regardless of whether it should still be considered usable. TASK 3
adds a `PromptLifecycleState` enum (ACTIVE/DEPRECATED/ARCHIVED) as a
new field on `PromptVersionRecord`, defaulting every newly-registered
version to `ACTIVE` — fully backward compatible with every existing
Phase 61.1 test in `tests/ai/test_prompt_registry.py`, none of which
ever exercises a non-default state.

## What do current tests guarantee?

- `tests/ai/cache/test_response_cache.py`: `CacheKey` requires all
  five *current* fields (`test_cache_key_requires_all_five_fields`);
  put/get round-trips by exact key match; TTL expiry; `clear()`
  semantics. None of these tests assert anything about freshness
  *correctness* (i.e., that identical content produces identical
  keys and different content produces different keys) — they only
  test the mechanism, using caller-chosen hashes. TASK 5 adds the
  missing correctness tests.
- `tests/ai/test_prompt_registry.py`: register/set_active/rollback/
  list_versions mechanics, all against implicitly-ACTIVE versions.
  None test rejection of a non-ACTIVE version. TASK 5 adds these.
- `tests/ai/context/test_context_versioning.py`: only
  `schema_version`/`context_version`, confirms `built_at` still
  works — no existing test touches snapshot identity.

## Reuse summary

| Concern | Reuse decision |
|---|---|
| Cache key freshness field | Extend existing `CacheKey` (add `snapshot_id`), do not create a new key type. |
| Snapshot ID hashing | Reuse `ai.cache.cache_policy.compute_context_hash()` directly from `ai/context/context_builder.py` — no second hash implementation. |
| Snapshot ID production | New logic inside `build_ai_context()` (TASK 2) — the one and only place `AIContext.snapshot_id` is ever set; no new module needed. |
| Cache key construction | New factory function `build_cache_key_from_context()` inside `ai/cache/cache_policy.py` (same file `CacheKey` already lives in — extend, don't split) so a caller is steered toward `ai_context.snapshot_id` instead of inventing one. |
| Prompt lifecycle | Extend `ai/prompts/prompt_registry.py` in place — `PromptLifecycleState` enum + a `state` field on the existing `PromptVersionRecord`, plus `deprecate()`/`archive()` methods on the existing `PromptRegistry` class. No new package, no new file — `PromptManager` itself untouched, matching TASK 3's own explicit instruction. |

No new package is created this phase. Every change is either an
additive field, a new method on an existing class, or a new function
in a file that already exists — matching this brief's own scope
("mavjud foundation'ni mustahkamlaydi", strengthens the existing
foundation, adds nothing new architecturally).
