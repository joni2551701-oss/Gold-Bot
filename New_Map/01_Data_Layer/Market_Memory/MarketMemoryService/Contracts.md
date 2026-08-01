# MarketMemoryService Contracts

Status: CANONICAL

---

# Purpose

MarketMemoryService modulining rasmiy Architecture Contract hujjati.

---

# Module Responsibility

MarketMemoryService quyidagilar uchun javobgar.

✓ Memory Layer Orchestration

✓ Runtime Coordination

✓ Lifecycle Management

✓ Recovery Management

✓ Health Monitoring

✓ Module Coordination

✓ Runtime Event Management

MarketMemoryService bajarmaydi.

✗ Memory Reading

✗ Memory Writing

✗ Persistent Storage

✗ Tick Validation

✗ Trading Logic

✗ AI Analysis

---

# Module Boundary

Live Data Layer

↓

MarketMemoryService

↓

Memory Modules

↓

Boundary End

---

# Input Contract

• Runtime Requests

• Startup Request

• Shutdown Request

• Recovery Request

• Module Events

---

# Output Contract

• Module Commands

• Runtime Events

• Recovery Commands

• Lifecycle Events

• Health Status

---

# Allowed Dependencies

✓ MemoryWriter

✓ MemoryStorage

✓ MemoryCache

✓ MemoryLifecycle

✓ MemoryReader

✓ Event Bus

✓ Configuration Layer

---

# Forbidden Dependencies

✗ Context Layer

✗ Strategy Layer

✗ Decision Layer

✗ Risk Layer

✗ AI Layer

✗ Platform Layer

✗ Business Layer

✗ Learning Layer

✗ Media Layer

✗ Future Expansion Layer

---

# State Contract

• Initializing

• Ready

• Running

• Recovering

• Restarting

• Stopping

• Failed

---

# Runtime Contract

1. MarketMemoryService Market Memory Layer'ning yagona Canonical Orchestrator'i hisoblanadi.

2. Barcha Memory modullari faqat MarketMemoryService koordinatsiyasi ostida ishlaydi.

3. Runtime Lifecycle markazlashgan boshqariladi.

4. Recovery avtomatik ishlashi mumkin.

5. Health Monitoring doimiy ishlaydi.

6. MarketMemoryService Memory ma'lumotlarini o'qimaydi.

7. MarketMemoryService Memory ma'lumotlarini yozmaydi.

8. Circular Dependency qat'iyan taqiqlanadi.

---

# Architecture Rules

MarketMemoryService:

✓ Runtime boshqaradi.

✓ Recovery boshqaradi.

✓ Lifecycle boshqaradi.

✓ Health Monitoring bajaradi.

✓ Memory modullarini koordinatsiya qiladi.

MarketMemoryService:

✗ Memory yozmaydi.

✗ Memory o'qimaydi.

✗ Storage boshqarmaydi.

✗ Trading Logic bajarmaydi.

✗ AI ishlatmaydi.

---

# Acceptance Criteria

✓ Runtime Lifecycle ishlaydi.

✓ Recovery ishlaydi.

✓ Health Monitoring ishlaydi.

✓ Memory modullari koordinatsiya qilinadi.

✓ Architecture Boundary buzilmaydi.

---

# Summary

MarketMemoryService Contract Market Memory Layer ichidagi markaziy Orchestrator komponentining rasmiy arxitektura shartnomasi hisoblanadi.

MarketMemoryService Memory Layer'ning Runtime Lifecycle, Recovery va Module Coordination jarayonlarini boshqaruvchi yagona Canonical modul hisoblanadi.
