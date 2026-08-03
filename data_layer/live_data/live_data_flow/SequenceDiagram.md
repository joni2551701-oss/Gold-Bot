# LiveDataFlow Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat LiveDataFlow modulining Runtime Sequence (ishlash ketma-ketligi) ni tavsiflaydi.

LiveDataFlow Live Data Pipeline ichidagi barcha modullar orasidagi ma'lumot oqimini belgilaydi.

Bu modul hech qanday biznes logikasini bajarmaydi.

Bu implementatsiya emas.

Bu LiveDataFlow modulining Canonical Runtime Blueprint hisoblanadi.

---

# Complete Runtime Sequence

```text
MarketCalendar

        │
        ▼
PriceStreamService

        │
        ▼
LiveProviders

        │
        ▼
CurrentPriceProvider

        │
        ▼
StreamValidator

        │
        ▼
CandleBuilder

        │
        ▼
Market Memory

        │
        ▼
Memory Reader

        │
        ▼
GoldBot Core
```

---

# Market Open Sequence

```text
MarketCalendar

↓

Market Open

↓

PriceStreamService

↓

Start Live Stream

↓

LiveProviders
```

---

# Provider Connection Sequence

```text
PriceStreamService

↓

LiveProviders

↓

Connect Provider

↓

Authenticate

↓

Subscribe Symbols

↓

Streaming Started
```

---

# Tick Processing Sequence

```text
Exchange API

↓

LiveProviders

↓

CurrentPriceProvider

↓

Update Current Price

↓

StreamValidator

↓

Validate Tick
```

---

# Candle Generation Sequence

```text
Validated Tick

↓

CandleBuilder

↓

Update Current Candle

↓

Close Candle (if needed)

↓

Create New Candle
```

---

# Memory Update Sequence

```text
CandleBuilder

↓

Market Memory

↓

Update Memory

↓

Publish Memory Event
```

---

# Core Access Sequence

```text
GoldBot Core

↓

Memory Reader

↓

Market Memory

↓

Receive Latest Candle

↓

Continue Analysis
```

---

# Market Close Sequence

```text
MarketCalendar

↓

Market Closed

↓

PriceStreamService

↓

Stop Stream

↓

Disconnect Provider

↓

Idle
```

---

# Recovery Sequence

```text
Connection Lost

↓

Reconnect Provider

↓

Restore Subscription

↓

Resume Streaming

↓

Continue Pipeline
```

---

# Error Sequence

```text
Pipeline Error

↓

Generate Error Event

↓

Notify PriceStreamService

↓

Retry

↓

Recovery

or

Pipeline Failed
```

---

# Runtime Rules

1. Pipeline har doim MarketCalendar bilan boshlanadi.

2. PriceStreamService Pipeline'ni boshqaradi.

3. LiveProviders faqat Live Tick qabul qiladi.

4. CurrentPriceProvider Current Price yaratadi.

5. StreamValidator barcha Tick'larni tekshiradi.

6. CandleBuilder faqat Validated Tick bilan ishlaydi.

7. Market Memory faqat tayyor Candle qabul qiladi.

8. GoldBot Core faqat Memory Reader orqali ma'lumot oladi.

9. Pipeline bosqichlari o'zgartirilmaydi.

10. Circular Flow qat'iyan taqiqlanadi.

---

# State Flow

```text
Idle

↓

Market Open

↓

Connecting

↓

Streaming

↓

Updating Price

↓

Validating

↓

Building Candle

↓

Updating Memory

↓

Ready

↓

Market Closed

↓

Idle
```

---

# Golden Rules

• Live Data faqat bitta Canonical Pipeline orqali harakatlanadi.

• Har bir Tick barcha bosqichlardan o'tishi shart.

• Validation bosqichi hech qachon chetlab o'tilmaydi.

• Candle faqat Validated Tick asosida yaratiladi.

• Market Memory faqat tayyor Candle qabul qiladi.

• GoldBot Core Provider yoki Stream bilan bevosita ishlamaydi.

• Pipeline uzilganda Recovery ishga tushadi.

• Circular Sequence taqiqlanadi.

---

# Summary

LiveDataFlow Sequence Diagram Live Data Pipeline ichidagi barcha Runtime jarayonlarining bajarilish ketma-ketligini belgilaydi.

Canonical Runtime Sequence:

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

Ushbu ketma-ketlik LiveDataFlow moduli uchun yagona rasmiy Runtime Sequence hisoblanadi.
