# broadcast/

Phase 63.0 (Senior Trading AI Foundation), TASK 4; extended Phase 63.8
(AI Broadcast Intelligence Foundation). Foundation only.

## Why this is a new top-level package (not under `ai/`)

`ai/content/broadcast_output.py` (Phase 61.5 TASK 6) is a narrow
adapter — one function, one dataclass — converting an accepted
`ContentResult` into `BroadcastReadyContent`. Nothing before this
phase managed broadcast *providers* (which channels exist, which are
Owner-enabled) or *triggers* (which content type is armed to go out).
Per `docs/PHASE63_0_FOUNDATION_AUDIT.md`'s Module Reuse Principle
check, both "does this exist?" and "can `ai/content/broadcast_output.py`
be extended into it?" were "no" — this package owns a genuinely
different, broader responsibility (channel/delivery management), the
same reasoning that keeps `execution/` a top-level package distinct
from `decision/`.

## What this package is

- `models.py` — `BroadcastProviderType` (YOUTUBE/OBS/RTMP/TWITCH/KICK/
  CUSTOM/TELEGRAM/MINI_APP — last two added Phase 63.8),
  `BroadcastProviderStatus` (ENABLED/DISABLED), `BroadcastProviderDescriptor`,
  `BroadcastTrigger` (gained `trigger_type: BroadcastTriggerType`,
  Phase 63.8), `BroadcastRequest`; `BroadcastStatus`/`BroadcastAsset`
  (Phase 63.8).
- `provider_manager.py` — `BroadcastProviderManager`, a static catalog
  of the eight provider types plus Owner-set ENABLED/DISABLED intent.
  Every provider starts `DISABLED`.
- `trigger_manager.py` — `BroadcastTriggerManager`, Owner-armed intent
  per `ai.content.content_types.ContentType`. Nothing is armed by
  default.
- `broadcast_manager.py` — `BroadcastManager`, composes the two above
  into `would_broadcast()`/`prepare()`. `prepare()` only ever builds a
  `BroadcastRequest` value — it never sends one anywhere. Phase 63.8
  added a deterministic `BroadcastAsset` surface: `create_broadcast()`/
  `validate_broadcast()`/`prepare_broadcast()`/`get_broadcast()`/
  `list_broadcasts()`.
- `broadcast_adapter.py` (Phase 63.8) — `broadcast_asset_from_content_and_media()`,
  type-only reads of an upstream `ai.content.content_schema.ContentResult`/
  `media.models.MediaAsset`/(optional) `ai.persona.persona.Persona`.

## What this package is not

- No YouTube API client, no OBS connection, no RTMP/Twitch/Kick SDK,
  no socket, no video, no stream (Rule 2). `grep -rn "youtube\|obs\|rtmp\|twitch\|kick" broadcast/` finds only the vocabulary names on
  the `BroadcastProviderType` enum, never a client import.
- No scheduling, no real delivery loop.
- No render/upload/publish/deliver call anywhere in this package —
  the Phase 63.8 asset surface only tracks `BroadcastAsset` state in
  memory.
- Not wired into `telegram/owner/broadcast_commands.py` yet — those
  commands report `NOT IMPLEMENTED` this phase (TASK 7).

## Related

- `docs/AI_BROADCAST_FOUNDATION.md` — the phase-level documentation.
- `ai/content/broadcast_output.py` — the upstream adapter this
  package's `BroadcastManager.prepare()` consumes as input.
- `docs/ai/AI_BROADCAST.md`, `docs/PHASE63_8_AUDIT.md`,
  `docs/PHASE63_8_FREEZE.md` — full documentation of this phase's
  extension.
