# REAL-DATA-006 — 03. Provider → Price Stream Verification

## XAUUSD → TwelveDataProvider → TwelveDataClient (real HTTP)

| Bosqich | file:line | Izoh |
|---|---|---|
| Ro'yxatga olish | `price_stream_service.py:238` | `TwelveDataProvider(asset="XAUUSD")` — **interval berilmagan, default "M1"** |
| Provider default interval | `twelve_data_provider.py:45` | `def __init__(self, asset, interval="M1", ...)` |
| read() | `twelve_data_provider.py:67-68` | `self._client.fetch_candles(self._asset, self._interval, outputsize=1)` — REAL HTTP |
| Client timeframe map | `twelve_data_client.py:30-33` | `INTERVAL_MAP = {"M5":"5min","M15":"15min", H1, H4, Daily}` — **M1 YO'Q** |
| Client rad etishi | `twelve_data_client.py:68-69` | `Unsupported timeframe 'M1'. GoldBot strictly supports: M5, M15, H1, H4, Daily` → `ValueError` |

### Status: **REAL HTTP capability PASS, lekin production wiring BLOCKED (M1 mismatch)**

`TwelveDataClient.fetch_candles()` haqiqiy HTTP client (REAL-DATA-002'da
tasdiqlangan). Ammo production Price Stream wiring uni **M1** interval
bilan chaqiradi, client esa M1'ni qo'llab-quvvatlamaydi. Natija: XAUUSD
`read()` har chaqiruvda `ValueError` beradi.

`PriceStream` bu xatoni izolyatsiya qiladi (DD-051 provider isolation) —
stream qulamaydi, lekin **hech qanday tick sink'ga yetib bormaydi**.
Local probe buni empirik ko'rsatdi:

```
PriceStream[XAUUSD] provider error isolated: ValueError: Unsupported timeframe 'M1'.
GoldBot strictly supports: M5, M15, H1, H4, Daily
```

**Xulosa:** production'da XAUUSD Price Stream real tick tushira olmaydi.
Bu KOD topilma (audit-only) — tuzatilmadi. To'g'ri tuzatish
`build_default_price_stream_service()` yoki `TwelveDataProvider` default
interval'ini `M5`/`M15`ga o'tkazish bo'lardi, lekin bu provider/stream
wiring o'zgarishi — Director Review talab qiladi (Trading Safety
chegarasidagi Data Layer wiring), shuning uchun ushbu auditda faqat qayd
etiladi.

## BTCUSDT → BitgetPriceSource (inert)

| Bosqich | file:line | Izoh |
|---|---|---|
| Ro'yxatga olish | `price_stream_service.py:242` | `BitgetPriceSource(asset="BTCUSDT")` |
| read() | `bitget_price_source/bitget_price_source.py:73-76` | stub'ning `NotImplementedError`'ini tarqatadi |

Status: **INERT (design bo'yicha)** — `BitgetProvider` ataylab
implement qilinmagan (REAL-DATA-002/003'da tasdiqlangan). `PriceStream`
`NotImplementedError`'ni izolyatsiya qiladi. Crypto oqimi Foundation.

## Stale docstring (documentation finding)

`price_stream_service.py:47` docstring: *"nothing drives `tick()` in
production"* — **ESKIRGAN**. `polling.py:308` uni haydaydi. Kod
o'zgartirilmadi; hujjat eskirganligi 12-faylda ham qayd etiladi.
