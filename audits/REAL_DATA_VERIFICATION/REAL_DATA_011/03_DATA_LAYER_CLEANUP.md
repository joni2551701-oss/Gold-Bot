# 03 — Data-Layer Cleanup (REAL-DATA-011, Item B)

## Ikki contract toza ajratilganmi? — HA

- **Current-price contract (/price, 008):** `TwelveDataPriceSource`
  (`data_layer/live_data/twelve_data_price_source/twelve_data_price_source.py:49`),
  production'da `PriceStreamService.register_source("XAUUSD",
  TwelveDataPriceSource(...))` orqali ulanadi
  (`price_stream_service.py:245`).
- **Candle contract (M5/M15/H1/H4/Daily):** batch `data_normalizer.
  get_candles()`, Pipeline tomonidan o'qiladi (`pipeline.py:325`).

Ikkalasi alohida modul, alohida import grafi. **Aralashmaydi.**

## Eski candle-close stream source `TwelveDataProvider` tasnifi

MUHIM: repoda **ikkita** `TwelveDataProvider` sinfi bor —
adashtirmaslik kerak:

1. **`data_layer/providers/twelve_data_provider/` `TwelveDataProvider`
   (MarketDataProvider)** — batch candle provider. Registry
   (`registry.py:103`), provider factory (`providers/__init__.py:65`)
   va testlar ishlatadi. → **PRODUCTION** (batch candle path). KEEP.

2. **`data_layer/live_data/twelve_data_provider/` `TwelveDataProvider`
   (PriceProvider)** — 008 `TwelveDataPriceSource` bilan
   ALMASHTIRILGAN M1-defaulted eski stream source. Import grafi:
   - Production consumer: **YO'Q** (grep butun repo: faqat
     `price_stream_service.py:20` — bu **izoh/docstring**, import emas).
   - Test reference: **BOR** —
     `tests/data/stream/test_twelve_data_provider.py:12`.
   - Production wiring `TwelveDataPriceSource` ishlatadi
     (`price_stream_service.py:245`), bu eski sinfni EMAS.

   → **TASNIF: TEST-ONLY** (production'da o'lik, ammo testi bor).

## Removal qarori (airtight-proof qoidasi)

Eski `live_data/twelve_data_provider` sinfini **O'CHIRMASLIK**:
airtight-proof qoidasining (2)-sharti buziladi — **test reference bor**
(`test_twelve_data_provider.py`). Shuning uchun **CLASSIFY-AND-DEFER**:

> **Tavsiya (keyingi ko'rib chiqilgan pass uchun):** agar Director eski
> M1-stream sinfini butunlay olib tashlashni istasa, avval uning testi
> (`tests/data/stream/test_twelve_data_provider.py`, ~test soni)
> olib tashlanadi, keyin sinf va moduli o'chiriladi. Bu RC1 oldidan
> qilinmaydi — non-orphan (testi bor), xavf-foyda nomutanosib.

## Xulosa

Current-price va candle contract'lari **toza ajratilgan (HA)**. Eski
stream `TwelveDataProvider` = **TEST-ONLY**, o'chirilmaydi
(test reference), keyingi pass uchun tavsiya qilinadi.
