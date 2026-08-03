# GoldBot Core Layer Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat GoldBot Core Layer ichidagi barcha modullar va ularning o'zaro bog'lanishini tavsiflaydi.
---
# Layer Architecture
```text
GoldBot Core Layer
            │
            ▼
       CoreEngine
            │
            ▼
       CoreService
            │
 ┌──────────┼───────────┐
 ▼          ▼           ▼
Pipeline   Scheduler   ServiceRegistry
     │          │
     ▼          ▼
Configuration  HealthMonitor
     │
     ▼
Startup
     │
     ▼
Shutdown
```
---
# Layer Modules
## CoreEngine
Runtime Engine.
---
## CoreService
Core Service Orchestrator.
---
## Pipeline
Runtime Pipeline.
---
## Scheduler
Runtime Scheduler.
---
## ServiceRegistry
Service Registry.
---
## Secrets
Secret Management (barcha maxfiy ma'lumotlar uchun yagona kirish nuqtasi).
---
## Configuration
Configuration Manager.
---
## HealthMonitor
Runtime Monitoring.
---
## Features
Feature Standardization (AI / Strategy / Backtesting / ML Export uchun umumiy Feature kutubxonasi).
---
## Startup
Runtime Initialization.
---
## Shutdown
Runtime Finalization.
---
# Dependency Map
```text
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
Runtime Layers
↓
HealthMonitor
↓
Shutdown
```
---
# Ownership
Core Layer egalik qiladi.
✓ Runtime Lifecycle
✓ Runtime Pipeline
✓ Runtime Scheduler
✓ Runtime Configuration
✓ Runtime Registry
✓ Runtime Monitoring
✓ Startup
✓ Shutdown
---
# Rules
1. CoreEngine yagona Runtime Engine.
2. CoreService yagona Service Orchestrator.
3. Pipeline Runtime Flow boshqaradi.
4. Scheduler Runtime Timing boshqaradi.
5. ServiceRegistry yagona Registry.
6. Configuration yagona Configuration Source.
7. HealthMonitor yagona Monitoring Engine.
8. Circular Dependency taqiqlanadi.
---
# Summary
GoldBot Core Layer GoldBot Runtime'ning markaziy boshqaruv qatlami bo'lib, barcha Layer va Service'larning ishlashini koordinatsiya qiluvchi Canonical Core Layer hisoblanadi.
