# CandleBuilder Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat CandleBuilder modulining ichki arxitekturasini, komponentlarini va boshqa modullar bilan bog'lanishini tavsiflaydi.

CandleBuilder Live Data modulidagi yagona Canonical OHLC Candle Generation komponenti hisoblanadi.

Bu implementatsiya emas.

Bu CandleBuilder modulining Canonical Architecture Blueprint hisoblanadi.

---

# Module Position

```text
                 Live Data

                     │
                     ▼
           PriceStreamService

                     │
                     ▼
         CurrentPriceProvider

                     │
                     ▼
          Stream Validator

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
                 CandleBuilder
                        │
      ┌─────────────────┼─────────────────┐
      ▼                 ▼                 ▼
 Tick Processor   Candle Manager   State Manager
      │                 │                 │
      └─────────────────┼─────────────────┘
                        ▼
               OHLC Calculator
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
      Open          High/Low         Close
                        │
                        ▼
               Timeframe Manager
                        │
                        ▼
             Candle Publisher
                        │
                        ▼
               Market Memory
```

---

# Internal Components

## Tick Processor

Validated Tick ma'lumotlarini qabul qiladi.

Mas'ul:

- Tick Receive

- Tick Ordering

- Tick Distribution

---

## Candle Manager

Faol Candle'larni boshqaradi.

Mas'ul:

- Active Candle

- Closed Candle

- New Candle

---

## State Manager

CandleBuilder holatini boshqaradi.

Holatlar:

- Idle

- Waiting Tick

- Updating

- Closing

- Publishing

- Failed

---

## OHLC Calculator

Har bir Tick asosida OHLC qiymatlarini hisoblaydi.

Mas'ul:

- Open

- High

- Low

- Close

---

## Timeframe Manager

Har bir Timeframe uchun Candle yaratishni boshqaradi.

Masalan:

- M1

- M5

- M15

- H1

- H4

- D1

---

## Candle Publisher

Yakuniy Candle'ni Market Memory'ga uzatadi.

---

# Dependency Map

```text
PriceStreamService

↓

CurrentPriceProvider

↓

Stream Validator

↓

CandleBuilder

↓

Tick Processor

↓

OHLC Calculator

↓

Timeframe Manager

↓

Candle Manager

↓

Candle Publisher

↓

Market Memory

↓

Memory Reader

↓

GoldBot Core
```

---

# Allowed Dependencies

CandleBuilder quyidagilar bilan ishlashi mumkin.

✓ PriceStreamService

✓ CurrentPriceProvider

✓ StreamValidator

✓ MarketMemory

✓ Event Bus

✓ Configuration Layer

---

# Forbidden Dependencies

CandleBuilder quyidagilar bilan ishlashi mumkin emas.

✗ Historical Data

✗ HistoricalDatabase

✗ HistoricalDataService

✗ Live Providers

✗ Market Calendar

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

CandleBuilder qabul qiladi:

• Validated Tick

• Current Price

• Timestamp

• Symbol

• Timeframe

---

# Output

CandleBuilder yaratadi:

• Current Candle

• Closed Candle

• New Candle

• OHLC Data

• Candle Event

---

# Ownership

CandleBuilder egalik qiladi:

✓ Active Candle

✓ Closed Candle

✓ OHLC Values

✓ Candle Lifecycle

✓ Timeframe Candles

✓ Candle State

CandleBuilder egalik qilmaydi:

✗ Live Stream

✗ Current Price

✗ Validation Logic

✗ Market Memory

✗ Trading Logic

✗ Strategy

✗ Decision

---

# Module Rules

1. CandleBuilder faqat Validation'dan o'tgan Tick bilan ishlaydi.

2. Har bir Tick faqat bitta faol Candle'ni yangilaydi.

3. Open narxi Candle boshida bir marta belgilanadi.

4. High faqat yuqoriga yangilanadi.

5. Low faqat pastga yangilanadi.

6. Close har bir Tick bilan yangilanadi.

7. Candle yopilgandan keyin qayta o'zgartirilmaydi.

8. Har bir Timeframe mustaqil Candle'ga ega bo'ladi.

9. Market Memory faqat yakuniy Candle'ni qabul qiladi.

10. Circular Dependency qat'iyan taqiqlanadi.

---

# Summary

CandleBuilder Module Map Live Data modulidagi OHLC Candle yaratish komponentining ichki arxitekturasini belgilaydi.

Canonical Module Flow:

PriceStreamService

↓

CurrentPriceProvider

↓

Stream Validator

↓

CandleBuilder

↓

Tick Processor

↓

OHLC Calculator

↓

Timeframe Manager

↓

Candle Manager

↓

Candle Publisher

↓

Market Memory

↓

Memory Reader

↓

GoldBot Core

CandleBuilder Live Data Pipeline ichidagi yagona Canonical Candle Generation moduli hisoblanadi.
