# AI Service Module Map
Status: CANONICAL
---
# Purpose
Ushbu hujjat AIService ichki arxitekturasini tavsiflaydi.
---
# Module Position
```text
Signal Layer
↓
AIService (Entry)
↓
AIEngine
↓
AICoordinator
↓
AIEngine
↓
AIService (Exit)
↓
Decision Layer
```
---
# Module Architecture
```text
AIService
        │
        ├── Request Receiver
        ├── Request Validator
        ├── Session Manager
        ├── Request Dispatcher
        ├── Response Formatter
        └── Service Monitor
```
---
# Internal Components
## Request Receiver
Signal Layer'dan AI so'rovlarini qabul qiladi.
---
## Request Validator
So'rov formatini tekshiradi.
---
## Session Manager
AI Session holatini boshqaradi.
---
## Request Dispatcher
Request'ni AIEngine'ga uzatadi.
---
## Response Formatter
AIEngine'dan qaytgan AI javobini standart formatga o'tkazadi va Decision Layer'ga uzatadi.
---
## Service Monitor
Service holati va ishlashini kuzatadi.
---
# Allowed Dependencies
✓ AIEngine
---
# Forbidden Dependencies
✗ AICoordinator (to'g'ridan-to'g'ri)
✗ PersonalAI / FundamentalAI / KnowledgeAI / VoiceAI / VisionAI / ExplanationAI / ConfidenceAI (to'g'ridan-to'g'ri)
✗ Risk Layer
✗ Execution Layer
✗ Database Layer
---
# Summary
AIService GoldBot AI Layer uchun ikki tomonlama Boundary Gateway va Public API moduli hisoblanadi.
