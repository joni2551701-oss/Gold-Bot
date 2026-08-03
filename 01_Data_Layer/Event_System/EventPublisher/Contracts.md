# EventPublisher Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat EventPublisher modulining rasmiy Architecture Contract hujjati hisoblanadi.

EventPublisher GoldBot ichidagi barcha Runtime Event'larni yaratish va Publish qilish uchun yagona Canonical Producer hisoblanadi.

---

# Module Responsibility

EventPublisher quyidagilar uchun javobgar.

✓ Event Creation

✓ Event Publishing

✓ Event Metadata

✓ Event ID Generation

✓ Timestamp Generation

✓ Event Priority

✓ Runtime Event Generation

EventPublisher bajarmaydi.

✗ Event Routing

✗ Event Queue

✗ Event Delivery

✗ Event Processing

✗ Business Logic

✗ Strategy

✗ Decision

✗ AI Analysis

---

# Module Boundary

Module

↓

EventPublisher

↓

EventBus

↓

Boundary End

---

# Input Contract

• Runtime Event

• Lifecycle Event

• Error Event

• System Event

---

# Output Contract

• Published Event

• Event Envelope

• Event Metadata

---

# Allowed Dependencies

✓ EventBus

✓ EventLifecycle

✓ Configuration Layer

---

# Forbidden Dependencies

✗ EventDispatcher

✗ EventSubscriber

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

• Preparing

• Publishing

• Completed

• Failed

---

# Runtime Contract

1. EventPublisher yagona Canonical Event Producer hisoblanadi.

2. Har bir Event Unique ID olishi shart.

3. Har bir Event Timestamp olishi shart.

4. Event Publish'dan keyin o'zgartirilmaydi.

5. Event faqat EventBus orqali uzatiladi.

6. Circular Event Publishing qat'iyan taqiqlanadi.

---

# Architecture Rules

EventPublisher:

✓ Event yaratadi.

✓ Metadata qo'shadi.

✓ EventBus'ga Publish qiladi.

EventPublisher:

✗ Event Processing bajarmaydi.

✗ Event Routing bajarmaydi.

✗ Event Delivery bajarmaydi.

✗ Trading Logic bajarmaydi.

✗ AI ishlatmaydi.

---

# Acceptance Criteria

✓ Event muvaffaqiyatli yaratiladi.

✓ Metadata to'liq bo'ladi.

✓ Unique Event ID yaratiladi.

✓ Timestamp yaratiladi.

✓ Event EventBus'ga Publish qilinadi.

✓ Architecture Boundary buzilmaydi.

---

# Summary

EventPublisher Contract GoldBot Event System ichidagi Canonical Event Producer komponentining rasmiy arxitektura shartnomasi hisoblanadi.

EventPublisher GoldBot Runtime davomida barcha Event'larni yaratish va EventBus'ga uzatish uchun yagona ruxsat etilgan modul hisoblanadi.
