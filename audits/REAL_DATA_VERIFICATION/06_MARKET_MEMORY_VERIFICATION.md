# 06 — Market Memory (SSOT) Verification

## CONFIRMED: yozish yo'li faqat validatsiyadan o'tgan ma'lumot bilan

`MarketDataService._hydrate_memory()` (`data_layer/live_data/market_data_service/market_data_service.py:88-105`):
`candles` parametri `get_candles()`/`get_snapshot()` ichida
`self._normalizer.get_candles()`dan (validatsiyadan o'tgan,
`05`-hujjat) qaytgan natija — xom provayder javobi emas. Memory'ga
yozish `memory.timeframe(interval).hydrate(candles)` orqali amalga
oshadi (satr 102), faqat `self._memory_registry` mavjud va
`memory.has_timeframe(interval)` bo'lsa (satr 96-99).

## MUHIM TOPILMA: production `TradingPipeline` Market Memory'ni ishlatMAYDI

`core_layer/pipeline/pipeline.py:219`: `self.data_normalizer =
MarketDataService()` — **hech qanday `memory_registry` argumenti
uzatilmaydi**. `MarketDataService.__init__()`
(`market_data_service.py:69-76`) default qiymat `memory_registry=None`.
`_hydrate_memory()` (satr 96): `if self._memory_registry is None or
not candles: return` — shuning uchun bugungi production pipeline'da
**hech qanday candle Market Memory'ga yozilmaydi**. Bu modul
docstring'ida ochiq e'tirof etilgan (`market_data_service.py:44-49`):
*"The default (no registry) writes nothing -- so the TradingPipeline
instance, constructed as bare MarketDataService() in core/pipeline.py,
is byte-for-byte unchanged and keeps working exactly the old way (no
consumer reads memory yet)."*

Market Memory to'liq va real kod bilan qurilgan (`data_layer/market_memory/`
— `TimeframeMemory`, `MarketMemoryRegistry`, `MemoryReader`,
`memory_writer`, persistence qatlami va h.k.), va **`PriceStreamService`
orqali** yoziladi (`data_layer/live_data/price_stream_service/price_stream_service.py`
— tick'larni `candle_builder` orqali Memory'ga yozadi, testlar bilan
tasdiqlangan: `test_tick_folds_into_market_memory_via_candle_builder`
PASSED, 12-hujjat). Ammo bu — asosiy `TradingPipeline.run()` signal
yo'lidan **mustaqil**, alohida "live tick" oqimi.

## Xulosa

Market Memory (SSOT) infratuzilmasi real va ishlaydi, lekin bu audit
buyurtmasi qamrab olgan asosiy signal yo'li (`TradingPipeline.run()` ->
`MarketDataService` bare) uni **ishlatmaydi** — signal generatsiyasi
candle'larni to'g'ridan-to'g'ri `MarketDataNormalizer`dan oladi, Memory
orqali emas. Bu Foundation-mavjud-lekin-hot-path'ga-ulanmagan
holatining yana bir namunasi (04-hujjatdagi `ProviderManager` topilmasiga
o'xshash). Yangi ulash taklif qilinmaydi (Order talabiga ko'ra).
