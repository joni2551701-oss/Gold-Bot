# 36 — REAL-DATA-004 Release Gate (Section-24 gate jadvali)

## Gate jadvali

| Transition / Gate | Talab | Natija | Evidence |
|---|---|---|---|
| Core → Context | PASS | ✅ PASS | `pipeline.py:369`; `context_orchestrator.py:107,289` |
| Context → Indicator | PASS | ✅ PASS (ownership: skeleton) | `context_orchestrator.py:121-132` |
| Indicator → Strategy | PASS | ✅ PASS | `signal_engine.py:23`; `strategy_manager.py:23-34` |
| Strategy → Signal | PASS | ✅ PASS | `strategy_manager.py:28-34`; `pipeline.py:405` |
| Signal → Decision (AI advisory boundary) | PASS | ✅ PASS | `pipeline.py:487`; `decision_engine.py:195-255` |
| Decision → Risk (Risk chetlab o'tilmagan) | PASS | ✅ PASS | `pipeline.py:495`; `risk_manager.py:131` |
| Risk → Execution (real order) | — | ⛔ NOT VERIFIED (dizayn) | `pipeline.py:176-179` |
| Execution → Trade Monitoring (real pozitsiya) | — | ⛔ NOT VERIFIED (dizayn) | `pipeline.py:1-29` (import yo'q) |
| Core/API → Service | PASS | ✅ PASS | `pipeline.py:568`; `handlers.py:171-179` |
| Service → Telegram (AI bypass yo'q) | PASS | ✅ PASS | `notifier.py:24-30`; `pipeline.py:599` |
| Telegram → User (real receipt) | — | ⛔ NOT VERIFIED | `notifier.py:39-41` |
| Bypass audit (provider re-fetch) | 0 bypass | ✅ 0 production bypass | 35-hujjat |
| Trading logic o'zgarishi | 0 | ✅ 0 (read-only audit) | — |
| Test suite | 5493 passed | ⏳ lokal PASS, CI kutilyapti | commit protokol |
| Real main.py runtime (CI dispatch) | real per-stage log | ⏳ PLACEHOLDER | 34-hujjat |

## ⏳ PLACEHOLDER — REAL runtime tasdiqi (GitHub Actions dispatch)

> Orchestrator `ci.yml`'ni `workflow_dispatch` bilan ishga tushirgandan
> keyin, `real_data_probe` job'idagi "Real pipeline runtime trace
> (main.py, real market data)" qadamining real logi bu yerga (va
> 34-hujjatga) qo'yiladi: real candle soni, real signal/decision/risk
> natija sonlari.

## Umumiy verdikt

REAL-DATA-004 (Core → User E2E) uchun halol umumiy verdikt:

**BLOCKED** — ikki aniq transitionда:
1. **Risk → Execution (real trade)** — execution ataylab inert (CLAUDE.md
   Trading Safety). Unblock: **Director approval** (execution'ni yoqish).
2. **Telegram → User (real receipt)** — noma'lum destination'ga real
   xabar yuborib bo'lmaydi. Unblock: **Director tasdiqlagan xavfsiz test
   chat ID**, yoki VPS'da nazorat ostidagi test kanali.

Qolgan barcha transitionlar: **PASS** (Core→Context, Context→Indicator,
Indicator→Strategy, Strategy→Signal, Signal→Decision, Decision→Risk,
Core/API→Service, Service→Telegram) — har biri real kod va file:line
dalili bilan.

Bu BLOCKED holati **kutilgan va order tomonidan oldindan ruxsat etilgan**
— execution-inert-by-design va Telegram→User xavfsiz emasligi yashiriladi
gan nosozlik emas, balki hujjatlashtirilgan dizayn/xavfsizlik chegarasi.
</content>
