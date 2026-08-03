# HealthMonitor Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat HealthMonitor modulining ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
GoldBot Runtime
↓
HealthMonitor
↓
CoreEngine
```
---
# Module Architecture
```text
HealthMonitor
        │
        ├── Health Checker
        ├── Heartbeat Manager
        ├── Metrics Collector
        ├── Status Evaluator
        ├── Alert Manager
        ├── State Manager
        ├── Report Generator
        └── Event Generator
```
---
# Internal Components
## Health Checker
Health Check bajaradi.
---
## Heartbeat Manager
Heartbeat'larni kuzatadi.
---
## Metrics Collector
Runtime Metrics yig'adi.
---
## Status Evaluator
Health holatini baholaydi.
---
## Alert Manager
Alert yaratadi.
---
## State Manager
Monitoring holatini boshqaradi.
---
## Report Generator
Health Report yaratadi.
---
## Event Generator
Health Event yaratadi.
---
# Dependency Map
```text
GoldBot Runtime
↓
HealthMonitor
↓
CoreEngine
```
---
# Allowed Dependencies
✓ CoreEngine
✓ ServiceRegistry
✓ Event System
✓ Configuration
---
# Forbidden Dependencies
✗ Data Layer
✗ Context Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Ownership
HealthMonitor egalik qiladi.
✓ Health State
✓ Runtime Metrics
✓ Alert State
✓ Health Reports
✓ Monitoring Metadata
---
# Module Rules
1. HealthMonitor yagona Monitoring Engine.
2. Health holati markazlashgan baholanadi.
3. Alert avtomatik yaratiladi.
4. Circular Dependency taqiqlanadi.
---
# Summary
HealthMonitor GoldBot Runtime Health Monitoring boshqaruvini amalga oshiruvchi Canonical Monitoring moduli hisoblanadi.
