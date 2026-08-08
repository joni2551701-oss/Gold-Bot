# 01 — Runtime Trace (Core → User) — REAL-DATA-009

## Maqsad

REAL-DATA-009 — Core→User runtime zanjirini file:line dalil bilan
tekshirish (AUDIT-ONLY, production `.py` o'zgartirilmaydi). Ushbu audit
REAL-DATA-004'ning haqiqiy runtime oqimini qayta ishlatadi (CI run
`31240675527`, commit `ea3d055`, real XAU/USD 200 candle) — CI qayta
dispatch qilinmaydi, o'sha dalil kuchda.

## Live pipeline

Barcha transition'lar `core_layer/pipeline/pipeline.py`'ning
`TradingPipeline.run()` (line 310-652) ichida yuritiladi. Stage tartibi
va aniq chaqiruv qatorlari:

| # | Stage | Chaqiruv | file:line |
|---|---|---|---|
| 1 | market_data | `self.data_normalizer.get_candles(...)` | `pipeline.py:325` |
| 2 | data_quality | `assess_data_quality(candles, interval)` | `pipeline.py:340` |
| 3 | htf_bias | `compute_htf_bias(htf_snapshot)` | `pipeline.py:358` |
| 4 | context | `build_context_snapshot(candles, htf_bias)` | `pipeline.py:369` |
| 5 | market_phase | `compute_market_phase(context)` | `pipeline.py:381` |
| 6 | signal | `self.signal_engine.generate_signals(context)` | `pipeline.py:405` |
| 7 | signal_quality | `compute_signal_quality(...)` | `pipeline.py:422` |
| 8 | explainability/features | `explain_signal` / `compute_market_features` | `pipeline.py:440,453` |
| 9 | ai | `self.ai_analyzer.analyze(candidate, context)` | `pipeline.py:477` |
| 10 | decision | `self.decision_engine.evaluate(candidate, ai_result, htf_bias)` | `pipeline.py:487` |
| 11 | risk | `self.risk_manager.evaluate(decision)` | `pipeline.py:495` |
| 12 | signal_history | `from_signal_candidate(...)` | `pipeline.py:519` |
| 13 | telegram_format | `self.signal_formatter.format_signal(...)` | `pipeline.py:568` |
| 14 | telegram_delivery | `self.notifier.send_messages(telegram_messages)` | `pipeline.py:599` |
| 15 | database | `self.signal_repository.save_signal_record(record)` | `pipeline.py:625` |

## Xulosa

Har bir transition alohida faylda (02-10) INPUT → PROCESSING → OUTPUT →
NEXT CONSUMER + Ownership + Status bo'yicha tahlil qilingan. Real
runtime dalil 12-faylda (REAL-DATA-004 run `31240675527`). Umumiy
holat: data→risk zanjiri real runtime bilan PASS; user delivery
(Telegram→User) NOT VERIFIED (xavfsiz destination + approved signal
kerak, sandbox'da bajarilmaydi).
</content>
</invoke>
