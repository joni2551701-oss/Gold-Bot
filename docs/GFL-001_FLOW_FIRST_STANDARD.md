# GFL-001 — Flow-First Development Standard

## Maqsad

GoldBot'ni Layer-first emas, Flow-first tamoyili asosida ishlab chiqish.

Asosiy maqsad — har bir ma'lumot oqimi (Data Flow) boshidan oxirigacha ishlaydigan holatga kelgandan keyingina keyingi oqimni boshlash.

## Asosiy qoida

Har bir Flow quyidagi zanjir bo'yicha quriladi:

Producer → Input → Processing → Output → Consumer

Har bir modul o'zidan oldingi modulning Output'ini qabul qiladi va keyingi modul uchun Input yaratadi.

## Development tartibi

Development yuqoridan pastga emas, balki ma'lumot oqimi bo'yicha ketadi.

**V3 Architecture (GFL-002, Director qarori):** Development endi
quyidagi olti Layer bo'yicha ketadi -- Foundation Layer -> Data Layer
-> GoldBot -> Application Services -> Platform Layer -> End User.
GoldBot ichida to'rtta parallel subsystem bor: GoldBot Core, Chart
Service, Personal AI Core, Backtesting Engine. To'liq diagramma:
`GFL-001_FLOW_FIRST_DIAGRAM.md`.

Misol:

Configuration (Foundation Layer)
→ Provider Factory / Price Stream / Data Validation (Data Layer)
→ Market Memory (SSOT, Data Layer)
→ GoldBot Core (Market Engine → ... → GoldBot Core API)
  | Chart Service | Personal AI Core | Backtesting Engine  (GoldBot, parallel subsystemlar)
→ Application Services
→ Telegram / Mini App / Android / iOS / Desktop / Web (Platform Layer)

Bu yerda bitta Producer'dan chiqqan data bir nechta Consumer'ga tarqalishi mumkin.

## Consumer qoidasi

Consumer hech qachon Producer'ni bevosita chetlab o'tmaydi.

Barcha Consumer'lar faqat:

- Market Memory
- GoldBot Core API
- Application Services

orqali o'qiydi.

## Module Contract

Har bir modul quyidagilarni aniq e'lon qiladi:

- Producer
- Input
- Processing
- Output
- Consumer
- Dependencies
- Validation
- Tests

## Completion Criteria

Har bir Flow quyidagilar bilan tugallangan hisoblanadi:

- Input ishlaydi
- Processing ishlaydi
- Output ishlaydi
- Consumer ishlaydi
- **Barcha Consumer'lar PASS** (Fan-Out Rule — pastga qarang)
- End-to-end test o'tadi
- **Har bir Producer→Consumer latency o'lchangan va yozilgan** (Latency Rule — pastga qarang)
- Documentation yangilanadi
- WORK_LOG yoziladi

## Fan-Out Rule

(Director qarori — GFL-001 pilot natijasidan keyin kiritildi.)

Bitta Producer bir nechta Consumer'ga ma'lumot tarqatishi mumkin
(fan-out). Bunday Flow faqat **barcha** Consumer'lar tekshirilib PASS
bo'lgandagina Completed hisoblanadi.

Misol:

Current Price
↓
Telegram   PASS
↓
Web        PASS
↓
Android    PASS
↓
Desktop    PASS
↓
Mini App   PASS

Agar bitta Consumer ishlamasa:

Flow Completed EMAS.

Eslatma (repo hozirgi holati, V3 raqamlash bo'yicha): canonical
25-Flow modelida ikkita fan-out nuqtasi bor. (1) Data Layer -> GoldBot:
Market Memory (FLOW-003) to'rtta parallel subsystemga -- GoldBot Core
(FLOW-004), Chart Service (FLOW-016), Personal AI Core (FLOW-017),
Backtesting Engine (FLOW-018) -- tarqaladi. (2) GoldBot -> Platform:
Telegram (FLOW-020), Mini App (FLOW-021), Android (FLOW-022), iOS
(FLOW-023), Desktop (FLOW-024), Web (FLOW-025) -- bularning barchasi
Application Services (FLOW-019) fan-out nuqtasining Consumer'lari.
Hozirda faqat Telegram real platforma sifatida va faqat GoldBot Core
zanjiri (FLOW-004..015) haqiqiy Flow sifatida mavjud; qolganlari
(Mini App/Android/iOS/Desktop/Web, Chart Service/Personal AI
Core/Backtesting Engine) hali Blueprint. Har bir platforma/subsystem
paydo bo'lgach, tegishli Flow uchun Fan-Out Rule majburiy bo'ladi.

## Latency Rule

(Director qarori — GFL-001 pilot natijasidan keyin kiritildi.)

Har bir Flow tugaganda Producer'dan har bir Consumer'gacha bo'lgan
latency o'lchanadi va `GFL-001_FLOW_DEPENDENCY.md` Dependency
Matrix'ining "Latency" ustuniga yoziladi.

Misol:

Provider → Telegram   340 ms
Provider → Web        290 ms
Provider → Android    310 ms

Bu orqali bottleneck qayerdaligi ko'rinadi.

Amaliy eslatma: real (network bilan) Producer→Consumer latency uchun
tirik provider (masalan TwelveData/Bitget) kerak. Agar test muhitida
network mavjud bo'lmasa, in-process latency (tick→cache→render, network
hisobga olinmagan) baseline sifatida yoziladi va shundayligi belgilab
qo'yiladi.

