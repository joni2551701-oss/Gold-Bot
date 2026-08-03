# EventPublisher Sequence Diagram

Status: CANONICAL

---

# Purpose

Ushbu hujjat EventPublisher modulining Runtime Sequence'ni tavsiflaydi.

Bu implementatsiya emas.

Bu EventPublisher modulining Canonical Runtime Blueprint hisoblanadi.

---

# Complete Runtime Sequence

```text
Module

↓

Trigger Event

↓

EventPublisher

↓

Generate Event ID

↓

Generate Timestamp

↓

Attach Metadata

↓

Publish Event

↓

EventBus
```

---

# Runtime Event Sequence

```text
Runtime Event

↓

EventPublisher

↓

Create Event

↓

Publish

↓

EventBus
```

---

# Error Event Sequence

```text
Module Error

↓

EventPublisher

↓

Create Error Event

↓

Publish

↓

EventBus
```

---

# Lifecycle Event Sequence

```text
Lifecycle Change

↓

EventPublisher

↓

Create Lifecycle Event

↓

Publish

↓

EventBus
```

---

# Runtime Rules

1. Har bir Event noyob ID oladi.

2. Har bir Event Timestamp oladi.

3. Metadata Publish'dan oldin qo'shiladi.

4. Event faqat EventBus'ga yuboriladi.

5. Circular Publishing taqiqlanadi.

---

# State Flow

```text
Idle

↓

Preparing

↓

Publishing

↓

Completed

or

Failed
```

---

# Summary

Canonical Runtime Sequence:

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
