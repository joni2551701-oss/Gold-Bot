# HistoricalDataService Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat HistoricalDataService modulining ichki arxitekturasini, komponentlarini va boshqa modullar bilan bog'lanishini tavsiflaydi.

HistoricalDataService Historical Data modulining markaziy Orchestrator'i hisoblanadi.

Bu implementatsiya emas.

Bu HistoricalDataService modulining Canonical Architecture Blueprint hisoblanadi.

---

# Module Position

```text
                   Historical Data

                          │
                          ▼
               HistoricalDataService
                          │
      ┌───────────────────┼───────────────────┐
      ▼                   ▼                   ▼
 Bootstrap            Recovery       Historical Providers
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
                 HistoricalDataService
                           │
      ┌────────────────────┼────────────────────┐
      ▼                    ▼                    ▼
 Request Manager     Flow Controller     State Manager
      │                    │                    │
      └───────────────┬────┴────────────────────┘
                      ▼
              Bootstrap Manager
                      │
                      ▼
              Recovery Manager
                      │
                      ▼
             Provider Coordinator
                      │
                      ▼
             Database Coordinator
                      │
                      ▼
            Validation Coordinator
                      │
                      ▼
              Memory Coordinator
```

---

# Internal Components

## Request Manager

Historical Data bilan bog'liq barcha so'rovlarni qabul qiladi.

Masalan:

- Bootstrap Request

- Recovery Request

- Historical Data Request

---

## Flow Controller

Historical Data Pipeline'ni boshqaradi.

Mas'ul:

- Flow Start

- Flow Routing

- Flow Completion

---

## State Manager

HistoricalDataService holatini boshqaradi.

Holatlar:

- Idle

- Bootstrap

- Recovery

- Processing

- Completed

- Failed

---

## Bootstrap Manager

Bootstrap modulini boshqaradi.

---

## Recovery Manager

Recovery modulini boshqaradi.

---

## Provider Coordinator

Historical Providers bilan ishlaydi.

Mas'ul:

- Provider Selection

- Provider Request

- Provider Response

---

## Database Coordinator

Historical Database bilan barcha operatsiyalarni boshqaradi.

Mas'ul:

- Read

- Write

- Query

---

## Validation Coordinator

Historical Data Validation jarayonini boshqaradi.

---

## Memory Coordinator

Validation'dan o'tgan ma'lumotni Market Memory'ga uzatadi.

---

# Dependency Map

```text
HistoricalDataService

↓

Request Manager

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

HistoricalDataService quyidagilar bilan ishlashi mumkin.

✓ Bootstrap

✓ Recovery

✓ Historical Providers

✓ Historical Database

✓ Data Validation

✓ Market Memory

✓ Memory Reader

✓ Configuration Layer

---

# Forbidden Dependencies

HistoricalDataService quyidagilar bilan ishlashi mumkin emas.

✗ Live Data

✗ CurrentPriceProvider

✗ CandleBuilder

✗ StreamValidator

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

HistoricalDataService qabul qiladi:

• Bootstrap Request

• Recovery Request

• Historical Data Request

• Provider Response

• Configuration

---

# Output

HistoricalDataService yaratadi:

• Bootstrap Process

• Recovery Process

• Historical Database Request

• Validation Request

• Memory Update Request

• Historical Dataset

• Processing Status

---

# Ownership

HistoricalDataService egalik qiladi:

✓ Historical Pipeline Coordination

✓ Bootstrap Coordination

✓ Recovery Coordination

✓ Provider Coordination

✓ Database Coordination

✓ Validation Coordination

✓ Memory Coordination

✓ Flow Management

HistoricalDataService egalik qilmaydi:

✗ Historical Download

✗ Historical Storage

✗ Validation Logic

✗ Market Memory Storage

✗ Trading Logic

✗ Analysis

✗ Strategy

✗ Decision

---

# Module Rules

1. HistoricalDataService Historical Data modulining yagona Orchestrator'i hisoblanadi.

2. Bootstrap va Recovery faqat HistoricalDataService orqali boshqariladi.

3. Historical Providers faqat HistoricalDataService orqali chaqiriladi.

4. Historical Database bilan barcha operatsiyalar HistoricalDataService orqali amalga oshiriladi.

5. Validation majburiy bosqich hisoblanadi.

6. Market Memory faqat Validation muvaffaqiyatli tugagandan keyin yangilanadi.

7. GoldBot Core HistoricalDataService bilan bevosita ishlamaydi.

8. HistoricalDataService faqat jarayonni boshqaradi, biznes logikasini bajarmaydi.

9. Circular Dependency qat'iyan taqiqlanadi.

---

# Summary

HistoricalDataService Module Map Historical Data modulining markaziy boshqaruv komponentini va uning ichki arxitekturasini belgilaydi.

Canonical Module Flow:

HistoricalDataService

↓

Request Manager

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

HistoricalDataService Historical Data modulidagi barcha jarayonlarni boshqaruvchi yagona Canonical Orchestrator hisoblanadi.
