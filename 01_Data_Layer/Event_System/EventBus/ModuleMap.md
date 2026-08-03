# EventBus Module Map

Status: CANONICAL

---

# Purpose

Ushbu hujjat EventBus modulining ichki arxitekturasi va komponentlarini tavsiflaydi.

---

# Module Position

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

# Module Architecture

```text
EventBus
      │
      ├── Receive Manager
      ├── Queue Manager
      ├── Routing Manager
      ├── Ordering Manager
      ├── Delivery Manager
      ├── State Manager
      └── Event Publisher
```

---

# Internal Components

## Receive Manager

Event qabul qiladi.

---

## Queue Manager

Event Queue'ni boshqaradi.

---

## Routing Manager

Event yo'nalishini belgilaydi.

---

## Ordering Manager

Event ketma-ketligini saqlaydi.

---

## Delivery Manager

Dispatcher'ga uzatadi.

---

## State Manager

EventBus holatini boshqaradi.

---

## Event Publisher

Ichki Runtime Event'larini yaratadi.

---

# Dependency Map

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

# Allowed Dependencies

✓ EventPublisher

✓ EventDispatcher

✓ EventLifecycle

✓ Configuration Layer

✓ Event Queue

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

# Ownership

EventBus egalik qiladi.

✓ Event Queue

✓ Delivery State

✓ Routing State

✓ Ordering State

✓ Runtime Event Transport

---

# Module Rules

1. EventBus yagona Transport Layer.

2. Event Queue markazlashgan.

3. Event Ordering saqlanadi.

4. Delivery Dispatcher orqali amalga oshiriladi.

5. Circular Dependency taqiqlanadi.

---

# Summary

EventBus GoldBot Event System ichidagi yagona Canonical Event Transport moduli hisoblanadi.
