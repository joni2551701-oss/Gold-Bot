# EventBus Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat EventBus modulining rasmiy Architecture Contract hujjati hisoblanadi.

EventBus GoldBot ichidagi barcha Event almashinuvi uchun yagona Canonical Transport komponentidir.

---

# Module Responsibility

EventBus quyidagilar uchun javobgar.

✓ Event Transport

✓ Event Queue

✓ Event Ordering

✓ Event Delivery

✓ Event Routing

✓ Runtime Event Flow

EventBus bajarmaydi.

✗ Event Creation

✗ Event Processing

✗ Business Logic

✗ Strategy

✗ Decision

✗ AI Analysis

---

# Module Boundary

Publisher

↓

EventBus

↓

Dispatcher

↓

Boundary End

---

# Input Contract

• Published Event

• Runtime Event

• Lifecycle Event

• Recovery Event

---

# Output Contract

• Routed Event

• Delivery Event

• Broadcast Event

---

# Allowed Dependencies

✓ EventPublisher

✓ EventDispatcher

✓ EventLifecycle

✓ Event Queue

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

---

# State Contract

• Initializing

• Ready

• Receiving

• Queueing

• Dispatching

• Failed

---

# Runtime Contract

1. EventBus yagona Canonical Event Transport hisoblanadi.

2. Har bir Event Queue orqali o'tadi.

3. Event Ordering saqlanishi shart.

4. Event mazmuni o'zgartirilmaydi.

5. Delivery Dispatcher orqali amalga oshiriladi.

6. Circular Event Routing qat'iyan taqiqlanadi.

---

# Architecture Rules

EventBus:

✓ Event uzatadi.

✓ Event Queue boshqaradi.

✓ Event Delivery bajaradi.

✓ Event Ordering saqlaydi.

EventBus:

✗ Event yaratmaydi.

✗ Event Processing bajarmaydi.

✗ Trading Logic bajarmaydi.

✗ AI ishlatmaydi.

---

# Acceptance Criteria

✓ Event Queue ishlaydi.

✓ Event Delivery ishlaydi.

✓ Event Ordering saqlanadi.

✓ Runtime Flow uzilmaydi.

✓ Architecture Boundary buzilmaydi.

---

# Summary

EventBus Contract GoldBot Event System ichidagi yagona Canonical Event Transport komponentining rasmiy arxitektura shartnomasi hisoblanadi.
