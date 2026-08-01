# Live Data Layer Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat Live Data Layer ichidagi barcha modullar, ularning vazifalari va o'zaro bog'lanishini tavsiflaydi.

Live Data Layer GoldBot'ning Real-Time Market Data bilan ishlovchi qatlami bo'lib, tashqi Provider'dan kelgan ma'lumotlarni qabul qiladi, qayta ishlaydi va Market Memory'ga uzatadi.

Bu implementatsiya emas.

Bu Live Data Layer'ning Canonical Architecture Blueprint hisoblanadi.

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

# Layer Architecture

```text
                    Live Data Layer
                            │
    ┌───────────────────────┼────────────────────────┐
    ▼                       ▼                        ▼
MarketCalendar      LiveDataService         LiveDataFlow
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

# Layer Modules

## LiveDataService

Layer'ning markaziy Orchestrator'i.

Mas'ul:

- Runtime Lifecycle
- Module Coordination
- Recovery
- Pipeline Management

---

## MarketCalendar

Bozor sessiyalarini boshqaradi.

Mas'ul:

- Market Open
- Market Close
- Trading Hours
- Holidays

---

## PriceStreamService

Live Stream Lifecycle'ni boshqaradi.

Mas'ul:

- Stream Start
- Stream Stop
- Stream Restart
- Provider Coordination

---

## LiveProviders

Tashqi Market Data Provider'lar bilan ishlaydi.

Mas'ul:

- Provider Connection
- Authentication
- Tick Receiving
- Failover

---

## CurrentPriceProvider

Joriy narxni boshqaradi.

Mas'ul:

- Current Price
- Latest Quote
- Bid
- Ask

---

## StreamValidator

Tick ma'lumotlarini tekshiradi.

Mas'ul:

- Tick Validation
- Duplicate Detection
- Integrity Check

---

## CandleBuilder

OHLC Candle yaratadi.

Mas'ul:

- Candle Lifecycle
- OHLC Calculation
- Timeframe Candle

---

## LiveDataFlow

Pipeline oqimini boshqaradi.

Mas'ul:

- Runtime Flow
- Stage Routing
- Pipeline Integrity

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

Market Memory

↓

Memory Reader

↓

GoldBot Core
```

---

# Module Dependencies

| Module | Depends On |
|----------|------------|
| LiveDataService | Configuration Layer |
| MarketCalendar | Configuration Layer |
| PriceStreamService | LiveDataService, MarketCalendar |
| LiveProviders | PriceStreamService |
| CurrentPriceProvider | LiveProviders |
| StreamValidator | CurrentPriceProvider |
| CandleBuilder | StreamValidator |
| LiveDataFlow | LiveDataService, PriceStreamService |
| Market Memory | CandleBuilder |

---

# Input

Live Data Layer qabul qiladi:

- Market Status
- Live Tick
- Provider Events
- Runtime Events
- Configuration

---

# Output

Live Data Layer yaratadi:

- Current Price
- Validated Tick
- OHLC Candle
- Market Memory Update
- Runtime Events

---

# Ownership

Live Data Layer egalik qiladi:

✓ Live Stream

✓ Current Price

✓ Tick Validation

✓ Candle Generation

✓ Runtime Pipeline

✓ Provider Connections

✓ Runtime State

✓ Pipeline Events

Live Data Layer egalik qilmaydi:

✗ Historical Data

✗ Context Analysis

✗ Strategy

✗ Decision

✗ Risk

✗ Signal

✗ AI Analysis

---

# Layer Rules

1. LiveDataService barcha modullarni boshqaradi.

2. MarketCalendar Market Status uchun yagona manba hisoblanadi.

3. PriceStreamService Live Stream'ni boshqaradi.

4. LiveProviders faqat tashqi Provider bilan ishlaydi.

5. CurrentPriceProvider yagona Current Price manbai hisoblanadi.

6. StreamValidator barcha Tick'larni tekshiradi.

7. CandleBuilder faqat Validated Tick bilan ishlaydi.

8. LiveDataFlow Pipeline tartibini nazorat qiladi.

9. Market Memory faqat yakuniy Candle qabul qiladi.

10. Circular Dependency qat'iyan taqiqlanadi.

---

# Summary

Live Data Layer Module Map Live Data Layer ichidagi barcha modullar, ularning vazifalari va o'zaro bog'lanishini belgilaydi.

Canonical Module Hierarchy:

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

Ushbu hujjat Live Data Layer uchun yagona Canonical Module Map hisoblanadi.
