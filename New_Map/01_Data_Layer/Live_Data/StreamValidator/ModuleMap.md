# StreamValidator Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat StreamValidator modulining ichki arxitekturasini, komponentlarini va boshqa modullar bilan bog'lanishini tavsiflaydi.

StreamValidator Live Data modulidagi yagona Canonical Live Stream Validation komponenti hisoblanadi.

Bu implementatsiya emas.

Bu StreamValidator modulining Canonical Architecture Blueprint hisoblanadi.

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
               StreamValidator
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
 Tick Receiver  Validation Engine  State Manager
      │               │                │
      └───────────────┼────────────────┘
                      ▼
              Timestamp Validator
                      │
                      ▼
               Symbol Validator
                      │
                      ▼
                Price Validator
                      │
                      ▼
             Duplicate Detector
                      │
                      ▼
             Integrity Checker
                      │
                      ▼
              Validation Result
                      │
                      ▼
              Validation Publisher
                      │
                      ▼
                CandleBuilder
```

---

# Internal Components

## Tick Receiver

CurrentPriceProvider'dan kelayotgan Tick ma'lumotlarini qabul qiladi.

Mas'ul:

- Tick Receive

- Tick Queue

- Tick Ordering

---

## Validation Engine

Barcha Validation jarayonlarini boshqaradi.

Mas'ul:

- Validation Flow

- Validation Rules

- Validation Result

---

## State Manager

StreamValidator holatini boshqaradi.

Holatlar:

- Idle

- Waiting Tick

- Validating

- Publishing

- Rejected

- Failed

---

## Timestamp Validator

Tick Timestamp to'g'riligini tekshiradi.

Tekshiradi:

- Missing Timestamp

- Invalid Timestamp

- Out-of-Order Timestamp

---

## Symbol Validator

Tick Symbol'ini tekshiradi.

Tekshiradi:

- Invalid Symbol

- Unsupported Symbol

---

## Price Validator

Narx qiymatlarini tekshiradi.

Tekshiradi:

- Invalid Bid

- Invalid Ask

- Negative Price

- Zero Price

- Price Range

---

## Duplicate Detector

Takrorlangan Tick'larni aniqlaydi.

Tekshiradi:

- Duplicate Timestamp

- Duplicate Tick

- Replayed Tick

---

## Integrity Checker

Live Stream yaxlitligini tekshiradi.

Tekshiradi:

- Missing Tick

- Stream Gap

- Sequence Integrity

---

## Validation Publisher

Tasdiqlangan Tick'ni CandleBuilder moduliga uzatadi.

---

# Dependency Map

```text
PriceStreamService

↓

CurrentPriceProvider

↓

StreamValidator

↓

Tick Receiver

↓

Validation Engine

↓

Timestamp Validator

↓

Symbol Validator

↓

Price Validator

↓

Duplicate Detector

↓

Integrity Checker

↓

Validation Publisher

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

StreamValidator quyidagilar bilan ishlashi mumkin.

✓ PriceStreamService

✓ CurrentPriceProvider

✓ CandleBuilder

✓ Event Bus

✓ Configuration Layer

---

# Forbidden Dependencies

StreamValidator quyidagilar bilan ishlashi mumkin emas.

✗ Historical Data

✗ HistoricalDatabase

✗ HistoricalDataService

✗ Live Providers

✗ Market Memory

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

StreamValidator qabul qiladi:

• Live Tick

• Current Price

• Bid Price

• Ask Price

• Timestamp

• Symbol

• Provider Metadata

---

# Output

StreamValidator yaratadi:

• Validated Tick

• Validation Result

• Validation Status

• Validation Error

• Stream Quality Status

• Validation Event

---

# Ownership

StreamValidator egalik qiladi:

✓ Validation Rules

✓ Validation Result

✓ Tick Integrity

✓ Duplicate Detection

✓ Stream Quality

✓ Validation Events

✓ Validation State

StreamValidator egalik qilmaydi:

✗ Current Price

✗ Candle

✗ Market Memory

✗ Trading Logic

✗ Strategy

✗ Decision

---

# Module Rules

1. Har bir Tick StreamValidator orqali o'tishi shart.

2. Validation Pipeline chetlab o'tilmaydi.

3. Duplicate Tick rad etiladi.

4. Invalid Timestamp rad etiladi.

5. Invalid Symbol rad etiladi.

6. Invalid Price rad etiladi.

7. CandleBuilder faqat Validated Tick qabul qiladi.

8. StreamValidator Market Memory bilan bevosita ishlamaydi.

9. Validation natijasi o'zgartirilmaydi.

10. Circular Dependency qat'iyan taqiqlanadi.

---

# Summary

StreamValidator Module Map Live Data modulidagi Validation komponentining ichki arxitekturasini belgilaydi.

Canonical Module Flow:

PriceStreamService

↓

CurrentPriceProvider

↓

StreamValidator

↓

Tick Receiver

↓

Validation Engine

↓

Timestamp Validator

↓

Symbol Validator

↓

Price Validator

↓

Duplicate Detector

↓

Integrity Checker

↓

Validation Publisher

↓

CandleBuilder

↓

Market Memory

↓

Memory Reader

↓

GoldBot Core

StreamValidator Live Data Pipeline ichidagi yagona Canonical Tick Validation moduli hisoblanadi.
