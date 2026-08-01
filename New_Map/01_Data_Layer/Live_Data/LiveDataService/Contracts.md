# LiveDataService Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat LiveDataService modulining rasmiy Architecture Contract hujjati hisoblanadi.

LiveDataService Live Data Layer ichidagi yagona Canonical Orchestrator hisoblanadi.

Live Data Layer'dagi barcha Runtime jarayonlari, modullar va Pipeline boshqaruvi aynan ushbu modul orqali amalga oshiriladi.

Har qanday implementatsiya ushbu Contract talablariga to'liq mos bo'lishi shart.

---

# Module Responsibility

LiveDataService quyidagi vazifalar uchun javobgar.

✓ Live Data Pipeline Management

✓ Runtime Lifecycle Management

✓ Module Coordination

✓ Pipeline Orchestration

✓ Runtime State Management

✓ Recovery Coordination

✓ Health Monitoring Coordination

✓ Pipeline Event Management

✓ Market Memory Update Coordination

LiveDataService quyidagi vazifalarni bajarmaydi.

✗ Live Tick Generation

✗ Provider Connection

✗ Current Price Calculation

✗ Tick Validation

✗ Candle Generation

✗ Market Memory Storage

✗ Historical Data

✗ Context Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal Generation

✗ AI Analysis

---

# Module Boundary

Configuration Layer

↓

LiveDataService

↓

MarketCalendar

↓

PriceStreamService

↓

LiveProviders

↓

CurrentPriceProvider

↓

StreamValidator

↓

CandleBuilder

↓

LiveDataFlow

↓

Market Memory

↓

Boundary End

---

# Input Contract

LiveDataService quyidagilarni qabul qiladi.

• Runtime Requests

• Start Request

• Stop Request

• Restart Request

• Recovery Request

• Market Status

• Provider Events

• Runtime Events

• Configuration

---

# Output Contract

LiveDataService quyidagilarni yaratadi.

• Module Commands

• Pipeline Commands

• Runtime Status

• Health Status

• Recovery Commands

• Pipeline Events

• Lifecycle Events

---

# Read Contract

LiveDataService quyidagilarni o'qishi mumkin.

✓ Configuration Layer

✓ Market Status

✓ Provider Status

✓ Runtime Status

✓ Pipeline Status

✓ Recovery Status

✓ Module Health

---

# Write Contract

LiveDataService quyidagilarga yozishi mumkin.

✓ MarketCalendar

✓ PriceStreamService

✓ LiveProviders

✓ CurrentPriceProvider

✓ StreamValidator

✓ CandleBuilder

✓ LiveDataFlow

✓ Event Bus

Boshqa modullarga yozish taqiqlanadi.

---

# Allowed Dependencies

LiveDataService quyidagilar bilan ishlashi mumkin.

✓ Configuration Layer

✓ MarketCalendar

✓ PriceStreamService

✓ LiveProviders

✓ CurrentPriceProvider

✓ StreamValidator

✓ CandleBuilder

✓ LiveDataFlow

✓ Event Bus

---

# Forbidden Dependencies

LiveDataService quyidagilar bilan ishlashi mumkin emas.

✗ Historical Data

✗ HistoricalDatabase

✗ HistoricalDataService

✗ Context Engine

✗ Analysis Engine

✗ Strategy Engine

✗ Confluence Engine

✗ Decision Engine

✗ Risk Engine

✗ Signal Engine

✗ AI Layer

✗ Platform Layer

✗ User Experience Layer

✗ Business Layer

✗ Learning Layer

✗ Media Layer

✗ Future Expansion Layer

---

# Ownership

LiveDataService egalik qiladi.

✓ Runtime Lifecycle

✓ Pipeline Lifecycle

✓ Module Coordination

✓ Runtime State

✓ Pipeline State

✓ Recovery State

✓ Health Monitoring

✓ Runtime Events

✓ Pipeline Events

LiveDataService egalik qilmaydi.

✗ Live Tick

✗ Current Price

✗ Validation Logic

✗ Candle Logic

✗ Market Memory

