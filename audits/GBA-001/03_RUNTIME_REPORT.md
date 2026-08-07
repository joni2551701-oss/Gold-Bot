# GBA-001 — RUNTIME AUDIT REPORT

## Buyruq va natija

```
$ time (timeout 60 python main.py)
exit=0
real  0m5.773s
```

## Pipeline bosqichlari — logdan olingan haqiqiy dalil

`python main.py` ishga tushganda quyidagi bosqichlar ketma-ket, real
vaqt shtampi bilan qayd etildi (`/tmp/main_run.log`dan iqtibos,
qisqartirilmagan ketma-ketlik):

1. `GoldBot starting...` / `Configuration loaded.`
2. Database schema init (`monitoring_error_events`,
   `monitoring_decision_pipeline`, `monitoring_process_starts`,
   `emergency_states`, `audit_log`, `risk_decisions`,
   `risk_account_state`, `signals` jadvallari) — barchasi
   "initialized successfully" natija bilan.
3. `TelegramBot init failed (token missing/invalid): Secret
   'TELEGRAM_BOT_TOKEN' not found in environment.` — WARNING, bu
   audit muhitida `.env` sozlanmagani uchun kutilgan holat (crash
   emas, graceful degradation).
4. `Trading Pipeline initialized.` / `GoldBot started` / `Starting
   pipeline...`
5. `pipeline_started` -> `stage=market_data` (TWELVE_DATA_API_KEY
   yo'qligi sababli 0 ta candle, `ExternalAPIError API_002` xatosi
   to'g'ri qayd etilgan, pipeline CRASH bo'lmadi)
6. `stage=data_quality` -> `valid=False score=0.00
   issues=['empty_data']`
7. `stage=htf_bias` -> `HTF bias computed: bias=UNKNOWN
   confidence=0.00`
8. `stage=context`
9. `stage=market_phase` -> `Market phase: UNKNOWN`
10. `stage=signal` -> `Generated 0 signal candidate(s).`
11. `stage=signal_quality`
12. `stage=explainability`
13. `stage=features`
14. `stage=ai`
15. `stage=decision` -> `Produced 0 trade decision(s).`
16. `stage=risk` -> `Produced 0 risk result(s).`
17. `stage=signal_history`
18. `stage=telegram_format` -> `Produced 0 telegram message(s).`
19. `stage=telegram_delivery` -> `Sent 0/0 telegram notification(s).`
20. `stage=database` -> `Persisted 0 signal record(s).`
21. `pipeline_finished duration=0.003s`
22. `Pipeline finished.` / `GoldBot run cycle completed: 0 signal(s),
    0 decision(s), 0 telegram message(s).` / `GoldBot finished.`

**Xulosa:** 12 ta asosiy bosqich (`market_data, data_quality,
htf_bias, context, market_phase, signal, signal_quality,
explainability, features, ai, decision, risk, signal_history,
telegram_format, telegram_delivery, database` — jami 15 ta nomlangan
stage yorlig'i) barchasi haqiqatda bajarildi, hech biri
o'tkazib yuborilmadi va hech qanday unhandled exception yoki
traceback chiqmadi (`exit=0`). Bu `core_layer/pipeline/pipeline.py`
orkestratori haqiqatan ham hujjatlashtirilgan
Data->Context->Signal->AI->Decision->Risk->Telegram->Database oqimini
bajarayotganining to'g'ridan-to'g'ri dalili.

## API kalitlari yo'qligi — nima bu, nima emas

Bu sandbox muhitida `TELEGRAM_BOT_TOKEN`, `TWELVE_DATA_API_KEY`,
`GEMINI_API_KEY` kabi maxfiy kalitlar sozlanmagan (`core_layer/secrets/secrets.py`
`Secrets.get()` ular yo'qligida `ValueError` tashlaydi va bu chaqiruv
joyida `try/except` bilan tutib olinib, pipeline davom etadi — bu
"buzilgan" emas, balki "graceful degradation" dizayn qarori. Real VPS
muhitida to'g'ri `.env`/environment variable bilan bu bosqichlar
haqiqiy candle ma'lumotlari bilan ishlaydi — buni ushbu audit muhitida
tekshirish MUMKIN EMAS edi (tashqi API kalitlari yo'q), shuning uchun
**qisman tasdiqlangan**: kod yo'li ishlaydi, lekin haqiqiy TwelveData/
Gemini javob formatlari bilan end-to-end ishlashi ushbu audit doirasida
tekshirilmadi (bu tashqi tarmoq chaqiruvlarini talab qiladi).

## Test suite orqali runtime tasdiqi

```
$ python -m pytest tests/ -q
5400 passed in 103.24s
```
Kutilgan "5400+ passed" mezoniga mos keladi — audit muhitida
qo'shimcha o'zgartirish kiritilmagan holda.
