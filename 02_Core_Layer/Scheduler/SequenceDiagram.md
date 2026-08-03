# Scheduler Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat Scheduler modulining Runtime Sequence'ni tavsiflaydi.
Bu implementatsiya emas.
Bu Scheduler modulining Canonical Runtime Blueprint hisoblanadi.
---
# Startup Sequence
```text
System Start
↓
Scheduler
↓
Load Schedules
↓
Register Timers
↓
Ready
```
---
# Runtime Sequence
```text
Schedule Registered
↓
Wait Timer
↓
Trigger
↓
Create Execution Event
↓
Pipeline
↓
Task Complete
```
---
# Retry Sequence
```text
Execution Failed
↓
Retry Schedule
↓
Wait
↓
Trigger Again
↓
Execute
```
---
# Shutdown Sequence
```text
Shutdown
↓
Stop Timers
↓
Clear Queue
↓
Stopped
```
---
# Runtime Rules
1. Har bir Schedule ro'yxatdan o'tadi.
2. Trigger vaqtida ishga tushadi.
3. Retry Schedule qo'llab-quvvatlanadi.
4. Runtime Queue saqlanadi.
5. Circular Scheduling taqiqlanadi.
---
# State Flow
```text
Idle
↓
Initializing
↓
Ready
↓
Waiting
↓
Triggered
↓
Executing
↓
Completed
or
Failed
```
---
# Summary
Canonical Runtime Sequence:
Scheduler
↓
Wait Trigger
↓
Execute
↓
Complete
