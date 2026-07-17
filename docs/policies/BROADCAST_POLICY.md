# Broadcast Policy

Governs `broadcast/`, `media/`, and `translation/` (Phase 63.0
Foundation) until a separately-approved phase wires any of them to a
real backend.

## No real integration without explicit approval

None of the following exists anywhere in this codebase today, and
none may be added without a dedicated Director-approved phase naming
it explicitly:

- A YouTube, OBS, RTMP, Twitch, or Kick API client or connection.
- TTS/voice synthesis, image generation, or video processing.
- A Google/DeepL/Gemini/OpenAI translation call.

`BroadcastProviderType`'s six members (YOUTUBE/OBS/RTMP/TWITCH/KICK/
CUSTOM) are enum vocabulary describing *what kind of channel a Broadcast
Provider descriptor represents* — never an import of, or connection to,
any of those services.

## Default-off, always

Every `BroadcastProviderManager` entry starts `DISABLED`. Every
`BroadcastTriggerManager` entry starts disarmed. `MediaManager` starts
only `TEXT` enabled (the one type this codebase actually produces
today). `TranslationManager.translate()` always returns a cleanly
rejected result — it never echoes the input or fabricates a
translation. A future phase that flips any of these defaults on is
itself the kind of change Article 9's Version Compatibility Law and
this policy both require explicit, dedicated Director approval for.

## `prepare()` builds a value, never sends one

`BroadcastManager.prepare()` returns a `BroadcastRequest` — pure data.
No code path in this codebase calls it from a live process loop, and
adding one is real wiring, not a foundation change.

## Related

- `docs/constitution/CONSTITUTION.md` Article 9.
- `docs/AI_BROADCAST_FOUNDATION.md` — the concrete package map.
- `docs/PHASE63_0_FREEZE.md`.
