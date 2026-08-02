# EventPublisher Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat EventPublisher modulining ichki arxitekturasini tavsiflaydi.

---

# Module Position

```text
Module

↓

EventPublisher

↓

EventBus
```

---

# Module Architecture

```text
EventPublisher
        │
        ├── Event Builder
        ├── Metadata Builder
        ├── Priority Manager
        ├── Timestamp Manager
        ├── ID Generator
        ├── Publish Manager
        ├── State Manager
        └── Event Reporter
```

---

# Internal Components

## Event Builder

Event obyektini yaratadi.

---

## Metadata Builder

Metadata biriktiradi.

---

## Priority Manager

Event Priority belgilaydi.

---

## Timestamp Manager

Timestamp yaratadi.

---

## ID Generator

Unique Event ID yaratadi.

---

## Publish Manager

EventBus'ga yuboradi.

---

## State Manager

Publisher holatini boshqaradi.

---

## Event Reporter

Publish natijalarini qayd qiladi.

---

# Dependency Map

```text
Module

↓

EventPublisher

↓

EventBus
```

---

# Allowed Dependencies

✓ EventBus

✓ Configuration Layer

✓ EventLifecycle

---

# Forbidden Dependencies

✗ EventSubscriber

✗ EventDispatcher

✗ Context Layer

✗ Strategy Layer

✗ Decision Layer

✗ Risk Layer

✗ AI Layer

✗ Platform Layer

✗ Business Layer

---

# Ownership

EventPublisher egalik qiladi.

✓ Event Creation

✓ Event Metadata

✓ Event Priority

✓ Event ID

✓ Publish State

---

# Module Rules

1. EventPublisher yagona Canonical Producer.

2. Event faqat EventBus'ga yuboriladi.

3. Publish'dan keyin Event o'zgarmaydi.

4. Circular Dependency taqiqlanadi.

---

# Summary

EventPublisher GoldBot Event System ichidagi yagona Canonical Event Producer moduli hisoblanadi.
