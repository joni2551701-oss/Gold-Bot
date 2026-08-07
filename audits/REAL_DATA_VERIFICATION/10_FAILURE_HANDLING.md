# 10 — Failure / Fallback Handling (mavjud holat, yangi dizayn yo'q)

Order talabiga ko'ra: faqat **mavjud** contract qayd etilgan, yangi
fallback arxitekturasi taklif qilinmagan.

## CONFIRMED: TwelveData muvaffaqiyatsiz bo'lsa nima bo'ladi (asosiy signal yo'lida)

`MarketDataNormalizer.get_candles()` (`data_layer/live_data/market_data/market_data.py`,
`fetch_candles()`ni chaqiruvchi try/except zanjiri): xatolik
(`ValueError`/`ConnectionError`) ushlanadi va `classify_api_error()`
bilan log qilinib, **bo'sh ro'yxat (`[]`) qaytariladi** — istisno
yuqoriga otilmaydi. Bu — TwelveData'dan Bitget'ga yoki boshqa
provayderga **hech qanday avtomatik fallback yo'q**; yagona
"fallback" — bo'sh natija bilan davom etish (pastga qarang, pipeline
darajasida qanday ishlov berilishi).

`data_layer/providers/twelve_data_provider/twelve_data_provider.py:get_candles()`
(ikkinchi, `ProviderManager` orqali ishlatiladigan qatlam,
`twelve_data_provider.py:76-97`) esa **aksincha** — istisnoni log
qilib qayta chiqaradi (`raise`), bo'sh javobda esa `[]` qaytaradi.
Ya'ni ikki qatlam turlicha ishlaydi: biri yutadi (production hot
path), ikkinchisi otadi (get_provider() yo'li, hot path'da
ishlatilmaydi).

## CONFIRMED: `ProviderManager` darajasidagi "fallback"

`ProviderManager.get_active_provider()`
(`data_layer/providers/provider_manager/provider_manager.py:127-138`)
— zanjirdagi (`provider_chain()`) birinchi `available=True` bo'lgan
provayderni qaytaradi. Bu **haqiqiy primary->fallback tanlash
mexanizmi**, lekin: (a) u faqat konstruksiya vaqtidagi
`get_market_status()` (statik holat, masalan "API kalit bormi")ga
qaraydi, real-vaqtli "so'rov muvaffaqiyatsiz bo'ldi" hodisasiga javob
bermaydi; (b) 04-hujjatda ko'rsatilganidek, bu mexanizm asosiy
`TradingPipeline.run()` signal yo'lida **ishlatilmaydi**.

## Xulosa: haqiqiy ishlaydigan fallback yo'q

Production signal yo'lida (`TradingPipeline` -> `MarketDataService` ->
`MarketDataNormalizer` -> `TwelveDataClient`) TwelveData
muvaffaqiyatsiz bo'lganda **Bitget'ga yoki boshqa provayderga
o'tuvchi hech qanday kod yo'q**. Yagona natija — bo'sh candle ro'yxati,
va `core_layer/pipeline/pipeline.py`ning Data Quality bosqichi
(`assess_data_quality`, pipeline.py:312 atrofi) buni "past sifat"/"ma'lumot yo'q"
sifatida hisobga oladi (pipeline'ning umumiy fail-safe siyosatiga
muvofiq — signal chiqarilmaydi, lekin bu Bitget'ga fallback emas).

Bitget provayderining o'zi ham (03-hujjat) implement qilinmagan bo'lgani
uchun, hatto kelajakda fallback chaqiruv yozilsa ham, u hozircha
haqiqiy natija bera olmaydi.

**Yangi fallback arxitekturasi bu hujjatda taklif qilinmaydi** — bu
faqat mavjud holatning halol qaydidir.
