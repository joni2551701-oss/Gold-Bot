# Live Data Layer Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat Live Data Layer'ning rasmiy Architecture Contract hujjati hisoblanadi.

Live Data Layer GoldBot ekotizimidagi yagona Canonical Real-Time Market Data Layer hisoblanadi.

Real-Time Market Data qabul qilish, Current Price yaratish, Tick Validation, Candle Generation va Market Memory'ni yangilash ushbu Layer orqali amalga oshiriladi.

Har qanday implementatsiya ushbu Contract talablariga to'liq mos bo'lishi shart.

---

# Layer Responsibility

Live Data Layer quyidagi vazifalar uchun javobgar.

✓ Market Session Management

✓ Live Stream Management

✓ Provider Management

✓ Current Price Management

✓ Tick Validation

✓ Candle Generation

✓ Runtime Pipeline Management

✓ Market Memory Update

✓ Runtime Recovery

✓ Pipeline Health Monitoring

Live Data Layer quyidagi vazifalarni bajarmaydi.

✗ Historical Data Download

✗ Historical Storage

✗ Market Structure Analysis

✗ Context Analysis

✗ Strategy Calculation

✗ Signal Generation

✗ Decision Making

✗ Risk Management

✗ Trade Execution

✗ AI Analysis

---

# Layer Boundary

Configuration Layer

↓

Live Data Layer

↓

Market Memory

↓

Boundary End

---

# Input Contract

Live Data Layer quyidagilarni qabul qiladi.

• Market Status

• Provider Configuration

• Live Tick

• Quote

• Bid

• Ask

• Runtime Events

• Recovery Events

---

# Output Contract

Live Data Layer quyidagilarni yaratadi.

• Current Price

• Validated Tick

• OHLC Candle

• Market Memory Update

• Runtime Events

• Health Status

• Pipeline Status

---

# Read Contract

Live Data Layer quyidagilarni o'qishi mumkin.

✓ Configuration Layer

✓ Provider Configuration

✓ Trading Sessions

✓ Market Calendar

✓ Runtime Configuration

---

# Write Contract

Live Data Layer quyidagilarga yozishi mumkin.

✓ Market Memory

✓ Event Bus

Boshqa Layer'larga yozish taqiqlanadi.

---

# Allowed Dependencies

Live Data Layer quyidagilar bilan ishlashi mumkin.

✓ Configuration Layer

✓ Market Memory

✓ Event Bus

✓ Time Service

✓ External Market Providers

---

# Forbidden Dependencies

Live Data Layer quyidagilar bilan ishlashi mumkin emas.

✗ Historical Data Layer

✗ Context Layer

✗ Analysis Layer

✗ Strategy Layer

✗ Confluence Layer

✗ Decision Layer

✗ Risk Layer

✗ Signal Layer

✗ AI Layer

✗ Platform Layer

✗ User Experience Layer

✗ Business Layer

✗ Learning Layer

✗ Media Layer

✗ Future Expansion Layer

---

# Layer Ownership

Live Data Layer egalik qiladi.

✓ Market Sessions

✓ Live Stream

✓ Provider Connections

✓ Current Price

✓ Tick Validation

✓ OHLC Candles

✓ Runtime Pipeline

✓ Runtime State

✓ Recovery State

✓ Pipeline Events

Live Data Layer egalik qilmaydi.

✗ Historical Candles

✗ Market Structure

✗ Trading Signals

✗ Trading Decisions

✗ Risk

✗ Orders

✗ Positions

✗ AI Results

---

# Layer State Contract

Live Data Layer quyidagi holatlarda bo'lishi mumkin.

• Initializing

• Waiting Market Open

• Connecting

• Streaming

• Processing

• Updating Memory

• Recovering

• Stopping

• Idle

• Failed

---

# Error Contract

Live Data Layer quyidagi xatolarni qaytarishi mumkin.

• ProviderConnectionFailed

• AuthenticationFailed

• SubscriptionFailed

• InvalidTick

• InvalidPrice

• InvalidTimestamp

• ValidationFailed

• CandleBuildFailed

• PipelineFailed

• RecoveryFailed

• RuntimeTimeout

• UnknownRuntimeError

Har qanday xato Event Bus orqali e'lon qilinadi va Runtime Recovery mexanizmi tomonidan boshqariladi.

---

# Runtime Contract

1. Live Data Layer yagona Canonical Real-Time Data Pipeline hisoblanadi.

2. Pipeline har doim MarketCalendar orqali boshlanadi.

3. Live Stream faqat Market Open holatida ishlaydi.

4. Har bir Tick CurrentPriceProvider orqali o'tishi shart.

5. Har bir Tick StreamValidator tomonidan tekshirilishi shart.

6. CandleBuilder faqat Validated Tick bilan ishlaydi.

7. Market Memory faqat yakuniy Candle qabul qiladi.

8. GoldBot Core Live Data Layer bilan bevosita ishlamaydi.

9. Runtime Recovery avtomatik ishga tushirilishi mumkin.

10. Circular Dependency qat'iyan taqiqlanadi.

---

# Architecture Rules

Live Data Layer:

✓ Live Stream boshqaradi.

✓ Provider'larni boshqaradi.

✓ Current Price yaratadi.

✓ Tick Validation bajaradi.

✓ OHLC Candle yaratadi.

✓ Runtime Pipeline boshqaradi.

✓ Market Memory'ni yangilaydi.

✓ Runtime Recovery bajaradi.

Live Data Layer:

✗ Historical Data yuklamaydi.

✗ Market Structure hisoblamaydi.

✗ Context yaratmaydi.

✗ Strategy hisoblamaydi.

✗ Signal yaratmaydi.

✗ Decision chiqarmaydi.

✗ Risk hisoblamaydi.

✗ Trade ochmaydi.

✗ AI ishlatmaydi.

---

# Contract Violations

Quyidagilar Architecture Violation hisoblanadi.

• Live Data Layer → Context Layer import

• Live Data Layer → Strategy Layer import

• Live Data Layer → Decision Layer import

• Live Data Layer → AI Layer import

• Live Data Layer → Business Layer import

• Live Data Layer → Trade Execution

• Validation bosqichini chetlab o'tish

• Current Price'ni Provider'dan tashqarida yaratish

• CandleBuilder'dan tashqarida Candle yaratish

• Market Memory'dan tashqariga yozish

• Circular Dependency

---

# Acceptance Criteria

Live Data Layer to'g'ri ishlaydi agar:

✓ Market Session to'g'ri boshqarilsa.

✓ Provider ulanishi barqaror ishlasa.

✓ Live Tick uzluksiz qabul qilinsa.

✓ Current Price doim yangilanib tursa.

✓ Tick Validation ishlasa.

✓ OHLC Candle to'g'ri yaratilsa.

✓ Market Memory yangilanib tursa.

✓ Runtime Recovery ishlasa.

✓ Pipeline Integrity saqlansa.

✓ Arxitektura chegaralari buzilmasa.

---

# Summary

Live Data Layer Contract GoldBot'ning Real-Time Market Data qatlami uchun rasmiy arxitektura shartnomasi hisoblanadi.

Live Data Layer tashqi Provider'lardan kelgan Real-Time Market Data'ni qabul qilish, Current Price yaratish, Tick Validation, OHLC Candle Generation va Market Memory yangilanishi uchun yagona Canonical Layer hisoblanadi.

Ushbu hujjatda belgilangan Boundary, Dependency, Runtime va Ownership qoidalaridan chetga chiqadigan har qanday implementatsiya **GoldBot Architecture Violation** hisoblanadi.
