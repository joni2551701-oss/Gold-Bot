# 18 — REAL-DATA-003 Runtime Trace (Tekshirilgan)

Director Order REAL-DATA-003 bo'yicha jonli trading pipeline'ning
market candle iste'mol yo'li `file:line` aniqligida tekshirildi. Har bir
da'vo quyida haqiqiy manba kodiga solishtirib tasdiqlangan.

## Trace (VERIFIED)

| # | Joy | Fakt | Holat |
|---|-----|------|-------|
| 1 | `core_layer/pipeline/pipeline.py:219` (o'zgartirishdan oldin) | `self.data_normalizer = MarketDataService()` — `memory_registry` YO'Q holda quriladi (root cause) | TASDIQLANDI |
| 2 | `core_layer/pipeline/pipeline.py:303` | `candles = self.data_normalizer.get_candles(self.symbol, self.interval, self.outputsize)` — PRIMARY execution-timeframe candle; Core/Context/Strategy/Signal/Decision/Risk shu candle'lar ustida savdo qiladi | TASDIQLANDI |
| 3 | `core_layer/pipeline/pipeline.py:333` | `htf_snapshot = self.data_normalizer.get_snapshot(self.symbol, list(SUPPORTED_HTF_TIMEFRAMES))` — ALOHIDA best-effort HTF-bias fetch | TASDIQLANDI |
| 4 | `pipeline.py:325-331` (kommentariy) | HTF bias context-only; hozircha undan keyin hech narsa bog'liq emas | TASDIQLANDI |
| 5 | `data_layer/live_data/market_data_service/market_data_service.py:78` | `get_candles()` — MarketDataNormalizer orqali fetch+validate, registry mavjud bo'lsa `_hydrate_memory()` bilan memory'ga yozadi | TASDIQLANDI |
| 6 | `market_data_service.py:114` | `get_candles_from_memory()` — `MemoryReader` orqali memory'dan candle'ni QAYTA o'qiydi, `record.to_candle()` bilan `List[Candle]` qaytaradi; fail-safe (miss'da `[]`, hech qachon raise qilmaydi) | TASDIQLANDI |
| 7 | `market_data_service.py:176` | `get_shared_market_data_service()` — shared `MarketMemoryRegistry`ga ulangan xizmat quradi | TASDIQLANDI |
| 8 | `market_data_service.py:199` | `reset_shared_market_data_service()` — test isolation uchun mavjud | TASDIQLANDI |
| 9 | `data_layer/market_memory/market_memory_registry/market_memory_registry.py:31-38` | `DEFAULT_TIMEFRAME_CAPACITY = {M1:500, M5:300, M15:200, H1:200, H4:100, D1:100}` — "D1", "Daily" EMAS | TASDIQLANDI |
| 10 | `context_layer/trend/htf_bias/htf_bias.py:38` | `SUPPORTED_HTF_TIMEFRAMES = ("Daily", "H4", "H1")` — "Daily" memory default set'ida YO'Q (u yerda "D1"). Bu — HAZARD | TASDIQLANDI |
| 11 | `config.py:224` | `TIMEFRAME_HISTORY` fetch chuqurliklari (M5=200, M15=200, H1=200, H4=100, Daily=100) | TASDIQLANDI |

## Capacity vs fetch depth (truncation tekshiruvi)

Memory orqali yo'naltirilgan primary timeframe (M15): capacity 200,
fetch depth 200 — teng, **truncation YO'Q**. Boshqa timeframe'lar ham
memory capacity >= fetch depth shartiga mos (M5: 300>=200, H1: 200>=200,
H4: 100>=100).

## Root cause (bir jumlada)

Pipeline `MarketDataService()`ni `memory_registry`siz qurgani uchun
`get_candles()` faqat MarketDataNormalizer'ning to'g'ridan-to'g'ri
chiqishini qaytaradi va Market Memory (SSOT) hech qachon Core tomonidan
o'qilmaydi — memory yoziladi (hech kim registry bermaganida u ham yo'q),
lekin qayta o'qilmaydi.
