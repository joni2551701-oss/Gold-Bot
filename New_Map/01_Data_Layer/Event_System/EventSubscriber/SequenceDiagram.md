# EventSubscriber Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat EventSubscriber modulining Runtime Sequence'ni tavsiflaydi.

Bu implementatsiya emas.

Bu EventSubscriber modulining Canonical Runtime Blueprint hisoblanadi.

---

# Complete Runtime Sequence

```text
Publisher

↓

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

# Subscription Sequence

```text
Subscribe Request

↓

Register Subscription

↓

Waiting Event

↓

Ready
```

---

# Event Receive Sequence

```text
Dispatcher

↓

EventSubscriber

↓

Match Subscription

↓

Accept Event

↓

Deliver Event
```

---

# Event Ignore Sequence

```text
Dispatcher

↓

EventSubscriber

↓

No Match

↓

Ignore Event
```

---

# Recovery Sequence

```text
Restart

↓

Restore Subscriptions

↓

Resume Listening
```

---

# Runtime Rules

1. EventSubscriber faqat Dispatcher orqali Event qabul qiladi.

2. Event Subscription tekshiriladi.

3. Mos kelmagan Event qabul qilinmaydi.

4. Event mazmuni o'zgartirilmaydi.

5. Circular Subscription taqiqlanadi.

---

# State Flow

```text
Idle

↓

Registering

↓

Listening

↓

Receiving

↓

Delivering

↓

Ready

or

Failed
```

---

# Summary

Canonical Runtime Sequence:

Publisher

↓

EventBus

↓

EventDispatcher

↓

EventSubscriber

↓

Target Module
