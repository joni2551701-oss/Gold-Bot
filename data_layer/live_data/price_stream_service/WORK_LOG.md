# WORK_LOG.md -- data_layer/live_data/price_stream_service

Append-only. Earlier entries are never deleted or rewritten -- only new
entries are appended below.

---

Issue ID: N/A
Date: 2026-08-03
Severity: N/A
Problem: N/A
Cause: N/A
Decision: N/A
Implementation: Module created. Migration completed. Engineering Standard
  initialized (Director Order No. 012/013).
Validation: N/A
Lessons Learned: N/A

---

Issue ID: GFL-001-FLOW-001
Date: 2026-08-04
Severity: Major
Problem: `build_default_price_stream_service()` hech qanday `tick()`
  chaqiruvchisiga ega emas edi -- production'da hech kim bu funksiyani
  chaqirmagan, shuning uchun `PriceCache` doim bo'sh qolar edi.
  `CurrentPriceProvider`'ning default `PriceStreamLastPriceSource`'i esa
  har safar YANGI, mustaqil `PriceStreamService` obyekti quradi -- hatto
  kimdir boshqa nusxani "tick" qilsa ham, `/price` buyrug'i buni
  ko'rmas edi.
Cause: `PriceStreamLastPriceSource._get_service()` har doim
  `build_default_price_stream_service()`'ni to'g'ridan-to'g'ri
  chaqirar edi -- bu esa har chaqiruvda yangi, alohida instance
  yaratadi. Shared (umumiy) instance mavjud emas edi.
Decision: `get_shared_price_stream_service()` -- process darajasida
  yagona (singleton) `PriceStreamService` instance qo'shildi.
  `PriceStreamLastPriceSource._get_service()` endi shu umumiy
  instance'ni ishlatadi. `build_default_price_stream_service()`
  esa har bir `register_source()` chaqiruviga default
  `StreamValidator` (TASK-ARCH-101, allaqachon mavjud) ni ulaydi va
  default `MarketMemoryRegistry`'ni yaratadi -- shunday qilib
  tasdiqlangan narx MarketMemory SSOT'ga ham yoziladi (TASK-DATA-004
  single-writer orqali).
Implementation: `get_shared_price_stream_service()` va
  `reset_shared_price_stream_service()` qo'shildi (package `__init__`
  orqali eksport qilindi). `build_default_price_stream_service()`
  ichida `validator=StreamValidator()` va default
  `MarketMemoryRegistry()` ulandi. Haqiqiy `tick()` chaqiruvchisi
  `platform_layer/telegram/polling.py`'da qo'shildi
  (`_price_stream_tick_loop`, `_heartbeat_loop` bilan bir xil naqshda,
  `Config.stream.polling_interval`dan foydalanadi).
Validation: pyflakes/compileall/pytest (5408 ta test o'tdi, jumladan
  6 ta yangi test) / `python main.py` -- barchasi PASS.
Lessons Learned: Lazy-constructed default'lar process darajasida
  umumiy bo'lishi kerak bo'lgan holatlarda xavfli -- har bir chaqiruv
  o'z nusxasini yaratib, "driver" va "reader" bir xil ob'ektga
  ishora qilmasligi mumkin. Shared getter + reset() naqshi bu holatni
  tuzatadi va test isolation'ni ham saqlab qoladi.

---

Issue ID: GFL-001-FLOW-003
Date: 2026-08-04
Severity: Minor
Problem: FLOW-003 (Market Memory) auditida aniqlandiki, yozish
  tomoni (`CandleBuilder` -- yagona yozuvchi) allaqachon production'da
  ishlagan (FLOW-001/002 natijasi), lekin `MarketMemoryRegistry`'ga
  o'qish tomonidan (Consumer) yetib borishning ochiq, sanksiyalangan
  usuli yo'q edi -- faqat testlar `service._memory_registry` orqali
  shaxsiy atributga to'g'ridan-to'g'ri kirar edi.
Cause: `PriceStreamService.__init__` `memory_registry`ni faqat
  shaxsiy `self._memory_registry` sifatida saqlagan -- ochiq accessor
  mavjud emas edi.
Decision: Kichik, qo'shimcha (additive) `PriceStreamService.memory_registry`
  property qo'shildi -- Consumer (masalan `MemoryReader`,
  `MarketManager`) endi shaxsiy atributga tegmasdan, xuddi shu jonli
  registry ustidan o'qiy oladi.
Implementation: `price_stream_service.py`ga `memory_registry` @property
  qo'shildi (faqat o'qish, `self._memory_registry`ni qaytaradi).
  Boshqa hech narsa o'zgarmadi -- signature buzilishi yo'q.
Validation: pyflakes/compileall/pytest (5411+ test, jumladan 3 ta
  yangi unit test) / `python main.py` -- barchasi PASS.
Lessons Learned: FLOW-001'da bo'lgani kabi, ko'p hollarda "Production
  Code" gap kichik va aniq bo'ladi -- yozish infratuzilmasi allaqachon
  mavjud bo'lganda, yetishmayotgan narsa ko'pincha faqat sanksiyalangan
  o'qish nuqtasi (public accessor) bo'ladi, yangi arxitektura emas.

---
