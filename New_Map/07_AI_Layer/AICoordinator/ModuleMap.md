# AI Coordinator Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat AICoordinator ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
AIEngine
↓
AICoordinator
↓
Decision Layer
```
---
# Module Architecture
```text
AICoordinator
        │
        ├── Workflow Manager
        ├── Module Scheduler
        ├── Context Aggregator
        ├── Result Collector
        ├── AI Package Builder
        └── Pipeline Monitor
```
---
# Internal Components
## Workflow Manager
AI Pipeline'ni boshqaradi.
---
## Module Scheduler
Qaysi AI modullar ishga tushishini tanlaydi.
---
## Context Aggregator
Barcha AI Context'larni birlashtiradi.
---
## Result Collector
AI natijalarini yig'adi.
---
## AI Package Builder
Decision Layer uchun AI Package yaratadi.
---
## Pipeline Monitor
AI Pipeline holatini kuzatadi.
---
# Allowed Dependencies
✓ PersonalAI
✓ FundamentalAI
✓ KnowledgeAI
✓ VisionAI
✓ ExplanationAI
✓ ConfidenceAI
---
# Forbidden Dependencies
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
---
# Summary
AICoordinator GoldBot AI Layer ichidagi barcha AI modullarini boshqaruvchi Canonical AI Orchestration markazi hisoblanadi.
