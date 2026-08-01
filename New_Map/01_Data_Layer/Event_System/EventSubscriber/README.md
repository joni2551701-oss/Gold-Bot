# Event Subscriber

Status: CANONICAL

---

# Purpose

EventSubscriber — GoldBot Event System ichidagi Event iste'molchisi (Consumer) komponentidir.

Uning asosiy vazifasi EventBus orqali kelayotgan Event'larni tinglash (Subscribe qilish), kerakli Event'larni filtrlash va ularni tegishli modulga yetkazishdir.

EventSubscriber Event yaratmaydi.

EventSubscriber Event'ni uzatmaydi.

U faqat Event'larni qabul qiladi.

---

# Objective

EventSubscriber quyidagi vazifalarni bajaradi:

• Event Subscription

• Event Listening

• Event Filtering

• Event Reception

• Event Acknowledgement

• Runtime Event Consumption

• Lifecycle Event Reception

• Error Event Reception

---

# Layer Position

```text
Publisher

↓

EventBus

↓

EventDispatcher

↓

EventSubscriber

↓

Target Module
```

---

# Responsibilities

EventSubscriber:

✓ Event tinglash

✓ Event qabul qilish

✓ Event Filter qilish

✓ Event Acknowledgement

✓ Runtime Event qabul qilish

✓ Lifecycle Event qabul qilish

✓ Error Event qabul qilish

---

# Not Responsible

EventSubscriber:

✗ Event Creation

✗ Event Publishing

✗ Event Routing

✗ Event Queue

✗ Business Logic

✗ Strategy

✗ Decision

✗ AI Analysis

---

# Input

EventSubscriber qabul qiladi:

• Routed Event

• Runtime Event

• Lifecycle Event

• Error Event

• Recovery Event

---

# Output

EventSubscriber yaratadi:

• Event Delivery

• Subscription Result

• Event Acknowledgement

• Delivery Status

---

# Managed Objects

EventSubscriber quyidagilar bilan ishlaydi:

• Subscription List

• Event Filters

• Runtime Events

• Delivery State

---

# Workflow

```text
EventBus

↓

EventDispatcher

↓

EventSubscriber

↓

Filter Event

↓

Target Module
```

---

# Golden Rules

1. EventSubscriber Event yaratmaydi.

2. EventSubscriber Event mazmunini o'zgartirmaydi.

3. Subscriber faqat o'zi Subscribe qilgan Event'larni qabul qiladi.

4. Event faqat Dispatcher orqali keladi.

5. Event Delivery tasdiqlanishi mumkin.

6. EventSubscriber Business Logic bajarmaydi.

7. EventSubscriber Runtime davomida ishlaydi.

8. Circular Event Subscription taqiqlanadi.

---

# Related Documents

```text
EventSubscriber/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

EventSubscriber GoldBot Event System ichidagi yagona Canonical Event Consumer komponentidir.

Uning vazifasi:

• Event'larni tinglash;

• Event'larni filtrlash;

• Tegishli modulga yetkazish;

• Runtime Event Consumption'ni ta'minlash.
