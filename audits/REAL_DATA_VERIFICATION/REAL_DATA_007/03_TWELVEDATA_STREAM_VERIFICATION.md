# REAL-DATA-007 — 03. TwelveData Stream Verification

## Tekshirilgan fayl
`data_layer/providers/twelve_data_client/twelve_data_client.py`

## Dalillar (file:line)
- `BASE_URL = "https://api.twelvedata.com/time_series"` (:28) — yagona
  endpoint, candle/vaqt-qatori.
- Yagona data metodi: `fetch_candles(symbol, interval, outputsize)` (:60).
- `/price` metodi — **YO'Q**. `/quote` metodi — **YO'Q**. `get_price()`,
  `get_quote()`, `fetch_price()`, `fetch_quote()` — reponing butun
  `data_layer/` bo'yicha manba kodida mavjud emas (grep: faqat `.pyc`
  keshlarida "price" so'zi uchraydi, hech qanday current-price metodi
  ta'rifi yo'q).
- `INTERVAL_MAP` (:31-39): `{M5:5min, M15:15min, H1:1h, H4:4h, Daily:1day}`.
  **M1 (1min) YO'Q.**
- Qo'llab-quvvatlanmagan interval → `ValueError` (:66-70).

## Vendor vs Repo
- TwelveData VENDOR haqiqatda `/price` va `/quote` real-time
  endpoint'larini taklif qiladi.
- Lekin GoldBot REPO ularni **amalga oshirmagan**.
- Ularni qo'shish = YANGI API arxitekturasi (yangi client metodi + yangi
  PriceProvider). CLAUDE.md Trading Safety + Module Reuse Principle +
  Direktor Review talab qiladi — bu audit doirasida TAQIQLANGAN.

## Xulosa
TwelveData integratsiyasi butunlay candle-shaped. Repoda hech qanday
current-price/quote kontrakti yo'q. Price Stream shu candle client
ustiga qurilgan → Price Stream candle polling.
