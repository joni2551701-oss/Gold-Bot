# REAL-DATA-006 — 01. Price Stream Audit (Umumiy ko'rinish)

**Vazifa:** GoldBot'ning mavjud live Price Stream runtime zanjirini
real TwelveData bilan tekshirish. Rejim: AUDIT-ONLY (faqat bitta yangi
probe script + gated CI step qo'shildi; hech qanday `.py` production
kodi o'zgartirilmadi).

## Trace (Provider → PriceStream → Validation → Market Memory → Event Bus → Core)

| Transition | Kod (file:line) | Status |
|---|---|---|
| tick() production driver | `platform_layer/telegram/polling.py:308` — `get_shared_price_stream_service().tick(now)` heartbeat yonidagi `_price_stream_tick_loop` ichida | PRODUCTION-WIRED |
| Shared instance | `data_layer/live_data/price_stream_service/price_stream_service.py:252` `get_shared_price_stream_service()` | PRODUCTION |
| Default wiring | `price_stream_service.py:212-246` `build_default_price_stream_service()` | PRODUCTION |
| XAUUSD source | `price_stream_service.py:238` `TwelveDataProvider(asset="XAUUSD")` (default `interval="M1"`) | REAL HTTP — lekin M1 mismatch (02/03/04 ga qarang) |
| Provider read | `twelve_data_provider.py:67-68` `TwelveDataClient.fetch_candles()` — real HTTP | REAL |
| Validation | `price_stream/price_stream.py:240,248-255` → `stream_validator/stream_validator.py:65` `StreamValidator.validate()` | PRODUCTION (drop-on-invalid) |
| Memory fold | `price_stream_service.py:107-113` → `CandleBuilder.on_event()` (single writer) | PRODUCTION |
| Event Bus publish | `price_stream_service.py:94-102` `EventBus.publish(PRICE_UPDATED, payload=PriceTick)` | PRODUCTION |
| Event Bus → Core | subscriber YO'Q (grep tasdiqlandi) | **FOUNDATION / NOT WIRED** |

## Asosiy topilmalar (qisqacha)

1. **tick() production'da haqiqatan ishlaydi** — `polling.py:308` uzoq
   yashovchi Telegram jarayonida `PRICE_STREAM_TICK_INTERVAL_SECONDS`
   (`polling.py:116`, `get_settings().stream.polling_interval`) bo'yicha
   `tick(now)` chaqiradi. Bu Foundation emas, real runtime driver.

2. **Stale docstring topildi (documentation finding).**
   `price_stream_service.py:47` docstring hali ham "nothing drives
   `tick()` in production" deydi — bu ESKIRGAN. `polling.py:308` uni
   haydaydi. Kod o'zgartirilmadi; faqat hujjat eskirganligi qayd
   etiladi (03/12 ga qarang).

3. **YANGI BLOKLOVCHI topilma — M1 interval mismatch (03/04).**
   Production `TwelveDataProvider(asset="XAUUSD")` default `interval="M1"`
   bilan quriladi (`twelve_data_provider.py:45`), ammo `TwelveDataClient`
   faqat M5/M15/H1/H4/Daily qo'llab-quvvatlaydi
   (`twelve_data_client.py:30-33,68`) — M1 `ValueError` bilan rad
   etiladi. `read()` har chaqiruvda `ValueError` beradi, `PriceStream`
   uni izolyatsiya qiladi (`price_stream.py` DD-051), natijada XAUUSD
   uchun **production'da hech qachon real tick tushmaydi**. Bu
   audit-only topilma — tuzatilmadi (Director Review kerak).

4. **Event Bus → Core NOT WIRED** — `PRICE_UPDATED` ga hech kim
   subscribe qilmaydi (07 ga qarang). Core (TradingPipeline) Market
   Memory'ni jadval bo'yicha o'qiydi (REAL-DATA-003), event-driven emas.

## Verdikt (13 da to'liq)

**PARTIAL / BLOCKED.** tick() → Validation → Memory fold → Event Bus
publish kod yo'llari REAL va production-wired, lekin: (a) Event Bus →
Core = FOUNDATION/NOT WIRED; (b) XAUUSD source M1 mismatch tufayli real
tick tushira olmaydi — continuous-update dalili BLOCKED (CI probe 0 real
update oladi, kutilganidek). To'liq honest verdikt 13-faylda.
