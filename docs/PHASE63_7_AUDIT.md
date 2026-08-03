# Phase 63.7 — AI Media Intelligence Foundation: Audit

TASK 0. Mandatory reading completed (`docs/constitution/CONSTITUTION.md`,
`docs/policies/DIRECTOR_POLICY.md`, `docs/architecture/*`,
`docs/roadmap/*`, `docs/ai/*`) before any code change, per this
phase's own rule.

## Honest correction: `ai/media/` does not exist — the real package is top-level `media/`

The brief's TASK 0–7 name every new/extended file under `ai/media/`
(`ai/media_layer/content_manager/models.py`, `ai/media_layer/content_manager/media_registry.py`,
`ai/media_layer/content_manager/media_manager.py`, `ai/media_layer/content_manager/media_adapter.py`,
`ai/media_layer/content_manager/media_pipeline.py`). A direct `ls ai/` confirms no `media/`
subpackage exists under `ai/` — the real Media Foundation was already
built as a **top-level package**, a sibling of `ai/`, in Phase 63.0
TASK 5:

```
media/
├── __init__.py
├── README.md
├── media_types.py     -- MediaType (TEXT/VOICE/IMAGE/VIDEO/LIVE)
├── media_registry.py  -- MediaDescriptor, build_media_registry()
└── media_manager.py   -- MediaManager (Owner ENABLED/DISABLED intent)
```

This is the same discrepancy this repository's audits have now caught
three times: Phase 63.2 (`ai/knowledge/` named in a brief, real path
`knowledge/`), Phase 63.0's own TASK 0 (`content/` named as top-level
in an earlier brief, real path `ai/content/`), and now the reverse
direction here — `ai/media/` named, real path top-level `media/`. Per
Constitution Article 7 (Reuse Principle), this audit records what is
actually real. **Decision: every file this phase touches or creates
lands inside the existing top-level `media/` package, never a new
`ai/media/` subpackage.** Creating `ai/media/` alongside the existing
`media/` would produce two competing Media foundations for the exact
same concern — precisely what Article 11 forbids.

## Foundation Reuse Audit (Article 11, TASK 0's own required table)

| Component | Brief's assumed location | Real state | Decision |
|---|---|---|---|
| Foundation | `ai/media/` | ✅ Exists — top-level `media/` (Phase 63.0 TASK 5) | Extend `media/`, do not create `ai/media/` |
| Manager | `ai/media_layer/content_manager/media_manager.py` | ✅ Exists — `media_layer/content_manager/media_manager.py`'s `MediaManager` (Owner ENABLED/DISABLED intent per `MediaType`, TEXT starts enabled) | Extend `MediaManager` in place with `create_asset`/`validate_asset`/`prepare_asset`/`get_asset` (TASK 3) |
| Contract | — | ➖ None yet at the per-asset level (only per-type, via `MediaDescriptor`) | Genuine gap — no contract to duplicate |
| Model | `ai/media_layer/content_manager/models.py` | ✅ Partial — `MediaType` enum (`media_types.py`) already has all five values the brief names (`TEXT`/`VOICE`/`IMAGE`/`VIDEO`/`LIVE`, exact match). ❌ `MediaAsset` (a per-instance object) does not exist | Reuse `MediaType` as-is; add `MediaAsset`/`MediaAssetStatus` as the one genuine new file, `media_layer/content_manager/models.py` (TASK 1) |
| Capability | `ai/capabilities/capability.py` | ✅ Exists — `Capability.AI_MEDIA` (Phase 63.0 TASK 8), already present in `ai/router/routing_rules.py`'s `_CAPABILITY_PROVIDER_PREFERENCE` (`openai`, `gemini`) with no runtime dispatch mapping yet — same foundation-only posture every other `AI_*` capability has | Reuse as-is (TASK 6) — no new capability |
| Registry | `ai/media_layer/content_manager/media_registry.py` | ✅ Exists — `media_layer/content_manager/media_registry.py`'s `build_media_registry()` + `MediaDescriptor`, a static, fixed five-entry catalog (Phase 63.0's own explicit design: "no processing logic of any kind") | Extend `media_registry.py` with `get()`/`exists()` (TASK 2); see naming resolution below for `register()`/`list()` |

