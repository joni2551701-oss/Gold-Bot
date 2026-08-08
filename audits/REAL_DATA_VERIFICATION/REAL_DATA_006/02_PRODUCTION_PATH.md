# REAL-DATA-006 — 02. Production Path (Qaysi PriceStreamService production)

## Savol: `main.py` mi yoki `polling.py` mi Price Stream'ni haydaydi?

**Javob: `polling.py`.**

- `main.py` — bir martalik (one-shot) pipeline ishga tushiruvchi. U
  `TradingPipeline.run()` ni chaqiradi va tugaydi; u Price Stream
  `tick()` loop'ini haydamayapti. Bu REAL-DATA-004'da E2E trace
  qilingan yo'l.
- `platform_layer/telegram/polling.py` — uzoq yashovchi (long-lived)
  jarayon. `run_polling()` ichida `_price_stream_tick_loop`
  (`polling.py:287`) `_heartbeat_loop` yonida `asyncio.create_task`
  bilan ishga tushiriladi (`polling.py:339`) va cheksiz aylanadi
  (`polling.py:305-311`), har `PRICE_STREAM_TICK_INTERVAL_SECONDS`
  (`polling.py:116`) da `get_shared_price_stream_service().tick(now)`
  (`polling.py:308`) ni chaqiradi.

Demak Price Stream **live Telegram jarayonida** production-wired.

## Production instance vs duplicate/dead/foundation

| Komponent | Yagona/Dublikat | Status |
|---|---|---|
| `price_stream_service/price_stream_service.py` `PriceStreamService` | Yagona (grep: bitta `price_stream_service.py`) | PRODUCTION |
| `get_shared_price_stream_service()` (`:252`) | Process-wide singleton (`_shared_service`, `:249`) | PRODUCTION |
| `data_layer/live_data/price_stream/price_stream.py` `PriceStream` | Production state-machine PriceStream (service shu bilan quriladi) | PRODUCTION |
| `data_layer/live_data/stream/price_stream/price_stream.py` `PriceStream` | ALOHIDA legacy stream-layer PriceStream (router/validator/state — boshqa API) | FOUNDATION / production yo'lda ISHLATILMAYDI |
| `data_layer/live_data/stream_validator/` | Canonical validator (production import: `price_stream_service.py:233`) | PRODUCTION |
| `data_layer/live_data/stream/stream_validator/` | Legacy validator (faqat `stream/`-layer PriceStream ishlatadi) | FOUNDATION |

**Muhim:** repoda ikkita `PriceStream` va ikkita `StreamValidator`
mavjud. Production Price Stream zanjiri
`data_layer.live_data.price_stream.PriceStream` +
`data_layer.live_data.stream_validator.StreamValidator` juftligini
ishlatadi. `data_layer/live_data/stream/...` ostidagi juftlik alohida
Foundation modul bo'lib, production `tick()` yo'lida ishtirok etmaydi.
Bu dublikat emas — ikkalasi turli API kontraktlariga ega (biri
sink/provider/calendar asosli, ikkinchisi router/state asosli).

## Singleton semantikasi

`get_shared_price_stream_service()` birinchi chaqiruvda `MarketMemoryRegistry()`
bilan quriladi (`:276-278`), keyingi chaqiruvlar aynan shu instance'ni
qaytaradi. Shu sababli `polling.py` haydagan instance, `/price` uchun
`CurrentPriceProvider` o'qigan instance bilan bir xil — ticking real
kuzatiladi (agar tick real bo'lsa; M1 mismatch buni bloklaydi — 03 ga
qarang).
