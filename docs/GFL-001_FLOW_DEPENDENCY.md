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

# Canonical raqamlash (Director qarori, GFL-002)

`GFL-001_FLOW_CATALOG.md` va `GFL-001_FLOW_PROGRESS.md` -- Flow
raqamlash uchun yagona canonical manba hisoblanadi, endi GoldBot V3
Architecture asosida:

Foundation Layer (FLOW-001) -> Data Layer (FLOW-002..003) -> GoldBot
[GoldBot Core (FLOW-004..015), Chart Service (FLOW-016), Personal AI
Core (FLOW-017), Backtesting Engine (FLOW-018)] -> Application
Services (FLOW-019) -> Platform Layer (FLOW-020..025) -> End User.

Bundan oldingi (GFL-001 pilot davridagi) 21-Flow raqamlash **bekor
qilindi**. Old -> New mapping jadvali shu refactor'ga javoban yozilgan
Director Review chat xabarida keltirilgan.

---

# Dependency Chain

FLOW-001
System Bootstrap / Configuration (Foundation Layer)
↓
FLOW-002

FLOW-002
Current Price (Data Layer)
↓
FLOW-003

FLOW-003
Market Memory / SSOT (Data Layer)
↓
FLOW-004
FLOW-016
FLOW-017
FLOW-018

FLOW-004
Market Engine (GoldBot > GoldBot Core)
↓
FLOW-005

FLOW-005
Context Engine (GoldBot > GoldBot Core)
↓
FLOW-006

FLOW-006
Analysis Engine (GoldBot > GoldBot Core)
↓
FLOW-007

FLOW-007
Indicator Engine (GoldBot > GoldBot Core)
↓
FLOW-008

FLOW-008
Strategy Engine (GoldBot > GoldBot Core)
↓
FLOW-009

FLOW-009
Confluence Engine (GoldBot > GoldBot Core)
↓
FLOW-010

FLOW-010
Decision Engine (GoldBot > GoldBot Core)
↓
FLOW-011

FLOW-011
Risk Engine (GoldBot > GoldBot Core)
↓
FLOW-012

FLOW-012
Signal Engine (GoldBot > GoldBot Core)
↓
FLOW-013

FLOW-013
Execution Engine (GoldBot > GoldBot Core)
↓
FLOW-014

FLOW-014
Trade Monitoring (GoldBot > GoldBot Core)
↓
FLOW-015

FLOW-015
GoldBot Core API (GoldBot > GoldBot Core)
↓
FLOW-019

FLOW-016
Chart Service (GoldBot > Chart Service)
↓
FLOW-019

FLOW-017
Personal AI Core (GoldBot > Personal AI Core)
↓
FLOW-019

FLOW-018
Backtesting Engine (GoldBot > Backtesting Engine)
↓
FLOW-019

FLOW-019
Application Services
↓
FLOW-020
FLOW-021
FLOW-022
FLOW-023
FLOW-024
FLOW-025

FLOW-020
Telegram (Platform Layer)

FLOW-021
Mini App (Platform Layer)

FLOW-022
Android (Platform Layer)

FLOW-023
iOS (Platform Layer)

FLOW-024
Desktop (Platform Layer)

FLOW-025
Web (Platform Layer)

---

# Dependency Matrix

