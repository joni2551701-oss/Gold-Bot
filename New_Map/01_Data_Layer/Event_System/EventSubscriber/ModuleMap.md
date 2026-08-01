# EventSubscriber Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat EventSubscriber modulining ichki arxitekturasi va komponentlarini tavsiflaydi.

---

# Module Position

```text
EventDispatcher

↓

EventSubscriber

↓

Target Module
```

---

# Module Architecture

```text
EventSubscriber
        │
        ├── Subscription Manager
        ├── Listener Manager
        ├── Filter Manager
        ├── Delivery Manager
        ├── Acknowledgement Manager
        ├── State Manager
        └── Event Reporter
```

---

# Internal Components

## Subscription Manager

Subscription ro'yxatini boshqaradi.

---

## Listener Manager

Event'larni tinglaydi.

---

## Filter Manager

Event Filter bajaradi.

---

## Delivery Manager

Event'ni Target Module'ga uzatadi.

---

## Acknowledgement Manager

Delivery tasdig'ini boshqaradi.

---

## State Manager

Subscriber holatini boshqaradi.

---

## Event Reporter

Subscriber Runtime hodisalarini yaratadi.

---

# Dependency Map

```text
EventDispatcher

↓

EventSubscriber

↓

Target Module
```

---

# Allowed Dependencies

✓ EventDispatcher

✓ EventLifecycle

✓ Configuration Layer

---

# Forbidden Dependencies

✗ EventPublisher

✗ EventBus

✗ Strategy Layer

✗ Decision Layer

✗ AI Layer

✗ Trading Logic

---

# Ownership

EventSubscriber egalik qiladi.

✓ Subscription List

✓ Event Filters

✓ Delivery State

✓ Listener State

---

# Module Rules

1. EventSubscriber yagona Canonical Consumer.

2. Event faqat Dispatcher orqali olinadi.

3. Subscriber faqat mos Event'larni qabul qiladi.

4. Event mazmuni o'zgartirilmaydi.

5. Circular Dependency taqiqlanadi.

---

# Summary

EventSubscriber GoldBot Event System ichidagi yagona Canonical Event Consumer moduli hisoblanadi.
