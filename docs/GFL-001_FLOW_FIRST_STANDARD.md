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
- End-to-end test o'tadi
- Documentation yangilanadi
- WORK_LOG yoziladi

## Forbidden

Quyidagilar taqiqlanadi:

- Input'siz modul yaratish
- Producer'siz Consumer yaratish
- Flow uzilishini yashirish
- Ishlamaydigan output'ni Completed deb belgilash
- Batch coding
- Bir nechta Flow'ni aralashtirish
- Verification qilmasdan keyingi bosqichga o'tish

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
