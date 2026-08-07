# 04 — Provider Factory / Manager Verification

## Aniqlangan komponentlar

1. `data_layer/providers/__init__.py:get_provider(name=None)` — bitta,
   Config-driven provayder tanlaydi (`Config.MARKET_DATA_PROVIDER`,
   default `"twelvedata"`, `config.py:195`). Noma'lum/o'chirilgan nom
   uchun `ValueError` chiqaradi (`__init__.py:88,94,98`).
2. `data_layer/providers/registry/registry.py:ProviderRegistry` —
   oddiy katalog (`register/get/available/all_names`), tanlash
   mantig'i yo'q. `build_default_registry()` 6ta provayderni
   ro'yxatdan o'tkazadi: TwelveData, MT5, Binance, Bitget, Keynorq,
   FRED (`registry.py:87-95`).
3. `data_layer/providers/provider_manager/provider_manager.py:ProviderManager`
   — buyurtmali primary->fallback zanjiri (`provider_chain()`),
   `get_active_provider()` orqali birinchi **available** provayderni
   tanlaydi.

## CONFIRMED: TwelveData va Bitget haqiqatan ham instantsiyalanadimi?

Ha — `build_default_registry()` (`registry.py:96`):
`registry.register(TwelveDataProvider())` va (`registry.py:99`)
`registry.register(BitgetProvider())` — ikkalasi ham `data_layer/providers/`
paketidagi (production-wired) sinflar, `data_layer/live_data/`dagilar
EMAS (01-hujjatdagi ikkilanish tahliliga mos).

## CONFIRMED: qaysi shart bilan biri ikkinchisidan tanlanadi

`ProviderManager.provider_chain()` (`provider_manager.py:104-118`):
`self.primary_name` (`_settings.providers.market_data_provider`,
lowercased) birinchi qo'yiladi, keyin `_PRIORITY = ("twelvedata",
"mt5", "binance", "bitget", "keynorq")` tartibida qolganlari, faqat
`self._enabled(name)` `True` bo'lsa (`_enabled()`, `provider_manager.py:87-93`
— `providers.enable_twelvedata`/`enable_bitget` kabi Config flag'lar).

`get_active_provider()` (`provider_manager.py:127-138`) zanjirdagi
birinchi `get_market_status().available == True` bo'lgan provayderni
qaytaradi. Bitget doim `available=False` (03-hujjat), shuning uchun
amalda **faqat TwelveData tanlanadi** (agar API kalit mavjud bo'lsa) —
qolgan barcha (MT5, Binance, Bitget, Keynorq) doim stub bo'lgani uchun
hech qachon tanlanmaydi.

`resolve(symbol)` (`provider_manager.py:141-151`) — `"USDT"` bilan
tugaydigan simvollar uchun avval crypto provayderlarni (`bitget`,
`binance`) sinaydi, aks holda oddiy zanjirga tushadi. XAUUSD bu
shartga mos kelmaydi.

## MUHIM ARXITEKTURA TOPILMASI: bu factory production live-signal yo'lida ISHLATILMAYDI

01-hujjatda ko'rsatilganidek, `TradingPipeline.run()`ning haqiqiy
candle-fetch yo'li (`core_layer/pipeline/pipeline.py:219,303`)
`MarketDataService()` -> `MarketDataNormalizer()` orqali **to'g'ridan-to'g'ri**
`TwelveDataClient()`ni yaratadi
(`data_layer/live_data/market_data/market_data.py:26`) — na
`get_provider()`, na `ProviderManager`, na `ProviderRegistry`ni
chaqiradi. Bu uch komponent (`get_provider`, `ProviderRegistry`,
`ProviderManager`) faqat quyidagilarda ishlatiladi:

- `MarketDataService.get_historical_candles()` (tarixiy backfill,
  `market_data_service.py:152-158`, `provider or get_provider()`);
- `core_layer/health_monitor/provider_health.py` (monitoring/health
  status uchun, registry docstring'iga ko'ra — `registry.py:14-18`);
- kelajakdagi `/providers` Owner-komandasi uchun (hali implement
  qilinmagan, faqat kontrakt, registry docstring'i);
- to'g'ridan-to'g'ri test fayllarida.

**Xulosa:** `ProviderFactory`/`ProviderManager`/`ProviderRegistry` —
haqiqiy, ishlaydigan kod (fake emas), lekin **asosiy live-signal
oqimiga ulangan emas**. Bu "Foundation exists but not fully wired into
the hot path" holatining yana bir namunasi — repo'ning o'zida
belgilangan patternga mos (GFL-001 progress hujjatlarida tez-tez
uchraydi). Yangi ulash/fallback dizayni taklif qilinmadi — Order aniq
taqiqlagan.
