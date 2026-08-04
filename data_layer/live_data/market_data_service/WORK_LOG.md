# WORK_LOG.md — data_layer/live_data/market_data_service

Append-only.

---

Issue ID: GB-GEL001-STRICT
Date: 2026-08-04
Severity: N/A
Problem: Flat canonical module `market_data_service.py` violated GEL-001 (Strict): one module = one package.
Cause: Foundation-Freeze migration left canonical code as flat group-level files.
Decision: Convert to package, preserve public import path via `__init__` re-export (Director Strict order; no API change, no code rewrite).
Implementation: git mv `market_data_service.py` -> `market_data_service/market_data_service.py`; added `__init__.py` re-exporting the public surface with `__all__`; added the 8-file standard doc set.
Validation: pyflakes/compileall/pytest/main.py green (per-layer, see Director Review).
Lessons Learned: Import-preserving and test-safe when `__init__` re-exports every externally-used name.

---

Issue ID: GFL-001-FLOW-004
Date: 2026-08-04
Severity: Major
Problem: FLOW-004 (Market Engine) Director Order bo'yicha audit
  o'tkazildi. Aniqlandiki, real GoldBot Core'da "Market Engine" nomli
  hech qanday modul mavjud emas (`core_layer/core_engine/` faqat
  "Foundation Freeze v1.0" bo'sh skeleton, GFL-001 doirasidan tashqari).
  `data_layer/live_data/market/` (MarketManager) esa arxitektura
  jihatidan mos kelmadi -- uning o'z hujjati aniq belgilaydi: "market/
  is NOT a Data Layer member and NOT GoldBot Core... an upper-layer
  (Application Services) read-only projection" -- FLOW-004 esa GoldBot
  Core doirasida (Market Memory va Context Engine orasida). Haqiqiy
  production pipeline (`core_layer/pipeline/pipeline.py`) hali ham
  har safar TwelveData'dan to'g'ridan-to'g'ri fetch qiladi, Market
  Memory'dan umuman o'qimaydi. Shu bilan birga, `MarketDataService`
  (`get_candles()`/`get_snapshot()`) Market Memory'ga allaqachon
  yozar edi (TASK-DATA-004, `_hydrate_memory()`), lekin o'qib
  qaytarish metodi yo'q edi -- va bu yozish yo'li ham real ishlab
  chiqarishda `TradingPipeline`'ning bare `MarketDataService()`
  qurilishi tufayli hali faol emas edi.
Cause: `MarketDataService`da Market Memory'dan o'qib qaytarish
  (`MemoryReader` orqali) metodi yo'q edi -- faqat yozish yo'nalishi
  mavjud edi.
Decision: Yangi modul yaratish o'rniga (Reuse Analysis, GFL-004 Zero
  Dummy Rule), `MarketDataService`ga `get_candles_from_memory()` metodi
  qo'shildi -- `data_layer.market_memory.MemoryReader` orqali Market
  Memory'dan yopilgan candle seriyasini o'qiydi,
  `context.context_orchestrator.ContextEngine.build()`ning mavjud,
  o'zgarmagan `candles` kontraktiga (`List[Candle]`) mos shaklda.
  `get_shared_market_data_service()` qo'shildi -- FLOW-001'ning
  `get_shared_price_stream_service()` bilan bir xil `MarketMemoryRegistry`
  ulashadi (`build_default_price_stream_service()`ning o'z hujjatida
  oldindan ko'zda tutilgan juftlik, TASK-DATA-004). `core_layer
  /pipeline/pipeline.py`ga tegilmadi -- bu FLOW-005 (Context Engine)
  doirasi, GFL-004 Sequential Flow / "Boshqa Layer'ga tegilmaydi"
  qoidasi bo'yicha.
Implementation: `market_data_service.py`ga `get_candles_from_memory()`
  va `get_shared_market_data_service()`/`reset_shared_market_data_service()`
  qo'shildi. `__init__.py` yangi nomlarni qayta eksport qildi.
  `tests/data/stream/test_flow_004_market_engine_e2e.py` (yangi) --
  Provider -> Validation -> Market Memory -> Market Engine to'liq
  zanjirini isbotlaydi (haqiqiy tick orqali yopilgan candle o'qiladi;
  yaroqsiz tick hech qachon chiqishga yetib bormaydi).
  `tests/data/test_market_data_service.py`ga 6 ta yangi unit test
  qo'shildi.
Validation: pyflakes/compileall/pytest (5433+ test, jumladan 8 ta
  yangi) / `python main.py` -- barchasi PASS.
Lessons Learned: FLOW-003'dagi naqsh yana takrorlandi -- yozish
  infratuzilmasi (TASK-DATA-004) allaqachon mavjud bo'lganda, real gap
  odatda faqat o'qish tomonidagi ochiq nuqta bo'ladi. Bundan tashqari,
  nom o'xshashligi (`market/` va "Market Engine") arxitektura jihatidan
  noto'g'ri xulosaga olib borishi mumkin -- har doim modulning o'z
  hujjatidagi Layer da'vosini (bu yerda "NOT GoldBot Core") tekshirish
  kerak, shunchaki nomiga qarab emas.

---
