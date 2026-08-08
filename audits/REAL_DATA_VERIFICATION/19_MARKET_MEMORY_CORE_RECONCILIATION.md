# 19 — Market Memory → Core Reconciliation (REAL-DATA-003)

## Muammo tavsifi

Jonli trading pipeline Core qatlami market candle'larni Market Memory
(SSOT)'dan emas, balki `MarketDataNormalizer`ning to'g'ridan-to'g'ri
chiqishidan iste'mol qilardi. Market Memory yozilardi (registry berilgan
bo'lsa) lekin hech qachon savdo yo'lida qayta o'qilmasdi.

## Root Cause Analysis

`core_layer/pipeline/pipeline.py:219` `MarketDataService()`ni
`memory_registry`siz qurar edi. `MarketDataService.get_candles()` esa
faqat normalizer chiqishini qaytarardi. Natijada Memory→Core o'qish yo'li
umuman yo'q edi (root cause: yetishmayotgan registry wiring, yo'q
arxitektura emas).

## Reuse-ga asoslangan tuzatish (yangi modul YO'Q)

Mavjud modullar qayta ishlatildi — yangi Market Memory, yangi SSOT,
yangi Provider yaratilmadi:

1. `MarketDataService.get_candles()` (`market_data_service.py:78`)
   endi write-through-then-read-back qiladi:
   ```
   candles = self._normalizer.get_candles(...)   # fetch + validate (o'zgarmagan)
   self._hydrate_memory(...)                      # memory'ga yozish (o'zgarmagan)
   if self._memory_registry is not None:
       from_memory = self.get_candles_from_memory(...)  # mavjud reuse
       if from_memory:
           return from_memory                     # Core endi SSOT'dan iste'mol qiladi
   return candles                                 # bare/bo'sh memory fallback: o'zgarmagan
   ```
   Bu yerda `get_candles_from_memory()` / `CandleRecord.to_candle()` /
   `MemoryReader` — barchasi allaqachon mavjud edi, yangi ekvivalent
   yozilmadi.

2. Pipeline endi registry-backed xizmatga ulanadi
   (`pipeline.py`, `__init__`):
   ```
   self.data_normalizer = build_default_market_data_service(
       memory_registry=MarketMemoryRegistry()
   )
   ```

## Option A/B tanlovi + sabab

**Tanlangan: Option B** — pipeline har instansiya uchun yangi
`MarketMemoryRegistry()` bilan `build_default_market_data_service()`
ishlatadi.

| | Option A (`get_shared_market_data_service()`) | Option B (fresh registry / pipeline) |
|---|---|---|
| SSOT darajasi | Process-wide, PriceStreamService registry'sini ulashadi (eng "haqiqiy" SSOT) | Pipeline ichida o'z-o'ziga izchil SSOT |
| Test isolation | Cross-test shared holat xavfi; `reset_shared_*` kerak | Shared holat yo'q — eng past xavf |
| Afzallik | Kelajakda PriceStream bilan bitta registry | Barcha 5490 testni buzmasdan yashil saqlaydi |

**Sabab:** CLAUDE.md Trading Safety talab qiladiki, tuzatish minimal va
test suite yashil qolsin. Option B cross-test shared holatni butunlay
yo'q qiladi (5490 test global singleton'ga tegmaydi), shu bilan eng past
xavfli. Order'ning o'zi ham "A test-isolation buzsa B'ni ishlat" degan.
Option B tanlandi; Option A kelajak ishi (PriceStream bilan haqiqiy
process-wide SSOT birlashtirish) sifatida ochiq qoldiriladi.

## HTF get_snapshot MEMORY orqali yo'naltirilMADI (ataylab)

`pipeline.py:333` HTF `get_snapshot()` (Daily/H4/H1) memory orqali
yo'naltirilmadi. Sabab: memory vocabulary'sida "Daily" YO'Q ("D1" bor),
shuning uchun uni memory orqali o'tkazish "Daily"ni jimgina tashlab
yuborib HTF bias'ni DEGRADE qilardi — bu Trading Safety regressiyasi,
taqiqlangan. HTF fetch o'zining joriy auxiliary-context yo'lida qoladi;
bu "traded data uchun ikkinchi parallel PRODUCTION data yo'li" EMAS — u
non-binding yordamchi context fetch.

## Daily/D1 vocabulary topilmasi (Director qaroriga)

Memory `DEFAULT_TIMEFRAME_CAPACITY` "D1" ishlatadi, HTF esa "Daily".
Ikkalasini moslashtirish (align) alohida keyingi task yoki Director
qarorini talab qiladi. Bu topilma yashirilmadi, majburlab degrade
qiluvchi o'zgartirish qilinmadi. Primary savdo yo'liga (M15) ta'siri
yo'q — u to'liq PASS. Tavsiya: alohida REAL-DATA task'da Daily→D1
mapping'ni HTF fetch ichida amalga oshirish yoki Director "Daily"ni
memory vocabulary'siga qo'shishni buyurishi.
