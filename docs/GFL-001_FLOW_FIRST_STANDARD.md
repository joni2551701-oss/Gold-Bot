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
- GLS-001 — Docs va reports O'zbek tilida
- DD-005 — Compatibility Exception registry
- GDS — Development Workflow
- Engineering Standard — repo hujjat tizimi
- Architecture Standard — global arxitektura qoidalari

## Yakuniy prinsip

GoldBot file-by-file emas, Flow-by-Flow ishlab chiqiladi.
Har bir Flow boshidan oxirigacha ishlaydigan holatga kelgandan keyingina keyingi Flow boshlanadi.
