# EventLifecycle Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat EventLifecycle modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu EventLifecycle modulining Canonical Runtime Blueprint hisoblanadi.
---
# Complete Runtime Sequence
```text
Event Created
↓
Register Lifecycle
↓
Published
↓
Queued
↓
Dispatched
↓
Delivered
↓
Completed
or
Failed
```
---
# Retry Sequence
```text
Failed
↓
Retry Requested
↓
Queued Again
↓
Dispatched
↓
Completed
```
---
# Timeout Sequence
```text
Waiting
↓
Timeout
↓
Timeout Event
↓
Retry
or
Failed
```
---
# Cleanup Sequence
```text
Completed
↓
Archive Metadata
↓
Cleanup Resources
↓
Lifecycle Closed
```
---
# Runtime Rules
1. Har bir Event Lifecycle Register qilinadi.
2. State ketma-ket o'zgaradi.
3. Timeout kuzatiladi.
4. Retry chegaralangan bo'ladi.
5. Circular Lifecycle taqiqlanadi.
---
# State Flow
```text
Created
↓
Published
↓
Queued
↓
Dispatched
↓
Delivered
↓
Completed
or
Failed
```
---
# Summary
Canonical Runtime Sequence:
Created
↓
Published
↓
Queued
↓
Dispatched
↓
Delivered
↓
Completed
