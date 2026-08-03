# ai_layer / voice_ai / stt / providers

**Module**

## Purpose

ai_layer.voice_ai.stt.providers — STT provider adapters.

Migrated from the pre-freeze voice/stt/providers/ package; internals
unchanged (SMR-001).

## Files

- `__init__.py` -- ai_layer.voice_ai.stt.providers — STT provider adapters.
- `custom.py` -- Voice Layer — Custom STT Provider Adapter Skeleton (Phase 65.2, TASK 2).
- `local.py` -- Voice Layer — Local STT Provider Adapter Skeleton (Phase 65.2, TASK 2).
- `openai.py` -- Voice Layer — Real OpenAI STT Provider Adapter (Phase 65.2, TASK 2).

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `custom.py`: class `CustomSTTProvider`
- `local.py`: class `LocalSTTProvider`
- `openai.py`: class `OpenAISTTProvider`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
