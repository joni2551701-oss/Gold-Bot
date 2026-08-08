# REAL-DATA-007 — 04. Provider Path Verification

## Savol (CLAUDE.md section 3)
ProviderManager / ProviderFactory / ProviderRegistry biror current-price
kontraktini ta'minlaydimi?

## Javob: **YO'Q** — ular candle MarketDataProvider tanlaydi.

## Dalillar (file:line)
### ProviderManager
`data_layer/providers/provider_manager/provider_manager.py`:
- `from data_layer.providers.base_provider import MarketDataProvider` (:37)
- `_market_providers()` (:67-74): faqat `isinstance(provider,
  MarketDataProvider)` bo'lganlarni tanlaydi — docstring (:68): *"Registered
  providers that are candle-shaped (MarketDataProvider)"*.
- `get_primary()` (:110), `get_active_provider()` (:123), `resolve()` (:137)
  — hammasi `MarketDataProvider` (candle, `get_candles()`) qaytaradi.
- `get_price()` / `get_quote()` / current-price metodi — **YO'Q**.

### ProviderRegistry
`data_layer/providers/registry/registry.py`:
- `register(provider: DataProvider)` (:57), `get()` (:69), `available()`
  (:73) — nomlar bo'yicha `DataProvider` ro'yxati. Current-price kontrakti
  yo'q.

### ProviderFactory
`data_layer/providers/provider_factory/__init__.py`: Foundation Freeze
skeleti (kanonik hujjat mirrori), current-price logikasi yo'q.

## Price Stream'ning ikki ro'yxatdan o'tgan manbai
`price_stream_service.py:238,242`:
1. `TwelveDataProvider(asset="XAUUSD")` — candle polling (default M1 → xato).
2. `BitgetPriceSource(asset="BTCUSDT")` — inert stub (`NotImplementedError`,
   `bitget_price_source.py` docstring + `BitgetProvider.get_latest_price()`).

## Xulosa
Provider path (Manager/Factory/Registry) faqat candle MarketDataProvider
tanlaydi. Hech bir yo'lda current-price kontrakti mavjud emas. Uni qo'shish
TAQIQLANGAN (audit-only).
