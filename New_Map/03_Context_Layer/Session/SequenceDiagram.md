# Session Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Session modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Session modulining Canonical Runtime Blueprint hisoblanadi.
---
# Runtime Sequence
```text
Current Time
↓
Load Trading Calendar
↓
Detect Session
↓
Detect Session Open
↓
Detect Session Close
↓
Detect Kill Zone
↓
Detect Session Overlap
↓
Analyze Session Activity
↓
Generate Session State
↓
ContextService
```
---
# Update Sequence
```text
Time Update
↓
Update Session
↓
Update Kill Zone
↓
Publish Session State
```
---
# Runtime Rules
1. Trading Calendar yuklanadi.
2. Session birinchi aniqlanadi.
3. Kill Zone Session ichida hisoblanadi.
4. Overlap alohida tekshiriladi.
5. Circular Dependency taqiqlanadi.
---
# State Flow
```text
Idle
↓
Calendar Loaded
↓
Session Detection
↓
Kill Zone Detection
↓
State Ready
↓
Completed
or
Failed
```
---
# Summary
Canonical Runtime Sequence
Current Time
↓
Session
↓
Session State
↓
ContextService
