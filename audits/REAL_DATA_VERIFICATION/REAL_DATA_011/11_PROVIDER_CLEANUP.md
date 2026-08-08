# 11 — Provider Cleanup Classification (REAL-DATA-011, Item J)

TwelveData + Bitget implementatsiyalari real import grafi bilan.

## TwelveData

| Modul | Sinf | Tasnif | Dalil |
|---|---|---|---|
| `data_layer/providers/twelve_data_provider/` | `TwelveDataProvider(MarketDataProvider)` | **PRODUCTION** | registry `registry.py:103`, factory `providers/__init__.py:65`, tests |
| `data_layer/live_data/twelve_data_price_source/` | `TwelveDataPriceSource(PriceProvider)` | **PRODUCTION** (008 current-price) | `price_stream_service.py:245` |
| `data_layer/live_data/twelve_data_provider/` | `TwelveDataProvider(PriceProvider)` | **TEST-ONLY** (008 almashtirgan eski M1 stream) | faqat `tests/data/stream/test_twelve_data_provider.py:12` |
| `data_layer/historical_data/twelve_data_historical_provider/` | historical | **PRODUCTION** (historical fetch) | modul mavjud |

## Bitget

| Modul | Tasnif | Dalil |
|---|---|---|
| `data_layer/providers/bitget_provider/` | **FOUNDATION / inert** | registry'da ro'yxatdan o'tgan (`registry.py`), ammo XAUUSD trading yo'lida faol emas |
| `data_layer/live_data/.../BitgetPriceSource` | **FOUNDATION** | `price_stream_service.py:249` — BTCUSDT uchun, XAUUSD spine'dan tashqari |

**Bitget inert qoladi — implementatsiya qilinmaydi** (guardrail).

## Removal qarori

Airtight-proof qoidasi bo'yicha **hech narsa o'chirilmaydi**:
- PRODUCTION provider'lar — KEEP.
- TEST-ONLY eski stream `TwelveDataProvider` — test reference bor,
  o'chirilmaydi (03_ dagi CLASSIFY-AND-DEFER tavsiyasi).
- Bitget FOUNDATION — Director qarori bo'yicha inert, KEEP.

## Xulosa

Barcha provider'lar tasniflandi. O'chirish uchun airtight-orphan
YO'Q. KEEP + eski stream sinfi uchun keyingi-pass tavsiyasi.
