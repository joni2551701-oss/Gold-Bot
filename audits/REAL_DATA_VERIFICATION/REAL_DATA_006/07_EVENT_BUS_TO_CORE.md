# REAL-DATA-006 — 07. Event Bus → Core (NOT WIRED)

## Xulosa: **FOUNDATION / NOT WIRED — published but unconsumed**

`PRICE_UPDATED` event chiqariladi (06), lekin uni **hech kim
iste'mol qilmaydi**. Core (TradingPipeline) data-layer event bus'iga
subscribe qilmaydi — u Market Memory'ni jadval bo'yicha o'qiydi
(REAL-DATA-003, registry-backed MarketDataService).

## Grep dalili (subscribe chaqiruvlari)

`grep -rn "\.subscribe(" --include=*.py` (tests tashqari) natijasi:

| file:line | Bus | EventType |
|---|---|---|
| `ai_layer/ai_service/audit/provider_stats.py:198-202` | **ALOHIDA** `ai_layer` event bus | CACHE_HIT, CACHE_MISS, VALIDATION_FAILED, PROVIDER_FAILED, PROVIDER_CHANGED |
| `platform_layer/telegram/owner/runtime_notifications.py:96-99` | AI runtime bus | PROVIDER_FAILED, PROVIDER_RECOVERED, RUNTIME_FAILED, RUNTIME_STATE_CHANGED |
| `data_layer/live_data/stream/price_stream/price_stream.py:78` | legacy stream router (`self.router.subscribe`) | — (Foundation stream, production emas) |

**`EventType.PRICE_UPDATED` ga birorta ham `.subscribe()` YO'Q.** Data
layer event bus'ida `PRICE_UPDATED`ga subscriber mavjud emas. AI
layer subscribe'lari butunlay boshqa bus va boshqa event turlari (AI
runtime metrics) — price bus emas.

## Nima uchun bu to'g'ri (design bo'yicha)

Order aniq talab qiladi: **Core'ni provider'ga qayta ulama, Event
Bus consumer QO'SHMA.** Core arxitekturasi (REAL-DATA-003) Market
Memory'ni SSOT sifatida jadval bo'yicha o'qishga asoslangan, event-driven
emas. `PRICE_UPDATED` — kelajakdagi event-driven consumer uchun
Foundation seam, hozircha ulanmagan.

## Status: **FOUNDATION / NOT WIRED (tasdiqlandi, ulanmadi)**

Ushbu segment ataylab ulanmagan. Auditda consumer QO'SHILMADI. Bu
REAL-DATA-006 verdiktining asosiy PARTIAL sababi (13 ga qarang).
