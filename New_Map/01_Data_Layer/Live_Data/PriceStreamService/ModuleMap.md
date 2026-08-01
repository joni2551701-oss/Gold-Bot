# PriceStreamService Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat PriceStreamService modulining ichki arxitekturasini, komponentlarini va boshqa modullar bilan bog'lanishini tavsiflaydi.

PriceStreamService Live Data modulining markaziy Orchestrator'i hisoblanadi.

Bu implementatsiya emas.

Bu PriceStreamService modulining Canonical Architecture Blueprint hisoblanadi.

---

# Module Position

```text
                    Live Data

                        │
                        ▼
               PriceStreamService
                        │
      ┌─────────────────┼──────────────────┐
      ▼                 ▼                  ▼
 Live Providers   Market Calendar   Stream Validator
      │                                   │
      ▼                                   ▼
CurrentPriceProvider               CandleBuilder
      │                                   │
      └─────────────────┬─────────────────┘
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

# Module Architecture

```text
                  PriceStreamService
                          │
      ┌───────────────────┼────────────────────┐
      ▼                   ▼                    ▼
 Request Manager    Stream Controller    State Manager
      │                   │                    │
      └──────────────┬────┴────────────────────┘
                     ▼
             Provider Coordinator
                     │
                     ▼
        Current Price Coordinator
                     │
                     ▼
         Stream Validation Manager
                     │
                     ▼
           Candle Build Manager
                     │
                     ▼
          Market Memory Coordinator
```

---

# Internal Components

## Request Manager

Live Stream bilan bog'liq barcha so'rovlarni qabul qiladi.

Masalan:

- Stream Start
- Stream Stop
- Reconnect
- Provider Switch

---

## Stream Controller

Butun Live Stream Pipeline'ni boshqaradi.

Mas'ul:

- Stream Start

- Stream Stop

- Stream Resume

- Stream Health

---

## State Manager

PriceStreamService holatini boshqaradi.

Holatlar:

- Idle

- Connecting

- Streaming

- Validating

- Updating

- Completed

- Failed

---

## Provider Coordinator

Live Provider'larni boshqaradi.

Mas'ul:

- Provider Selection

- Connection

- Authentication

- Provider Switching

---

## Current Price Coordinator

CurrentPriceProvider bilan ishlaydi.

Mas'ul:

- Tick Receive

- Price Update

- Price Synchronization

---

## Stream Validation Manager

Har bir Live Tick tekshirilishini boshqaradi.

---

## Candle Build Manager

Current Tick'lardan Candle yaratishni boshqaradi.

---

## Market Memory Coordinator

Tasdiqlangan Live Data'ni Market Memory'ga uzatadi.

---

# Dependency Map

```text
PriceStreamService

↓

Request Manager

↓

Stream Controller

↓

Live Providers

↓

CurrentPriceProvider

↓

Stream Validator

↓

CandleBuilder

↓

Market Memory

↓

Memory Reader

↓

GoldBot Core
```

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

✓ Configuration Layer

✓ Event Bus

---

# Forbidden Dependencies

PriceStreamService quyidagilar bilan ishlashi mumkin emas.

✗ Historical Data

✗ Historical Database

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

# Input

PriceStreamService qabul qiladi:

• Live Tick

• Provider Response

• Stream Request

• Market Status

• Configuration

---

# Output

PriceStreamService yaratadi:

• Validated Tick

• Current Price

• Candle Update

• Market Memory Update

• Live Stream Status

---

# Ownership

PriceStreamService egalik qiladi:

✓ Live Stream Coordination

✓ Provider Coordination

✓ Tick Routing

✓ Stream Lifecycle

✓ Validation Coordination

✓ Candle Coordination

✓ Memory Coordination

✓ Live Pipeline

PriceStreamService egalik qilmaydi:

✗ Historical Data

✗ Database Storage

✗ Validation Logic

✗ Candle Calculation

✗ Market Memory Storage

✗ Trading Logic

✗ Strategy

✗ Decision

---

# Module Rules

1. PriceStreamService Live Data modulining yagona Orchestrator'i hisoblanadi.

2. Live Provider faqat PriceStreamService orqali boshqariladi.

3. Har bir Tick CurrentPriceProvider orqali o'tadi.

4. Validation majburiy bosqich hisoblanadi.

5. CandleBuilder faqat tasdiqlangan Tick bilan ishlaydi.

6. Market Memory faqat Validation'dan o'tgan ma'lumotni qabul qiladi.

7. GoldBot Core Live Provider bilan bevosita ishlamaydi.

8. PriceStreamService faqat Live Data Pipeline'ni boshqaradi.

9. Circular Dependency qat'iyan taqiqlanadi.

---

# Summary

PriceStreamService Module Map Live Data modulining markaziy boshqaruv komponentini va uning ichki arxitekturasini belgilaydi.

Canonical Module Flow:

PriceStreamService

↓

Request Manager

↓

Stream Controller

↓

Live Providers

↓

CurrentPriceProvider

↓

Stream Validator

↓

CandleBuilder

↓

Market Memory

↓

Memory Reader

↓

GoldBot Core

PriceStreamService Live Data modulidagi barcha real vaqt ma'lumot oqimini boshqaruvchi yagona Canonical Orchestrator hisoblanadi.
