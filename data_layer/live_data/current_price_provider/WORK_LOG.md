# WORK_LOG.md -- data_layer/live_data/current_price_provider

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
Problem: `PriceStreamLastPriceSource._get_service()` default holatda
  har chaqiruvda YANGI `PriceStreamService` quradi -- shu sababli
  boshqa joyda "tick" qilingan narx bu yerga hech qachon yetib
  kelmasdi.
Cause: `build_default_price_stream_service()`'ga to'g'ridan-to'g'ri
  murojaat -- process darajasida umumiy instance yo'q edi.
Decision: `_get_service()` endi
  `data_layer.live_data.price_stream_service.get_shared_price_stream_service()`
  orqali umumiy instance'ni oladi. Public kontrakt (`CurrentPrice`,
  `LastPriceSource`, `PriceStreamLastPriceSource`,
  `SmartCacheLastPriceSource`, `CurrentPriceProvider`,
  `build_default_current_price_provider()`) o'zgarmadi -- faqat ichki
  wiring.
Implementation: Bitta qatorlik o'zgarish
  (`data_layer/live_data/current_price_provider/current_price_provider.py`).
Validation: `tests/data/test_current_price_provider.py` mavjud testlar
  o'zgarishsiz PASS; yangi integratsiya testi
  `tests/data/stream/test_price_stream_service.py::test_shared_service_ticked_by_one_caller_is_seen_by_another_reader`
  aynan shu holatni tekshiradi.
Lessons Learned: N/A

---