## TASK 2's `register()`/`get()`/`list()`/`exists()` naming resolution

The brief asks for four registry methods. Three of the four already
have a real, functionally-equivalent counterpart in this codebase — a
new name would duplicate, not add, capability:

- **`list()`** — already is `build_media_registry()` itself (returns
  every `MediaDescriptor`, the "list all" operation Phase 63.0 built).
  Reused as-is, no new function.
- **`get()`** — genuine, small gap at the Registry layer (`MediaManager.descriptor_of()`
  covers this at the Manager layer, but the Registry itself has no
  standalone lookup). Added as `media_registry.get(media_type)`.
- **`exists()`** — same genuine small gap. Added as
  `media_registry.exists(media_type)`.
- **`register()`** — **not built.** `media_registry.py`'s own module
  docstring (Phase 63.0, LOCKed) is explicit: "Static catalog... No
  processing logic of any kind." `build_media_registry()` returns a
  fixed, five-entry catalog by design — every `MediaType` the enum
  defines already has exactly one descriptor. A real `register()` that
  mutates this catalog at runtime would contradict that LOCKed design
  decision and has no caller this phase (no dynamic media type is
  being added — `MediaAsset.media_type` always draws from the existing
  fixed `MediaType` enum). Documented here per the same
  "naming difference, not a functional gap" resolution Phase 63.2 used
  for `KnowledgeItem`/`KnowledgeEntry`.

## `ai/content/broadcast_output.py` — the pre-existing Content→Broadcast shortcut

`ai_layer.ai_service.content.broadcast_output.prepare_broadcast(ContentResult) -> BroadcastReadyContent`
(Phase 61.5 TASK 6) already adapts Content directly into a
broadcast-ready shape, skipping over Media entirely. This predates
Media's real foundation (Phase 63.0) and the Official Intelligence
Pipeline's `Content → Media → Broadcast` ordering (Phase 63.3 Director
Decision). It is LOCKed since Phase 61.5 and out of this phase's scope
(`media/` only) — not modified. This phase adds the missing middle
adapter (`content_result_to_media_asset()`, TASK 4) as a new,
independent path; `prepare_broadcast()` is untouched and both paths
coexist (a future Broadcast-layer phase decides which one it reads
from, not this one).

## Dependency Compliance (Intelligence Dependency Principle)

`media/*.py` today imports nothing outside `media/` and `core/`
(`core_layer.logger.logger`) — zero dependency on `ai/`, `decision/`, `risk/`,
`execution/`, `strategies/`, `signals/`, `broadcast/`, or
`translation/`. TASK 4 will add one new, type-only import:
`ai_layer.ai_service.content.content_schema.ContentResult` — allowed, since `ai/content/`
sits immediately upstream of `media/` in the Official Intelligence
Pipeline (`... → Content → Media → Broadcast`, `docs/roadmap/AI_EVOLUTION.md`).
`media/` will continue to never import `broadcast/` or `translation/`
this phase (both downstream/parallel, TASK 8's isolation test
enforces this permanently).

The Director's own brief visualizes `Translation` as
"Future/Parallel" to `Media` rather than strictly before it (the
Phase 63.3 Director Decision's diagram placed
`... Content → Translation → Media → Broadcast`). This phase does not
touch `translation/` at all — `media/` neither imports it nor is
imported by it — so this is a documentation-visualization note, not a
code conflict; no Director Decision pause required.

## Trading Core Isolation

`git diff --stat -- core/ decision/ risk/ execution/ strategies/
signals/` — zero output before any change this phase. Nothing in
`media/`'s existing or planned files imports any of these six
directories.

## Conclusion

No Constitution Article conflict. TASK 1 (`MediaAsset`/`MediaAssetStatus`
model), TASK 2 (`get()`/`exists()` on the registry), TASK 3
(`MediaManager` extended with `create_asset`/`validate_asset`/
`prepare_asset`/`get_asset`), and TASK 4 (`content_result_to_media_asset()`
adapter) are the four genuine pieces of new/extended work this phase
does — all inside the real, existing top-level `media/` package.
Requesting no Director Decision.
