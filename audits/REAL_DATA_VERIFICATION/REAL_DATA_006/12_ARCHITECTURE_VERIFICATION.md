# REAL-DATA-006 — 12. Architecture Verification

## Layer boundary tekshiruvlari

| Savol | Natija | Dalil |
|---|---|---|
| `data_layer` `context`/`core`ni illegal import qiladimi? | **YO'Q** | `price_stream_service.py:49` docstring: "never imports from any layer above data/"; `twelve_data_provider.py:15`, `stream_validator.py:26` bir xil. Import'lar faqat `core_layer.logger` (logger utility) va `data_layer.*` |
| Core provider'ni qayta so'raydimi? | **YO'Q** | Core Market Memory'ni o'qiydi (REAL-DATA-003); Event Bus → Core NOT WIRED (07). Provider'ga to'g'ridan-to'g'ri qayta ulanish yo'q |
| Memory SSOT chetlab o'tilganmi? | **YO'Q** | Fold yagona writer CandleBuilder orqali (`price_stream_service.py:169-185`, 05). Ikkinchi yozuv yo'li yo'q |
| Foundation Freeze buzilganmi? | **YO'Q** | Auditda production `.py` o'zgartirilmadi; faqat probe + gated CI step qo'shildi |

## `core_layer.logger` importi — legal

`data_layer` `core_layer.logger.logger.setup_logger`ni import qiladi.
Bu logger utility (cross-cutting infrastructure), Layer contract
buzilishi emas — repo bo'ylab qabul qilingan naqsh (barcha layerlar
logger ishlatadi).

## Duplicate modul holati (02 dan)

Ikkita `PriceStream` va ikkita `StreamValidator` mavjud
(`live_data/price_stream/` + `live_data/stream/price_stream/`;
`live_data/stream_validator/` + `live_data/stream/stream_validator/`).
Bu GEL-001 canonical-package migratsiyasining natijasi — production
zanjiri faqat `live_data/price_stream/` + `live_data/stream_validator/`
juftligini ishlatadi. `stream/` ostidagilar alohida Foundation modul
(turli API kontrakti). Bu Violation emas — har biri o'z canonical
paketiga ega, lekin ikkita parallel stream implementatsiyasi mavjudligi
kelajakda konsolidatsiya nomzodi (backlog, ARCA emas — hozir buzilish
yo'q).

## Documentation finding (stale docstring)

`price_stream_service.py:47`: "nothing drives `tick()` in production"
— ESKIRGAN, `polling.py:308` haydaydi. Kod o'zgartirilmadi (audit-only);
hujjat yangilanishi kelajakdagi Documentation Evolution ishi sifatida
qayd etiladi (Order No. 016 Worker Authority ostida ruxsat etilgan,
lekin bu audit doirasida faqat topilma).

## Kod topilmasi (M1 mismatch) — arxitektura ta'siri

03-fayldagi M1 interval mismatch arxitektura buzilishi emas, balki
production wiring nuqsoni (`price_stream_service.py:238` default
`interval="M1"` vs client M5/M15/H1/H4/Daily). Layer chegaralari to'g'ri,
lekin runtime data oqimi bloklangan.

## Status: **Architecture PASS** (Layer boundary'lar buzilmagan, SSOT
chetlab o'tilmagan, Foundation Freeze saqlangan). Ikkita ochiq topilma:
(1) M1 wiring nuqsoni [kod, Director Review kerak], (2) stale docstring
[hujjat] — ikkalasi ham arxitektura PASS'ni buzmaydi.
