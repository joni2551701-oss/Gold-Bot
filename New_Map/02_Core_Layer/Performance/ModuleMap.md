# Performance Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat Performance ichki arxitekturasini tavsiflaydi (ichki submodullar implementatsiya bosqichida to'ldiriladi).
---
# Internal Architecture (Planned)
```text
Performance
├── PerformanceTimer
├── PerformanceMetric
├── PerformanceCollector
└── ResourceSampler
```
---
# Module Position
```text
All GoldBot Layers
↓
Performance
↓
HealthMonitor
```
---
# Processing Pipeline (Planned)
```text
PerformanceTimer → PerformanceMetric → PerformanceCollector → ResourceSampler
```
---
# Dependency Map
```text
All GoldBot Layers
↓
Performance
↓
HealthMonitor
```
---
# Allowed Dependencies
✓ CoreEngine
✓ HealthMonitor
✓ Configuration
---
# Forbidden Dependencies
✗ Strategy Layer
✗ Signal Layer
✗ AI Layer
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
✗ Platform Layer
---
# Runtime Flow
```text
Receive Input
↓
Process (Performance)
↓
Emit Output
↓
HealthMonitor
```
---
# Summary
Performance Performance GoldBot Runtime'ining bajarilish vaqti va resurs sarfini o'lchovchi Canonical Performance Monitoring moduli hisoblanadi. U faqat o'lchaydi — baholash HealthMonitor zimmasida.
