# 34 — Full Runtime Trace (Section-20 jadvali)

## Transition jadvali

| Transition | Runtime | Evidence (file:line) | Status |
|---|---|---|---|
| Core → Context | `build_context_snapshot(candles, htf_bias)` → `ContextEngine.build()` | `core_layer/pipeline/pipeline.py:369`; `context_layer/context_engine/context_orchestrator/context_orchestrator.py:107,289` | PASS |
| Context → Indicator | Indicator-ekvivalent detektorlar `ContextEngine.build()` ichida | `context_layer/context_engine/context_orchestrator/context_orchestrator.py:121-132`; `indicator_layer/indicator_service/__init__.py:1-13` (skeleton) | PASS (ownership: skeleton) |
| Indicator → Strategy | `SignalEngine.generate_signals` → `StrategyManager.run_all_strategies` | `signal_layer/signal_engine/signal_engine.py:17,23`; `strategy_layer/strategy_manager/strategy_manager.py:23-34` | PASS |
| Strategy → Signal | StrategyManager → SignalCandidate list; SignalScoring/Formatter | `strategy_layer/strategy_manager/strategy_manager.py:28-34`; `core_layer/pipeline/pipeline.py:405,421,568` | PASS |
| Signal → Decision | `DecisionEngine.evaluate(candidate, ai_result, htf_bias)` | `core_layer/pipeline/pipeline.py:487`; `decision_layer/decision_engine/decision_engine.py:195-255` | PASS |
| Decision → Risk | `RiskManager.evaluate(decision)` (chetlab o'tilmagan) | `core_layer/pipeline/pipeline.py:495`; `risk_layer/risk_engine/risk_manager.py:100-248` | PASS |
| Risk → Execution | Real order yo'q; execution inert | `core_layer/pipeline/pipeline.py:176-179` (import yo'q `:1-29`) | NOT VERIFIED (dizayn) |
| Execution → Trade Monitoring | Real pozitsiya yo'q; monitoring live yo'lda emas | `core_layer/pipeline/pipeline.py:1-29` (import yo'q) | NOT VERIFIED (dizayn) |
| Core/API → Service | SignalFormatter DTO; handlers → `*_service.py` (FLOW-019) | `core_layer/pipeline/pipeline.py:568`; `platform_layer/telegram/handlers.py:171-179` | PASS |
| Service → Telegram | `Notifier.send_messages` / handler → Telegram API; AI→TG bypass yo'q | `core_layer/pipeline/pipeline.py:599`; `platform_layer/telegram/notifier.py:24-30` | PASS |
| Telegram → User | Real send noma'lum destination'ga qilinmadi | `platform_layer/telegram/notifier.py:39-41` | NOT VERIFIED |

## Lokal runtime trace (main.py, egress-blocked sandbox, key yo'q)

main.py graceful ishladi — barcha bosqichlar yuritildi:
```
stage=market_data ... Fetched 0 candles.
stage=data_quality ... valid=False issues=['empty_data']
stage=htf_bias ... HTF bias: UNKNOWN
stage=context / stage=market_phase (UNKNOWN)
stage=signal ... Generated 0 signal candidate(s).
stage=signal_quality / explainability / features
stage=ai / stage=decision ... Produced 0 trade decision(s).
stage=risk ... Produced 0 risk result(s).
stage=signal_history / telegram_format ... Produced 0 telegram message(s).
Sent 0/0 telegram notification(s).
stage=database ... Persisted 0 signal record(s).
pipeline_finished
```
Lokal muhitda 0 candle (kalit yo'q, egress-blocked — kutilgan). Har bir
bosqich log qatori mavjud — pipeline butun zanjirni ishga tushiradi.

## ⏳ PLACEHOLDER — REAL main.py runtime log (GitHub Actions dispatch)

> **To'ldiriladi (orchestrator dispatch qilgandan keyin):** `ci.yml`ning
> `real_data_probe` job'iga qo'shilgan "Real pipeline runtime trace
> (main.py, real market data)" qadami real `TWELVE_DATA_API_KEY` bilan
> ishlaydi va real per-stage loglarni beradi ("Fetched N candles",
> "Generated K signal candidate(s)", "Produced M decision(s)",
> "Produced R risk result(s)"). Bu bo'lim o'sha real log bilan
> to'ldiriladi.
>
> ```
> [ REAL main.py RUNTIME LOG — to be filled from CI run ]
> ```
</content>

---

## ⚡ REAL main.py RUNTIME LOG (GitHub Actions, run 31240675527, commit ea3d055)

Real TwelveData XAU/USD (200 candles) bilan to'liq pipeline bir marta
ishga tushdi. Har bir stage real data bilan bajarildi:

```
stage=market_data     Fetched 200 candles        (0.466s, real API)
stage=data_quality    valid=True score=100.00
stage=htf_bias        NEUTRAL conf=50 quality=0.67 timeframes=['H4','H1']
                      (Daily parse FAILED -- yangi finding, pastda)
stage=context         (ran)
stage=market_phase    MARKUP (TRENDING BULLISH)
stage=signal          Generated 1 signal candidate(s)   [FVG_STRATEGY, BUY]
stage=signal_quality  grade=B score=40 criteria=[STRUCTURE_ALIGNED, FVG_ALIGNED]
stage=features        [('TRENDING','LONDON_NEW_YORK_OVERLAP','B')]
stage=ai              approved=False confidence=0.00 risk_score=1.00 (heuristic stub)
stage=decision        Produced 1 trade decision(s)
stage=risk            Produced 1 risk result(s)          [RiskManager.evaluate() ran]
stage=signal_history  1 record linked to context snapshot b1b6fcee-...
stage=telegram_format Produced 0 telegram message(s)     (AI approved=False -> not notification-eligible)
stage=telegram_delivery Sent 0/0
stage=database        Persisted 1 signal record(s)
run cycle: 1 signal(s), 1 decision(s), 0 telegram message(s)
```

**Bu real runtime isbot:** Core -> Context -> market_phase -> Signal
(FVG_STRATEGY) -> signal_quality -> features -> AI (advisory, rad etdi)
-> Decision -> Risk (RiskManager.evaluate ishladi) -> signal_history
-> telegram_format -> database — barchasi real XAU/USD data bilan
bajarildi. `telegram_format` 0 xabar ishlab chiqardi, chunki AI
signalni rad etdi (approved=False) — bu Trading Safety notification-
eligibility filtri to'g'ri ishlayotganini ko'rsatadi (REJECT/BLOCKED
signallar Telegram'ga o'tmaydi), xatolik emas.

## ⚠️ YANGI FINDING — Daily timeframe parse bug (real runtime'da topildi)

`TwelveDataClient.fetch_candles()` (`data_layer/providers/twelve_data_client/twelve_data_client.py:112`)
`v["datetime"]`ni `"%Y-%m-%d %H:%M:%S"` formati bilan parse qiladi,
ammo Daily interval uchun TwelveData faqat sana (`"2026-08-08"`, vaqtsiz)
qaytaradi -> `ValueError` -> Daily candles parse bo'lmaydi -> HTF bias
Daily'ni yo'qotadi (faqat H4/H1 ishlatildi, quality_score 0.67).

Bu REAL-DATA-003'dagi Daily/D1 memory-vocabulary finding'idan ALOHIDA
— bu haqiqiy parse-format bug. Order section 22'ga ko'ra ("HTF Daily
uchun yangi fix kiritilmasin") bu task'da TUZATILMAYDI, faqat finding
sifatida qayd etiladi. Director qaroriga havola (keyingi Sprint):
Daily uchun date-only formatni ham qo'llab-quvvatlash. Ta'sir: HTF
bias context-only, hozircha hech qanday trading qarorini bloklamaydi
(pipeline HTF'siz ham to'liq ishladi va signal ishlab chiqardi).
