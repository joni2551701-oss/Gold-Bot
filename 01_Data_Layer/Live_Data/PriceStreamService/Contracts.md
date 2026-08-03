# PriceStreamService Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat PriceStreamService modulining rasmiy Architecture Contract hujjati hisoblanadi.

PriceStreamService Live Data modulining yagona Orchestrator'i hisoblanadi.

Real vaqt (Live Market) ma'lumotlari bilan bog'liq barcha jarayonlar aynan ushbu modul orqali boshqariladi.

Har qanday implementatsiya ushbu Contract talablariga to'liq mos bo'lishi shart.

---

# Module Responsibility

PriceStreamService quyidagi vazifalar uchun javobgar.

✓ Live Stream Pipeline Management

✓ Live Provider Coordination

✓ Stream Lifecycle Management

✓ Current Price Coordination

✓ Stream Validation Coordination

✓ Candle Builder Coordination

✓ Market Calendar Coordination

✓ Market Memory Coordination

✓ Live Stream State Management

PriceStreamService quyidagi vazifalarni bajarmaydi.

✗ Historical Data

✗ Historical Storage

✗ Data Validation Logic

✗ Candle Calculation

✗ Market Memory Storage

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

PriceStreamService

↓

Market Calendar

↓

Live Providers

↓

CurrentPriceProvider

↓

Stream Validator

↓

Candle Builder

↓

Market Memory

↓

Boundary End

---

# Input Contract

PriceStreamService quyidagilarni qabul qiladi.

• Stream Start Request

• Stream Stop Request

• Live Tick

• Provider Events

• Market Status

• Configuration

• System Events

---

# Output Contract

PriceStreamService quyidagilarni yaratadi.

• Current Price Update

• Stream Validation Request

• Candle Build Request

• Market Memory Update

• Stream Status

• Stream Events

---

# Read Contract

PriceStreamService quyidagilarni o'qishi mumkin.

✓ Configuration

✓ Market Calendar Status

✓ Provider Status

✓ Current Price Status

✓ Stream Status

✓ Market Memory Status

---

# Write Contract

PriceStreamService quyidagilarga yozishi mumkin.

✓ CurrentPriceProvider

✓ Stream Validator

✓ Candle Builder

✓ Market Memory

✓ Event Bus

---

# Allowed Dependencies

PriceStreamService quyidagilar bilan ishlashi mumkin.

✓ Live Providers

✓ CurrentPriceProvider

✓ StreamValidator

✓ CandleBuilder

✓ MarketCalendar

✓ Market Memory

✓ Memory Reader

✓ Event Bus

✓ Configuration Layer

---

# Forbidden Dependencies

PriceStreamService quyidagilar bilan ishlashi mumkin emas.

✗ Historical Data

✗ Historical Database

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

PriceStreamService egalik qiladi.

✓ Live Stream Pipeline

✓ Live Stream Lifecycle

✓ Provider Coordination

✓ Tick Routing

✓ Stream Coordination

✓ Validation Coordination

✓ Candle Coordination

✓ Market Memory Coordination

✓ Stream Health Monitoring

PriceStreamService egalik qilmaydi.

✗ Historical Data

✗ Historical Storage

✗ Validation Logic

✗ Candle Generation Logic

✗ Market Memory Logic

✗ Trading Logic

✗ Business Logic

---

# State Contract

PriceStreamService quyidagi holatlarda bo'lishi mumkin.

• Idle

• Initializing

• Connecting

• Connected

• Streaming

• Validating

• Building Candle

• Updating Memory

• Reconnecting

• Completed

• Failed

---

# Error Contract

PriceStreamService quyidagi xatolarni qaytarishi mumkin.

• ProviderUnavailable

• ProviderDisconnected

• ConnectionTimeout

• AuthenticationFailed

• StreamInterrupted

• InvalidTick

• ValidationFailed

• MemoryUpdateFailed

• MarketClosed

• UnknownStreamError

Har qanday xato Event Bus orqali e'lon qilinadi va Service tomonidan boshqariladi.

---

# Runtime Contract

1. PriceStreamService Live Data modulining yagona Orchestrator'i hisoblanadi.

2. Live Stream faqat Market Calendar ruxsati bilan boshlanadi.

3. Live Provider faqat PriceStreamService orqali boshqariladi.

4. Har bir Tick CurrentPriceProvider orqali qabul qilinadi.

5. Har bir Tick Stream Validator orqali tekshiriladi.

6. Validation'dan o'tgan Tick Candle Builder'ga uzatiladi.

7. Candle Builder tayyorlagan Candle Market Memory'ga yoziladi.

8. GoldBot Core Live Provider bilan bevosita ishlamaydi.

9. PriceStreamService hech qachon Trading Decision chiqarmaydi.

10. Live Stream Pipeline bosqichlarini chetlab o'tish taqiqlanadi.

---

# Architecture Rules

PriceStreamService:

✓ Live Data Pipeline'ni boshqaradi.

✓ Live Provider'larni boshqaradi.

✓ Current Price oqimini boshqaradi.

✓ Validation jarayonini boshqaradi.

✓ Candle Builder ishini koordinatsiya qiladi.

✓ Market Memory yangilanishini boshqaradi.

PriceStreamService:

✗ Tick yaratmaydi.

✗ Candle hisoblamaydi.

✗ Validation bajarmaydi.

✗ Market Memory'da ma'lumot saqlamaydi.

✗ Strategy hisoblamaydi.

✗ Decision chiqarmaydi.

✗ Signal yaratmaydi.

✗ AI ishlatmaydi.

---

# Contract Violations

Quyidagilar Architecture Violation hisoblanadi.

• PriceStreamService → Historical Data import

• PriceStreamService → Context Engine import

• PriceStreamService → Strategy Engine import

• PriceStreamService → Decision Engine import

• PriceStreamService → AI Layer import

• PriceStreamService → Business Layer import

• PriceStreamService → GoldBot Core import

• Stream Validator bosqichini chetlab o'tish

• CurrentPriceProvider'ni chetlab o'tish

• Market Memory'ga Validation'siz yozish

• Live Provider'ni to'g'ridan-to'g'ri chaqirish

• Circular Dependency

---

# Acceptance Criteria

PriceStreamService to'g'ri ishlaydi agar:

✓ Live Stream muvaffaqiyatli ishga tushsa.

✓ Live Provider bilan aloqa barqaror bo'lsa.

✓ Har bir Tick qabul qilinsa.

✓ Validation har doim bajarilsa.

✓ Candle Builder to'g'ri ishlasa.

✓ Market Memory yangilansa.

✓ Stream uzilganda avtomatik Recovery/Reconnect ishlasa.

✓ Live Pipeline bosqichlari buzilmasa.

---

# Summary

PriceStreamService Contract Live Data modulining rasmiy arxitektura shartnomasi hisoblanadi.

PriceStreamService Live Data ichidagi barcha komponentlarni boshqaruvchi yagona Canonical Orchestrator hisoblanadi.

Live Providers, CurrentPriceProvider, StreamValidator, CandleBuilder, MarketCalendar va Market Memory o'rtasidagi barcha jarayonlar faqat PriceStreamService orqali amalga oshiriladi.

Ushbu hujjatda belgilangan Boundary, Dependency, Runtime va Ownership qoidalaridan chetga chiqadigan har qanday implementatsiya **GoldBot Architecture Violation** hisoblanadi.
