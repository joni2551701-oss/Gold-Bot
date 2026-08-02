# AI Engine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat AIEngine ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Signal Layer
↓
AIEngine
↓
AI Modules
↓
AICoordinator
```
---
# Module Architecture
```text
AIEngine
        │
        ├── Request Manager
        ├── Pipeline Manager
        ├── Module Router
        ├── Execution Manager
        ├── State Manager
        ├── Result Collector
        └── Event Publisher
```
---
# Internal Components
## Request Manager
AI Request'larni qabul qiladi.
---
## Pipeline Manager
AI Pipeline'ni boshqaradi.
---
## Module Router
Kerakli AI modullarini tanlaydi.
---
## Execution Manager
AI modullarini ishga tushiradi.
---
## State Manager
AI holatini boshqaradi.
---
## Result Collector
AI natijalarini yig'adi.
---
## Event Publisher
AI Event yaratadi.
---
# Allowed Dependencies
✓ PersonalAI
✓ FundamentalAI
✓ KnowledgeAI
✓ VoiceAI
✓ VisionAI
✓ ExplanationAI
✓ ConfidenceAI
✓ AICoordinator
---
# Forbidden Dependencies
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Summary
AIEngine GoldBot AI Layer ichidagi barcha AI modullarini boshqaruvchi Canonical Orchestrator hisoblanadi.
