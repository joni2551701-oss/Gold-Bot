# REAL-DATA-007 — 01. Price Stream Audit

## Vazifa
Direktor topshirig'i REAL-DATA-007: GoldBot Price Stream'ining HAQIQIY
kontraktini aniqlash — bu chinakam real-time narx oqimimi yoki candle-API
polling'ni "Price Stream" deb qayta nomlangan holimi.

## Markaziy javob (qisqacha)
GoldBot Price Stream — **candle-API polling** (TwelveData `/time_series`,
bitta candle, faqat yangi candle yopilganda emit qiladi). Bu chinakam
current-price / real-time tick oqimi **EMAS**.

## Tekshirilgan kod dalillari

### 1. Stream manbai = candle-close polling
`data_layer/live_data/twelve_data_provider/twelve_data_provider.py:67-88`
`read()` metodi:
```
candles = self._client.fetch_candles(self._asset, self._interval, outputsize=1)   # :68-69
...
if self._last_ts is not None and ts <= self._last_ts:   # :77
    return []                                            # :78  (dedupe)
...
return [StreamEvent(price=candle.close, ...)]            # :81-87
```
- Manba: candle (OHLC) endpoint, `outputsize=1` — eng oxirgi candle.
- `price = candle.close` — ya'ni **yopilgan candle close narxi**, tick emas.
- Faqat YANGI candle timestamp'i kelganda emit qiladi (dedupe :77-78).
- `supports_streaming=False, supports_polling=True` (:37-43) — provayder
  o'zi ham streaming emasligini e'lon qiladi.

### 2. Client'da faqat candle metodi bor
`data_layer/providers/twelve_data_client/twelve_data_client.py`:
- `BASE_URL = "https://api.twelvedata.com/time_series"` (:28) — candle/vaqt
  qatori endpoint'i.
- Yagona data metodi: `fetch_candles()` (:60). `/price` yoki `/quote`
  metodi **YO'Q**.
- `INTERVAL_MAP` (:31-39): faqat M5, M15, H1, H4, Daily. **M1 yo'q.**

### 3. Ishlab chiqarish wiring'i (production)
`data_layer/live_data/price_stream_service/price_stream_service.py:238`:
```
service.register_source("XAUUSD", TwelveDataProvider(asset="XAUUSD"), ...)
```
`interval` berilmagan → default `interval="M1"`
(`twelve_data_provider.py:45`). Client M1'ni rad etadi (`ValueError`,
`twelve_data_client.py:66-70`).

## Xulosa
Price Stream = candle-API polling. Chinakam current-price oqimi emas.
M1 xatosi (REAL-DATA-006) — shu kontrakt bo'shlig'ining alomati:
candle-only API'ga tick-darajali M1 interval berilgan.

Batafsil kontrakt farqi → `02_PRICE_CONTRACT_VERIFICATION.md`.
