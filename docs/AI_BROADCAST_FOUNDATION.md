# GoldBot — AI Broadcast Foundation

Phase 63.0 (Senior Trading AI Foundation), TASK 4/5/6/7. Foundation
only. No real API/OBS/RTMP/streaming/TTS/voice/image/video/translation
call anywhere in any package this document describes (Rules 2/3/4).

## Package map

```
Content (ai/content/) -> Broadcast (broadcast/) -> Media (media/)
                                                  -> Translation (translation/)
```

### `broadcast/` — new top-level package (TASK 4)

Why top-level, not `ai/broadcast/`: see
`docs/PHASE63_0_FOUNDATION_AUDIT.md` — channel/delivery management is
a genuinely different responsibility than AI content generation, the
same reasoning that keeps `execution/` separate from `decision/`.

- `models.py` — `BroadcastProviderType` (YOUTUBE/OBS/RTMP/TWITCH/KICK/
  CUSTOM), `BroadcastProviderStatus` (ENABLED/DISABLED),
  `BroadcastTrigger`, `BroadcastRequest`.
- `provider_manager.py` — `BroadcastProviderManager`: static catalog
  of the six channel types, all `DISABLED` by default.
- `trigger_manager.py` — `BroadcastTriggerManager`: Owner-armed intent
  per `ContentType`, nothing armed by default.
- `broadcast_manager.py` — `BroadcastManager.would_broadcast()`/
  `prepare()`. `prepare()` only ever builds a `BroadcastRequest`
  value — it never sends one anywhere.

### `media/` — new top-level package (TASK 5)

- `media_types.py` — `MediaType` (TEXT/VOICE/IMAGE/VIDEO/LIVE).
- `media_registry.py` — static catalog.
- `media_manager.py` — `MediaManager`: `TEXT` starts enabled (the only
  type this codebase actually produces today); everything else starts
  disabled.

### `translation/` — new top-level package (TASK 6)

- `models.py` — `Language` (UZ/RU/EN), `TranslationRequest`,
  `TranslationResult`.
- `language_registry.py` — static catalog of the three languages.
- `translation_manager.py` — `TranslationManager.translate()` always
  returns a cleanly rejected result this phase — never echoes or
  fabricates a translation.

### `telegram/owner/broadcast_commands.py` — Owner commands (TASK 7)

`/broadcast_status`, `/broadcast_provider`, `/broadcast_enable`,
`/broadcast_disable` — every one returns `NOT IMPLEMENTED`. Not
registered in `telegram/commands.py`'s `OWNER_COMMANDS`, not dispatched
by `telegram/command_router.py`/`telegram/handlers.py` (Rule 7 — same
"foundation, backend not wired" posture
`telegram/owner/provider_commands.py` originally used).

## Capability vocabulary (TASK 8)

Four new, purely additive `Capability` members:
`AI_CONTENT`/`AI_MEDIA`/`AI_TRANSLATION`/`AI_BROADCAST`. No
`ai/router/router.py` selection-logic change; `ai/router/routing_rules.py`
(declarative data) gained one entry per new capability, same as every
prior capability addition. No `ai/runtime/ai_service.py`
`_CAPABILITY_METHOD` mapping — all four are cleanly rejected by
`AIService.ask()` until a future phase adds real dispatch.

## What none of this does yet

- No YouTube/OBS/RTMP/Twitch/Kick client or connection.
- No TTS, voice synthesis, image generation, or video processing.
- No Google/DeepL/Gemini/OpenAI translation call.
- No Owner command is wired to a real backend.
- Trading pipeline (`core/pipeline.py`, `decision/`, `risk/`,
  `execution/`, `strategies/`): zero diff.

## Related

- `docs/PHASE63_0_FOUNDATION_AUDIT.md`
- `docs/PHASE63_0_FREEZE.md`
- `docs/AI_CONTENT_FOUNDATION.md`
- `docs/AI_PERSONA.md`
