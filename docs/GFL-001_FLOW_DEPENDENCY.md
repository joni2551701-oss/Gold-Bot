# GFL-001 — Flow Dependency

## Maqsad

Ushbu hujjat GoldBot Data Flow o'rtasidagi bog'liqliklarni (Dependency) boshqaradi.

Har bir Flow:

- qayerdan ma'lumot oladi;
- nimani qayta ishlaydi;
- qayerga uzatadi;
- qaysi Flow'ga bog'liq;
- qaysi Flow'ni bloklaydi;

aniq ko'rsatiladi.

---

# Canonical raqamlash (Director qarori)

`GFL-001_FLOW_CATALOG.md` va `GFL-001_FLOW_PROGRESS.md` — Flow
raqamlash uchun yagona canonical manba hisoblanadi.

Ushbu hujjat (`GFL-001_FLOW_DEPENDENCY.md`) o'sha canonical raqamlashga
moslashtiriladi.

Eski 25 ta Flow raqamlashi (FLOW-001 = Configuration ... FLOW-020 =
Telegram ... FLOW-025 = Web) **bekor qilindi**. Amaldagi yagona
raqamlash — 21 ta Flow:

FLOW-001 Current Price ... FLOW-016 Telegram ... FLOW-021 Web.

---

# Dependency Chain

FLOW-001
Current Price
↓
FLOW-002

FLOW-002
Market Memory
↓
FLOW-003

FLOW-003
Market Engine
↓
FLOW-004

FLOW-004
Context Engine
↓
FLOW-005

FLOW-005
Analysis Engine
↓
FLOW-006

FLOW-006
Indicator Engine
↓
FLOW-007

FLOW-007
Strategy Engine
↓
FLOW-008

FLOW-008
Confluence Engine
↓
FLOW-009

FLOW-009
Decision Engine
↓
FLOW-010

FLOW-010
Risk Engine
↓
FLOW-011

FLOW-011
Signal Engine
↓
FLOW-012

FLOW-012
Execution Engine
↓
FLOW-013

FLOW-013
Trade Monitoring
↓
FLOW-014

FLOW-014
GoldBot Core API
↓
FLOW-015

FLOW-015
Application Services
↓
FLOW-016
FLOW-017
FLOW-018
FLOW-019
FLOW-020
FLOW-021

FLOW-016
Telegram

FLOW-017
Mini App

FLOW-018
Android

FLOW-019
iOS

FLOW-020
Desktop

FLOW-021
Web

---

# Dependency Matrix

