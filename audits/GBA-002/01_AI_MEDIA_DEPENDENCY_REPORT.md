# GBA-002 — TASK-01: AI -> Media Dependency Report

## Muammo

GBA-001'ning `16_DIRECTOR_RECOMMENDATIONS.md` (Savol 1) va
`18_VPS_READINESS_VERDICT.md` (Required Fix #2) `ai_layer ->
media_layer.telegram_broadcast` importini "hujjatlashtirilmagan
chegara" sifatida qayd etgan edi, lekin funksional xavfsizligini
to'liq isbotlamagan. Ushbu hujjat GBA-002 doirasida shu importni
to'liq Evidence bilan qayta tekshiradi.

## Topilgan barcha import joylari (Grep bilan)

`ai_layer/`ning quyidagi 4 faylida `media_layer.telegram_broadcast`dan
import mavjud:

1. `ai_layer/ai_engine/intelligence_runtime.py:53-54`
   ```
   from media_layer.telegram_broadcast.broadcast_adapter import broadcast_asset_from_content_and_media
   from media_layer.telegram_broadcast.broadcast_manager import BroadcastManager
   ```
2. `ai_layer/vision_ai/content_adapter.py:34-36`
   ```
   from media_layer.telegram_broadcast.broadcast_adapter import broadcast_asset_from_content_and_media
   from media_layer.telegram_broadcast.broadcast_manager import BroadcastManager
   from media_layer.telegram_broadcast.models import BroadcastAsset
   ```
3. `ai_layer/ai_engine/trading_analyst/content_adapter.py:29-31`
   ```
   from media_layer.telegram_broadcast.broadcast_adapter import broadcast_asset_from_content_and_media
   from media_layer.telegram_broadcast.broadcast_manager import BroadcastManager
   from media_layer.telegram_broadcast.models import BroadcastAsset
   ```
4. `ai_layer/voice_ai/adapter.py:32`
   ```
   from media_layer.telegram_broadcast.models import BroadcastAsset, BroadcastStatus
   ```

Qo'shimcha: `ai_layer/ai_engine/trading_analyst/CONTRACTS.md:36` ushbu
Dependency'ni hujjat darajasida allaqachon ro'yxatga olgan (lekin
`docs/ARCHITECTURE.md`da yo'q — quyida `03_LAYER_BOUNDARY_VERIFICATION.md`da
tafsilot berilgan).

## Call site'lar (funksiya darajasida)

- `intelligence_runtime.py:179-183` — `IntelligenceRuntime.run()`
  ichida, `broadcast_asset_from_content_and_media()` chaqiriladi, so'ng
  natija `self._broadcast.prepare_broadcast(broadcast_asset)`ga
  uzatiladi (`self._broadcast` — `BroadcastManager` instansi).
- `trading_analyst/content_adapter.py:75-80` — `prepare_content()`
  funksiyasi xuddi shu ikki chaqiruvni bajaradi:
  `broadcast_asset_from_content_and_media(...)` va
  `broadcast_manager.prepare_broadcast(broadcast_asset)`.
- `vision_ai/content_adapter.py:91` — bir xil naqsh (`prepare_content()`
  ekvivalenti, vision content uchun).
- `voice_ai/adapter.py:32` — faqat `BroadcastAsset`/`BroadcastStatus`
  DTO klasslarini import qiladi, `BroadcastManager`ni chaqirmaydi
  (eng cheklangan foydalanish holati).

## Xulosa (qisqacha)

Barcha 4 fayl `media_layer.telegram_broadcast`dan faqat DTO
qurish (`BroadcastAsset`) va holat o'tkazish (`prepare_broadcast()`
— DRAFT -> READY/FAILED) uchun foydalanadi. Hech bir call site
`platform_layer/telegram/`ga yoki har qanday tarmoq/SDK chaqiruviga
yo'l ochmaydi — to'liq dalil `02_RUNTIME_CALL_GRAPH.md`da.

**Verdict: Variant A (Allowed)** — `AI -> Media DTO -> Broadcast Queue
-> Media Layer -> Telegram` naqshiga mos keladi; `ai_layer` hech qachon
Telegram send'ni to'g'ridan-to'g'ri yoki bilvosita ishga tushirmaydi.
