# GBA-002 — Release Candidate (RC1) Plan

`RELEASE_MANAGEMENT_STANDARD.md` (Director Order No. 020)ga ko'ra,
Release Lifecycle: Planning -> Development -> Internal Testing -> QA
-> Alpha -> Beta -> Release Candidate -> Production -> Maintenance ->
Hotfix -> End of Life. Worker Authority Release Candidate darajasida
to'xtaydi — Production Release har doim Director tasdig'ini talab
qiladi.

## RC1 yaratish shartlari (Success Criteria)

RC1 quyidagi shartlar bajarilgandan **keyingina** yaratilishi mumkin:

1. **Branch Strategy qarori qabul qilingan** — Variant A/B/C'dan biri
   Director tomonidan tasdiqlangan (`09_DIRECTOR_RECOMMENDATION.md`).
   Hozircha bu qaror yo'q — RC1 hali yaratilmaydi.
2. **AI/Media chegarasi hujjatlashtirilgan** — `docs/ARCHITECTURE.md`
   `ai_layer -> media_layer.telegram_broadcast` (va yangi topilgan
   `media_layer -> ai_layer` teskari) chetlarini rasman qamrab olishi
   kerak. Bu — kod o'zgarishi emas, faqat hujjat yangilanishi, Worker
   o'z vakolati doirasida (Documentation Evolution, Order No. 016)
   amalga oshira oladi, lekin ushbu GBA-002 auditi doirasida (read-only)
   bajarilmaydi.
3. **CLAUDE.md'ning to'liq Commit Protocol'i o'tgan** — `pyflakes`,
   `compileall`, `pytest tests/` (5490+ o'tgan bo'lishi kerak),
   `python main.py` smoke check — barchasi tanlangan canonical
   branch'da PASS bo'lishi kerak (RC1 tayyorlash vaqtida qayta
   tekshiriladi).
4. **Version Number va Release Notes** — `RELEASE_MANAGEMENT_STANDARD.md`
   talab qiladigan majburiy maydonlar (Version Number, Scope, Features,
   Breaking Changes, Migration Guide, Test Summary, Performance
   Summary, Security Review, Known Issues, Rollback Strategy) tayyor
   bo'lishi kerak.
5. **Release Checklist** (`RELEASE_MANAGEMENT_STANDARD.md`) — Architecture
   Validation, Engineering Validation, Development Validation,
   Regression Test, Performance Test, Security Review, Documentation
   Review, CHANGELOG, Director Approval — barchasi bajarilishi kerak.

## Hozirgi holat GBA-002 nuqtai nazaridan

- Shart 1 — **bajarilmagan**: Branch strategy qarori hali Director
  tomonidan qabul qilinmagan (ushbu audit shu qarorni tayyorlash uchun
  material taqdim etadi, `09_DIRECTOR_RECOMMENDATION.md`).
- Shart 2 — **qisman bajarilmagan**: AI/Media chegarasi Variant A
  (Allowed) ekanligi tasdiqlangan, lekin `docs/ARCHITECTURE.md`
  hujjatining o'zi hali yangilanmagan.
- Shart 3 — GBA-001'da `goldbot-v1`da tasdiqlangan (5400/5400 pytest,
  0 pyflakes/compileall xato, `main.py` exit=0). GBA-002 o'zining
  Commit Protocol bosqichida bu holatni qayta tasdiqlaydi (quyida,
  yakuniy hisobotda).
- Shart 4-5 — hali tayyorlanmagan (Branch qarori qabul qilingandan
  keyingi bosqich).

## Xulosa

**RC1 hozircha yaratilishga tayyor emas.** Ikkita ochiq blocker bor:
(a) qaysi branch canonical ekanligi haqida Director qarori, (b)
ARCHITECTURE.md'ning AI/Media chegarasini hujjatlashtirishi. Ikkalasi
ham past-o'rta xavfli va tez hal qilinadigan (kod o'zgarishi talab
qilmaydi), lekin ushbu GBA-002 auditi doirasida (read-only investigation)
bajarilmaydi — Director qaroridan keyingi alohida ish sifatida
rejalashtiriladi.
