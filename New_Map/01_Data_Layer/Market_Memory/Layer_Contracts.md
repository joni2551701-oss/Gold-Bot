# Market Memory Layer Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat Market Memory Layer'ning rasmiy Architecture Contract hujjati hisoblanadi.

Market Memory Layer GoldBot Runtime davomida Market Memory boshqaruvining yagona Canonical Layer hisoblanadi.

---

# Layer Responsibility

Market Memory Layer javobgar:

✓ Runtime Memory

✓ Persistent Storage

✓ Runtime Cache

✓ Read Interface

✓ Write Interface

✓ Lifecycle

✓ Recovery

✓ Health Monitoring

---

# Layer Boundary

Live Data Layer

↓

Market Memory Layer

↓

GoldBot Core

↓

Boundary End

---

# Input Contract

• Validated Candle

• Current Price

• Runtime Snapshot

• Recovery Request

• Startup Request

---

# Output Contract

• Runtime Snapshot

• Current Market

• Current Candle

• Current Price

• Memory Events

---

# Allowed Dependencies

✓ Live Data Layer

✓ Event Bus

✓ Configuration Layer

---

# Forbidden Dependencies

✗ Context Layer

✗ Analysis Layer

✗ Strategy Layer

✗ Decision Layer

✗ Risk Layer

✗ Signal Layer

✗ AI Layer

✗ Platform Layer

✗ Business Layer

✗ Learning Layer

✗ Media Layer

✗ Future Expansion Layer

---

# Runtime Contract

1. MemoryWriter yagona Write Interface.

2. MemoryStorage yagona Persistent Storage.

3. MemoryCache yagona Runtime Cache.

4. MemoryReader yagona Read Interface.

5. MarketMemoryService yagona Orchestrator.

6. MemoryLifecycle Runtime Lifecycle'ni boshqaradi.

7. GoldBot Core faqat MemoryReader orqali ma'lumot oladi.

8. Circular Dependency qat'iyan taqiqlanadi.

---

# Architecture Rules

Market Memory Layer:

✓ Runtime Memory boshqaradi.

✓ Cache boshqaradi.

✓ Storage boshqaradi.

✓ Recovery bajaradi.

✓ Lifecycle boshqaradi.

Market Memory Layer:

✗ Trading Logic bajarmaydi.

✗ Strategy hisoblamaydi.

✗ Signal yaratmaydi.

✗ Decision chiqarmaydi.

✗ AI ishlatmaydi.

---

# Acceptance Criteria

✓ Runtime Memory ishlaydi.

✓ Storage ishlaydi.

✓ Cache ishlaydi.

✓ Reader va Writer ishlaydi.

✓ Recovery ishlaydi.

✓ Lifecycle ishlaydi.

✓ Architecture Boundary buzilmaydi.

---

# Summary

Market Memory Layer Contract Market Memory qatlami uchun rasmiy arxitektura shartnomasi hisoblanadi.

Market Memory Layer GoldBot Runtime davomida Memory Storage, Cache, Reader, Writer, Lifecycle va Runtime Coordination uchun yagona Canonical Layer hisoblanadi.