Latency ustuni GFL-001 Latency Rule bo'yicha to'ldiriladi (pastdagi
"Latency Rule" bo'limiga qarang).

| Flow | Producer | Input | Output | Consumer | Depends On | Blocks | Latency |
|------|----------|-------|--------|----------|------------|--------|---------|
| FLOW-001 | System Start | Env/Secrets | Runtime Config | Data Layer | - | FLOW-002 | - |
| FLOW-002 | Provider Factory | Price Stream | Validated Current Price | Market Memory | FLOW-001 | FLOW-003 | - (¹) |
| FLOW-003 | FLOW-002 | Validated Current Price | Market State | GoldBot Core / Chart Service / Personal AI Core / Backtesting Engine | FLOW-002 | FLOW-004, FLOW-016, FLOW-017, FLOW-018 | - |
| FLOW-004 | Market Memory | Market State | Market Context | Context Engine | FLOW-003 | FLOW-005 | - |
| FLOW-005 | Market Engine | Market Context | Market Context Result | Analysis Engine | FLOW-004 | FLOW-006 | - |
| FLOW-006 | Context Engine | Market Context Result | Analysis Result | Indicator Engine | FLOW-005 | FLOW-007 | - |
| FLOW-007 | Analysis Engine | Analysis Result | Indicators | Strategy Engine | FLOW-006 | FLOW-008 | - |
| FLOW-008 | Indicator Engine | Indicators | Strategy Result | Confluence Engine | FLOW-007 | FLOW-009 | - |
| FLOW-009 | Strategy Engine | Strategy Result | Confluence | Decision Engine | FLOW-008 | FLOW-010 | - |
| FLOW-010 | Confluence Engine | Confluence | Decision | Risk Engine | FLOW-009 | FLOW-011 | - |
| FLOW-011 | Decision Engine | Decision | Safe Decision | Signal Engine | FLOW-010 | FLOW-012 | - |
| FLOW-012 | Risk Engine | Safe Decision | Signal | Execution Engine | FLOW-011 | FLOW-013 | - |
| FLOW-013 | Signal Engine | Signal | Execution Result | Trade Monitoring | FLOW-012 | FLOW-014 | - |
| FLOW-014 | Execution Engine | Execution Result | Trade State | GoldBot Core API | FLOW-013 | FLOW-015 | - |
| FLOW-015 | Trade Monitoring | Trade State | API Response | Application Services | FLOW-014 | FLOW-019 | - |
| FLOW-016 | Market Memory | Market State (²) | Aniqlanmagan | Application Services | FLOW-003 | FLOW-019 | - |
| FLOW-017 | Market Memory / GoldBot Core (²) | Aniqlanmagan | Aniqlanmagan | Application Services | FLOW-003 | FLOW-019 | - |
| FLOW-018 | Data Layer / GoldBot Core (²) | Aniqlanmagan | Aniqlanmagan | Application Services | FLOW-003 | FLOW-019 | - |
| FLOW-019 | GoldBot Core API / Chart Service / Personal AI Core / Backtesting Engine | API Response (va boshqalar) | Service Data | Telegram / Mini App / Android / iOS / Desktop / Web | FLOW-015, FLOW-016, FLOW-017, FLOW-018 | FLOW-020...025 | - |
| FLOW-020 | Application Services | Service Data | User Message | End User | FLOW-019 | - | - |
| FLOW-021 | Application Services | Service Data | UI View | End User | FLOW-019 | - | - |
| FLOW-022 | Application Services | Service Data | UI View | End User | FLOW-019 | - | - |
| FLOW-023 | Application Services | Service Data | UI View | End User | FLOW-019 | - | - |
| FLOW-024 | Application Services | Service Data | UI View | End User | FLOW-019 | - | - |
| FLOW-025 | Application Services | Service Data | UI View | End User | FLOW-019 | - | - |

(¹) FLOW-002 (Current Price) Director tomonidan Latency Rule
kiritilishidan oldin APPROVED bo'lgan. Uning Producer→Consumer latency
o'lchovi keyinchalik (agar Director talab qilsa) qo'shiladi.

(²) FLOW-016/017/018 (Chart Service / Personal AI Core / Backtesting
Engine) hali Blueprint -- aniq Input/Output kontraktlari Director
tomonidan tasdiqlanmagan. Bu ustunlar shu Flow'lar audit qilinganda
to'ldiriladi.

Izoh (FLOW-002): canonical Consumer -- Market Memory (validated
current price CandleBuilder single-writer orqali MarketMemory'ga
folded). Bundan tashqari, xuddi shu "Validated Current Price"
output'ini Telegram `/price` surface `PriceCache` orqali
to'g'ridan-to'g'ri o'qiydi (ikkinchi Consumer). Bu
`GFL-001_FLOW_FIRST_DIAGRAM.md`'dagi Data Layer tavsifiga mos keladi.

---

# Dependency Rules

Har bir Flow:

- faqat bitta asosiy Producer'ga ega bo'lishi kerak (FLOW-019 va
  FLOW-003 kabi ko'p-Producer holatlar Fan-Out Rule doirasida
  hujjatlashtiriladi).
- kamida bitta Consumer'ga ega bo'lishi kerak.
- Input va Output aniq hujjatlashtirilgan bo'lishi kerak.

---

# Fan-Out Rule (Director qarori)

Agar bitta Producer bir nechta Consumer'ga ma'lumot tarqatsa
(fan-out), Flow faqat **barcha** Consumer'lar PASS bo'lgandagina
Completed hisoblanadi.

Ikkita fan-out nuqtasi mavjud:

## 1. FLOW-003 (Market Memory) -> GoldBot ichidagi 4 subsystem

Market Memory
↓
GoldBot Core (FLOW-004)      PASS
Chart Service (FLOW-016)     PASS
Personal AI Core (FLOW-017)  PASS
Backtesting Engine (FLOW-018) PASS

## 2. FLOW-019 (Application Services) -> Platform Layer

Application Services
↓
Telegram      PASS
Mini App      PASS
Android       PASS
iOS           PASS
Desktop       PASS
Web           PASS

Agar bitta Consumer ishlamasa:

Flow Completed EMAS.

Eslatma (repo hozirgi holati): hozirda faqat **Telegram** real
platforma sifatida mavjud (FLOW-020); Mini App/Android/iOS/Desktop/Web
hali kod sifatida mavjud emas. GoldBot ichida esa faqat **GoldBot
Core** zanjiri (FLOW-004..015) haqiqiy Flow sifatida rasmiylashtirilgan
-- Chart Service/Personal AI Core/Backtesting Engine hali Blueprint.
Har bir yangi platforma/subsystem paydo bo'lgach, tegishli Flow uchun
Fan-Out Rule majburiy bo'ladi.

To'liq ta'rif `GFL-001_FLOW_FIRST_STANDARD.md`'dagi "Fan-Out Rule"
bo'limida.

---

# Latency Rule (Director qarori)

Har bir Flow tugaganda Producer'dan har bir Consumer'gacha bo'lgan
latency o'lchanadi va Dependency Matrix'ning "Latency" ustuniga
yoziladi.

Misol:

Provider → Telegram   340 ms
Provider → Web        290 ms
Provider → Android    310 ms

Bu orqali bottleneck qayerdaligi ko'rinadi.

To'liq ta'rif `GFL-001_FLOW_FIRST_STANDARD.md`'dagi "Latency Rule"
bo'limida.

---

# Blocking Rules

Agar Producer ishlamasa:

↓

barcha Consumer Blocked bo'ladi.

Misol:

FLOW-002 Current Price

↓

FLOW-003 Market Memory

↓

FLOW-004...015 GoldBot Core / FLOW-016...018 (Chart/AI/Backtesting)

↓

FLOW-019 Application Services

↓

FLOW-020 Telegram

FLOW-002 (Current Price) ishlamasa,

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
- GoldBot Core API'ni chetlab o'tish.
- Dependency hujjatini yangilamasdan yangi Flow qo'shish.
- Documentation'siz Dependency yaratish.
- CATALOG/PROGRESS canonical raqamlashidan chetga chiqadigan raqamlash ishlatish.
- V3 Architecture'dan tashqari yangi Layer/Subsystem qo'shish (Director tasdig'isiz).

---

# Final Principle

Har bir Flow boshqa Flow bilan bog'langan.

Har bir Dependency hujjatlashtirilgan bo'lishi shart.

GoldBot'da hujjatlashtirilmagan Dependency mavjud bo'lishi mumkin emas.
