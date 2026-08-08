# REAL-DATA-006 — 05. Stream → Market Memory (single-writer fold)

## Transition

- **Input:** validated `StreamEvent` (`price_stream.py:243` `self._sink.on_event(e)`)
- **Processing:** `_PriceTickSink.on_event()`
  (`price_stream_service.py:85-113`) — tick'ni `PriceCache`ga yozadi
  (`:93`), `PRICE_UPDATED` publish qiladi (`:94-102`), so'ng
  `candle_builder.on_event(event)` orqali MarketMemory'ga folds
  (`:107-113`).
- **Output:** MarketMemory'dagi candle (yangilangan/hydrated).
- **NextConsumer:** `MemoryReader` (`get_last_candle` va h.k.) — Core
  shu orqali o'qiydi (REAL-DATA-003).

## Single writer (CandleBuilder) tasdiqlash

`price_stream_service.py:169-185` `_build_candle_builder()`: agar
`_memory_registry` mavjud bo'lsa,
`CandleBuilder(symbol, memory)`ni `registry.get_or_create(symbol)`
memory'si ustida quradi. Bu MarketMemory'ning **yagona hujjatlangan
yozuvchisi** (SINGLE WRITER, MA-001). Ikkinchi parallel yozuv yo'li
YO'Q — tick shu bir writer orqali folds.

`get_shared_price_stream_service()` (`:276-278`) default'da
`MarketMemoryRegistry()` bilan quriladi, shuning uchun production'da
memory fold FAOL (registry mavjud → `candle_builder` quriladi).

## Fail-safe

`price_stream_service.py:107-113`: `candle_builder.on_event()`
`try/except` ichida — memory yozuv xatosi cache/event yo'lini
buzmaydi (DD-051 posture). `_build_candle_builder` ham fail-safe
(`:181-185`) — qurilish muammosi `None`ga degrade bo'ladi (memory
yozuvsiz), stream ro'yxatga olishni bloklamaydi.

## Status: **PASS (kod yo'li REAL, single-writer, production-wired)**

Kod yo'li real va to'g'ri: validated tick → PriceCache → EventBus →
CandleBuilder → MarketMemory. Yagona yozuvchi buzilmagan, Memory SSOT
chetlab o'tilmagan.

**Ogohlantirish:** 03-fayldagi M1 mismatch tufayli XAUUSD uchun
production'da hech qanday validated tick sink'ga yetib bormaydi,
demak fold ham amalda ishga tushmaydi. Kod to'g'ri, lekin upstream
BLOCKED. Real fold dalili (memory read-back PASS) CI probe'dan keladi
(M1 tuzatilgach yoki M5/M15 wiring bilan).
