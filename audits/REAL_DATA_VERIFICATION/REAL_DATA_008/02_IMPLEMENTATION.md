# 02 — Implementatsiya

## 1. `TwelveDataClient.get_price(symbol) -> Optional[float]`

Fayl: `data_layer/providers/twelve_data_client/twelve_data_client.py`

- Yangi `PRICE_URL = "https://api.twelvedata.com/price"` konstantasi.
- Yangi metod `get_price()` — `/price` endpointini chaqiradi, `symbol` ni
  `_format_symbol()` bilan formatlaydi, `{"price":"<num>"}` → `float`.
- Xato rejimi `fetch_candles()` bilan bir xil: kalit yo'q → `ValueError`;
  API error body → `ValueError` (429 → backoff); tarmoq → `ConnectionError`.
- API kaliti FAQAT params ichida; hech qayerda logga chiqmaydi.
- `fetch_candles()` GA TEGILMADI — bayt-ma-bayt o'zgarmagan.

## 2. `TwelveDataPriceSource` (yangi `PriceProvider`)

Fayl: `data_layer/live_data/twelve_data_price_source/twelve_data_price_source.py`

- Mavjud `PriceProvider` ABC ni amalga oshiradi (capabilities / connect /
  disconnect / read / health / status).
- `read()` → `TwelveDataClient().get_price(self._asset)` ni chaqiradi va
  `[StreamEvent(asset, price=<real current price>,
  timestamp=datetime.now(timezone.utc), source=CandleSource.STREAM)]`
  qaytaradi. Kuzatuv vaqti (`/price` o'z timestampini bermaydi).
- `capabilities`: `supports_streaming=False, supports_polling=True`.
- Narx bo'yicha dedupe YO'Q — har `read()` bitta yangi kuzatuv.
- Fail-safe: muvaffaqiyatsiz `read()` statusni DOWN qiladi va xatoni
  ko'taradi (PriceStream DD-051 orqali izolyatsiya qiladi).

**Nega yangi modul (Module Reuse Principle):** 1-qadam — joriy narx
`PriceProvider` mavjud emas (yagona XAUUSD manba `TwelveDataProvider`
candle.close ni beradi). 2-qadam — `TwelveDataProvider` ni buzmasdan
kengaytirib bo'lmaydi (uning `read()` kontrakti — candle close + candle
timestamp + dedupe — hali ishlatiladi va testlari buni tasdiqlaydi).
Shu sabab alohida kichik adapter — to'g'ri reuse. Modul docstringida
yozilgan.

## 3. Ro'yxatga olish (registration swap)

Fayl: `data_layer/live_data/price_stream_service/price_stream_service.py`,
`build_default_price_stream_service()`.

Oldingi: `register_source("XAUUSD", TwelveDataProvider(asset="XAUUSD"), ...)`
Yangi:   `register_source("XAUUSD", TwelveDataPriceSource(asset="XAUUSD"), ...)`

BTCUSDT `BitgetPriceSource` da qoladi (inert, NOT VERIFIED — o'zgarmadi).

## Batch-yo'l tegilmaganligi isboti

- `MarketDataService.get_candles()` va `fetch_candles()` — o'zgarmagan.
- `TwelveDataProvider` (candle stream manbasi) repoda qoladi (testlar hali
  import qiladi) — o'chirilmadi.
- `python main.py` hamon 200 candle oladi va barcha bosqichlarni avvalgidek
  ishga tushiradi (07_TESTS / VERDICT hujjatlarida).
