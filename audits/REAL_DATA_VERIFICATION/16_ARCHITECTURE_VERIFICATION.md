# 16 — Architecture Verification

## Layer Boundary

`data_layer/` o'z chegarasida qoladi — hech qanday provider/validation/
memory kodi `context_layer`, `strategy_layer` yoki boshqa yuqori
Layer'ga to'g'ridan-to'g'ri yozmaydi yoki ulardan import qilmaydi.
`core_layer/pipeline/pipeline.py` `data_layer.live_data.market_data_service.MarketDataService`ni
iste'mol qiladi — bu Layer Direction Rule'ga mos (`core_layer` `data_layer`dan
pastga emas, undan iste'mol qiladi, mos yo'nalish). **Buzilish
topilmadi.**

## Foundation Freeze

Hech qanday yangi Layer, yangi Module, yangi Canonical Contract
yaratilmadi yoki o'zgartirilmadi — bu audit faqat mavjud kodni o'qidi.
**Buzilish yo'q.**

## Muhim arxitektura topilmasi — Order'ning diagrammasi bilan real kod orasidagi farq

Order'ning "REAL DATA FLOW" diagrammasi quyidagini taxmin qiladi:

```
Provider -> Validation -> Market Memory (SSOT) -> Event Bus -> Core
```

01, 04, 06, 07-hujjatlarda tasdiqlangan real kod bu taxminga **to'liq
mos kelmaydi**:

1. **Asosiy signal yo'li (`TradingPipeline.run()`) Market Memory'ni
   ham, Event Bus'ni ham ishlatmaydi.** `core_layer/pipeline/pipeline.py:219`
   `MarketDataService()`ni **hech qanday `memory_registry` argumentisiz**
   quradi — shuning uchun `_hydrate_memory()` har doim erta qaytadi
   (06-hujjat). Candle'lar to'g'ridan-to'g'ri
   `MarketDataNormalizer`dan (validatsiyadan o'tgan holda) olinadi,
   Memory orqali emas.
2. **`ProviderFactory`/`ProviderManager`/`ProviderRegistry` asosiy
   yo'lda ishlatilmaydi.** Bu komponentlar real va ishlaydi (04-hujjat),
   lekin faqat tarixiy backfill va monitoring uchun chaqiriladi — canli
   candle-fetch yo'li ularni chetlab o'tib, `TwelveDataClient()`ni
   to'g'ridan-to'g'ri yaratadi.
3. **Event Bus real va ishlaydi, lekin Core uni iste'mol qilmaydi**
   (07-hujjat) — faqat ikkinchi darajali `PriceStreamService` oqimida
   ishlatiladi.

## Bu — Architecture Violation emas, balki Documentation/Reality Gap

Muhim: yuqoridagi uchala band ham **mavjud kodni buzish** emas — bu
kod har biri o'z docstring'ida ochiq va qasddan shunday deb yozilgan
(masalan `market_data_service.py:44-49`: "The default (no registry)
writes nothing... keeps working exactly the old way"). Demak bu
**qasddan qilingan, hujjatlashtirilgan dizayn qarori** — lekin
Order'ning diagrammasi (va ehtimol boshqa arxitektura hujjatlari) bu
haqiqiy holatni to'liq aks ettirmaydi. Bu **Documentation/Reality
mismatch** sifatida qayd etiladi, Architecture Violation sifatida
emas — chunki hech qanday Canonical Contract yoki Foundation Freeze
qoidasi buzilmagan, faqat "SSOT orqali oqish" g'oyasi hali to'liq
amalga oshirilmagan (GFL-001 progress hujjatlarida keng tarqalgan
"Foundation exists, not wired to hot path" patterniga mos).

## Xulosa

Layer Boundary: **PASS**. Foundation Freeze: **PASS**. Ammo Real Data
Flow arxitekturasi (Provider->Validation->Memory->EventBus->Core)
hujjatlashtirilgan dizayn bilan mos, ammo bu **SSOT/EventBus qatlami
asosiy signal yo'lida hali ishlatilmayapti** — bu keyingi bosqichda
(RC1'dan keyingi Sprint) Director qaroriga loyiq alohida topilma,
Real Market Data Verification'ning o'zidan mustaqil.