## GFL-003 — Sequential Flow Rule

(Director qarori — GFL-002 tasdig'idan keyin kiritildi.)

Navbatdagi ishlanadigan Flow — **eng kichik raqamli bajarilmagan Flow
ID** hisoblanadi. Bu "tabiiy" yoki ixtiyoriy tanlov emas, balki qoida:

Har bir Flow faqat o'zidan oldingi Flow:

✓ Approved (Director tomonidan)

✓ Completed

✓ CI Passed

bo'lgandan keyingina boshlanishi mumkin.

Ya'ni:

FLOW-001
↓
FLOW-002
↓
FLOW-003
↓
FLOW-004
↓
...

Hech qachon:

FLOW-010
↓
FLOW-005

bo'lmaydi -- ID tartibidan tashqariga chiqib, keyinroq orqaga qaytib
kichikroq ID'li Flow'ni boshlash taqiqlanadi.

Amaliy natija: `GFL-001_FLOW_PROGRESS.md` jadvalida yuqoridan pastga
qarab birinchi 🟦/🟨/🟥 statusli (ya'ni hali 🟩 Completed bo'lmagan) Flow
-- navbatdagi ishlanadigan Flow'dir. Worker bu tartibni o'zi tanlamaydi
-- jadval o'zi ko'rsatadi.

## GFL-004 — Development v1 Lightweight Flow Loop Rule

(Owner Order — FLOW-004 Director Review'idan keyin kiritildi. "Qabul
qilindi" bilan boshlangan, o'zgartirilmaydigan, kengaytirilmaydigan va
qisqartirilmaydigan Owner Order.)

FLOW-001 dan FLOW-025 gacha (GFL-001 Canonical Flow raqamlash) har bir
Flow endi faqat uch qadamli, engil tsiklda ishlanadi:

Qisqa Audit → Kod yozish → Commit

Qat'iy qoidalar (Owner Order matnidan, so'zma-so'z):

- Har bir Flow faqat shu uch qadamda bajariladi -- avvalgi, og'irroq
  jarayon (to'liq Audit Report / Input-Output-Producer-Consumer
  hujjatlashtirish / Reuse Analysis / Production Wiring tekshiruvi /
  Unit+Integration+E2E Test to'plami / WORK_LOG / 13-15 bo'limli
  Director Review) endi HAR BIR Flow uchun majburiy emas -- "Qisqa
  Audit" va "Kod yozish" shu ishning zaruriy qismini o'z ichiga oladi,
  lekin alohida hujjat/hisobot sifatida talab qilinmaydi.
- Keyingi Flow faqat oldingi Flow commit qilingandan keyin boshlanadi
  (GFL-003 Sequential Flow Rule -- eng kichik raqamli bajarilmagan
  Flow ID -- o'zgarishsiz kuchda qoladi).
- Oraliq Director Review o'tkazilmaydi -- har bir Flow'dan keyin
  alohida 13-15 bo'limli hisobot yozilmaydi.
- Umumiy Full Project Audit, Full System Test, Bug Analysis,
  Architecture Review va Final Director Review -- faqat FLOW-025 (End
  User) commit qilingandan KEYIN, bir marta o'tkaziladi.
- Worker ushbu ketma-ketlikni o'zgartirish, qo'shimcha bosqich qo'shish
  yoki bosqichlarni almashtirish huquqiga ega emas.

Bu qoida CLAUDE.md'ning majburiy Commit Protocol'ini (git add -A →
pyflakes → compileall → pytest → main.py smoke → git status clean →
diff review → commit → push → CI SUCCESS tasdiqlash) BEKOR QILMAYDI --
"Verification qilmasdan keyingi bosqichga o'tish" (Forbidden ro'yxati,
yuqorida) hamon taqiqlanadi; Commit Protocol shu verification'ning
o'zi. GFL-004 faqat FLOW'ning ICHKI tarkibini (audit chuqurligi,
hujjatlashtirish hajmi, review chastotasi) yengillashtiradi --
git/CI validatsiya darvozasini emas.

## GoldBot Subsystem Sub-Status Lifecycle

(Director qarori — GFL-002 tasdig'idan keyin kiritildi.)

GoldBot ichidagi parallel subsystem darajasidagi Flow'lar (masalan
Chart Service, Personal AI Core, Backtesting Engine) -- oddiy
5-holatli Flow Status'dan (Blueprint/In Progress/Review/
Completed/Blocked) tashqari, qo'shimcha ichki bosqichlarga ega:

Blueprint
↓
Design
↓
Development
↓
Testing
↓
Stable

Bu subsystemning o'zi hali GFL Flow sifatida to'liq audit
qilinmaganini va shu sabab hech kim uni shoshilib implement
qilmasligini aniq ko'rsatadi. Flow Status (Blueprint/In
Progress/...) subsystem qachon rasmiy Development'ga kirishini
belgilaydi; Sub-Status Lifecycle esa o'sha subsystem ichidagi
progress'ni ko'rsatadi.

