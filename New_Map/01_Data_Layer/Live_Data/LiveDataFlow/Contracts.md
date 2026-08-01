# LiveDataFlow Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat LiveDataFlow modulining rasmiy Architecture Contract hujjati hisoblanadi.

LiveDataFlow Live Data Layer ichidagi yagona Canonical Runtime Pipeline hisoblanadi.

Live Market Data oqimining barcha bosqichlari aynan ushbu Pipeline orqali amalga oshiriladi.

Har qanday implementatsiya ushbu Contract talablariga to'liq mos bo'lishi shart.

---

# Module Responsibility

LiveDataFlow quyidagi vazifalar uchun javobgar.

✓ Runtime Pipeline Management

✓ Stage Coordination

✓ Module Routing

✓ Pipeline Integrity

✓ Runtime Flow Management

✓ Pipeline Event Management

✓ Flow Monitoring

✓ Recovery Coordination

LiveDataFlow quyidagi vazifalarni bajarmaydi.

✗ Live Tick Generation

✗ Current Price Generation

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

Market Memory

↓

Memory Reader

↓

GoldBot Core

↓

Boundary End

---

# Input Contract

LiveDataFlow quyidagilarni qabul qiladi.

• Market Status

• Live Tick

• Current Price

• Validated Tick

• Candle

• Pipeline Events

• Recovery Events

---

# Output Contract

LiveDataFlow quyidagilarni yaratadi.

• Runtime Flow

• Pipeline Status

• Flow Events

• Stage Events

• Recovery Events

• Pipeline State

---

# Read Contract

LiveDataFlow quyidagilarni o'qishi mumkin.

✓ Market Status

✓ Live Tick

✓ Current Price

✓ Validation Status

✓ Candle Status

✓ Market Memory Status

✓ Configuration Layer

---

# Write Contract

LiveDataFlow quyidagilarga yozishi mumkin.

✓ Event Bus

✓ Pipeline State

Boshqa modullarga yozish taqiqlanadi.

---

# Allowed Dependencies

LiveDataFlow quyidagilar bilan ishlashi mumkin.

✓ MarketCalendar

✓ PriceStreamService

✓ LiveProviders

✓ CurrentPriceProvider

✓ StreamValidator

✓ CandleBuilder

✓ Market Memory

✓ Memory Reader

✓ Event Bus

✓ Configuration Layer

---

# Forbidden Dependencies

LiveDataFlow quyidagilar bilan ishlashi mumkin emas.

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

LiveDataFlow egalik qiladi.

✓ Runtime Pipeline

✓ Stage Order

✓ Flow Rules

✓ Routing Rules

✓ Pipeline State

✓ Flow Integrity

✓ Pipeline Events

✓ Recovery State

LiveDataFlow egalik qilmaydi.

✗ Live Tick

✗ Current Price

✗ Validation Logic

✗ Candle

✗ Market Memory

✗ Trading Logic

✗ Strategy

✗ Decision

---

# State Contract

LiveDataFlow quyidagi holatlarda bo'lishi mumkin.

• Idle

• Starting

• Running

• Waiting

• Recovering

• Stopping

• Stopped

• Failed

---

# Error Contract

LiveDataFlow quyidagi xatolarni qaytarishi mumkin.

• PipelineInitializationFailed

• InvalidPipelineOrder

• InvalidRouting

• MissingPipelineStage

• BrokenPipeline

• CircularFlowDetected

• PipelineRecoveryFailed

• StageExecutionFailed

• RuntimePipelineError

• UnknownPipelineError

Har qanday xato Event Bus orqali e'lon qilinadi va PriceStreamService tomonidan boshqariladi.

---

# Runtime Contract

1. LiveDataFlow Live Data Layer uchun yagona Canonical Runtime Pipeline hisoblanadi.

2. Pipeline har doim MarketCalendar bosqichidan boshlanadi.

3. Har bir Tick barcha Pipeline bosqichlaridan o'tishi shart.

4. Validation bosqichi hech qachon chetlab o'tilmaydi.

5. CandleBuilder faqat Validated Tick bilan ishlaydi.

6. Market Memory faqat tayyor Candle qabul qiladi.

7. GoldBot Core faqat Memory Reader orqali ma'lumot oladi.

8. Pipeline bosqichlari Runtime vaqtida o'zgartirilmaydi.

9. Pipeline uzilganda Recovery ishga tushishi mumkin.

10. Circular Data Flow qat'iyan taqiqlanadi.

---

# Architecture Rules

LiveDataFlow:

✓ Pipeline tartibini boshqaradi.

✓ Modul Routing'ni boshqaradi.

✓ Runtime Flow'ni nazorat qiladi.

✓ Pipeline Integrity'ni tekshiradi.

✓ Recovery Flow'ni boshqaradi.

✓ Pipeline Event'larini yaratadi.

LiveDataFlow:

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

• LiveDataFlow → Historical Data import

• LiveDataFlow → Context Engine import

• LiveDataFlow → Analysis Engine import

• LiveDataFlow → Strategy Engine import

• LiveDataFlow → Decision Engine import

• LiveDataFlow → AI Layer import

• LiveDataFlow → Business Layer import

• Pipeline bosqichini chetlab o'tish

• Validation bosqichini o'tkazib yuborish

• CandleBuilder'dan oldin Market Memory'ga yozish

• GoldBot Core'ning Pipeline'ni chetlab o'tishi

• Circular Dependency

---

# Acceptance Criteria

LiveDataFlow to'g'ri ishlaydi agar:

✓ Pipeline har doim bir xil ketma-ketlikda ishlasa.

✓ Har bir Tick barcha bosqichlardan o'tsa.

✓ Validation bosqichi bajarilsa.

✓ Candle to'g'ri yaratilsa.

✓ Market Memory yangilansa.

✓ GoldBot Core faqat Memory Reader orqali ma'lumot olsa.

✓ Recovery mexanizmi ishlasa.

✓ Pipeline Integrity buzilmasa.

---

# Summary

LiveDataFlow Contract Live Data Layer ichidagi Canonical Runtime Pipeline uchun rasmiy arxitektura shartnomasi hisoblanadi.

LiveDataFlow Live Market Data oqimining yagona standart marshrutini belgilaydi va barcha modullar o'rtasidagi Runtime ketma-ketlikni boshqaradi.

Ushbu hujjatda belgilangan Boundary, Dependency, Runtime va Ownership qoidalaridan chetga chiqadigan har qanday implementatsiya **GoldBot Architecture Violation** hisoblanadi.
