# Live Data Layer Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat Live Data Layer ichidagi barcha Runtime jarayonlarining bajarilish ketma-ketligini tavsiflaydi.

Live Data Layer tashqi Provider'dan kelgan Real-Time Market Data'ni qabul qiladi, uni qayta ishlaydi va Market Memory orqali GoldBot Core'ga uzatadi.

Bu implementatsiya emas.

Bu Live Data Layer'ning Canonical Runtime Sequence Blueprint hisoblanadi.

---

# Layer Runtime Sequence

```text
GoldBot Start

        │
        ▼
Load Configuration

        │
        ▼
Initialize LiveDataService

        │
        ▼
Initialize MarketCalendar

        │
        ▼
Wait Market Open

        │
        ▼
Start PriceStreamService

        │
        ▼
Connect LiveProviders

        │
        ▼
Authenticate Provider

        │
        ▼
Subscribe Symbols

        │
        ▼
Receive Live Tick

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

Configuration Loaded

↓

Initialize LiveDataService

↓

Initialize Layer Modules

↓

Wait Market Open

↓

Ready
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
Exchange API

↓

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

Build Candle

↓

Market Memory
```

---

# Memory Update Sequence

```text
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

Stop Streaming

↓

Disconnect Providers

↓

Layer Idle
```

---

# Recovery Sequence

```text
Connection Lost

↓

Detect Failure

↓

Recovery Manager

↓

Reconnect Provider

↓

Restore Subscription

↓

Resume Streaming
```

---

# Restart Sequence

```text
Restart Request

↓

Restore Runtime State

↓

Reconnect Providers

↓

Resume Pipeline
```

---

# Shutdown Sequence

```text
Shutdown Request

↓

Stop Streaming

↓

Disconnect Providers

↓

Release Resources

↓

Shutdown Complete
```

---

# Error Sequence

```text
Runtime Error

↓

Generate Error Event

↓

Recovery Manager

↓

Retry

↓

Recovered

or

Layer Failed
```

---

# Runtime Rules

1. Live Data Layer har doim LiveDataService orqali boshqariladi.

2. MarketCalendar Pipeline'ni boshlaydi.

3. Streaming faqat Market Open holatida ishlaydi.

4. Provider ulanishidan oldin Authentication bajariladi.

5. Validation CandleBuilder'dan oldin bajarilishi shart.

6. Market Memory faqat yakuniy Candle qabul qiladi.

7. GoldBot Core Provider bilan bevosita ishlamaydi.

8. Recovery avtomatik ishga tushirilishi mumkin.

9. Runtime Sequence qat'iy saqlanadi.

10. Circular Sequence qat'iyan taqiqlanadi.

---

# State Flow

```text
Idle

↓

Initializing

↓

Ready

↓

Market Open

↓

Streaming

↓

Processing Tick

↓

Building Candle

↓

Updating Memory

↓

Waiting Tick

↓

Market Closed

↓

Stopping

↓

Idle

or

Failed
```

---

# Golden Rules

• LiveDataService barcha Runtime jarayonlarini boshqaradi.

• MarketCalendar yagona Market Status manbai hisoblanadi.

• PriceStreamService Stream Lifecycle'ni boshqaradi.

• LiveProviders faqat Tick qabul qiladi.

• CurrentPriceProvider Current Price yaratadi.

• StreamValidator barcha Tick'larni tekshiradi.

• CandleBuilder OHLC Candle yaratadi.

• Market Memory faqat yakuniy Candle saqlaydi.

• GoldBot Core faqat Memory Reader orqali ma'lumot oladi.

• Circular Runtime Sequence taqiqlanadi.

---

# Summary

Live Data Layer Sequence Diagram Live Data Layer ichidagi barcha Runtime jarayonlarining rasmiy bajarilish ketma-ketligini belgilaydi.

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

Ushbu ketma-ketlik Live Data Layer uchun yagona Canonical Runtime Sequence hisoblanadi.
