# LiveDataFlow Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat LiveDataFlow modulining ichki arxitekturasini, Data Pipeline komponentlarini va modullar orasidagi bog'lanishni tavsiflaydi.

LiveDataFlow Live Data Layer ichidagi yagona Canonical Runtime Data Pipeline hisoblanadi.

Bu implementatsiya emas.

Bu LiveDataFlow modulining Canonical Architecture Blueprint hisoblanadi.

---

# Module Position

```text
                 Live Data Layer

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

# Module Architecture

```text
                  LiveDataFlow
                         │
      ┌──────────────────┼──────────────────┐
      ▼                  ▼                  ▼
 Flow Controller   Pipeline Manager   State Manager
      │                  │                  │
      └──────────────────┼──────────────────┘
                         ▼
                 Stage Coordinator
                         │
                         ▼
                Routing Controller
                         │
                         ▼
                 Flow Validator
                         │
                         ▼
                 Event Dispatcher
                         │
                         ▼
                 Pipeline Monitor
```

---

# Internal Components

## Flow Controller

Pipeline ishga tushishini boshqaradi.

Mas'ul:

- Start Flow

- Stop Flow

- Resume Flow

- Pause Flow

---

## Pipeline Manager

Pipeline bosqichlarini boshqaradi.

Mas'ul:

- Stage Order

- Stage Execution

- Stage Completion

---

## State Manager

LiveDataFlow holatini boshqaradi.

Holatlar:

- Idle

- Starting

- Running

- Waiting

- Recovering

- Stopped

- Failed

---

## Stage Coordinator

Har bir Pipeline bosqichini ketma-ket boshqaradi.

Bosqichlar:

- Market Status

- Stream

- Current Price

- Validation

- Candle

- Memory

---

## Routing Controller

Ma'lumotni keyingi modulga uzatadi.

Mas'ul:

- Route Tick

- Route Candle

- Route Events

---

## Flow Validator

Pipeline tartibi buzilmaganligini nazorat qiladi.

Tekshiradi:

- Missing Stage

- Invalid Order

- Broken Flow

- Circular Flow

---

## Event Dispatcher

Pipeline Event'larini yaratadi.

Masalan:

- Pipeline Started

- Pipeline Stopped

- Pipeline Error

- Recovery Started

---

## Pipeline Monitor

Pipeline sog'ligini kuzatadi.

Tekshiradi:

- Runtime Status

- Processing Latency

- Stage Health

- Flow Integrity

---

# Dependency Map

```text
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
```

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

# Input

LiveDataFlow qabul qiladi:

• Market Status

• Live Tick

• Current Price

• Validated Tick

• Candle

• Pipeline Events

---

# Output

LiveDataFlow yaratadi:

• Runtime Flow

• Pipeline Status

• Stage Events

• Flow Events

• Processing Status

---

# Ownership

LiveDataFlow egalik qiladi:

✓ Pipeline Structure

✓ Stage Order

✓ Runtime Flow

✓ Routing Rules

✓ Pipeline Events

✓ Pipeline State

✓ Flow Integrity

LiveDataFlow egalik qilmaydi:

✗ Live Tick

✗ Current Price

✗ Validation Logic

✗ Candle

✗ Market Memory

✗ Trading Logic

✗ Strategy

✗ Decision

---

# Module Rules

1. LiveDataFlow Live Data Layer uchun yagona Canonical Pipeline hisoblanadi.

2. Pipeline bosqichlari qat'iy ketma-ketlikda bajariladi.

3. Hech bir modul Pipeline bosqichini chetlab o'tolmaydi.

4. Validation har doim CandleBuilder'dan oldin bajariladi.

5. Market Memory faqat tayyor Candle qabul qiladi.

6. GoldBot Core faqat Memory Reader orqali ma'lumot oladi.

7. Pipeline Recovery avtomatik ishlashi mumkin.

8. Pipeline tartibi Runtime davomida o'zgarmaydi.

9. Circular Dependency qat'iyan taqiqlanadi.

---

# Summary

LiveDataFlow Module Map Live Data Layer ichidagi Canonical Runtime Pipeline arxitekturasini belgilaydi.

Canonical Module Flow:

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

LiveDataFlow Live Data Layer ichidagi barcha Runtime Data Flow uchun yagona Canonical Architecture Blueprint hisoblanadi.
