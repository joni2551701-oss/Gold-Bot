# GBA-001 — PRODUCTION READINESS REPORT

## Branch holati — muhim kuzatuv

`.github/workflows/production_deploy.yml`ning izohida aniq yozilgan:
"Deploy branch: main -- the single authoritative production branch."
Ushbu audit esa `goldbot-v1` branch'ida o'tkazilmoqda (order shartiga
ko'ra shu branch'da qolish talab qilingan). Bu ikkisi orasidagi
farq — `goldbot-v1`dagi holat production'ga chiqmagan bo'lishi
mumkinligini bildiradi, agar `main` bilan sinxron bo'lmasa. Bu audit
faqat `goldbot-v1`dagi kodni baholaydi; `main` bilan solishtirish
ushbu audit doirasidan tashqarida.

## CI/CD

`.github/workflows/` ostida 3 ta workflow: `ci.yml`,
`production_deploy.yml`, `trading_bot.yml`.

`production_deploy.yml` release-based, symlink-almashtiriladigan
joylashuv (`/opt/goldbot/{releases,shared,current}`) ishlatadi, VPS
kirish faqat GitHub Secrets orqali (`VPS_HOST/VPS_PORT/VPS_USER/
VPS_SSH_KEY/DEPLOY_PATH`) — fayl ichida "no plaintext credential
appears anywhere in this file" deb ta'kidlangan va bu haqiqatda
tekshirildi (fayl boshidagi izohlarda plaintext qiymat yo'q).
`deploy` bosqichi faqat `validate` (checkout, Python setup, install,
lint, compile, tests) muvaffaqiyatli bo'lgandan keyin ishga tushadi.

## Docker

`Dockerfile` mavjud (repo ildizida). O'z izohida aniq: "Not required
for the current deployment ... This exists as a ready foundation for
a future containerized deployment." `python:3.11-slim` bazasidan
foydalanadi, `requirements.txt`ni o'rnatadi, `CMD ["python",
"main.py"]`. `docker-compose.yml` ham mavjud. **Xulosa: Docker
tayyorgarligi mavjud, lekin hozirgi ishlab chiqarish yo'li (systemd +
GitHub Actions scheduled run) Docker'ga bog'liq emas** — bu ataylab
shunday, docstringda aniq yozilgan.

## systemd

`deploy/systemd/` ostida 7 ta service/timer fayli:
`goldbot-polling.service`, `goldbot.service`,
`goldbot-healthcheck.service`, `goldbot-pipeline.timer`,
`goldbot-healthcheck.timer`, `goldbot-notify-failure@.service`,
`goldbot-pipeline.service`. Bu restart/recovery va scheduled-run
infratuzilmasi mavjudligini ko'rsatadi (timer + healthcheck +
failure-notify alohida service sifatida ajratilgan — bu yaxshi amaliyot).

## Environment variables / Secrets

`09_SECURITY_REPORT.md`da batafsil: `.env.production`/`.env.example`
faqat shablon (bo'sh qiymatlar), `.env` gitignored, real sirlar
`core_layer/secrets/secrets.py` orqali faqat environment
variable'lardan o'qiladi ("No .env file usage for production
security" — docstring, kod bilan mos).

## Logging va error handling

`python main.py` smoke-run logi (`03_RUNTIME_REPORT.md`) tashqi API
kaliti yo'qligida ham structured error (`ExternalAPIError API_002`)
qayd etib, pipeline'ni CRASH qilmasdan davom ettirdi — bu graceful
degradation va logging sifatining ijobiy dalili.

## CLAUDE.md Deployment Authority (Director Order No. 021) muvofiqligi

Ushbu audit **hech qanday deploy amalini bajarmadi** — faqat
mahalliy `python main.py`/`pytest`/`pyflakes`/`compileall` ishga
tushirildi (order aniq belgilagan "read-only" cheklovga mos). VPS'ga
ulanish, production API key o'zgartirish, DNS/firewall o'zgartirish —
bularning hech biri amalga oshirilmadi va oshirilmasligi kerak edi.

## Xulosa

Deployment infratuzilmasi (CI/CD, systemd, Docker foundation, secret
handling) hujjatlashtirilgan holatga mos va real fayllar bilan
tasdiqlangan. Yagona diqqatga molik band — `goldbot-v1` (audit
qilinayotgan branch) va `main` (production deploy branch) orasidagi
farq holati Director tomonidan aniqlashtirilishi kerak (qaysi commit
production'da ishlayotgani ushbu audit doirasida tekshirilmadi).
