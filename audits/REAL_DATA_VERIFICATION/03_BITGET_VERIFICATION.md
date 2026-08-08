# 03 — Bitget Verification

Production-wired implementation (registry orqali): `data_layer/providers/bitget_provider/bitget_provider.py`
(`BitgetProvider(MarketDataProvider)`), `ProviderRegistry`ga
`build_default_registry()` orqali ro'yxatdan o'tgan
(`data_layer/providers/registry/registry.py:87-95`).

## Eng muhim topilma: Bitget REAL emas — qasddan yaratilgan inert stub

`bitget_provider.py:1-24` o'z docstring'ida ochiq yozadi: *"Foundation
only for a future crypto/fallback phase — **no real Bitget API
connection exists in this file**. No `ccxt`/`bitget` SDK, no HTTP call,
no websocket. Every data-fetch method raises NotImplementedError."*

## CONFIRMED (kod o'qish orqali)

1. **HTTP client** — yo'q. `requests`, `ccxt`, websocket yoki boshqa
   HTTP kutubxona import qilinmagan (`bitget_provider.py` import
   ro'yxati: faqat `typing`, `config`, `data_layer.providers.base_provider`).

2. **Credential loading** — `self._settings.providers.bitget_api_key`
   (`config.get_settings()` orqali, `bitget_provider.py:60-63`), tur —
   `MaskedSecret` (11-hujjatda tasdiqlangan, hech qachon xom `str` emas).
   Kalit hech qachon real chaqiruvda ishlatilmaydi — chunki chaqiruv
   umuman mavjud emas.

3. **Symbol mapping** — `SUPPORTED_SYMBOLS = ("BTCUSDT", "ETHUSDT")`
   (`bitget_provider.py:26`) — Bitget spot formatiga mos (suffiks
   qo'shilgan, separatorsiz), lekin bu faqat validatsiya ro'yxati,
   haqiqiy API chaqiruvda ishlatilmaydi.

4. **get_candles()** (`bitget_provider.py:66-68`): `_validate_symbol()`
   chaqiradi, so'ng **har doim** `raise NotImplementedError(self.UNIMPLEMENTED_REASON)`.

5. **get_latest_price()** (`bitget_provider.py:70-72`): xuddi shunday —
   `NotImplementedError`.

6. **get_market_status()** (`bitget_provider.py:74-76`): **har doim**
   `ProviderStatus(available=False, reason=self.UNIMPLEMENTED_REASON)`
   qaytaradi — real tarmoqqa hech qachon murojaat qilinmaydi, hatto
   status-tekshiruvda ham.

7. **`ProviderManager`/`ProviderRegistry` munosabati**
   (`data_layer/providers/provider_manager/provider_manager.py:31-33,
   127-138`): Bitget `_PRIORITY` ro'yxatida bor, lekin
   `get_active_provider()` faqat `get_market_status().available == True`
   bo'lgan provayderni tanlaydi — Bitget doim `False` qaytargani uchun,
   u **hech qachon** amaliy tanlanmaydi (kod sharhi buni ochiq
   tasdiqlaydi: `provider_manager.py:31-34`, "the rest are inert stubs
   (so they report available=False and are skipped)").

8. **`data_layer/live_data/bitget_price_source/bitget_price_source.py`**
   (ikkinchi, live_data'dagi nusxa) — bu ham `PriceStreamService`ning
   crypto branch'ida ishlatiladi, lekin u ham underlying real Bitget
   ulanishga ega emas (fayl mavjud, lekin bu audit doirasida
   production XAUUSD signal yo'liga umuman aloqasi yo'q — XAUUSD forex
   instrumenti, Bitget faqat crypto (`BTCUSDT`/`ETHUSDT`) uchun
   marshrutlanadi, `provider_manager.py:37-40`dagi
   `_CRYPTO_PROVIDERS`/symbol-suffix heuristikasiga ko'ra).

## Bitget XAUUSD signal yo'liga umuman aloqasi yo'qligi

`main.py:26-31`: `TradingPipeline(symbol="XAUUSD", ...)`. Bitget faqat
`"USDT"` bilan tugaydigan simvollar uchun tanlanishi mumkin
(`provider_manager.py:141-151`, `resolve()` metodi). GoldBot faqat
XAUUSD savdo qiladi (`CLAUDE.md`: "Signal logic (`strategies/`,
`signals/`)" XAUUSD-ga qaratilgan; `assets/profiles/gold.py`,
`twelve_data_provider.py:37`dagi sharh ham buni tasdiqlaydi: "strategies/assets/
only trade 'XAUUSD' today"). Demak Bitget bugungi production oqimida
**hech qachon** chaqirilmaydi — na fallback sifatida, na to'g'ridan-to'g'ri.

## BLOCKED

Real HTTP/tarmoq tekshiruvi — kerak emas, chunki hech qanday HTTP
chaqiruv kodi mavjud emas (yuqoridagi 1-band). Bu "network policy
denial" sababli emas, balki **kodning o'zida hech qanday real
integratsiya yo'qligi** sababli BLOCKED emas — bu "N/A: not
implemented" holati, alohida qayd etiladi.

## Xulosa

Bitget — Foundation-only inert stub. Hech qanday real yoki soxta
ma'lumot qaytarmaydi (har doim `NotImplementedError` yoki
`available=False`). Xavfsiz, halol dizayn: hech qachon signal
yo'lida ishtirok etmaydi va hech qachon "ishlayapti" deb yolg'on
signal bermaydi.


---

## ⚡ REAL RUN NATIJASI (REAL-DATA-002, 2026-08-08, run 31229724552)

**Ikki alohida natija (Order section 7):**
- **Diagnostic (public ticker BTC/USDT): ✅ PASS (REAL)** — `https://api.bitget.com/api/v2/spot/market/tickers?symbol=BTCUSDT`, HTTP 200, Price 64870.01, Timestamp 1786148320401. Bu Bitget API real narx berayotganini isbotlaydi (auth talab qilmaydi; BITGET_API_SECRET/PASSPHRASE MISSING bo'lsa ham public ticker ishlaydi).
- **Production-path: NOT_VERIFIED** — `BitgetProvider` ataylab inert stub (`NotImplementedError`), `BitgetPriceSource` ham shu stub ustidagi adapter. Repo'da real Bitget HTTP kodi umuman yo'q. GoldBot XAUUSD savdo qiladi — Bitget/crypto signal yo'lida ishlatilmaydi. Yangi Bitget provider yozish bu task'da taqiqlangan.
