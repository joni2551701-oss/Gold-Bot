# Event Publisher

Status: CANONICAL

---

# Purpose

EventPublisher — GoldBot Event System ichidagi Event yaratuvchi (Producer) komponentidir.

Uning asosiy vazifasi modul yoki Layer ichida yuz bergan Runtime hodisalarini Event ko'rinishida yaratish va EventBus'ga yuborishdir.

EventPublisher Event'ni qayta ishlamaydi.

EventPublisher Event'ni yetkazmaydi.

U faqat Event yaratadi va Publish qiladi.

---

# Objective

EventPublisher quyidagi vazifalarni bajaradi:

• Event Creation

• Event Publishing

• Event Metadata Creation

• Event Priority Assignment

• Event Timestamp Generation

• Runtime Event Generation

• Lifecycle Event Generation

• Error Event Generation

---

# Layer Position

```text
Module

↓

EventPublisher

↓

EventBus

↓

EventDispatcher

↓

EventSubscriber
```

---

# Responsibilities

EventPublisher:

✓ Event yaratish

✓ Event ID yaratish

✓ Event Timestamp yaratish

✓ Event Metadata yaratish

✓ Event Priority belgilash

✓ Event Publish qilish

✓ Runtime Event yaratish

---

# Not Responsible

EventPublisher:

✗ Event Routing

✗ Event Delivery

✗ Event Queue

✗ Event Processing

✗ Business Logic

✗ Strategy

✗ Decision

✗ AI Analysis

---

# Input

EventPublisher qabul qiladi:

• Runtime Event Request

• Module Event

• Error Event

• Lifecycle Event

• System Event

---

# Output

EventPublisher yaratadi:

• Published Event

• Event Envelope

• Event Metadata

• Event ID

• Event Timestamp

---

# Managed Objects

EventPublisher quyidagilar bilan ishlaydi:

• Runtime Events

• Event Metadata

• Event Priority

• Event Headers

---

# Workflow

```text
Module

↓

EventPublisher

↓

Create Event

↓

Attach Metadata

↓

Publish

↓

EventBus
```

---

# Golden Rules

1. EventPublisher Event yaratadi.

2. EventPublisher Event mazmunini Publish'dan keyin o'zgartirmaydi.

3. Har bir Event noyob Event ID olishi kerak.

4. Har bir Event Timestamp olishi kerak.

5. EventBus yagona Publish manzili hisoblanadi.

6. EventPublisher Event Processing bajarmaydi.

7. EventPublisher Business Logic bajarmaydi.

8. Circular Event Publishing taqiqlanadi.

---

# Related Documents

```text
EventPublisher/

├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```

---

# Summary

EventPublisher GoldBot Event System ichidagi yagona Canonical Event Producer hisoblanadi.

Uning vazifasi:

• Event yaratish;

• Metadata biriktirish;

• EventBus'ga Publish qilish;

• Runtime Event oqimini boshlash.
