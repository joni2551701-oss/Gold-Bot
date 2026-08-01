# Historical Data Flow Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat Historical Data Flow modulining ichki arxitekturasini va Data Layer ichidagi barcha modullar o'rtasidagi ma'lumot oqimini tavsiflaydi.

Bu hujjat Historical Data Flow uchun Canonical Architecture Blueprint hisoblanadi.

Bu implementatsiya emas.

---

# Module Position

```text
                 Historical Data

                        │
                        ▼
              HistoricalDataService

                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
   Bootstrap                       Recovery
        │                               │
        └───────────────┬───────────────┘
                        ▼
              Historical Providers
                        │
                        ▼
            Historical Database
                        │
                        ▼
              Data Validation
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
               Historical Data Flow
                        │
    ┌───────────────────┼────────────────────┐
    ▼                   ▼                    ▼
 Flow Controller   Request Router     State Manager
    │                   │                    │
    └──────────────┬────┴────────────────────┘
                   ▼
          HistoricalDataService
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
   Bootstrap              Recovery
        │                     │
        └──────────┬──────────┘
                   ▼
         Historical Providers
                   │
                   ▼
        Historical Database
                   │
                   ▼
          Data Validation
                   │
                   ▼
           Market Memory
                   │
                   ▼
            Memory Reader
```

---

# Internal Components

## Flow Controller

Historical Data oqimini boshqaradi.

Mas'ul:

- Flow Initialization

- Flow Coordination

- Flow Completion

---

## Request Router

Bootstrap yoki Recovery so'rovlarini tegishli modulga yo'naltiradi.

---

## State Manager

Historical Data Flow holatini boshqaradi.

Holatlar:

- Idle

- Bootstrap

- Recovery

- Validation

- Completed

- Failed

---

## HistoricalDataService

Historical Data modulining asosiy orchestratori.

---

## Bootstrap

Boshlang'ich tarixiy ma'lumotlarni yuklaydi.

---

## Recovery

Yetishmayotgan tarixiy ma'lumotlarni tiklaydi.

---

## Historical Providers

Tashqi providerlardan tarixiy ma'lumotlarni oladi.

---

## Historical Database

Tarixiy ma'lumotlarni saqlaydi.

---

## Data Validation

Ma'lumotlarni tekshiradi.

---

## Market Memory

Tasdiqlangan ma'lumotlarni saqlaydi.

---

## Memory Reader

GoldBot Core uchun Read-Only interfeys.

---

# Dependency Map

```text
HistoricalDataService

↓

Flow Controller

↓

Bootstrap / Recovery

↓

Historical Providers

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

Memory Reader

↓

GoldBot Core
```

---

# Allowed Dependencies

Historical Data Flow quyidagilar bilan ishlashi mumkin.

✓ HistoricalDataService

✓ Bootstrap

✓ Recovery

✓ Historical Providers

✓ Historical Database

✓ Data Validation

✓ Market Memory

✓ Memory Reader

---

# Forbidden Dependencies

Historical Data Flow quyidagilar bilan ishlashi mumkin emas.

✗ Live Data

✗ CurrentPriceProvider

✗ CandleBuilder

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

Historical Data Flow qabul qiladi:

• Historical Request

• Bootstrap Request

• Recovery Request

• Provider Response

---

# Output

Historical Data Flow yaratadi:

• Historical Dataset

• Validated Historical Data

• Updated Market Memory

• Historical Flow Status

---

# Ownership

Historical Data Flow egalik qiladi:

✓ Historical Data Pipeline

✓ Flow Coordination

✓ Flow State

✓ Module Routing

Historical Data Flow egalik qilmaydi:

✗ Historical Storage

✗ Validation Logic

✗ Market Memory Logic

✗ Trading Logic

✗ Analysis

✗ Strategy

✗ Decision

---

# Module Rules

1. Historical Data Flow barcha Historical Data oqimini boshqaradi.

2. Bootstrap va Recovery yagona Flow orqali ishlaydi.

3. Historical Providers yagona ma'lumot manbai hisoblanadi.

4. Historical Database yagona Storage hisoblanadi.

5. Validation majburiy bosqich.

6. Market Memory faqat Validation'dan o'tgan ma'lumotni qabul qiladi.

7. GoldBot Core faqat Memory Reader orqali ma'lumot oladi.

8. Circular Dependency qat'iyan taqiqlanadi.

---

# Summary

Historical Data Flow Module Map Historical Data modulining to'liq Data Pipeline arxitekturasini belgilaydi.

Canonical Module Flow:

HistoricalDataService

↓

Bootstrap / Recovery

↓

Historical Providers

↓

Historical Database

↓

Data Validation

↓

Market Memory

↓

Memory Reader

↓

GoldBot Core

Historical Data Flow Data Layer ichidagi barcha tarixiy ma'lumotlar harakatini boshqaruvchi yagona Canonical Pipeline hisoblanadi.
