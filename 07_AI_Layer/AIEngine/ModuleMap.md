# AI Engine Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat AIEngine ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
AIService
↓
AIEngine
↓
AICoordinator
```
---
# Module Architecture
```text
AIEngine
        │
        ├── Request Manager
        ├── Pipeline Controller
        ├── Routing Manager
        ├── State Manager
        └── Event Publisher
```
---
# Internal Components
## Request Manager
AIService'dan kelgan AI Request'larni qabul qiladi.
---
## Pipeline Controller
Runtime Pipeline'ni boshqaradi.
---
## Routing Manager
So'rovni AICoordinator'ga yo'naltiradi.
---
## State Manager
AI Lifecycle holatini boshqaradi.
---
## Event Publisher
AI Runtime Event yaratadi.
---
# Allowed Dependencies
✓ AIService
✓ AICoordinator
---
# Forbidden Dependencies
✗ PersonalAI (to'g'ridan-to'g'ri)
✗ FundamentalAI (to'g'ridan-to'g'ri)
✗ KnowledgeAI (to'g'ridan-to'g'ri)
✗ VoiceAI (to'g'ridan-to'g'ri)
✗ VisionAI (to'g'ridan-to'g'ri)
✗ ExplanationAI (to'g'ridan-to'g'ri)
✗ ConfidenceAI (to'g'ridan-to'g'ri)
✗ Decision Layer
✗ Risk Layer
✗ Execution Layer
✗ Platform Layer
---
# Summary
AIEngine GoldBot AI Layer ichidagi Entry Orchestration, Request Routing va Runtime Pipeline Control'ni boshqaruvchi Canonical Orchestrator hisoblanadi. AI modullarini bevosita chaqirmaydi — bu AICoordinator vazifasi.