✗ Trading Logic

✗ Strategy

✗ Decision

---

# State Contract

LiveDataService quyidagi holatlarda bo'lishi mumkin.

• Idle

• Initializing

• Ready

• Running

• Recovering

• Restarting

• Stopping

• Stopped

• Failed

---

# Error Contract

LiveDataService quyidagi xatolarni qaytarishi mumkin.

• InitializationFailed

• RuntimeFailed

• PipelineFailed

• ModuleFailed

• RecoveryFailed

• InvalidConfiguration

• InvalidPipelineState

• HealthCheckFailed

• RuntimeTimeout

• UnknownRuntimeError

Har qanday xato Event Bus orqali e'lon qilinadi va Runtime Recovery mexanizmi tomonidan boshqariladi.

---

# Runtime Contract

1. LiveDataService Live Data Layer'ning yagona Canonical Orchestrator'i hisoblanadi.

2. Live Data Pipeline faqat LiveDataService tomonidan boshqariladi.

3. Har bir Live Data moduli faqat LiveDataService koordinatsiyasi ostida ishlaydi.

4. Runtime Lifecycle markazlashgan holda boshqariladi.

5. Recovery avtomatik ishga tushirilishi mumkin.

6. Pipeline Health doim monitoring qilinadi.

7. Runtime State izchil saqlanishi shart.

8. GoldBot Core LiveDataService bilan bevosita ishlamaydi.

9. LiveDataService biznes logikasini bajarmaydi.

10. Circular Dependency qat'iyan taqiqlanadi.

---

# Architecture Rules

LiveDataService:

✓ Pipeline'ni boshqaradi.

✓ Modullarni koordinatsiya qiladi.

✓ Runtime Lifecycle'ni boshqaradi.

✓ Recovery jarayonini boshqaradi.

✓ Health Monitoring'ni boshqaradi.

✓ Runtime Event'larini yaratadi.

✓ Pipeline Event'larini yaratadi.

LiveDataService:

✗ Tick yaratmaydi.

✗ Current Price yaratmaydi.

✗ Validation bajarmaydi.

✗ Candle yaratmaydi.

✗ Market Memory'ga yozmaydi.

✗ Trading qilmaydi.

✗ Strategy hisoblamaydi.

✗ Signal yaratmaydi.

✗ Decision chiqarmaydi.

✗ AI ishlatmaydi.

---

# Contract Violations

Quyidagilar Architecture Violation hisoblanadi.

• LiveDataService → Historical Data import

• LiveDataService → Context Engine import

• LiveDataService → Analysis Engine import

• LiveDataService → Strategy Engine import

• LiveDataService → Decision Engine import

• LiveDataService → AI Layer import

• LiveDataService → Business Layer import

• LiveDataService → GoldBot Core import

• Pipeline bosqichlarini chetlab o'tish

• Module'larni LiveDataService'dan tashqaridan boshqarish

• Runtime Lifecycle'ni buzish

• Circular Dependency

---

# Acceptance Criteria

LiveDataService to'g'ri ishlaydi agar:

✓ Live Data Pipeline to'liq boshqarilsa.

✓ Barcha modullar koordinatsiya qilinsa.

✓ Runtime Lifecycle izchil ishlasa.

✓ Recovery muvaffaqiyatli bajarilsa.

✓ Health Monitoring ishlasa.

✓ Runtime State saqlansa.

✓ Pipeline Integrity buzilmasa.

✓ Arxitektura chegaralari buzilmasa.

---

# Summary

LiveDataService Contract Live Data Layer'ning markaziy boshqaruv moduli uchun rasmiy arxitektura shartnomasi hisoblanadi.

LiveDataService Live Data Layer ichidagi barcha Runtime Pipeline, modullar va Lifecycle jarayonlarini boshqaruvchi yagona Canonical Orchestrator hisoblanadi.

Ushbu hujjatda belgilangan Boundary, Dependency, Runtime va Ownership qoidalaridan chetga chiqadigan har qanday implementatsiya **GoldBot Architecture Violation** hisoblanadi.
