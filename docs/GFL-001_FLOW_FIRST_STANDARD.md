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

Misol:

Current Price
→ Provider Factory
→ Data Validation
→ Market Memory (SSOT)
→ Market Engine
→ Core API
→ Application Services
→ Telegram / Mini App / Android / iOS / PC / Web

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

Eslatma (repo hozirgi holati): canonical 21-Flow modelida Telegram
(FLOW-016), Mini App (FLOW-017), Android (FLOW-018), iOS (FLOW-019),
Desktop (FLOW-020), Web (FLOW-021) — bularning barchasi Application
Services (FLOW-015) fan-out nuqtasining Consumer'lari. Shu sabab
Fan-Out Rule eng kuchli aynan FLOW-015 tugaganda qo'llanadi. Hozirda
faqat Telegram real platforma sifatida mavjud; qolgan platformalar
(Mini App/Android/iOS/Desktop/Web) hali kod sifatida mavjud emas —
ular kelajakdagi FLOW-017...021. Har bir platforma paydo bo'lgach,
o'sha Flow uchun Fan-Out Rule majburiy bo'ladi.

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
`GFL-001_FLOW_CATALOG.md` va `GFL-001_FLOW_PROGRESS.md` (21 ta Flow:
FLOW-001 Current Price ... FLOW-021 Web).

`GFL-001_FLOW_DEPENDENCY.md` shu raqamlashga moslashtiriladi. Eski 25
ta Flow raqamlashi bekor qilingan.

## Relationship with other standards

Bu hujjat quyidagi standartlar bilan birga ishlaydi:

- GEL-001 — Canonical Module = Package
- GLS-001 — Docs va reports O'zbek tilida
- DD-005 — Compatibility Exception registry
- GDS — Development Workflow
- Engineering Standard — repo hujjat tizimi
- Architecture Standard — global arxitektura qoidalari

## Yakuniy prinsip

GoldBot file-by-file emas, Flow-by-Flow ishlab chiqiladi.
Har bir Flow boshidan oxirigacha ishlaydigan holatga kelgandan keyingina keyingi Flow boshlanadi.
