# 02 — TwelveData Verification

Production-wired implementation: `data_layer/providers/twelve_data_client/twelve_data_client.py`
(`TwelveDataClient`), production yo'lida
`data_layer/live_data/market_data/market_data.py:26` orqali
`MarketDataNormalizer` ichida to'g'ridan-to'g'ri instantsiyalanadi (01-hujjatga qarang).

## CONFIRMED (kod o'qish orqali)

1. **Credential loading** — `TwelveDataClient.__init__()`
   (`twelve_data_client.py:39-46`): `self.secrets = Secrets()`,
   `self.api_key = self.secrets.TWELVE_DATA_API_KEY`
   (`core_layer/secrets/secrets.py:30-31` — `.env`dan `TWELVE_DATA_API_KEY`
   o'qiydi). Xato bo'lsa (`Exception`) `api_key = None`ga tushadi —
   crash bermaydi, keyinchalik har chaqiruvda tekshiriladi.

2. **Symbol mapping** — `_format_symbol()` (`twelve_data_client.py:48-54`):
   `"XAUUSD"` -> `"XAU/USD"` (6 belgili, "/" yo'q bo'lsa 3+3 split).
   Umumiy, XAUUSD, EURUSD va h.k. uchun ishlaydi.

3. **HTTP client** — `requests` kutubxonasi (`import requests`,
   `twelve_data_client.py:2`), `requests.get(self.BASE_URL, params=params,
   timeout=10)` (`twelve_data_client.py:87`). `BASE_URL =
   "https://api.twelvedata.com/time_series"` (`twelve_data_client.py:26`).

4. **Timeout** — `timeout=10` sekund, HTTP so'rov darajasida
   (`twelve_data_client.py:87`).

5. **Rate-limit handling** — `error_code == 429` bo'lsa
   `time.sleep(2 ** attempt)` bilan eksponensial backoff, `max_retries = 3`
   (`twelve_data_client.py:83,96-98`).

6. **Parsed response fields** — `Candle` dataclass (`twelve_data_client.py:11-19`):
   `timestamp` (UTC-aware `datetime`), `open`, `high`, `low`, `close`
   (barchasi `float`). **Bid/ask yo'q, volume yo'q** — Twelve Data
   `time_series` endpointi candle-based, tick/quote emas
   (`data_layer/providers/twelve_data_provider/twelve_data_provider.py:112-121`
   o'z docstring'ida buni ochiq e'tirof etadi: "not a live bid/ask").

7. **Error handling — HTTP failure**: `requests.exceptions.RequestException`
   ushlanadi, oxirgi urinishda `ConnectionError` chiqariladi
   (`twelve_data_client.py:118-122`).

8. **Error handling — API xato javobi**: `data.get("status") == "error"`
   bo'lsa, 429 bo'lmasa `ValueError(f"Twelve Data API Error: {error_message}")`
   chiqariladi (`twelve_data_client.py:91-95`).

9. **Error handling — bo'sh javob**: `values` bo'sh bo'lsa, `logger.warning`
   va `return []` (crash emas) — `twelve_data_client.py:101-103`.

10. **Error handling — noto'g'ri interval**: `interval not in
    self.INTERVAL_MAP` bo'lsa `ValueError` (`twelve_data_client.py:69-73`),
    chaqiruv amalga oshmasdan oldin tekshiriladi.

11. **Error handling — API key yo'q**: `self.api_key is None` bo'lsa
    `ValueError("TWELVE_DATA_API_KEY not configured.")`
    (`twelve_data_client.py:75-76`) — hech qanday tarmoq chaqiruvi
    qilinmaydi.

12. **Ikkinchi wrapper qatlami** (`data_layer/providers/twelve_data_provider/twelve_data_provider.py`)
    — `get_market_status()` (satr 116-124) API kalitini haqiqiy so'rov
    yubormasdan tekshiradi (`self.client.api_key is None`). Bu sessiyada
    API kalit yo'qligi sababli, bu metod `available=False` qaytaradi —
    kod real chaqiruv qilishga urinmaydi (fail-safe tasdiqlangan, keyingi
    band).

## BLOCKED (real tarmoq/kredensial talab qiladi)

- **Real HTTP so'rov/javob** — bloklangan (`403`,
  `api.twelvedata.com:443`, tashkilot siyosati). `curl` orqali
  tasdiqlangan: `CONNECT tunnel failed, response 403`.
- **Real narx dalili** (bid/ask/close qiymati) — 08-hujjatga qarang,
  BLOCKED.
- **Real API xato javoblarini amalda ko'rish** (masalan haqiqiy 429
  javobi) — faqat kod orqali (yuqoridagi 5, 8, 9-bandlar) tasdiqlangan,
  amalda sinalmagan.

## Xulosa

Kredensial yuklash, symbol mapping, timeout, retry/backoff va xato
qayta ishlash yo'llarining barchasi kod darajasida **CONFIRMED**. Real
tarmoq orqali ishlashi esa bu sessiyada **BLOCKED** — bu muhit
cheklovi, kod sifati muammosi emas.
