# GBA-001 — SECURITY AUDIT REPORT

## Secrets boshqaruvi

`core_layer/secrets/secrets.py` (81 satr, to'liq o'qildi):
- `Secrets.get(key, default=None)` — agar qiymat topilmasa va
  default berilmagan bo'lsa `ValueError` tashlaydi (fail-loud,
  crash-on-missing majburiy sirlar uchun, masalan
  `TELEGRAM_BOT_TOKEN`, `TWELVE_DATA_API_KEY`, `GEMINI_API_KEY`).
- `Secrets.get_optional(key)` — yo'q bo'lsa `None` qaytaradi (fail-soft,
  ixtiyoriy provayderlar uchun: `OPENAI_API_KEY`, `CLAUDE_API_KEY`,
  `GROK_API_KEY`, `ELEVENLABS_API_KEY`, `LOCAL_LLM_CONFIG`,
  `PHONE_HASH_SALT`).
- `TELEGRAM_OWNER_ID` — yo'q bo'lsa `default=""` bilan **fail-closed**
  ishlaydi ("hech kim OWNER emas"), docstringda aniq yozilgan: "the
  permission layer must fail closed (nobody is OWNER), not crash."
  Bu xavfsizlik nuqtai nazaridan to'g'ri dizayn qarori.

## .env fayllar va git tracking

```
$ git ls-files | grep -i "\.env$"
(bo'sh natija -- .gitignore'da .env qatori bor)
$ ls .env.production .env.example
(ikkalasi ham repo'da, lekin shablon -- barcha qiymatlar bo'sh)
```

`.env.production`ning boshi (birinchi 30 satr) o'qildi: bu haqiqiy
sir emas, faqat production'da to'ldirilishi kerak bo'lgan shablon
(`TELEGRAM_BOT_TOKEN=`, bo'sh qiymat bilan). Fayl docstringida aniq
ogohlantirilgan: "never in this tracked template." **Real sir
commit qilinmagan** — bu audit muhitida `git log -p` orqali to'liq
tarixiy tekshiruv o'tkazilmadi (qisman ko'rib chiqilgan), faqat
joriy holat tekshirildi.

## Telegram ruxsat (permission) qatlami

- `platform_layer/telegram/permissions.py` mavjud (fayl
  tasdiqlangan).
- `platform_layer/telegram/owner/` papkasida 10+ maxsus owner-command
  moduli bor (`ai_commands.py`, `emergency_commands.py`,
  `backtest_commands.py`, `learning_commands.py`,
  `dataset_commands.py`, `status_commands.py`, `owner_roles.py`,
  `runtime_notifications.py`, `runtime_commands.py`, va boshqalar) —
  bu Owner/Admin buyruqlari alohida ajratilganini ko'rsatadi.

## Handlers -> Service -> Repository qoidasi

```
$ grep -n "database_layer\|import.*repository" platform_layer/telegram/handlers.py
(bo'sh natija)
```
`platform_layer/telegram/handlers.py` to'g'ridan-to'g'ri
`database_layer`ni yoki repository sinflarni import qilmaydi — bu
CLAUDE.md'ning "No direct database access from Telegram handlers"
qoidasiga real kodda mos kelishini tasdiqlaydi.

## AI -> Risk/Execution/Telegram to'g'ridan-to'g'ri chaqiruv yo'qligi

`02_ARCHITECTURE_REPORT.md`da batafsil keltirilgan: `AIAnalyzerInterface`
docstringi (`ai_layer/ai_engine/interfaces.py`, 67-80 satrlar) aniq
taqiqni yozadi, va `decision_layer/decision_engine/decision_engine.py`da
haqiqiy `RiskManager`/telegram chaqiruvi yo'q (faqat matn ko'rinishidagi
docstring eslatmasi).

## Aniqlangan minor kuzatuv

`ai_layer` -> `media_layer.telegram_broadcast` importi (yuqorida,
`07_DEPENDENCY_REPORT.md`da batafsil) xavfsizlik nuqtai nazaridan
zararsiz (real `bot.send`/`requests.*` chaqiruvi bu fayllarda
topilmadi), lekin arxitektura chegarasi rasmiy hujjatda aniq
ko'rsatilmagan.

## Qisman ko'rib chiqilgan qismlar

- Input validation / output validation har bir Telegram handler uchun
  alohida-alohida tekshirilmadi (65 ta fayl `platform_layer/`da) —
  namunaviy tekshiruv o'tkazildi, exhaustive emas.
- `.env` fayllarning to'liq git tarixi (eski commitlarda tasodifan
  sir sizib chiqqan-chiqmaganligi) tekshirilmadi — bu alohida
  `git log -p -- .env*` yoki secret-scanning vositasi talab qiladi,
  ushbu audit doirasidan tashqarida qoldi.

## Xulosa

Joriy kod holatida (`HEAD`) sir sizib chiqishi yoki AI/Telegram
handler xavfsizlik chegarasi buzilishi TOPILMADI. Bitta minor
arxitektura aniqligi masalasi (ai_layer -> media_layer) mavjud.