Hozirgi holat (`GFL-001_FLOW_CATALOG.md`): FLOW-016 (Chart Service),
FLOW-017 (Personal AI Core), FLOW-018 (Backtesting Engine) --
uchalasi ham Sub-Status: **Blueprint** (Design hali boshlanmagan).

## Forbidden

Quyidagilar taqiqlanadi:

- Input'siz modul yaratish
- Producer'siz Consumer yaratish
- Flow uzilishini yashirish
- Ishlamaydigan output'ni Completed deb belgilash
- Batch coding
- Bir nechta Flow'ni aralashtirish
- Verification qilmasdan keyingi bosqichga o'tish

## Canonical Flow raqamlash

Flow raqamlash uchun yagona canonical manba —
`GFL-001_FLOW_CATALOG.md` va `GFL-001_FLOW_PROGRESS.md`.

**V3 qayta ko'rib chiqish (GFL-002, Director qarori):** canonical
raqamlash endi GoldBot V3 Architecture asosida, 25 ta Flow: FLOW-001
(Foundation Layer, System Bootstrap) ... FLOW-002/003 (Data Layer) ...
FLOW-004..018 (GoldBot: GoldBot Core / Chart Service / Personal AI
Core / Backtesting Engine) ... FLOW-019 (Application Services) ...
FLOW-020..025 (Platform Layer).

Bundan oldingi GFL-001 pilot davridagi 21-Flow raqamlash bekor
qilingan (undan ham oldingi 25-Flow legacy raqamlash allaqachon bekor
qilingan edi). Old -> New mapping GFL-002 Director Review hisobotida
qayd etilgan.

`GFL-001_FLOW_DEPENDENCY.md` shu V3 raqamlashga moslashtirilgan.

## Relationship with other standards

Bu hujjat quyidagi standartlar bilan birga ishlaydi:

- GEL-001 — Canonical Module = Package
- GFL-002 — V3 Architecture Flow Catalog Refactor
- GFL-003 — Sequential Flow Rule (shu hujjat ichida)
- GFL-004 — Development v1 Lightweight Flow Loop Rule (shu hujjat ichida)
- GLS-001 — Docs va reports O'zbek tilida
- Compatibility Exception registry — `docs/ai/COMPATIBILITY_REPORT.md`
  (PHASE-01 Foundation Audit'da to'g'rilandi: bu material DD raqamiga
  ega emas. Director registri (`docs/governance/director/README.md`)
  DD-005..DD-023 raqamlarini ataylab band/ishlatilmagan deb belgilaydi,
  shuning uchun oldingi "DD-005 — Compatibility Exception registry"
  havolasi dangling edi va shu haqiqiy joyga yo'naltirildi.)
- GDS — Development Workflow
- Engineering Standard — repo hujjat tizimi
- Architecture Standard — global arxitektura qoidalari

## Yakuniy prinsip

GoldBot file-by-file emas, Flow-by-Flow ishlab chiqiladi.
Har bir Flow boshidan oxirigacha ishlaydigan holatga kelgandan keyingina keyingi Flow boshlanadi.
