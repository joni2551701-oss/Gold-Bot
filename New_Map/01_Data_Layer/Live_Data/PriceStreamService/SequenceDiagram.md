# PriceStreamService Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat PriceStreamService modulining Runtime Sequence (ishlash ketma-ketligi) ni tavsiflaydi.

PriceStreamService Live Data modulining markaziy Orchestrator'i bo'lib, Live Providers, CurrentPriceProvider, CandleBuilder, StreamValidator, MarketCalendar va Market Memory o'rtasidagi barcha jarayonlarni boshqaradi.

Bu implementatsiya emas.

Bu PriceStreamService modulining Canonical Runtime Blueprint hisoblanadi.

---

# Complete Runtime Sequence

```text
Market Open

        │
        ▼
Market Calendar

        │
        ▼
PriceStreamService

        │
        ▼
Live Providers

        │
        ▼
CurrentPriceProvider

        │
        ▼
Stream Validator

        │
        ▼
Candle Builder

        │
        ▼
Market Memory

        │
        ▼
GoldBot Core
```

---

# Stream Startup Sequence

```text
GoldBot Start

↓

Configuration Loaded

↓

PriceStreamService

↓

Market Calendar

↓

Open Live Stream

↓

Live Providers Connected

↓

Streaming Started
```

---

# Live Price Update Sequence

```text
Live Provider

↓

PriceStreamService

↓

CurrentPriceProvider

↓

Receive Tick

↓

Stream Validator

↓

Validated Tick

↓

Candle Builder

↓

Market Memory
```

---

# Candle Generation Sequence

```text
CurrentPriceProvider

↓

PriceStreamService

↓

Candle Builder

↓

Update Current Candle

↓

Close Candle

↓

Generate New Candle

↓

Market Memory
```

---

# Validation Sequence

```text
Live Tick

↓

Stream Validator

↓

Structure Check

↓

Timestamp Check

↓

Price Validation

↓

Validation Passed

↓

PriceStreamService
```

---

# Market Closed Sequence

```text
Market Calendar

↓

Market Closed

↓

PriceStreamService

↓

Stop Live Stream

↓

Disconnect Provider

↓

Idle
```

---

# Provider Reconnect Sequence

```text
Connection Lost

↓

PriceStreamService

↓

Reconnect Provider

↓

Authentication

↓

Connection Restored

↓

Resume Streaming
```

---

# Error Sequence

```text
Live Provider

↓

Connection Error

↓

Retry

↓

Retry Failed

↓

Provider Offline

↓

Notify PriceStreamService
```

---

# Runtime Rules

1. PriceStreamService Live Data modulining yagona Orchestrator'i hisoblanadi.

2. Live Stream Market Calendar ruxsati bilan boshlanadi.

3. Har bir Tick CurrentPriceProvider orqali qabul qilinadi.

4. Har bir Tick Stream Validator orqali tekshiriladi.

5. Validation'dan o'tgan Tick Candle Builder'ga uzatiladi.

6. Candle Builder yangi Candle yaratadi yoki mavjud Candle'ni yangilaydi.

7. Market Memory faqat tekshirilgan ma'lumot bilan yangilanadi.

8. GoldBot Core Live Provider bilan bevosita ishlamaydi.

---

# State Flow

```text
Idle

↓

Initializing

↓

Connecting

↓

Streaming

↓

Validating

↓

Building Candle

↓

Updating Memory

↓

Completed

or

Failed
```

---

# Golden Rules

• PriceStreamService Live Data oqimini boshqaradi.

• Live Stream faqat Market Calendar ochiq bo'lsa ishlaydi.

• CurrentPriceProvider yagona narx manbai hisoblanadi.

• Validation majburiy.

• Candle Builder faqat Validation'dan o'tgan Tick bilan ishlaydi.

• Market Memory faqat tasdiqlangan Live Data'ni qabul qiladi.

• GoldBot Core faqat Market Memory orqali ma'lumot oladi.

• Circular Sequence taqiqlanadi.

---

# Summary

PriceStreamService Sequence Diagram Live Data modulidagi barcha Runtime jarayonlarning bajarilish ketma-ketligini belgilaydi.

Canonical Runtime Sequence:

Market Calendar

↓

PriceStreamService

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

GoldBot Core

Ushbu ketma-ketlik PriceStreamService moduli uchun yagona rasmiy Runtime Sequence hisoblanadi.
