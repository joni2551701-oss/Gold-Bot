# FLOW-018 — Backtesting Engine: Production Wiring + Tool-First Foundation

Sana: 2026-08-06. Authority: Director Order (PHASE-02 FLOW-018).
Til: GLS-001 (proza O'zbek, texnik terminlar English).

> Maqsad: Backtesting Engine'ni jonli Telegram `/backtest` Consumer bilan
> **Production Backtesting Service**ga aylantirish. Yangi Backtesting/
> Statistics/Replay/Trading Engine yozilmaydi — faqat mavjud subsystemlar
> Production'ga ulanadi (Reuse First + Tool First).

## 1. Short Audit
Backtesting subsystem allaqachon real kod bilan mavjud edi, lekin jonli
user-facing Consumer YO'Q edi (FLOW-018 Partial re-audit):
- `backtesting_layer/backtest_engine/backtest_engine.py` — `BacktestEngine.run()`
  (to'liq Data→Context→Signal→AI→Decision→Risk→PaperTrade zanjirini
  mavjud, o'zgartirilmagan funksiyalardan composes qiladi).
- `backtesting_layer/statistics/*` — `signal_performance`, `strategy_report`,
  `equity_curve`, `performance_metrics` va h.k. (real).
- `backtesting_layer/backtest_report/backtest_result.py` —
  `BacktestResult` + `build_backtest_result()` + `format_backtest_report()`.
- `backtesting_layer/backtest_service/` — **bo'sh Foundation Freeze
  skeleton** (faqat `__init__.py`).
- `platform_layer/telegram/owner/backtest_commands.py` — `backtest_run()`
  real, ammo **orphaned** (`OWNER_COMMANDS`da yo'q, `handlers.py`da yo'q,
  router yo'q).

Xulosa: Engine + Statistics + Result tayyor; yetishmagani — (a) Director
Pipeline nomlagan **Backtesting Service** qatlami, (b) jonli `/backtest`
komandasi.

## 2. Reuse Analysis
| Kerak | Mavjud modul (o'zgartirilmadi) |
|---|---|
| Backtest hisoblash | `BacktestEngine.run()` |
| Historical Data | `RawCandleRepository` → `ReplayEngine` (DB) |
| Statistics | `statistics/strategy_report` + `signal_performance` |
| Result + format | `backtest_report.format_backtest_report()` |
| Config | `replay_engine.replay_models.ReplayConfig` |
| Telegram Consumer | `commands.OWNER_COMMANDS` + `handlers` + `command_router` |
| Service uyi | mavjud bo'sh `backtest_service` paketi |

Yetishmagani — **service composition** (parse → validate → engine →
format) va **jonli `/backtest`**. Ikkisi ham wiring, yangi engine emas.

## 3. Architecture Review
Yangi fayl: `backtesting_layer/backtest_service/backtest_service.py` —
**composition root**, mavjud bo'sh `backtest_service` paketi ichida
(yangi top-level paket yaratilmadi — Module Reuse Principle). O'z
backtesting/trading logikasi yo'q. `backtest_commands.backtest_run()`
endi shu servisga **delegatsiya** qiladi (duplicate composition yo'q —
CLAUDE.md "No duplicate logic"). Architecture Rule saqlangan:
Backtesting ↔ Chart ↔ Personal AI to'g'ridan-to'g'ri bog'lanmaydi;
Telegram → Handler → Service → Engine yagona yo'l.

## 4. Input → Processing → Output → Consumer
- **Input:** owner Telegram `/backtest <SYMBOL> <TIMEFRAME> <START> <END>`
  (+ optional provider). Historical Data — DB (`RawCandleRepository`).
- **Processing:** parse → validate → `ReplayConfig` → `BacktestEngine.run()`
  (Historical Data → Strategy → Statistics → Result Validation).
- **Output:** `BacktestOutcome{success, message, result, reason}` — `result`
  Performance Summary (counts + `overall_win_rate`), Statistics
  (`strategy_report`), Trade List (`performances`), Validation Status.
- **Consumer:** Telegram (`backtest_handler` → `command_router` → user). ✅ **Jonli.**

## 5. Production Wiring Diagram
```
Telegram (/backtest XAUUSD M15 2026-01-01 2026-02-01)
  → command_router  (OWNER_COMMANDS gate: faqat OWNER)
  → handlers.backtest_handler
  → BacktestService.run_from_args
      → parse_backtest_request          [validation]
      → ReplayConfig
      → BacktestEngine.run()            [Historical Data(DB) → Strategy → Statistics → Result]
      → format_backtest_report(result)
  → javob matni → Telegram → User
```

## 6. Tool Flow Diagram (Tool-First)
```
/backtest
  → BacktestService              [Backtesting Tool]
      → RawCandleRepository / ReplayEngine   [Database]
      → BacktestEngine.run()                 [Tool compute]
      → format_backtest_report               [Result]
  → Response
```
API **yo'q** — butun yo'lda birorta tashqi API chaqiruvi mavjud emas
(Director "Backtesting Tool → Database → Result. API emas.").

## 7. Production Code Summary
- YANGI `backtesting_layer/backtest_service/backtest_service.py`:
  `BacktestRequest` (Input Contract), `BacktestOutcome` (Output Contract),
  `parse_backtest_request()`, `BacktestService.run()/.run_from_args()`,
  `get_backtest_service()` shared singleton.
- MODIFIED `platform_layer/telegram/owner/backtest_commands.py`:
  `backtest_run()` endi `BacktestService`ga delegatsiya qiladi.
- MODIFIED `platform_layer/telegram/handlers.py`: `backtest_handler()`.
- MODIFIED `platform_layer/telegram/commands.py`: `OWNER_COMMANDS["backtest"]`.

## 8-10. Test natijalari
`tests/backtesting/test_backtest_service.py` — **15 test PASS**:
- **Unit:** parse (valid / normalize / kam argument → usage / bad date /
  end≤start rad), service injected engine, engine xatosida raise
  qilmaydi, `run_from_args` invalid → usage.
- **Integration:** real `BacktestEngine` + real DB seed (250 candle →
  `candles_processed=250`), bo'sh dataset → success + 0 candle.
- **End-to-End:** `/backtest` OWNER_COMMANDS'da (COMMANDS'da emas),
  `backtest_handler` mavjud, bo'sh argument → usage, owner `/backtest`
  route → real hisobot ("Backtest natijasi" + "XAUUSD"), non-owner →
  permission denied, shared service singleton.

Regressiya: `tests/telegram/owner/test_backtest_commands.py` +
`tests/backtesting/` = **99 PASS** (delegatsiya mavjud xatti-harakatni
buzmaydi). Full suite: **5490 passed** (5475 → +15).

## 11. Topilgan muammolar
- `backtest_service` paketi bo'sh Foundation skeleton edi — Reuse Rule
  bo'yicha yangi top-level paket o'rniga shu paket ichida
  implement qilindi.
- `backtest_run()` (Phase 60.2) va yangi service o'rtasida duplicate
  composition xavfi bor edi — `backtest_run()` servisga delegatsiya
  qilib bartaraf etildi (bitta joyda engine haydaydi).
- `/backtest` uzoq davom etuvchi sinxron hisoblash (katta oyna uchun)
  — hozircha sinxron; async/progress kelajak optimizatsiya (Recommendation).

## 12. Director Recommendations
1. Katta sana oynasi uchun `/backtest` ni async yoki progress-report
   bilan kengaytirish (hozir sinxron, kichik oynalar uchun yetarli).
2. `/backtest_report` (oxirgi natijani DB'dan Tool orqali ko'rsatish) va
   `/equity` (Equity Curve) keyingi kichik Sprint sifatida — Foundation
   (`equity_curve`, `strategy_report`) tayyor.
3. Per-strategy filter (`BacktestRequest.strategy`) hozircha reserved;
   real filtrlash keyingi Flow'da yoqilishi mumkin.

## 13. Commit ID
Ushbu FLOW-018 ishi `goldbot-v1` branch'iga bitta commit sifatida push
qilindi. Yakuniy commit SHA va GitHub Actions `success` tasdig'i Worker
hisobotining Pre-Commit Verification bo'limida keltiriladi.

## 14. Pre-Commit Verification
CLAUDE.md Commit Protocol to'liq bajarildi (git add -A → pyflakes →
compileall → pytest tests/ → python main.py → git status clean →
git diff --cached reviewed → commit → push → GitHub Actions). To'liq
belgilangan checklist Worker hisobotida.

## 15. GitHub Actions natijasi
Worker hisobotida yakuniy `success` tasdig'i bilan beriladi.

## Success Criteria tekshiruvi
- ✅ Input→Processing→Output→**Real Telegram Consumer** (`/backtest`) mavjud va ishlaydi.
- ✅ Real Production Wiring (Handler → Service → Engine → Result → Telegram).
- ✅ Reuse First (Engine/Statistics/Result/Config o'zgartirilmadi).
- ✅ Tool First (Backtesting Tool → Database → Result; API yo'q).
- ✅ Memory First tamoyiliga zid emas (backtest — Tool/DB compute, Memory oqimiga tegmaydi).
- ✅ Unit / Integration / End-to-End PASS.
