# media/

Phase 63.0 (Senior Trading AI Foundation), TASK 5; extended Phase 63.7
(AI Media Intelligence Foundation). Foundation only.

## What this package is

- `media_types.py` — `MediaType` (TEXT/VOICE/IMAGE/VIDEO/LIVE).
- `media_registry.py` — static catalog, one `MediaDescriptor` per
  type; `get()`/`exists()` (Phase 63.7).
- `media_manager.py` — `MediaManager`, Owner-set ENABLED/DISABLED
  intent per type. `TEXT` starts enabled (the only type this codebase
  actually produces today); every other type starts disabled. Phase
  63.7 added a deterministic `MediaAsset` surface: `create_asset()`/
  `validate_asset()`/`prepare_asset()`/`get_asset()`.
- `models.py` (Phase 63.7) — `MediaAsset`/`MediaAssetStatus`
  (`PENDING`/`READY`/`REJECTED`).
- `media_adapter.py` (Phase 63.7) — `content_result_to_media_asset()`,
  a type-only read of an upstream `ai_layer.ai_service.content.content_schema.ContentResult`.
- `media_pipeline.py` (Phase 63.7) — `prepare_media_from_content()`,
  composes the adapter with `MediaManager.prepare_asset()`.

## What this package is not

No TTS/voice synthesis, no image generation, no video processing, no
streaming (Rule 3). No render/upload/publish call anywhere in this
package. This package tracks *intent* and *asset state* only.

## Related

- `ai/content/` — the immediately upstream package this package reads
  from (type-only, `media_adapter.py`).
- `broadcast/` — the delivery-channel counterpart to this package's
  media-type counterpart; a future phase composes both.
- `docs/ai/AI_MEDIA.md`, `docs/PHASE63_7_AUDIT.md`,
  `docs/PHASE63_7_FREEZE.md` — full documentation of this phase's
  extension.
