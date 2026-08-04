# WORK_LOG.md -- platform_layer/telegram

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
Problem: `polling.py` -- yagona uzoq muddat ishlaydigan (long-running)
  process, `/price` buyrug'ini shu yerda qabul qiladi -- lekin hech
  qanday joyda Price Stream'ning `tick()`ini chaqirmas edi. Shu sabab
  `PriceCache` doim bo'sh qolib, `/price` doim "price.empty" holatini
  qaytarar edi.
Cause: `_heartbeat_loop()` naqshiga o'xshash fon (background) tsikl
  Price Stream uchun mavjud emas edi.
Decision: `_price_stream_tick_loop()` qo'shildi -- `_heartbeat_loop()`
  bilan bir xil naqsh (`asyncio.sleep` + fail-safe try/except,
  `dispatcher.start_polling()` bilan bir vaqtda `asyncio.create_task`
  orqali ishga tushiriladi, `finally`da bekor qilinadi). Interval
  allaqachon mavjud, lekin ishlatilmagan
  `get_settings().stream.polling_interval` (StreamConfig,
  `POLLING_INTERVAL`, default 60s) konfiguratsiyasidan olinadi --
  yangi konfiguratsiya o'zgaruvchisi qo'shilmadi.
Implementation: `platform_layer/telegram/polling.py`:
  `PRICE_STREAM_TICK_INTERVAL_SECONDS` konstantasi,
  `_price_stream_tick_loop()` funksiyasi, `run_polling()` ichida
  `heartbeat_task` bilan bir qatorda `price_stream_task` yaratildi va
  yopilishda bekor qilindi.
Validation: `tests/telegram/test_polling.py` -- mavjud
  `test_run_polling_cancels_heartbeat_task_on_exit` testi ikkinchi
  fon vazifasini kutishga yangilandi (1 emas, 2 ta task); 3 ta yangi
  test qo'shildi (interval config bilan mos kelishi, real tick
  chaqirilishi, xato bo'lsa ham tsikl o'lmasligi). Full suite: 5408
  o'tdi. `python main.py` -- exit 0.
Lessons Learned: `_heartbeat_loop()` naqshi boshqa fon vazifalar
  uchun ham to'g'ridan-to'g'ri qayta ishlatilishi mumkin ekan --
  Module Reuse Principle'ga mos.

---
