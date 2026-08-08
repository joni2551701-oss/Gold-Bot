# 01 — Joriy narx (current price) kontrakti

**Buyruq:** REAL-DATA-008 — TwelveData `/price` real-time endpoint orqali
HAQIQIY joriy narx oqimi (REAL-DATA-007 Option A tasdiqlangan).

## `/price` endpoint kontrakti

- **URL:** `https://api.twelvedata.com/price` (`TwelveDataClient.PRICE_URL`).
  Bu `/time_series` (candle) endpointidan (`BASE_URL`) TUBDAN farq qiladi —
   hech qachon qayta ishlatilmaydi.
- **Parametrlar:** `symbol` (masalan `XAU/USD`, mavjud `_format_symbol()`
  bilan `XAUUSD`→`XAU/USD` ga aylantiriladi) va `apikey`. API kaliti FAQAT
  params ichida — hech qachon log/print/message matniga chiqmaydi.
- **Muvaffaqiyatli javob:** `{"price": "<num>"}` → `float`.
- **Xato javob:** `{"status":"error", "code":..., "message":...}`.
  `code == 429` (rate-limit) → `fetch_candles()` bilan bir xil eksponensial
  backoff; boshqa kodlar → `ValueError`.
- **Tarmoq xatosi:** `max_retries` (3) urinishdan keyin `ConnectionError`.
- **Kalit yo'q:** `ValueError("TWELVE_DATA_API_KEY not configured.")`.

## PriceUpdate (tick) vs Candle — ajratish

| Xususiyat        | Candle (`fetch_candles`)          | Current price (`/price`)          |
|------------------|-----------------------------------|-----------------------------------|
| Manba            | `/time_series` (OHLC)             | `/price` (spot)                   |
| Qiymat           | `candle.close`                    | joriy real spot narx              |
| Vaqt             | candle timestamp'i               | kuzatuv vaqti `now(utc)`          |
| Chastota         | faqat candle yopilganda          | har `read()` da yangi kuzatuv     |
| Dedupe           | candle timestamp bo'yicha        | YO'Q (takror narx ham haqiqiy tick) |

Bu ajratish REAL-DATA-008 ning mohiyati: STREAM manbasi endi candle.close
emas, HAQIQIY joriy narxni beradi.

## Batch/trading yo'liga tegilmadi

`MarketDataService.get_candles()` (M15 candle yo'li, REAL-DATA-003/004)
`fetch_candles()` dan foydalanadi va o'zgarmagan. REAL-DATA-008 FAQAT
STREAM manbasini (`tick()`/polling yo'li) o'zgartiradi.
