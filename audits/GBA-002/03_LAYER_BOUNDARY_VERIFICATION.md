# GBA-002 — TASK-01: Layer Boundary Verification

## Layer Boundary (ARCHITECTURE.md'dagi hujjatlashtirilgan yo'nalish)

CLAUDE.md'ning Architecture Rules bo'limi qatlam zanjirini shunday
belgilaydi:

```
data/ -> context/ -> strategies/ -> signals/ -> ai/ -> decision/ -> risk/ -> telegram/ -> database/
```

`docs/ARCHITECTURE.md`da `ai_layer -> media_layer` chetini alohida
qidirsak (`grep -n "media_layer" docs/ARCHITECTURE.md`) — natija:
`ai_layer`ning media_layer'ga bog'liqligi haqida hech qanday rasmiy
diagram/matn topilmadi (faqat `ai_layer`ning ichki modullari — masalan
`knowledge_ai/`, `ai_analyzer.py` — tilga olingan, `media_layer`
bilan chegara emas).

**Xulosa:** `ai_layer -> media_layer.telegram_broadcast` cheti
`docs/ARCHITECTURE.md`da rasmiy ravishda hujjatlashtirilmagan — bu
GBA-001'ning MAJOR-001 topilmasini tasdiqlaydi (kod ishlaydi,
funksional xavfsiz — Variant A — lekin arxitektura hujjati bilan
mos emas).

## Ownership (kim egalik qiladi)

- `BroadcastAsset` DTO va `BroadcastManager` klassi — `media_layer/
  telegram_broadcast/`ga tegishli (fayl joylashuvi, `MODULE_MAP.md`,
  `CONTRACTS.md` shuni ko'rsatadi).
- `media_layer/telegram_broadcast/broadcast_manager.py`ning o'zi
  **teskari yo'nalishda** `ai_layer.ai_service.content.broadcast_output.
  BroadcastReadyContent` va `ai_layer.ai_service.content.
  content_type_vocabulary.ContentType`dan import qiladi (satr 30-31).
  Bu — `media_layer -> ai_layer` importi, ya'ni ikkala qatlam ham
  bir-biridan import qiladi (ikki tomonlama bog'liqlik). Bu holat
  `ai_layer -> media_layer` chetidan mustaqil, alohida topilma
  sifatida qayd etiladi (quyida).

## Public API / Contract

`ai_layer/ai_engine/trading_analyst/CONTRACTS.md:36` `media_layer.
telegram_broadcast`ni bog'liqlik sifatida ro'yxatga olgan — ya'ni
modul darajasidagi CONTRACTS.md hujjati bu chegarani biladi va
kutilgan deb belgilaydi. Ammo bu faqat bitta modulning (`trading_
analyst/`) o'z CONTRACTS.md fayli — repozitoriy darajasidagi rasmiy
`docs/ARCHITECTURE.md`da mos yozuv yo'q. Demak, **modul darajasida
qisman hujjatlashtirilgan, repozitoriy darajasida yo'q** — aralash
holat.

## Data Flow (chegaradan qanday ma'lumot o'tadi)

O'tadigan narsa: `ContentResult` + `MediaAsset` (allaqachon
`media_layer.content_manager`/`media_layer.media_manager` orqali
yaratilgan obyektlar) -> `BroadcastAsset` (DRAFT) -> `prepare_
broadcast()` orqali `READY`/`FAILED` holatiga o'tkaziladi. Bu — sof
ma'lumot (metadata + status enum), tarmoq chaqiruvi yoki buyruq emas.
`ai_layer` faqat shu DTO'ni yaratish/holatini o'tkazish uchun
`media_layer`ning ochiq (public) klasslaridan foydalanadi — `media_
layer`ning ichki implementatsiya detallariga kirmaydi.

## Qo'shimcha topilma — ikki tomonlama Layer bog'liqligi (yangi, GBA-001'da qayd etilmagan)

`media_layer/telegram_broadcast/broadcast_manager.py:30-31`:
```python
from ai_layer.ai_service.content.broadcast_output import BroadcastReadyContent
from ai_layer.ai_service.content.content_type_vocabulary import ContentType
```

Bu `media_layer -> ai_layer` importi mavjudligini anglatadi — CLAUDE.md
"Keep modules isolated: ... `ai/` doesn't import `database/`, etc."
qoidasi aynan shu importni nomlab ko'rsatmagan, lekin "Module talks to
the layer immediately below it, never reaches two layers down" umumiy
tamoyili nuqtai nazaridan, `ai_layer <-> media_layer` ikki tomonlama
import — arxitektura diagrammasidagi bir yo'nalishli qatlam zanjiriga
mos emas. Bu **Variant B emas** (hech qanday Telegram send yo'q, faqat
DTO klasslarini import qilish), lekin **Layer Direction** nuqtai
nazaridan alohida dokumentatsiya-qarz topilmasi sifatida qayd etiladi.
GBA-001'ning Variant 1 tavsiyasi (ARCHITECTURE.md'ni yangilash) shu
ikki tomonlama holatni ham qamrab olishi kerak.

## Yakuniy Verdict

- **Runtime xavf: yo'q.** `ai_layer -> media_layer.telegram_broadcast`
  — Variant A (Allowed), Telegram send'ga hech qanday yo'l yo'q.
- **Layer Boundary hujjat darajasida:** buzilgan emas (funksional),
  lekin **hujjatlashtirilmagan** (`docs/ARCHITECTURE.md`da yo'q) —
  GBA-001 MAJOR-001 hali ochiq.
- **Yangi topilma:** `media_layer -> ai_layer` teskari importi ham
  hujjatlashtirilmagan va ARCHITECTURE.md yangilanganda hisobga
  olinishi kerak.
