# LiveDataService Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat LiveDataService modulining Runtime Sequence (ishlash ketma-ketligi) ni tavsiflaydi.

LiveDataService Live Data Layer ichidagi barcha modullarni boshqaruvchi markaziy Orchestrator hisoblanadi.

U Live Data Pipeline'ni ishga tushiradi, modullarni koordinatsiya qiladi va Runtime jarayonlarini nazorat qiladi.

Bu implementatsiya emas.

Bu LiveDataService modulining Canonical Runtime Blueprint hisoblanadi.

---

# Complete Runtime Sequence

```text
GoldBot Start

        │
        ▼
Configuration Loaded

        │
        ▼
LiveDataService

        │
        ▼
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

# Startup Sequence

```text
GoldBot Start

↓

Load Configuration

↓

Initialize LiveDataService

↓

Initialize MarketCalendar

↓

Initialize PriceStreamService

↓

Initialize Providers

↓

Live Data Ready
```

---

# Market Open Sequence

```text
MarketCalendar

↓

Market Open

↓

LiveDataService

↓

Start PriceStreamService

↓

Connect LiveProviders

↓

Start Streaming
```

---

# Tick Processing Sequence

```text
LiveProviders

↓

Receive Tick

↓

CurrentPriceProvider

↓

Update Current Price

↓

StreamValidator

↓

Validate Tick

↓

CandleBuilder

↓

Update Candle

↓

Market Memory
```

---

# Memory Update Sequence

```text
CandleBuilder

↓

Completed Candle

↓

Market Memory

↓

Update Cache

↓

Memory Ready

↓

GoldBot Core
```

---

# Market Close Sequence

```text
MarketCalendar

↓

Market Closed

↓

LiveDataService

↓

Stop PriceStreamService

↓

Disconnect Providers

↓

Pipeline Stopped
```

---

# Recovery Sequence

```text
Connection Lost

↓

LiveDataService

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

# Restart Sequence

```text
System Restart

↓

Initialize Modules

↓

Restore Runtime State

↓

Reconnect Providers

↓

Resume Streaming
```

---

# Shutdown Sequence

```text
Shutdown Request

↓

LiveDataService

↓

Stop Streaming

↓

Disconnect Providers

↓

Release Resources

↓

Shutdown Completed
```

---

# Error Sequence

```text
Runtime Error

↓

LiveDataService

↓

Detect Failed Module

↓

Generate Error Event

↓

Recovery

↓

Recovery Failed

↓

Pipeline Stopped
```

---

# Runtime Rules

1. LiveDataService Live Data Layer'ning yagona Orchestrator'i hisoblanadi.

2. Pipeline har doim MarketCalendar bilan boshlanadi.

3. PriceStreamService faqat LiveDataService tomonidan boshqariladi.

4. LiveProviders faqat PriceStreamService orqali ishlaydi.

5. Validation bosqichi hech qachon o'tkazib yuborilmaydi.

6. CandleBuilder faqat Validated Tick bilan ishlaydi.

7. Market Memory faqat yakuniy Candle qabul qiladi.

8. GoldBot Core faqat Memory Reader orqali ma'lumot oladi.

9. Runtime Recovery avtomatik ishga tushirilishi mumkin.

10. Circular Runtime Sequence qat'iyan taqiqlanadi.

---

# State Flow

```text
Idle

↓

Initializing

↓

Ready

↓

Streaming

↓

Processing

↓

Updating Memory

↓

Recovering

↓

Stopping

↓

Stopped

or

Failed
```

---

# Golden Rules

• LiveDataService barcha Live Data modullarini boshqaradi.

• Pipeline ketma-ketligi o'zgarmaydi.

• Har bir Tick barcha bosqichlardan o'tishi shart.

• Validation majburiy.

• Market Memory faqat tayyor Candle qabul qiladi.

• GoldBot Core Pipeline'ni chetlab o'tmaydi.

• Recovery avtomatik ishlashi mumkin.

• Circular Sequence taqiqlanadi.

---

# Summary

LiveDataService Sequence Diagram Live Data Layer ichidagi barcha Runtime jarayonlarining bajarilish ketma-ketligini belgilaydi.

Canonical Runtime Sequence:

GoldBot Start

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

Market Memory

↓

Memory Reader

↓

GoldBot Core

Ushbu ketma-ketlik LiveDataService moduli uchun yagona rasmiy Runtime Sequence hisoblanadi.
