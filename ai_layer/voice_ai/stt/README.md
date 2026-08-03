# ai_layer / voice_ai / stt

**Module**

## Purpose

No module-level docstring was present in `__init__.py` at the time this file was generated (2026-08-03) by the Engineering Standard v1.0 rollout (Director Order No. 012/013). This is a placeholder pending a real description from a future Development Phase -- content below is limited to what could be verified mechanically from the code.

## Files

- `__init__.py`
- `contract.py` -- Voice Layer — STT Provider Contract (Phase 65.2, TASK 1).
- `manager.py` -- Voice Layer — STT Manager (Phase 65.2, TASK 1/2).
- `models.py` -- Voice Layer — Speech-To-Text Data Models (Phase 65.2, TASK 1).

## Responsibilities

See `CONTRACTS.md` and `MODULE_MAP.md` in this directory.

## Dependencies

See `CONTRACTS.md` in this directory for cross-layer dependencies (mechanically derived from actual imports).

## Public API

- `contract.py`: class `STTProviderError`
- `contract.py`: class `STTProviderTimeoutError`
- `contract.py`: class `STTProviderUnavailableError`
- `contract.py`: class `STTProviderInvalidResponseError`
- `contract.py`: class `STTProviderContract`
- `manager.py`: class `STTManager`
- `models.py`: class `STTResultStatus`
- `models.py`: class `STTRequest`
- `models.py`: class `STTResult`

---
*Generated 2026-08-03 by GoldBot Engineering Standard v1.0 rollout (Director Order No. 012/013). Documentation standardization only -- content mechanically derived from existing code, not authored from scratch.*
