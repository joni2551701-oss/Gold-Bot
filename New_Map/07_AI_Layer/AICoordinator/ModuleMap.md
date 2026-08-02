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
AI Modules (PersonalAI / FundamentalAI / KnowledgeAI / VisionAI / VoiceAI / ExplanationAI / ConfidenceAI)
↓
AICoordinator
↓
AIEngine
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
AIEngine uchun AI Package yaratadi.
---
## Pipeline Monitor
AI Pipeline holatini kuzatadi.
---
# Allowed Dependencies
✓ AIEngine
✓ PersonalAI
✓ FundamentalAI
✓ KnowledgeAI
✓ VisionAI
✓ VoiceAI
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
