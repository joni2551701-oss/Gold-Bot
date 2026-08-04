# IMPLEMENTATION.md -- decision_layer/decision_service

## `decision_manager.py`

Decision — STEP-09 orchestrator (TASK-CORE-009).

Class'lar: `DecisionManager`

## `decision_router.py`

Decision — STEP-09 router (TASK-CORE-009).

Class'lar: `DecisionConsumer`

Top-level function'lar: `route()`, `route_values()`

## Runtime / Algorithms / Pipeline / Event Flow / Sequence / Design Decisions / Performance Notes

Rollout vaqtida yozilmagan -- bu bo'lim koddan mexanik ravishda chiqarib bo'lmaydigan domain tushunchasini talab qiladi va kelajakdagi Development Phase tomonidan to'ldirish uchun qoldirilgan (Director Order No. 012/013'ga ko'ra, bu rollout faqat hujjatlashtirish standartizatsiyasi, texnik bayonning yangi muallifligi emas).

---
*2026-08-03'da GoldBot Engineering Standard v1.0 rollout tomonidan yaratilgan (Director Order No. 012/013).*