Latency ustuni GFL-001 Latency Rule bo'yicha to'ldiriladi (pastdagi
"Latency Rule" bo'limiga qarang).

| Flow | Producer | Input | Output | Consumer | Depends On | Blocks | Latency |
|------|----------|-------|--------|----------|------------|--------|---------|
| FLOW-001 | Provider Factory | Price Stream | Validated Current Price | Market Memory | - | FLOW-002 | - (¹) |
| FLOW-002 | Market Memory | Validated Current Price | Market State | Market Engine | FLOW-001 | FLOW-003 | - |
| FLOW-003 | Market Engine | Market State | Market Context | Context Engine | FLOW-002 | FLOW-004 | - |
| FLOW-004 | Context Engine | Market Context | Market Context Result | Analysis Engine | FLOW-003 | FLOW-005 | - |
| FLOW-005 | Analysis Engine | Market Context Result | Analysis Result | Indicator Engine | FLOW-004 | FLOW-006 | - |
| FLOW-006 | Indicator Engine | Analysis Result | Indicators | Strategy Engine | FLOW-005 | FLOW-007 | - |
| FLOW-007 | Strategy Engine | Indicators | Strategy Result | Confluence Engine | FLOW-006 | FLOW-008 | - |
| FLOW-008 | Confluence Engine | Strategy Result | Confluence | Decision Engine | FLOW-007 | FLOW-009 | - |
| FLOW-009 | Decision Engine | Confluence | Decision | Risk Engine | FLOW-008 | FLOW-010 | - |
| FLOW-010 | Risk Engine | Decision | Safe Decision | Signal Engine | FLOW-009 | FLOW-011 | - |
| FLOW-011 | Signal Engine | Safe Decision | Signal | Execution Engine | FLOW-010 | FLOW-012 | - |
| FLOW-012 | Execution Engine | Signal | Execution Result | Trade Monitoring | FLOW-011 | FLOW-013 | - |
| FLOW-013 | Trade Monitoring | Execution Result | Trade State | GoldBot Core API | FLOW-012 | FLOW-014 | - |
| FLOW-014 | GoldBot Core API | Trade State | API Response | Application Services | FLOW-013 | FLOW-015 | - |
| FLOW-015 | Application Services | API Response | Service Data | Telegram / Mini App / Android / iOS / Desktop / Web | FLOW-014 | FLOW-016...021 | - |
| FLOW-016 | Telegram | Service Data | User Message | User | FLOW-015 | - | - |
| FLOW-017 | Mini App | Service Data | UI View | User | FLOW-015 | - | - |
| FLOW-018 | Android | Service Data | UI View | User | FLOW-015 | - | - |
| FLOW-019 | iOS | Service Data | UI View | User | FLOW-015 | - | - |
| FLOW-020 | Desktop | Service Data | UI View | User | FLOW-015 | - | - |
| FLOW-021 | Web | Service Data | UI View | User | FLOW-015 | - | - |

(¹) FLOW-001 Director tomonidan Latency Rule kiritilishidan oldin
APPROVED bo'lgan. Uning Producer→Consumer latency o'lchovi keyinchalik
(agar Director talab qilsa) qo'shiladi. FLOW-002'dan boshlab har bir
Flow tugaganda latency o'lchanadi va shu ustunga yoziladi.

Izoh (FLOW-001): canonical Consumer — Market Memory (validated current
price CandleBuilder single-writer orqali MarketMemory'ga folded).
Bundan tashqari, xuddi shu "Validated Current Price" output'ini
Telegram `/price` surface `PriceCache` orqali to'g'ridan-to'g'ri
o'qiydi (ikkinchi Consumer). Bu `GFL-001_FLOW_FIRST_DIAGRAM.md`'dagi
"Current Price — Market Memory SSOT'dan fork" ko'rinishiga mos keladi.

---

# Dependency Rules

Har bir Flow:

- faqat bitta asosiy Producer'ga ega bo'lishi kerak.
- kamida bitta Consumer'ga ega bo'lishi kerak.
- Input va Output aniq hujjatlashtirilgan bo'lishi kerak.

---

# Fan-Out Rule (Director qarori)

Agar bitta Producer bir nechta Consumer'ga ma'lumot tarqatsa
(fan-out), Flow faqat **barcha** Consumer'lar PASS bo'lgandagina
Completed hisoblanadi.

Asosiy fan-out nuqtasi — FLOW-015 (Application Services):

Application Services
↓
Telegram      PASS
Mini App      PASS
Android       PASS
iOS           PASS
Desktop       PASS
Web           PASS

Agar bitta Consumer (masalan Web) ishlamasa:

Flow Completed EMAS.

To'liq ta'rif `GFL-001_FLOW_FIRST_STANDARD.md`'dagi "Fan-Out Rule"
bo'limida.

---

# Latency Rule (Director qarori)

Har bir Flow tugaganda Producer'dan har bir Consumer'gacha bo'lgan
latency o'lchanadi va Dependency Matrix'ning "Latency" ustuniga
yoziladi.

Misol:

Provider
↓
Telegram   340 ms

Provider
↓
Web        290 ms

Provider
↓
Android    310 ms

Shu orqali bottleneck qayerdaligi ko'rinadi. To'liq ta'rif
`GFL-001_FLOW_FIRST_STANDARD.md`'dagi "Latency Rule" bo'limida.

---

# Blocking Rules

Agar Producer ishlamasa:

↓

barcha Consumer Blocked bo'ladi.

Misol:

FLOW-001 Current Price

↓

FLOW-002 Market Memory

↓

FLOW-003 Market Engine

↓

... (FLOW-004 ... FLOW-015)

↓

FLOW-016 Telegram

FLOW-001 (Current Price) ishlamasa,

ushbu zanjirning barchasi Blocked hisoblanadi.

---

# End-to-End Rule

Har bir yangi Flow quyidagicha tekshiriladi:

Producer

↓

Input

↓

Processing

↓

Output

↓

Consumer

↓

Platform

↓

User

Har bir bosqich PASS bo'lishi kerak.

Fan-Out Rule bo'yicha barcha Consumer'lar, Latency Rule bo'yicha har
bir Producer→Consumer latency ham shu tekshiruvga kiradi.

---

# Forbidden

Taqiqlanadi:

- Producer'ni chetlab o'tish.
- Market Memory'ni chetlab o'tish.
- Core API'ni chetlab o'tish.
- Dependency hujjatini yangilamasdan yangi Flow qo'shish.
- Documentation'siz Dependency yaratish.
- CATALOG/PROGRESS canonical raqamlashidan chetga chiqadigan raqamlash ishlatish.

---

# Final Principle

Har bir Flow boshqa Flow bilan bog'langan.

Har bir Dependency hujjatlashtirilgan bo'lishi shart.

GoldBot'da hujjatlashtirilmagan Dependency mavjud bo'lishi mumkin emas.
