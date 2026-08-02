# AI Engine
Status: CANONICAL
---
# Purpose
AIEngine GoldBot AI Layer ichidagi Entry Orchestrator hisoblanadi.
Uning asosiy vazifasi AIService orqali kelgan AI Request'ni qabul qilish, Runtime Pipeline'ni boshqarish va so'rovni AICoordinator'ga yo'naltirishdir.
AIEngine AI modullarini bevosita chaqirmaydi — bu AICoordinator vazifasi.
AIEngine AI tahlilini o'zi bajarmaydi.
AIEngine signal yaratmaydi.
AIEngine yakuniy trading qarorini qabul qilmaydi.
AIEngine faqat Request Routing va Runtime Pipeline Control bilan shug'ullanadi.
---
# Objective
AIEngine quyidagi vazifalarni bajaradi.
• Entry Orchestration
• Request Routing
• Runtime Pipeline Control
• AI Lifecycle Management
• AI State Management
---
# Layer Position
```text
AIService
↓
AIEngine
↓
AICoordinator
```
---
# Responsibilities
AIEngine
✓ AIService'dan Request qabul qiladi
✓ Runtime Pipeline'ni boshqaradi
✓ AICoordinator'ga yo'naltiradi
✓ AI Lifecycle'ni nazorat qiladi
✓ AI State'ni boshqaradi
---
# Not Responsible
AIEngine
✗ AI Module Execution (AICoordinator vazifasi)
✗ Personal AI
✗ News Analysis
✗ Sentiment Analysis
✗ Knowledge Search
✗ Voice Processing
✗ Vision Processing
✗ Explanation Generation
✗ Confidence Calculation
✗ Decision Making
✗ Risk Management
✗ Trade Execution
---
# Input
AIEngine qabul qiladi.
• AI Request (AIService'dan)
• Context
---
# Output
AIEngine yaratadi.
• AI Execution Plan
• Runtime Status
---
# Workflow
```text
Receive Request (AIService)
↓
Analyze Request
↓
Control Pipeline
↓
Route to AICoordinator
↓
Receive AI Package (AICoordinator)
↓
Return to AIService
```
---
# Golden Rules
1. AIEngine AI modullarining o'rniga ishlamaydi.
2. AIEngine AI modullarini bevosita chaqirmaydi — faqat AICoordinator'ga yo'naltiradi.
3. AIEngine faqat Request Routing va Pipeline Control bajaradi.
4. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
AIEngine/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
AIEngine GoldBot AI Layer ichidagi Entry Orchestration, Request Routing va Runtime Pipeline Control'ni boshqaruvchi Canonical Orchestrator hisoblanadi. AI modullarining bevosita ishga tushirilishi AICoordinator vakolatida qoladi.
