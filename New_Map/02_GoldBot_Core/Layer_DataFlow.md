# GoldBot Core Layer Data Flow
Status: CANONICAL
---
# Purpose
Ushbu hujjat GoldBot Core Layer ichidagi barcha Runtime Data Flow'ni tavsiflaydi.
Core Layer GoldBot Runtime'ning markaziy boshqaruv qatlami hisoblanadi.
Bu implementatsiya emas.
Bu GoldBot Core Layer'ning Canonical Runtime Data Flow hujjati hisoblanadi.
---
# Layer Position
```text
System Runtime
↓
GoldBot Core Layer
↓
All Runtime Layers
```
---
# Complete Runtime Flow
```text
System Boot
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
Target Layer
↓
HealthMonitor
↓
Shutdown
```
---
# Runtime Command Flow
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
CoreEngine
```
---
# Startup Flow
```text
System Boot
↓
Startup
↓
Configuration
↓
ServiceRegistry
↓
CoreEngine
↓
Runtime Ready
```
---
# Shutdown Flow
```text
Shutdown Request
↓
CoreEngine
↓
CoreService
↓
Shutdown
↓
Release Resources
↓
Runtime Stopped
```
---
# Recovery Flow
```text
Runtime Failure
↓
HealthMonitor
↓
CoreEngine
↓
Recovery
↓
Restore Runtime
↓
Resume Pipeline
```
---
# Layer Rules
1. Startup har doim birinchi ishlaydi.
2. Configuration Startup'dan oldin yuklanmaydi.
3. CoreEngine Runtime markazini boshqaradi.
4. CoreService Core modullarni koordinatsiya qiladi.
5. Pipeline barcha Layer Flow'ni boshqaradi.
6. Scheduler Runtime Trigger'larni boshqaradi.
7. HealthMonitor Runtime sog'ligini kuzatadi.
8. Shutdown oxirgi bosqich hisoblanadi.
9. Circular Runtime Flow taqiqlanadi.
---
# Summary
Canonical Runtime Flow:
System Boot
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
Target Layer
↓
HealthMonitor
↓
Shutdown
