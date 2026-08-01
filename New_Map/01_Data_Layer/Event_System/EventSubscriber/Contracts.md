# EventSubscriber Contracts

Status: CANONICAL

---

# Purpose

Ushbu hujjat EventSubscriber modulining rasmiy Architecture Contract hujjati hisoblanadi.

EventSubscriber GoldBot ichidagi barcha Runtime Event'larni qabul qiluvchi yagona Canonical Consumer hisoblanadi.

---

# Module Responsibility

EventSubscriber quyidagilar uchun javobgar.

✓ Event Subscription

✓ Event Listening

✓ Event Filtering

✓ Event Reception

✓ Event Delivery

✓ Event Acknowledgement

✓ Runtime Event Consumption

EventSubscriber bajarmaydi.

✗ Event Creation

✗ Event Publishing

✗ Event Routing

✗ Event Queue

✗ Business Logic

✗ Strategy

✗ Decision

✗ AI Analysis

---

# Module Boundary

EventDispatcher

↓

EventSubscriber

↓

Target Module

↓

Boundary End

---

# Input Contract

• Routed Event

• Runtime Event

• Lifecycle Event

• Error Event

• Recovery Event

---

# Output Contract

• Delivered Event

• Delivery Status

• Event Acknowledgement

---

# Allowed Dependencies

✓ EventDispatcher

✓ EventLifecycle

✓ Configuration Layer

---

# Forbidden Dependencies

✗ EventPublisher

✗ EventBus

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

• Listening

• Receiving

• Delivering

• Failed

---

# Runtime Contract

1. EventSubscriber yagona Canonical Event Consumer hisoblanadi.

2. Event faqat EventDispatcher orqali olinadi.

3. Subscriber faqat Subscribe qilingan Event'larni qabul qiladi.

4. Event mazmuni o'zgartirilmaydi.

5. Delivery muvaffaqiyatli yakunlanishi kerak.

6. Circular Subscription qat'iyan taqiqlanadi.

---

# Architecture Rules

EventSubscriber:

✓ Event qabul qiladi.

✓ Event filtrlaydi.

✓ Event yetkazadi.

✓ Delivery Status yaratadi.

EventSubscriber:

✗ Event yaratmaydi.

✗ Event Publish qilmaydi.

✗ Event Routing bajarmaydi.

✗ Trading Logic bajarmaydi.

✗ AI ishlatmaydi.

---

# Acceptance Criteria

✓ Subscription ishlaydi.

✓ Event qabul qilinadi.

✓ Filter ishlaydi.

✓ Delivery ishlaydi.

✓ Event mazmuni o'zgarmaydi.

✓ Architecture Boundary buzilmaydi.

---

# Summary

EventSubscriber Contract GoldBot Event System ichidagi Canonical Event Consumer komponentining rasmiy arxitektura shartnomasi hisoblanadi.

EventSubscriber GoldBot Runtime davomida EventDispatcher orqali uzatilgan Event'larni qabul qiluvchi va tegishli modulga yetkazuvchi yagona ruxsat etilgan modul hisoblanadi.
