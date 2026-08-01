# Event Bus

Status: CANONICAL

---

# Purpose

EventBus — GoldBot Data Layer ichidagi barcha Event almashinuvi uchun markaziy transport (Event Backbone) komponentidir.

Uning asosiy vazifasi modul va layerlar o'rtasida Event'larni xavfsiz, izchil va asinxron tarzda uzatishdir.

EventBus Event yaratmaydi.

EventBus Event iste'mol qilmaydi.

U faqat Event'larni uzatadi.

---

# Objective

EventBus quyidagi vazifalarni bajaradi:

• Event Routing

• Event Transport

• Event Delivery

• Event Queue Management

• Event Ordering

• Event Broadcasting

• Event Isolation

• Runtime Event Flow

---

# Layer Position

```text
Publisher

↓

EventBus

↓

Dispatcher

↓

Subscriber
```

---

# Responsibilities

EventBus:

✓ Event qabul qilish

✓ Event Queue boshqarish

✓ Event uzatish

✓ Event Ordering

✓ Event Routing

✓ Event Delivery

✓ Runtime Event Transport

---

# Not Responsible

EventBus:

✗ Event yaratish

✗ Event Processing

✗ Business Logic

✗ Strategy

✗ Decision

✗ AI Analysis

✗ Tick Validation

✗ Candle Generation

---

# Input

EventBus qabul qiladi:

• Published Event

• System Event

• Runtime Event

• Recovery Event

• Lifecycle Event

---

# Output

EventBus yaratadi:

• Routed Event

• Broadcast Event

• Delivery Event

• Queue Events

---

# Managed Objects

EventBus quyidagilar bilan ishlaydi:

• Runtime Events

• Event Queue

• Event Metadata

• Event Priority

• Delivery State

---

# Workflow

```text
Publisher

↓

EventBus

↓

Queue

↓

Dispatcher

↓

Subscriber
```

---

# Golden Rules

1. EventBus Event yaratmaydi.

2. EventBus Event mazmunini o'zgartirmaydi.

3. EventBus faqat Event transportini bajaradi.

4. Event tartibi saqlanishi kerak.

5. Event Delivery kafolatlanishi kerak.

6. EventBus Business Logic bajarmaydi.

7. EventBus Runtime davomida ishlaydi.

8. Circular Event Routing taqiqlanadi.

---

# Related Documents

```text
EventBus/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

EventBus GoldBot Event System ichidagi yagona Canonical Event Backbone hisoblanadi.

Uning vazifasi:

• Event qabul qilish;

• Event Queue boshqarish;

• Event'larni Dispatcher'ga uzatish;

• Runtime Event Flow'ni boshqarish.

EventBus Event System ichidagi yagona Canonical Transport komponenti hisoblanadi.
