# LiveDataService Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat LiveDataService modulining ichki arxitekturasini, komponentlarini va boshqa modullar bilan bog'lanishini tavsiflaydi.

LiveDataService Live Data Layer ichidagi yagona Canonical Orchestrator hisoblanadi.

Bu implementatsiya emas.

Bu LiveDataService modulining Canonical Architecture Blueprint hisoblanadi.

---

# Module Position

```text
                  Configuration Layer
                           │
                           ▼
                    LiveDataService
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
 MarketCalendar   PriceStreamService   LiveDataFlow
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
                   LiveDataService
                           │
      ┌────────────────────┼────────────────────┐
      ▼                    ▼                    ▼
 Request Manager   Pipeline Controller   State Manager
      │                    │                    │
      └────────────────────┼────────────────────┘
                           ▼
                Module Coordinator
                           │
                           ▼
                Lifecycle Manager
                           │
                           ▼
                Runtime Controller
                           │
                           ▼
                Recovery Manager
                           │
                           ▼
                 Event Dispatcher
                           │
                           ▼
                 Health Monitor
```

---

# Internal Components

## Request Manager

Live Data bilan bog'liq barcha Runtime so'rovlarni qabul qiladi.

Mas'ul:

- Start Request

- Stop Request

- Restart Request

- Recovery Request

---

## Pipeline Controller

Butun Live Data Pipeline'ni boshqaradi.

Mas'ul:

- Pipeline Start

- Pipeline Stop

- Pipeline Resume

- Pipeline Coordination

---

## State Manager

LiveDataService holatini boshqaradi.

Holatlar:

- Idle

- Initializing

- Ready

- Running

- Recovering

- Stopping

- Failed

---

## Module Coordinator

Live Data modullarini koordinatsiya qiladi.

Boshqaradi:

- MarketCalendar

- PriceStreamService

- LiveProviders

- CurrentPriceProvider

- StreamValidator

- CandleBuilder

- LiveDataFlow

---

## Lifecycle Manager

Modullar hayot siklini boshqaradi.

Mas'ul:

- Initialize

- Start

- Pause

- Resume

- Stop

- Shutdown

---

## Runtime Controller

Runtime ishlash jarayonini nazorat qiladi.

Tekshiradi:

- Runtime Status

- Processing State

- Pipeline Health

---

## Recovery Manager

Nosozliklardan tiklanishni boshqaradi.

Mas'ul:

- Recovery Detection

- Restart Module

- Resume Pipeline

- Restore State

---

## Event Dispatcher

Live Data hodisalarini yaratadi.

Masalan:

- Pipeline Started

- Pipeline Stopped

- Recovery Started

- Recovery Completed

- Runtime Error

---

## Health Monitor

Live Data Layer sog'ligini kuzatadi.

Tekshiradi:

- Module Health

- Runtime Health

- Pipeline Health

- Recovery Status

---

# Dependency Map

```text
Configuration Layer

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

LiveDataFlow

↓

Market Memory

↓

Memory Reader

↓

GoldBot Core
```

---

# Allowed Dependencies

LiveDataService quyidagilar bilan ishlashi mumkin.

✓ Configuration Layer

✓ MarketCalendar

✓ PriceStreamService

✓ LiveProviders

✓ CurrentPriceProvider

✓ StreamValidator

✓ CandleBuilder

✓ LiveDataFlow

✓ Event Bus

---

# Forbidden Dependencies

LiveDataService quyidagilar bilan ishlashi mumkin emas.

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

LiveDataService qabul qiladi:

• Runtime Requests

• Market Status

• Live Tick Events

• Provider Events

• Recovery Events

• Configuration

---

# Output

LiveDataService yaratadi:

• Module Commands

• Pipeline Commands

• Runtime Events

• Recovery Commands

• Pipeline Status

• Health Status

---

# Ownership

LiveDataService egalik qiladi.

✓ Live Data Pipeline

✓ Runtime Lifecycle

✓ Module Coordination

✓ Recovery Coordination

✓ Pipeline State

✓ Runtime State

✓ Health Monitoring

✓ Pipeline Events

LiveDataService egalik qilmaydi.

✗ Live Tick

✗ Current Price

✗ Validation Logic

✗ Candle Generation

✗ Market Memory Storage

✗ Trading Logic

✗ Strategy

✗ Decision

---

# Module Rules

1. LiveDataService Live Data Layer'ning yagona Canonical Orchestrator'i hisoblanadi.

2. Live Data Pipeline faqat LiveDataService tomonidan boshqariladi.

3. Barcha Live Data modullari LiveDataService koordinatsiyasi ostida ishlaydi.

4. Runtime Lifecycle markazlashgan holda boshqariladi.

5. Recovery avtomatik boshqarilishi mumkin.

6. Pipeline Health doim monitoring qilinadi.

7. GoldBot Core LiveDataService bilan bevosita ishlamaydi.

8. LiveDataService biznes logikasini bajarmaydi.

9. Circular Dependency qat'iyan taqiqlanadi.

---

# Summary

LiveDataService Module Map Live Data Layer ichidagi markaziy boshqaruv modulining ichki arxitekturasini belgilaydi.

Canonical Module Flow:

Configuration Layer

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

LiveDataFlow

↓

Market Memory

↓

Memory Reader

↓

GoldBot Core

LiveDataService Live Data Layer ichidagi barcha Runtime jarayonlarini boshqaruvchi yagona Canonical Orchestrator hisoblanadi.
