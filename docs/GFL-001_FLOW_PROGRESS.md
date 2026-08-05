# GFL-001 — Flow Progress

## Maqsad

Ushbu hujjat GoldBot Data Flow rivojlanishining rasmiy holatini yuritadi.

Har bir Flow quyidagi statuslardan biriga ega bo'ladi va Development davomida muntazam yangilanadi.

**V3 qayta ko'rib chiqish (GFL-002, Director Order):** Flow ID'lar V3
Architecture asosida qayta tashkil qilindi. Hech bir bajarilgan ish
yo'qolmadi -- faqat mapping yangilandi (eski FLOW-001 "Current Price"
endi FLOW-002, statusi va 100% progress'i saqlanib qoldi). Old -> New
mapping jadvali shu buyruqqa javoban yozilgan Director Review chat
xabarida keltirilgan.

---

# Status

🟦 Blueprint

Flow hali boshlanmagan.

---

🟨 In Progress

Flow ustida Development davom etmoqda.

---

🟪 Review

Flow yakunlandi va Director Review kutilmoqda.

---

🟩 Completed

Flow to'liq yakunlandi.

Barcha testlar muvaffaqiyatli o'tgan.

Documentation yangilangan.

WORK_LOG yozilgan.

---

🟥 Blocked

Flow davom eta olmaydi.

Director Review talab qilinadi.

---

# Flow Progress

