# CurrentPriceProvider Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat CurrentPriceProvider modulining ichki arxitekturasini, komponentlarini va boshqa modullar bilan bog'lanishini tavsiflaydi.

CurrentPriceProvider Live Data modulidagi yagona Canonical Current Price manbai hisoblanadi.

Bu implementatsiya emas.

Bu CurrentPriceProvider modulining Canonical Architecture Blueprint hisoblanadi.

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
           Candle Builder

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
             CurrentPriceProvider
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
 Tick Receiver   Price Processor   State Manager
      │               │                │
      └───────────────┼────────────────┘
                      ▼
             Current Price Cache
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
      Bid Price   Ask Price   Mid Price
                      │
                      ▼
              Price Publisher
                      │
                      ▼
             Stream Validator
```

---

# Internal Components

## Tick Receiver

Live Provider'dan kelayotgan Tick ma'lumotlarini qabul qiladi.

Mas'ul:

- Tick Receive

- Timestamp Receive

- Symbol Receive

---

## Price Processor

Kelgan Tick'dan Current Price hosil qiladi.

Mas'ul:

- Bid Extraction

- Ask Extraction

- Spread Calculation

- Mid Price Calculation (Optional)

---

## State Manager

CurrentPriceProvider holatini boshqaradi.

Holatlar:

- Idle

- Waiting Tick

- Receiving

- Updating

- Publishing

- Failed

---

## Current Price Cache

Eng so'nggi Current Price'ni saqlaydi.

Saqlanadigan ma'lumotlar:

- Bid

- Ask

- Mid

- Timestamp

- Symbol

---

## Price Publisher

Current Price'ni keyingi modulga uzatadi.

Qabul qiluvchi:

- Stream Validator

---

# Dependency Map

```text
PriceStreamService

↓

CurrentPriceProvider

↓

Tick Receiver

↓

Price Processor

↓

Current Price Cache

↓

Price Publisher

↓

Stream Validator

↓

Candle Builder

↓

Market Memory

↓

Memory Reader

↓

GoldBot Core
```

---

# Allowed Dependencies

CurrentPriceProvider quyidagilar bilan ishlashi mumkin.

✓ PriceStreamService

✓ Live Providers

✓ Stream Validator

✓ Event Bus

✓ Configuration Layer

---

# Forbidden Dependencies

CurrentPriceProvider quyidagilar bilan ishlashi mumkin emas.

✗ Historical Data

✗ Historical Database

✗ HistoricalDataService

✗ Bootstrap

✗ Recovery

✗ Candle Builder

✗ Market Memory

✗ Memory Reader

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

CurrentPriceProvider qabul qiladi:

• Live Tick

• Bid Price

• Ask Price

• Timestamp

• Symbol

• Provider Status

---

# Output

CurrentPriceProvider yaratadi:

• Current Price

• Latest Tick

• Bid Price

• Ask Price

• Mid Price

• Price Update Event

---

# Ownership

CurrentPriceProvider egalik qiladi:

✓ Current Price

✓ Latest Tick

✓ Bid Price

✓ Ask Price

✓ Mid Price

✓ Latest Timestamp

✓ Current Price Cache

CurrentPriceProvider egalik qilmaydi:

✗ Live Stream

✗ Candle Building

✗ Validation Logic

✗ Market Memory

✗ Trading Logic

✗ Strategy

✗ Decision

---

# Module Rules

1. CurrentPriceProvider Live Data modulining yagona Current Price manbai hisoblanadi.

2. Har bir Tick Current Price'ni yangilaydi.

3. Tick tartibi saqlanishi shart.

4. Current Price Cache faqat eng so'nggi narxni saqlaydi.

5. CurrentPriceProvider Validation bajarmaydi.

6. Price Publisher faqat Stream Validator'ga uzatadi.

7. CurrentPriceProvider Candle yaratmaydi.

8. CurrentPriceProvider Market Memory bilan bevosita ishlamaydi.

9. Circular Dependency qat'iyan taqiqlanadi.

---

# Summary

CurrentPriceProvider Module Map Live Data modulidagi Current Price komponentining ichki arxitekturasini belgilaydi.

Canonical Module Flow:

PriceStreamService

↓

CurrentPriceProvider

↓

Tick Receiver

↓

Price Processor

↓

Current Price Cache

↓

Price Publisher

↓

Stream Validator

↓

Candle Builder

↓

Market Memory

↓

Memory Reader

↓

GoldBot Core

CurrentPriceProvider Live Data Pipeline ichidagi yagona Canonical Current Price manbai hisoblanadi.
