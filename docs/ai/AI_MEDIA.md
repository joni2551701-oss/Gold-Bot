# GoldBot — AI Media

Governed by `docs/constitution/CONSTITUTION.md` Article 1 and the
Intelligence Dependency Principle (Director Policy,
`docs/policies/DIRECTOR_POLICY.md`). `media/` (Phase 63.0, extended
Phase 63.7), real code, foundation-only — no live Telegram handler,
`translation/`, or `broadcast/` wires this up yet.

**`media/` is a top-level package, a sibling of `ai/` — not
`ai/media/`.** See `docs/PHASE63_7_AUDIT.md` for the naming
correction.

## Two surfaces on the same `MediaManager`

```
media/media_manager.py
  list_types()      Phase 63.0 -- unchanged
  descriptor_of()    Phase 63.0 -- unchanged
  is_enabled()        Phase 63.0 -- unchanged
  set_enabled()        Phase 63.0 -- unchanged (Owner intent toggle)
  create_asset()     Phase 63.7 -- deterministic, no external call
  validate_asset()    Phase 63.7 -- deterministic, no external call
  prepare_asset()      Phase 63.7 -- deterministic, no external call
  get_asset()            Phase 63.7 -- deterministic, no external call
```

Per `docs/PHASE63_7_AUDIT.md`'s own finding, `MediaManager` already
existed as the one real Manager for Media before this phase —
Constitution Article 11 forbade a second, competing class for the same
concern, so Phase 63.7's asset surface was added as new methods on the
same, LOCKed (since Phase 63.0) class, rather than a sibling class.
`list_types()`/`descriptor_of()`/`is_enabled()`/`set_enabled()` are
byte-for-byte unchanged.

## Position in the Official Intelligence Pipeline

```
Knowledge → Memory → Reasoning → Conversation → Explanation → Content → Media → Broadcast
```

(`translation/` sits parallel to this chain rather than strictly
before Media — this phase does not touch it either way.)

## Model

`media/models.py` (Phase 63.7): `MediaAssetStatus`
(`PENDING`/`READY`/`REJECTED`) and `MediaAsset` (`id`, `content_id`,
`media_type`, `status`, `title`, `description`, `metadata`,
`created_at`). `MediaType` (`media_types.py`, Phase 63.0:
`TEXT`/`VOICE`/`IMAGE`/`VIDEO`/`LIVE`) already existed and is reused
as-is — `MediaAsset` is the one genuine gap this phase's Foundation
Reuse Audit found. Every field is primitive, enum, or a plain dict —
no `ContentResult`, `DecisionResult`, `RiskResult`, `Trade`, `Order`,
or `Position` anywhere.

## Registry

`media/media_registry.py`'s `build_media_registry()`/`MediaDescriptor`
(Phase 63.0) is a fixed, five-entry static catalog — unchanged.
Phase 63.7 added `get(media_type)`/`exists(media_type)` (Article 9 —
additive-only); `register()` was deliberately not added since the
catalog is fixed by design (see `docs/PHASE63_7_AUDIT.md`'s naming
resolution).

## Content integration (TASK 4/5 — real, type-only)

`media/media_adapter.py`'s `content_result_to_media_asset(result, manager)`
reads an upstream `ContentResult`'s own already-public fields (`title`,
`body`, `content_type`, `metadata`) into a new `MediaAsset` via
`MediaManager.create_asset()` — never touches `ContentEngine`'s
internal state. `media/media_pipeline.py`'s
`prepare_media_from_content(result, manager)` composes that adapter
with `MediaManager.prepare_asset()` into the one-call flow the brief
names: `ExplanationOutput → ContentResult → MediaPreparation →
MediaAsset → (future provider)`. `ExplanationOutput → ContentResult`
remains `ai/content/`'s own job (`content_adapters.py`, Phase 63.6) —
neither Media module duplicates it.

## Capability / Router

`Capability.AI_MEDIA` (`ai/capabilities/capability.py`, Phase 63.0
TASK 8) and its entry in `ai/router/routing_rules.py`'s
`_CAPABILITY_PROVIDER_PREFERENCE` already existed — reused as-is, no
new capability, no router logic change (Phase 63.7 TASK 6/7).

## What it is not

- Not a rendering/upload/publish system — the four new methods only
  track `MediaAsset` state in memory; `MediaManager` has no
  `render()`/`upload()`/`publish()` method at all.
- Not real TTS/image/video generation — Rule 3 (Phase 63.0) and this
  phase's own TASK 7 both explicitly forbid any real media generation;
  every `MediaType` other than `TEXT` starts `DISABLED` and stays that
  way.
- Not a trading decision — `media/` is never imported by `core/`,
  `decision/`, `risk/`, `execution/`, or `strategies/`, and never
  imports any of them either (Constitution Article 3).
- Not Broadcast or Translation — `media/` never imports `broadcast/`
  or `translation/` (both downstream/parallel in the Intelligence
  Dependency Principle).
- Not wired into `telegram/command_router.py`, `translation/`, or
  `broadcast/` this phase — foundation only.

## Related

- `docs/PHASE63_7_AUDIT.md`, `docs/PHASE63_7_FREEZE.md` — TASK 0's
  audit and the phase this extension was built in.
- `docs/policies/DIRECTOR_POLICY.md` — the Intelligence Dependency
  Principle this package's own dependency direction is checked
  against.
- `docs/roadmap/AI_EVOLUTION.md` — the Official Intelligence Pipeline
  Media's position is defined by.
- `docs/ai/AI_CONTENT.md` — the immediately upstream package this
  package reads from.
