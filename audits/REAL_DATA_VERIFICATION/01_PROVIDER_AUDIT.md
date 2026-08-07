# 01 — Provider Audit (Real Market Data Production Verification)

Status: STATIK KOD TEKSHIRUVI (real API chaqiruvsiz)
Sana: 2026-08-07
Branch: `goldbot-v1`

---

## 0. Muhim ogohlantirish (headline)

Ushbu audit **real API dalilini taqdim eta olmaydi**. Sessiya muhitida
`api.twelvedata.com` va `api.bitget.com`ga chiquvchi HTTPS so'rovlari
tashkilot siyosati tomonidan bloklangan (`403` — "gateway answered 403
to CONNECT (policy denial or upstream failure)"), va `TWELVE_DATA_API_KEY`
bu sessiyada umuman sozlanmagan. Bu — Worker'ning nazorati ostida
bo'lmagan muhit cheklovi, konfiguratsiya xatosi emas. Har qanday "real
javob" ko'rinishidagi ma'lumot ushbu hujjatlar to'plamida **taqiqlangan**
(order o'zi buni aniq belgilagan). Shu sababli 08 va 09-hujjatlar
BLOCKED deb belgilangan va hech qanday narx/timestamp o'ylab
topilmagan.

Qolgan barcha bandlar — kod o'qish orqali statik tarzda, `file:line`
iqtibos bilan tasdiqlangan.

---

## 1. Ikki nusxa muammosi — hal qilindi (dead code aniqlandi)

Repo'da haqiqatan ham TwelveData va Bitget'ning ikkitadan nusxasi bor:

| Joylashuv | Sinf | Ishlatilishi |
|---|---|---|
| `data_layer/providers/twelve_data_provider/twelve_data_provider.py` | `TwelveDataProvider(MarketDataProvider)` | **PRODUCTION-WIRED** — `get_provider()` orqali `TradingPipeline`ga yetib boradi |
| `data_layer/live_data/twelve_data_provider/twelve_data_provider.py` | `TwelveDataProvider(PriceProvider)` | Faqat `PriceStreamService`ga ulangan (alohida "live tick" oqimi), `TradingPipeline.run()` uni chaqirmaydi |
| `data_layer/providers/bitget_provider/bitget_provider.py` | `BitgetProvider(MarketDataProvider)` | `ProviderRegistry`/`ProviderManager`ga ro'yxatdan o'tgan, lekin **inert stub** — real HTTP yo'q |
| `data_layer/live_data/bitget_price_source/bitget_price_source.py` | `BitgetPriceSource` | Faqat `PriceStreamService`ning crypto branch'ida ishlatiladi, lekin bu ham underlying'da real bitget SDK/HTTP chaqirmaydi (04-hujjatda tasdiqlangan) |
| `data_layer/providers/twelve_data_client/twelve_data_client.py` | `TwelveDataClient` | **Yagona real HTTP client.** Ikkala `TwelveDataProvider` nusxasi HAM shu bitta clientni wrap qiladi (quyida isbotlangan) — demak bu ikkilanish "ikki xil client" emas, balki "bitta client ustidan ikki xil adapter interfeysi" |
| `data_layer/providers/bitget` (papka) | bo'sh/hujjat skeleton | Foundation Freeze mirror, kod yo'q |
| `data_layer/providers/twelve_data` (papka) | bo'sh/hujjat skeleton | Foundation Freeze mirror, kod yo'q |

### Isbot: bitta HTTP client, ikkita adapter

`data_layer/live_data/twelve_data_provider/twelve_data_provider.py:24`:
```python
from data_layer.providers.twelve_data_client import TwelveDataClient
```
va o'z docstring'ida (satr 1-4): *"a PriceProvider adapter over the
existing `data_layer.providers.twelve_data_client.TwelveDataClient`...
This is the ONE place that knows about Twelve Data (DD-048)."*

`data_layer/providers/twelve_data_provider/twelve_data_provider.py:26`:
```python
from data_layer.providers.twelve_data_client import TwelveDataClient
```

Demak, ikkilanish real HTTP darajasida emas — faqat **interfeys**
darajasida: biri `MarketDataProvider` (candle-ko'rinishli, pipeline
uchun), ikkinchisi `PriceProvider` (stream/tick-ko'rinishli,
`PriceStreamService` uchun). Ikkalasi ham bitta
`TwelveDataClient`ni chaqiradi — shuning uchun bu "duplicate logic"
emas, balki qasddan ajratilgan ikki xil iste'molchi uchun ikki xil
adapter (`data_layer/live_data/market_data_service/market_data_service.py:8-15`
o'zining docstring'ida buni aniq izohlaydi: `TradingPipeline ->
MarketDataService (candles/snapshot)` vs `CurrentPriceProvider,
Telegram, Dashboard -> PriceStreamService`).

**Xulosa:** bu duplicate/dead code emas, balki qasddan ajratilgan ikki
qatlamli adapter arxitekturasi — lekin fayl nomlanishi va papka
tuzilishi (`data_layer/providers/` vs `data_layer/live_data/`) chalkash
va audit vaqtida noaniqlik keltirib chiqardi. Bu **kelgusi
refaktoring uchun kandidat** sifatida qayd etiladi (yangi kod
o'zgartirilmadi, faqat topilma sifatida yozildi — Order talabiga ko'ra
"yangi arxitektura ixtiro qilinmasin").

Bitget uchun esa haqiqiy funksional ikkilanish yo'q — ikkalasi ham
inert stub (03-hujjatda batafsil).

---

## 2. Production-wired zanjir (main.py'dan boshlab, real import'lar)

```
main.py:GoldBot.__init__()
  -> core_layer.pipeline.TradingPipeline(symbol="XAUUSD", interval="M15", ...)
     core_layer/pipeline/pipeline.py:219
       self.data_normalizer = MarketDataService()   # data_layer/live_data/market_data_service/market_data_service.py
         -> self._normalizer = MarketDataNormalizer()  # data_layer/live_data/market_data/market_data.py
              -> self.client = TwelveDataClient()       # data_layer/providers/twelve_data_client/twelve_data_client.py
  TradingPipeline.run() -> self.data_normalizer.get_candles(...)  (pipeline.py:303)
     -> MarketDataService.get_candles() -> MarketDataNormalizer.get_candles()
        -> TwelveDataClient.fetch_candles()  # real HTTP (requests.get) — BLOKLANGAN bu sessiyada
```

`data_layer/providers/get_provider()` (`data_layer/providers/__init__.py:70`)
`Config.MARKET_DATA_PROVIDER`ni o'qiydi (`config.py:195`, default
`"twelvedata"`) va shu nom bilan mos provayderni qaytaradi. Bu funksiya
`MarketDataService.get_historical_candles()` (tarixiy oraliqlar uchun,
`data_layer/live_data/market_data_service/market_data_service.py:152`)
va `ProviderManager`/`ProviderRegistry` orqali ishlatiladi — lekin
**oddiy live-candle yo'li** (`TradingPipeline.run()` har sikl chaqiradigan
yo'l) undan ham qisqaroq — to'g'ridan-to'g'ri
`MarketDataNormalizer.client = TwelveDataClient()` bilan bog'langan
(`data_layer/live_data/market_data/market_data.py:5,26`), `get_provider()`ni
chetlab o'tadi.

**Muhim topilma:** demak ikkita mustaqil "TwelveData tanlash" yo'li
mavjud:
1. `TradingPipeline` -> `MarketDataService` -> `MarketDataNormalizer` ->
   hardcoded `TwelveDataClient()` (Config.MARKET_DATA_PROVIDER'ni
   HECH QACHON o'qimaydi — har doim TwelveData, provider almashtirilmaydi).
2. `data_layer.providers.get_provider()` (Config-driven, `ProviderManager`/
   `ProviderRegistry` ishlatadigan) — faqat tarixiy backfill
   (`get_historical_candles()`) va boshqa yordamchi funksiyalarda
   ishlatiladi, asosiy live-signal yo'lida ISHLATILMAYDI.

Bu shuni anglatadiki: `MARKET_DATA_PROVIDER=mt5` yoki boshqa qiymatga
o'zgartirilsa ham, `TradingPipeline`ning asosiy candle-fetch yo'li
baribir TwelveData'dan foydalanishda davom etadi — chunki u
`get_provider()`ni chaqirmaydi. Bu **arxitektura nomuvofiqligi**
sifatida qayd etiladi (yangi fallback dizayn taklif qilinmaydi, faqat
mavjud holat qayd etiladi, Order talabiga muvofiq).

Batafsil dalillar 02, 03, 04-hujjatlarda.
