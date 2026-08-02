# Historical Data Service

Status: CANONICAL

---

# Purpose

HistoricalDataService — Historical Data modulining markaziy boshqaruv (Orchestrator) komponentidir.

Uning asosiy vazifasi Historical Data ichidagi barcha modullarni boshqarish, ular orasidagi Data Flow'ni muvofiqlashtirish va GoldBot Core uchun tayyor tarixiy ma'lumotlarni shakllantirishdir.

HistoricalDataService tarixiy ma'lumotlarni o'zi saqlamaydi, yuklamaydi yoki tahlil qilmaydi.

U faqat jarayonni boshqaradi.

---

# Objective

HistoricalDataService quyidagi vazifalarni bajaradi:

• Historical Data Orchestration

• Bootstrap Management

• Recovery Management

• Historical Provider Coordination

• Historical Database Coordination

• Data Flow Management

• Validation Coordination

• Market Memory Update Coordination

---

# Layer Position

```text
Configuration Layer

↓

HistoricalDataService

├── Bootstrap
├── Recovery
├── Historical Providers
├── Historical Database
├── Data Validation
└── Market Memory

↓

GoldBot Core
```

---

# Responsibilities

HistoricalDataService:

✓ Bootstrap jarayonini boshqarish

✓ Recovery jarayonini boshqarish

✓ Historical Provider'larni boshqarish

✓ Historical Database bilan ishlash

✓ Validation jarayonini boshqarish

✓ Market Memory yangilanishini boshqarish

✓ Historical Data Flow'ni nazorat qilish

✓ Barcha tarixiy ma'lumotlar oqimini koordinatsiya qilish

---

# Not Responsible

HistoricalDataService:

✗ Historical Data Download

✗ Provider Authentication

✗ Database Storage

✗ Data Validation

✗ Market Memory Storage

✗ Live Data

✗ Current Price

✗ Strategy

✗ Context Analysis

✗ Decision

✗ Risk

✗ Signal Generation

---

# Input

HistoricalDataService quyidagilarni qabul qiladi:

• Bootstrap Request

• Recovery Request

• Historical Data Request

• Provider Response

• Configuration

---

# Output

HistoricalDataService quyidagilarni yaratadi:

• Bootstrap Process

• Recovery Process

• Historical Database Request

• Validation Request

• Market Memory Update Request

• Historical Dataset

---

# Controlled Modules

HistoricalDataService quyidagi modullarni boshqaradi:

• Bootstrap

• Recovery

• Historical Providers

• Historical Database

• Data Validation

• Market Memory

---

# Allowed Dependencies

HistoricalDataService quyidagilar bilan ishlashi mumkin:

• Bootstrap

• Recovery

• Historical Providers

• Historical Database

• Data Validation

• Market Memory

• Event Bus

• Configuration Layer

---

# Workflow

```text
Historical Request

↓

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

GoldBot Core
```

---

# Golden Rules

1. HistoricalDataService Historical Data modulining yagona Orchestrator'i hisoblanadi.

2. Bootstrap va Recovery faqat HistoricalDataService orqali ishga tushiriladi.

3. Historical Provider'lar faqat HistoricalDataService tomonidan chaqiriladi.

4. Historical Database bilan barcha ishlash HistoricalDataService orqali amalga oshiriladi.

5. Validation majburiy bosqich hisoblanadi.

6. Market Memory faqat Validation'dan o'tgan ma'lumot bilan yangilanadi.

7. GoldBot Core HistoricalDataService bilan bevosita ishlamaydi, faqat Market Memory orqali ishlaydi.

8. HistoricalDataService biznes logikasini bajarmaydi, faqat koordinatsiya qiladi.

---

# Related Documents

```text
HistoricalDataService/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

HistoricalDataService — Historical Data modulining markaziy boshqaruv (Orchestrator) komponentidir.

U Bootstrap, Recovery, Historical Providers, Historical Database, Data Validation va Market Memory modullarini yagona Data Pipeline ichida boshqaradi.

HistoricalDataService tarixiy ma'lumotlarni o'zi saqlamaydi yoki yuklamaydi. Uning yagona vazifasi barcha Historical Data jarayonlarini tartibli va izchil boshqarishdir.
