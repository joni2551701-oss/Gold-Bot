# MarketMemoryService

Status: CANONICAL

---

# Purpose

MarketMemoryService — Market Memory Layer'ning markaziy Orchestrator komponentidir.

Uning asosiy vazifasi Market Memory Layer ichidagi barcha modullarni yagona Runtime Pipeline ichida boshqarish va koordinatsiya qilishdir.

MarketMemoryService Memory ma'lumotlarini yaratmaydi, o'qimaydi yoki yozmaydi.

U faqat Memory komponentlari o'rtasidagi Runtime jarayonlarini boshqaradi.

---

# Objective

MarketMemoryService quyidagi vazifalarni bajaradi:

• Memory Layer Orchestration

• Runtime Lifecycle Coordination

• Storage Coordination

• Cache Coordination

• Reader Coordination

• Writer Coordination

• Recovery Coordination

• Memory Health Monitoring

---

# Layer Position

```text
Live Data Layer

↓

MarketMemoryService

├── MemoryWriter
├── MemoryStorage
├── MemoryCache
├── MemoryLifecycle
└── MemoryReader

↓

GoldBot Core
```

---

# Responsibilities

MarketMemoryService:

✓ Memory Layer Coordination

✓ Runtime Lifecycle

✓ Memory Workflow

✓ Recovery Workflow

✓ Health Monitoring

✓ Memory Synchronization

✓ Module Coordination

---

# Not Responsible

MarketMemoryService:

✗ Memory Storage

✗ Memory Reading

✗ Memory Writing

✗ Cache Storage

✗ Tick Validation

✗ Candle Generation

✗ Strategy

✗ Decision

✗ AI Analysis

---

# Input

MarketMemoryService qabul qiladi:

• Runtime Requests

• Startup Request

• Shutdown Request

• Recovery Request

• Module Events

---

# Output

MarketMemoryService yaratadi:

• Module Commands

• Runtime Events

• Recovery Commands

• Health Status

• Lifecycle Events

---

# Controlled Modules

MarketMemoryService boshqaradi:

• MemoryWriter

• MemoryStorage

• MemoryCache

• MemoryLifecycle

• MemoryReader

---

# Workflow

```text
Live Data Layer

↓

MarketMemoryService

↓

MemoryWriter

↓

MemoryStorage

↓

MemoryCache

↓

MemoryReader

↓

GoldBot Core
```

---

# Golden Rules

1. MarketMemoryService Market Memory Layer'ning yagona Orchestrator'i hisoblanadi.

2. Memory komponentlari faqat MarketMemoryService koordinatsiyasi ostida ishlaydi.

3. Runtime Lifecycle markazlashgan holda boshqariladi.

4. Recovery avtomatik ishga tushirilishi mumkin.

5. Health Monitoring doimiy ishlaydi.

6. MarketMemoryService ma'lumotni o'qimaydi.

7. MarketMemoryService ma'lumotni yozmaydi.

8. Trading Logic bajarmaydi.

---

# Related Documents

```text
MarketMemoryService/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

MarketMemoryService Market Memory Layer ichidagi barcha Runtime jarayonlarini boshqaruvchi yagona Canonical Orchestrator hisoblanadi.    
