# GoldBot Core Layer Sequence Diagram
Status: CANONICAL
---
# Purpose
Ushbu hujjat GoldBot Core Layer Runtime Sequence'ni tavsiflaydi.
---
# Complete Runtime Sequence
```text
System Start
↓
Startup
↓
Configuration
↓
ServiceRegistry
↓
CoreEngine
↓
CoreService
↓
Scheduler
↓
Pipeline
↓
Runtime Ready
```
---
# Runtime Sequence
```text
Runtime Request
↓
CoreEngine
↓
CoreService
↓
Pipeline
↓
Target Layer
↓
Response
↓
Runtime Updated
```
---
# Recovery Sequence
```text
Failure
↓
HealthMonitor
↓
CoreEngine
↓
Recovery
↓
Restore Services
↓
Resume Runtime
```
---
# Shutdown Sequence
```text
Shutdown Request
↓
CoreEngine
↓
CoreService
↓
Shutdown
↓
Runtime Stopped
```
---
# Runtime Rules
1. Startup har doim birinchi bajariladi.
2. CoreEngine Runtime'ni boshqaradi.
3. Pipeline ketma-ket ishlaydi.
4. Recovery markazlashgan.
5. Shutdown xavfsiz bajariladi.
6. Circular Runtime Sequence taqiqlanadi.
---
# Summary
Canonical Runtime Sequence:
Startup
↓
CoreEngine
↓
CoreService
↓
Pipeline
↓
Runtime
↓
Shutdown
