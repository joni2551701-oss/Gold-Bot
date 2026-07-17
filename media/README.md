# media/

Phase 63.0 (Senior Trading AI Foundation), TASK 5. Foundation only.

## What this package is

- `media_types.py` — `MediaType` (TEXT/VOICE/IMAGE/VIDEO/LIVE).
- `media_registry.py` — static catalog, one `MediaDescriptor` per type.
- `media_manager.py` — `MediaManager`, Owner-set ENABLED/DISABLED
  intent per type. `TEXT` starts enabled (the only type this codebase
  actually produces today); every other type starts disabled.

## What this package is not

No TTS/voice synthesis, no image generation, no video processing, no
streaming (Rule 3). This package tracks *intent* only.

## Related

- `broadcast/` — the delivery-channel counterpart to this package's
  media-type counterpart; a future phase composes both.
