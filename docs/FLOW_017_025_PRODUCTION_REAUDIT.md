# FLOW-017 … FLOW-025 — Production Re-Audit + Production Roadmap

Sana: 2026-08-05
Muallif: Worker (Director Order: Production-mezon bo'yicha qayta audit)
Til: GLS-001 (proza O'zbek, texnik terminlar English)

> Direktor buyrug'i: FLOW-017…025 ni **Production mezoni** bo'yicha
> qayta audit qil. Oldingi docs-only "Completed" statuslariga ishonma.
> Har bir Flow uchun haqiqiy **Input → Processing → Output → Consumer**
> zanjiri **ishlashini** tekshir. Ishlasa — Completed; ishlamasa —
> Blueprint yoki Partial. Yangi Feature yozilmaydi — maqsad PHASE-02
> holatini 100% **real** holatga keltirish.

## 0. Production Completion mezoni (bu auditda ishlatilgan)

Bir Flow **Completed** deb belgilanadi, faqat va faqat:
1. **Input** — real kirish manbai mavjud;
2. **Processing** — real ishlov beruvchi kod mavjud (skeleton emas);
3. **Output** — real natija (contract) chiqadi;
4. **Consumer** — natijani **jonli** (live) iste'mol qiluvchi mavjud —
   ya'ni production kod yo'lida (Telegram command router, pipeline,
   entry-point yoki workflow) haqiqatan chaqiriladi.

Agar 1–3 bor, lekin 4 (jonli Consumer) yo'q bo'lsa → **Partial**.
Agar real Processing kodi ham yo'q bo'lsa → **Blueprint**.

Tekshirish usuli: import graph (kim kimni import qiladi), Telegram
command registry (`platform_layer/telegram/commands.py` —
`COMMANDS`/`OWNER_COMMANDS`/`ADMIN_COMMANDS`) va handler wiring
(`handlers.py` + `command_router.py`), pipeline stage'lari
(`core_layer/pipeline/pipeline.py`), `.github/workflows/`, va runtime
probe (`python main.py`, engine import).

---

## 1. Natijalar jadvali (eski vs real)

| Flow | Nomi | Eski status | **Real status** | Sabab (qisqa) |
|---|---|---|---|---|
| 017 | Personal AI Core | 🟩 100% | **🟨 Partial** | Pipeline advisory `AIAnalyzer → DecisionEngine` **jonli + test qilingan** (haqiqiy sub-zanjir). Ammo Personal AI **mahsuloti** (assistant/trading_analyst, Phase 61-66) uchun jonli user-facing Consumer **yo'q** — faqat `ai_status`/`runtime_*` monitoring komandalar ro'yxatga olingan. |
| 018 | Backtesting Engine | 🟩 100% | **🟨 Partial** | `BacktestEngine`/`BacktestResult`/statistics real + test qilingan; statistics modullari `ai_layer` tomonidan iste'mol qilinadi. Ammo `BacktestEngine.run()` uchun **jonli Consumer yo'q** — `backtest_commands.py` orphaned (`OWNER_COMMANDS`da yo'q, `handlers.py`da yo'q, workflow'da yo'q). |
| 019 | Application Services | 🟩 100% | **🟨 Partial** | Telegram application services (`user_service` va h.k.) **jonli** (FLOW-001). Ammo `platform_layer/platform_service` (PlatformRegistry/MenuRegistry/NavigationCore) uchun **0 ta jonli importer** — orphaned Foundation. |
| 020 | Telegram | 🟩 100% | **🟩 Completed** | Handler → Service → Repository jonli; `COMMANDS`+`OWNER_COMMANDS` `handlers.py`+`command_router`da ro'yxatga olingan; yetkazish `Notifier` orqali `main.py`da isbotlangan; 40 test fayli. Haqiqiy Production. |
| 021 | Mini App | 🟦 Blueprint | **🟦 Blueprint** | Jonli UI render yo'q; `PlatformAdapterBase` abstract, concrete client yo'q. |
| 022 | Android | 🟦 Blueprint | **🟦 Blueprint** | `platform_layer/mobile_api/` 13-qatorli skeleton. |
| 023 | iOS | 🟦 Blueprint | **🟦 Blueprint** | `platform_layer/mobile_api/` 13-qatorli skeleton. |
| 024 | Desktop | 🟦 Blueprint | **🟦 Blueprint** | `platform_layer/desktop_api/` 13-qatorli skeleton. |
| 025 | Web | 🟦 Blueprint | **🟦 Blueprint** | `platform_layer/web_api/` 13-qatorli skeleton. |

Xulosa: 4 ta Flow'ning statusi kamaytirildi (017/018/019: Completed → **Partial**).
FLOW-020 haqiqatan Completed. 021-025 Blueprint (avvalgi holat to'g'ri edi).

---

## 2. Har bir Flow uchun Input→Processing→Output→Consumer tahlili

### FLOW-017 — Personal AI Core → 🟨 Partial
- **Input:** ContextSnapshot + SignalCandidate (pipeline), yoki owner so'rovi (Telegram).
- **Processing:** ikki xil AI mavjud:
  - `ai_layer.ai_engine.ai_analyzer.AIAnalyzer` — pipeline advisory (kichik). **Jonli.**
  - `ai_layer.personal_ai` / assistant / trading_analyst / runtime `AIService` — katta mahsulot qatlami (Phase 61-66).
- **Output:** `AIAnalysisResult` (pipeline) — real. Personal AI javob mahsuloti — mavjud lekin.
- **Consumer:**
  - `DecisionEngine.evaluate(candidate, ai_result, htf_bias)` — **jonli, test qilingan** (pipeline `ai` stage).
  - Telegram: faqat `ai_status/ai_provider/ai_cost/ai_usage/ai_health` + `runtime_*` (monitoring/status). **"AI'ga savol ber → AI javob bersin" jonli komandasi YO'Q.**
- **Verdikt:** advisory AI sub-zanjiri **Completed**; Personal AI **mahsulot** Consumer'i **yo'q** → Flow butun holda **Partial**. (Qo'shimcha: real LLM inference `GEMINI_API_KEY`/provider secret talab qiladi; ularsiz AI graceful "offline".)

### FLOW-018 — Backtesting Engine → 🟨 Partial
- **Input:** IDataFeed / ReplayFeed (historical candles).
- **Processing:** `backtesting_layer.backtest_engine.BacktestEngine.run()` — real.
- **Output:** `BacktestResult` + statistics (`performance_metrics`, `equity_curve`, `strategy_report` …) — real.
- **Consumer:**
  - Statistics modullari `ai_layer` analytics tomonidan import qilinadi (learning_loop, analytics_tool, performance) — **jonli, lekin bu "backtest ishga tushirish" emas**.
  - `BacktestEngine.run()` ni **hech kim jonli chaqirmaydi**: `backtest_commands.py` orphaned, `OWNER_COMMANDS`da yo'q, `handlers.py`da yo'q, `.github/workflows/`da backtest runner yo'q.
- **Verdikt:** Processing/Output real + test qilingan; **jonli backtest Consumer yo'q** → **Partial**.

### FLOW-019 — Application Services → 🟨 Partial
- **Jonli qism (Completed):** `platform_layer/telegram/*_service.py` (UserService va h.k.) — Handler'lar SSOT'dan shu servislar orqali o'qiydi (FLOW-001 Module 5, `main.py`da isbotlangan).
- **Orphaned qism (Partial sabab):** `platform_layer/platform_service` (PlatformRegistry / MenuRegistry / NavigationCore / PlatformAdapterBase) — **0 ta jonli importer** (faqat `tests/`). Jonli Telegram oqimi bu registry'ni ishlatmaydi.
- **Verdikt:** Telegram services jonli, lekin "Application Services" deb belgilangan platform_service Foundation jonli iste'molsiz → **Partial**.

### FLOW-020 — Telegram → 🟩 Completed
- **Input:** Telegram update (command/callback/contact).
- **Processing:** `command_router` → `handlers.py` → `*_service.py`.
- **Output:** javob matni / signal notification.
- **Consumer:** foydalanuvchi (jonli yetkazish `Notifier` orqali; `main.py` `telegram_delivery` stage).
- **Verdikt:** to'liq jonli zanjir + 40 test fayli → **Completed**.

### FLOW-021…025 — Platform Clients → 🟦 Blueprint
- `mobile_api` / `desktop_api` / `web_api` — 13-qatorli Foundation Freeze skeleton. Concrete client (Mini App/Android/iOS/Desktop/Web) va server-side client API real kodi yo'q.
- **Verdikt:** **Blueprint** (avvalgi status to'g'ri).

---

## 3. Production Roadmap — PHASE-02 ni 100% real qilish

Ketma-ketlik GFL-003 (Sequential Flow Rule) bo'yicha: eng kichik
raqamli non-Completed Flow avval. Har bir qadam **mavjud modullarni
jonli Consumer'ga ulash** (wiring) — yangi Feature emas.

### Sprint P1 — FLOW-017 Personal AI Core (Partial → Completed)
- Jonli owner-facing AI komandasi ulash (masalan `/ai_ask` yoki
  `/analyze`) — `AIService`/personal_ai runtime'ni chaqirib, javobni
  formatlab qaytaradi. `commands.py` (`OWNER_COMMANDS`) + `handlers.py`
  + `command_router` ga ro'yxatga olish.
- Secret yo'q bo'lsa graceful "AI offline" (mavjud xatti-harakat).
- Consumer test: permission-tier + offline/online.
- **Yangi AI logikasi yozilmaydi** — faqat mavjud runtime'ni jonli
  komandaga ulash.

### Sprint P2 — FLOW-018 Backtesting Engine (Partial → Completed)
- `backtest_commands.py` (allaqachon mavjud) ni jonli ulash:
  `OWNER_COMMANDS`ga `backtest` (+ ehtimol `replay`) qo'shish,
  `handlers.py`da dispatch, `command_router`da ruxsat tekshiruvi.
- Handler `BacktestEngine.run()` → `BacktestResult` → formatlangan
  owner javobi.
- Consumer test: owner `/backtest` → natija.
- **Yangi engine logikasi yozilmaydi.**

### Sprint P3 — FLOW-019 Application Services (Partial → Completed)
- Ikki variant, Director qaroriga havola qilinadi:
  - (A) `platform_service` (NavigationCore/MenuRegistry) ni jonli
    Telegram menu oqimiga ulash; yoki
  - (B) `platform_service` ni rasman **Foundation** (Flow deliverable
    emas) deb qayta tasniflab, FLOW-019 ni jonli telegram services
    asosida Completed deb yopish.
- Tavsiya: (B) — Telegram services allaqachon jonli; platform_service
  kelajakdagi ko'p-platformali abstraction sifatida Foundation'da
  qoladi. Bu Director tasdig'ini talab qiladi.

### Sprint P4 — Orphaned Owner Command modullari (umumiy tozalash)
- FLOW-018 bilan bir qatorda, Phase 59-66'da qurilgan lekin orphaned
  bo'lgan owner command modullari (replay/learning/dataset/execution/
  validation/fundamental/snapshot) uchun **jonli ulash yoki rasman
  "deferred" deb belgilash** — ular hozir `OWNER_COMMANDS`da yo'q. Bu
  PHASE-02 "100% real" maqsadining bir qismi. (Har biri wiring, yangi
  feature emas.)

### Sprint P5 — FLOW-021…025 Platform Clients (Blueprint → Production)
- Yuqori xarajatli, alohida katta ish: server-side client API
  (mobile/desktop/web) + real client. Bu PHASE-02'ning oxirgi va eng
  katta bloki; alohida Director Order va reja talab qiladi. Hozir
  Blueprint sifatida to'g'ri belgilangan.

---

## 4. Director Review — xulosa

- **Topilgan asosiy muammo:** 017/018/019 "Completed" statuslari
  docs-only edi — kod va testlar mavjud, lekin **jonli Consumer** yo'q
  (yoki qisman). Bu Production mezoni bo'yicha **Partial**.
- **FLOW-020** haqiqatan Production Completed.
- **021-025** to'g'ri Blueprint.
- **Reja:** P1→P5 ketma-ketligi PHASE-02 ni 100% real holatga keltiradi;
  har bir qadam mavjud modullarni jonli Consumer'ga ulash (wiring),
  yangi Feature emas.
- **Bu turda kod yozilmadi** — faqat audit, qayta tasniflash va
  roadmap (Director buyrug'iga muvofiq). Implementatsiya keyingi
  Sprint'larda, Sequential Flow Rule bo'yicha FLOW-017'dan boshlanadi.

Kutilayotgan Director qarori: (1) P3 uchun variant (A) yoki (B);
(2) Sprint P1'dan (FLOW-017) boshlashga ruxsat.
