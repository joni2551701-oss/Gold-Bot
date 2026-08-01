# EventBus Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat EventBus modulining Runtime Sequence'ni tavsiflaydi.

Bu implementatsiya emas.

Bu EventBus modulining Canonical Runtime Blueprint hisoblanadi.

---

# Complete Runtime Sequence

```text
Publisher

↓

EventBus

↓

Receive Event

↓

Validate Envelope

↓

Queue Event

↓

Dispatcher

↓

Subscriber
```

---

# Event Publish Sequence

```text
Publisher

↓

Create Event

↓

EventBus

↓

Queue Event

↓

Dispatcher
```

---

# Event Delivery Sequence

```text
Queued Event

↓

EventBus

↓

Dispatcher

↓

Subscriber

↓

Delivery Complete
```

---

# Broadcast Sequence

```text
Publisher

↓

EventBus

↓

Dispatcher

↓

Subscriber A

Subscriber B

Subscriber C
```

---

# Recovery Sequence

```text
Failure

↓

Retry Queue

↓

Restore Queue

↓

Continue Delivery
```

---

# Runtime Rules

1. EventBus barcha Event'larni Queue orqali uzatadi.

2. Event tartibi saqlanadi.

3. Event mazmuni o'zgartirilmaydi.

4. Delivery Dispatcher orqali amalga oshiriladi.

5. Circular Event Flow taqiqlanadi.

---

# State Flow

```text
Idle

↓

Receiving

↓

Queueing

↓

Dispatching

↓

Completed

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

Queue

↓

Dispatcher

↓

Subscriber
