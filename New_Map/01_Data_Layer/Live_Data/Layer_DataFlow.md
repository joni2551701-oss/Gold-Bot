# Live Data Layer Data Flow

Status: CANONICAL

---

# Purpose

Ushbu hujjat Live Data Layer ichidagi barcha Runtime Data Flow'ni tavsiflaydi.

Live Data Layer tashqi Provider'lardan kelayotgan Real-Time Market Data'ni qabul qiladi, uni tekshiradi, Candle'ga aylantiradi va Market Memory'ga uzatadi.

Bu implementatsiya emas.

Bu Live Data Layer'ning Canonical Runtime Data Flow hujjati hisoblanadi.

---

# Layer Position

```text
Configuration Layer

        │
        ▼
Live Data Layer

        │
        ▼
Market Memory

        │
        ▼
GoldBot Core
```

---

# Complete Data Flow

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

# Pipeline Flow

```text
Market Status

↓

Start Stream

↓

Provider Connection

↓

Receive Tick

↓

Update Current Price

↓

Validate Tick

↓

Build Candle

↓

Store Candle

↓

Read Memory

↓

GoldBot Core
```

---

# Data Objects Flow

```text
Market Status
        │
        ▼
Connection State
        │
        ▼
Live Tick
        │
        ▼
Current Price
        │
        ▼
Validated Tick
        │
        ▼
OHLC Candle
        │
        ▼
Market Memory
        │
        ▼
Market Context
```

---

# Runtime Flow

```text
Initialize Layer

↓

Wait Market Open

↓

Start Stream

↓

Receive Tick

↓

Validate Tick

↓

Generate Candle

↓

Update Memory

↓

Repeat
```

---

# Module Interaction Flow

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
```

---

# Recovery Flow

```text
Connection Lost

↓

Detect Failure

↓

Reconnect Provider

↓

Restore Subscription

↓

Resume Stream

↓

Continue Pipeline
```

---

# Shutdown Flow

```text
Market Close

↓

Stop Stream

↓

Disconnect Provider

↓

Flush Runtime State

↓

Idle
```

---

# Runtime Rules

1. Pipeline har doim MarketCalendar bilan boshlanadi.

2. Live Stream faqat Market Open holatida ishlaydi.

3. Har bir Tick CurrentPriceProvider orqali o'tadi.

4. Har bir Tick StreamValidator tomonidan tekshiriladi.

5. Validation'dan o'tgan Tick CandleBuilder'ga uzatiladi.

6. CandleBuilder faqat OHLC Candle yaratadi.

7. Market Memory faqat tayyor Candle qabul qiladi.

8. GoldBot Core faqat Memory Reader orqali ma'lumot oladi.

9. Pipeline ketma-ketligi Runtime davomida o'zgarmaydi.

10. Circular Data Flow qat'iyan taqiqlanadi.

---

# Layer Boundaries

Live Data Layer qabul qiladi:

• Market Status

• Live Tick

• Provider Events

• Runtime Events

Live Data Layer uzatadi:

• OHLC Candle

• Market Memory Update

• Runtime Events

---

# Summary

Live Data Layer Data Flow hujjati Live Data Layer ichidagi barcha Runtime ma'lumot oqimini belgilaydi.

Canonical Layer Flow:

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

Ushbu Data Flow GoldBot Live Data Layer uchun yagona Canonical Runtime Pipeline hisoblanadi.