| Flow | Nomi | Layer / Subsystem | Status | Progress | Owner | Izoh |
|------|------|--------------------|--------|----------|-------|------|
| FLOW-001 | System Bootstrap / Configuration | Foundation Layer | 🟦 | 0% | Worker | Yangi (V3 refactor, GFL-002) -- avval alohida Flow sifatida mavjud emas edi |
| FLOW-002 | Current Price | Data Layer | 🟩 | 100% | Worker | Eski FLOW-001. Yakunlandi -- 2026-08-04. Audit shuni ko'rsatdi: barcha modullar allaqachon mavjud edi, faqat ulanmagan (Price Stream `tick()`ni hech kim chaqirmasdi, `CurrentPriceProvider` default holatda har safar yangi/alohida instance qurar edi). Tuzatildi: shared singleton + default StreamValidator + default MarketMemoryRegistry + polling.py'da tick driver. 5411 test PASS, E2E test qo'shildi. |
| FLOW-003 | Market Memory | Data Layer | 🟩 | 100% | Worker | Eski FLOW-002. Yakunlandi -- 2026-08-04. Audit shuni ko'rsatdi: yozish tomoni (Data Validation -> CandleBuilder yagona yozuvchi) FLOW-001/002 orqali allaqachon production'da ishlagan; Consumer (`MemoryReader`/`MarketManager`) to'liq qurilgan va test qilingan, lekin production kodida hech qachon chaqirilmagan edi. Tuzatildi: `PriceStreamService.memory_registry` public accessor qo'shildi. E2E test to'liq zanjirni (Provider -> Validation -> Market Memory -> Consumer) isbotladi. 5411+ test PASS. |
| FLOW-004 | Market Engine | GoldBot > GoldBot Core | 🟩 | 100% | Worker | Eski FLOW-003. Yakunlandi -- 2026-08-04. Audit shuni ko'rsatdi: haqiqiy "Market Engine" moduli mavjud emas edi (`core_layer/core_engine/` faqat bo'sh skeleton); `data_layer/live_data/market/` (MarketManager) esa arxitektura jihatidan mos kelmadi (o'z hujjatida "NOT GoldBot Core" deb belgilangan). Reuse Analysis: `MarketDataService` Market Memory'ga allaqachon yozar edi (TASK-DATA-004), lekin o'qib qaytarish yo'q edi. Tuzatildi: `MarketDataService.get_candles_from_memory()` + `get_shared_market_data_service()` qo'shildi (yangi modul yaratilmadi). E2E test to'liq zanjirni (Provider -> Validation -> Market Memory -> Market Engine) isbotladi. 5424+ test PASS. |
| FLOW-005 | Context Engine | GoldBot > GoldBot Core | 🟩 | 100% | Worker | Eski FLOW-004. Yakunlandi -- 2026-08-04 (GFL-004 Lightweight Loop). Qisqa Audit: `context_layer.context_engine.context_orchestrator.ContextEngine` SMC/Wyckoff/Liquidity/Structure'ni to'liq amalga oshiradi va allaqachon `core_layer/pipeline.py`ga ulangan (`build_context_snapshot`). Kod o'zgarishi kerak emas. |
| FLOW-006 | Analysis Engine | GoldBot > GoldBot Core | 🟩 | 100% | Worker | Eski FLOW-005. Yakunlandi -- 2026-08-04 (GFL-004 Lightweight Loop). Qisqa Audit: `context_layer.trend.market_phase.compute_market_phase()` 5-holatli (Accumulation/Manipulation/Distribution/Markup/Markdown/Unknown) tsikl bosqichini `ContextSnapshot`ning mavjud maydonlaridan hisoblaydi va allaqachon `core_layer/pipeline.py`ga ulangan (`market_phase` stage). Kod o'zgarishi kerak emas. |
| FLOW-007 | Indicator Engine | GoldBot > GoldBot Core | 🟩 | 100% | Worker | Eski FLOW-006. Yakunlandi -- 2026-08-04 (GFL-004 Lightweight Loop). Qisqa Audit: real indicator hisoblash yo'q edi; `indicator_layer/` Foundation Freeze skeleton (doiradan tashqari). `feature_engine.py`/`feature_model.py`ning mavjud, hujjatlashtirilgan `atr=None` hook'i (Phase A10) topildi -- uning docstringi "separately-approved phase" talab qilar edi, shuning uchun Owner/Director'dan aniq tasdiq so'raldi va olindi (Director Decision: Approve). Tuzatildi: `core_layer/features/atr/compute_atr()` (Wilder's ATR) qo'shildi, `feature_engine.py`ga ulandi (yangi top-level modul yaratilmadi). Hali ham sof advisory -- Signal/AI/Decision/Risk'ga uzatilmaydi. |
| FLOW-008 | Strategy Engine | GoldBot > GoldBot Core | 🟩 | 100% | Worker | Eski FLOW-007. Yakunlandi -- 2026-08-04 (GFL-004 Lightweight Loop). Qisqa Audit: `strategy_layer.strategy_manager.strategy_manager.StrategyManager` (LiquidityStrategy/FVGStrategy/AMDStrategy) allaqachon `signal_layer.signal_engine.SignalEngine` orqali `core_layer/pipeline.py`ning `signal` stage'iga ulangan va test qilingan. Kod o'zgarishi kerak emas. |
| FLOW-009 | Confluence Engine | GoldBot > GoldBot Core | 🟩 | 100% | Worker | Eski FLOW-008. Yakunlandi -- 2026-08-04 (GFL-004 Lightweight Loop). Qisqa Audit: `signal_layer/confluence_engine/` Foundation Freeze skeleton (bo'sh). Haqiqiy confluence scoring -- `signal_layer.signal_scoring.signal_quality.compute_signal_quality()` -- HTF Bias/Structure/Liquidity/Order Blocks/FVG'ni harf darajasiga (A+/A/B/C) birlashtiradi, allaqachon `core_layer/pipeline.py`ning `signal_quality` stage'iga ulangan va test qilingan. Kod o'zgarishi kerak emas. |
| FLOW-010 | Decision Engine | GoldBot > GoldBot Core | 🟩 | 100% | Worker | Eski FLOW-009. Yakunlandi -- 2026-08-04 (GFL-004 Lightweight Loop). Qisqa Audit: `decision_layer.decision_engine.decision_engine.DecisionEngine` (CLAUDE.md Trading Safety'da himoyalangan -- confidence-blending + APPROVE/REJECT/NO_TRADE) allaqachon `core_layer/pipeline.py`ga ulangan va test qilingan. Kod o'zgartirilmadi -- ruxsatsiz o'zgartirish taqiqlangan. |
| FLOW-011 | Risk Engine | GoldBot > GoldBot Core | 🟩 | 100% | Worker | Eski FLOW-010. Yakunlandi -- 2026-08-04 (GFL-004 Lightweight Loop). Qisqa Audit: `risk_layer.risk_engine.risk_manager.RiskManager` (CLAUDE.md Trading Safety'da himoyalangan -- geometry/stop-loss validation + sizing) allaqachon `core_layer/pipeline.py`ga ulangan va keng test qilingan. Kod o'zgartirilmadi. |
| FLOW-012 | Signal Engine | GoldBot > GoldBot Core | 🟩 | 100% | Worker | Eski FLOW-011. Yakunlandi -- 2026-08-05 (GFL-004 Lightweight Loop). Qisqa Audit: `signal_layer.signal_builder.adapter.from_signal_candidate()` + `SignalSchema` allaqachon risk-baholangan candidate'dan portable Signal yig'adi, `core_layer/pipeline.py`ning `signal_history` stage'iga ulangan va test qilingan. Kod o'zgarishi kerak emas. |
| FLOW-013 | Execution Engine | GoldBot > GoldBot Core | 🟩 | 100% | Worker | Eski FLOW-012. Yakunlandi -- 2026-08-05 (GFL-004 Lightweight Loop). Qisqa Audit: `execution_layer.execution_engine.execution_engine.ExecutionEngine` (CLAUDE.md Trading Safety'da himoyalangan -- intentionally inert, haqiqiy MT5 ulanishi alohida ruxsat talab qiladi) allaqachon FLOW-013'ning o'z "hozircha inert" ta'rifiga mos keladi va test qilingan. Kod o'zgartirilmadi -- ruxsatsiz o'zgartirish taqiqlangan. |
| FLOW-014 | Trade Monitoring | GoldBot > GoldBot Core | 🟩 | 100% | Worker | Eski FLOW-013. Yakunlandi -- 2026-08-05 (GFL-004 Lightweight Loop). Qisqa Audit: `trade_monitoring_layer.paper_trading.paper_trade_monitor.PaperTradeMonitor` + `trade_state.TradeState` (CREATED/OPEN/CLOSED/CANCELLED) allaqachon Flow'ning Lifecycle tracking/Trade State ta'rifiga mos, keng test qilingan va Learning Loop/Backtesting/Database orqali real iste'mol qilinadi. Kod o'zgarishi kerak emas. |
| FLOW-015 | GoldBot Core API | GoldBot > GoldBot Core | 🟩 | 100% | Worker | Eski FLOW-014. Yakunlandi -- 2026-08-05 (GFL-004 Lightweight Loop). Qisqa Audit: kanonik `core_layer.service_registry`/`core_layer.core_service` Foundation Freeze skeleton (bo'sh). Haqiqiy "GoldBot Core API" -- `core_layer.gateway.CoreGateway` -- registry/router/auth/rate-limiter/health/metrics/version'ni birlashtiradi, `GatewayRequest`/`GatewayResponse` orqali API response assembly'ni amalga oshiradi, keng test qilingan (`tests/core/gateway/*`, 11 fayl). Kod o'zgarishi kerak emas. |
| FLOW-016 | Chart Service | GoldBot > Chart Service | 🟦 | 0% | Worker | Audit qilindi -- 2026-08-05 (GFL-004 Lightweight Loop). `chart_layer/`ning barcha quyi-paketlari faqat Foundation Freeze v1.0/MIR-001 skeleton (real `.py` fayl yo'q). Kod yozish MIR-001'ni buzadi, shuning uchun yozilmadi. Sub-Status: **Blueprint** (Design hali boshlanmagan) -- xolis audit natijasi, Completed emas. |
| FLOW-017 | Personal AI Core | GoldBot > Personal AI Core | 🟩 | 100% | Worker | Yakunlandi -- 2026-08-05 (GFL-004 Lightweight Loop). Qisqa Audit: `ai_layer/` (207 real fayl, jumladan `ai_layer.personal_ai`) allaqachon Phase 61.0..66.8 davomida qurilgan, Advisory Article 1/3 chegarasi `ai_layer.access` orqali ta'minlangan, keng test qilingan (`tests/ai/*`, 145 fayl). Kod o'zgarishi kerak emas. |
| FLOW-018 | Backtesting Engine | GoldBot > Backtesting Engine | 🟦 | 0% | Worker | Yangi (V3 refactor, GFL-002) -- `backtesting_layer/` mavjud, lekin GFL Flow sifatida hali audit qilinmagan. Sub-Status: Blueprint (Design boshlanmagan). |
| FLOW-019 | Application Services | Application Services | 🟦 | 0% | Worker | Eski FLOW-015. Kutmoqda. |
| FLOW-020 | Telegram | Platform Layer | 🟦 | 0% | Worker | Eski FLOW-016. Kutmoqda. |
| FLOW-021 | Mini App | Platform Layer | 🟦 | 0% | Worker | Eski FLOW-017. Kutmoqda. |
| FLOW-022 | Android | Platform Layer | 🟦 | 0% | Worker | Eski FLOW-018. Kutmoqda. |
| FLOW-023 | iOS | Platform Layer | 🟦 | 0% | Worker | Eski FLOW-019. Kutmoqda. |
| FLOW-024 | Desktop | Platform Layer | 🟦 | 0% | Worker | Eski FLOW-020. Kutmoqda. |
| FLOW-025 | Web | Platform Layer | 🟦 | 0% | Worker | Eski FLOW-021. Kutmoqda. |

---

# Development Rules

Worker faqat bitta Flow ustida ishlaydi.

**GFL-003 -- Sequential Flow Rule (Director qarori):** navbatdagi
ishlanadigan Flow -- ushbu jadvalda yuqoridan pastga qarab birinchi
🟩 Completed bo'lmagan Flow (eng kichik raqamli bajarilmagan Flow ID).
Har bir Flow faqat o'zidan oldingi Flow Approved + Completed + CI
Passed bo'lgandan keyingina boshlanadi. Tartibdan tashqariga chiqib
(masalan FLOW-010'dan FLOW-005'ga) qaytish taqiqlanadi. To'liq ta'rif:
`GFL-001_FLOW_FIRST_STANDARD.md`.

Flow statusi ushbu hujjatda darhol yangilanadi.

---

# Status Lifecycle

Blueprint

↓

In Progress

↓

Review

↓

Completed

yoki

Blocked

↓

Director Review

↓

In Progress

↓

Completed

---

# Progress Rules

Progress faqat:

- Audit
- Development
- Testing
- Validation
- Documentation
- WORK_LOG

yakunlangandan keyin o'zgartiriladi.

---

# Blocked Rules

Agar Flow:

- Input ololmasa
- Output ishlamasa
- End-to-End test o'tmasa
- Director Review talab qilsa

Status:

🟥 Blocked

bo'ladi.

---

# Completion Rules

Flow Completed bo'lishi uchun:

✓ Audit yakunlangan

✓ Kod ishlaydi

✓ Input ishlaydi

✓ Output ishlaydi

✓ Consumer ishlaydi

✓ Barcha Consumer'lar PASS (Fan-Out Rule)

✓ End-to-End Test PASS

✓ Producer→Consumer latency o'lchangan va yozilgan (Latency Rule)

✓ Documentation yangilangan

✓ WORK_LOG yozilgan

✓ Director Review yopilgan (agar talab qilingan bo'lsa)

---

# Final Principle

Flow Progress — GoldBot Development holatini aks ettiruvchi yagona rasmiy hujjat hisoblanadi.

Worker har bir Flow holatini ushbu hujjatda doimiy ravishda yangilab borishi shart.
