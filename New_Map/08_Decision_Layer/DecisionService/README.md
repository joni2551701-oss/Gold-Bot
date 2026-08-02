# Decision Service
Status: CANONICAL
---
# Purpose
DecisionService GoldBot Decision Layer ichidagi Canonical Public Decision Interface moduli hisoblanadi.
Uning asosiy vazifasi Decision Layer uchun yagona Service Gateway bo'lish va boshqa Layer'larga standart Decision API taqdim etishdir.
DecisionService Decision yaratmaydi.
DecisionService Rule tekshirmaydi.
DecisionService faqat Decision Layer Service Gateway hisoblanadi.
---
# Objective
DecisionService quyidagi vazifalarni bajaradi.
• Decision Request Management
• Decision API Gateway
• Request Validation
• Response Standardization
• Decision Session Management
• Decision Layer Integration
---
# Layer Position
```text
External Layers
↓
DecisionService
↓
DecisionEngine
↓
DecisionLogger
↓
Risk Layer
```
---
# Responsibilities
DecisionService
✓ Decision Request qabul qiladi
✓ Request formatini tekshiradi
✓ DecisionEngine'ga uzatadi
✓ Decision Response standartlashtiradi
✓ Session boshqaradi
✓ Public API vazifasini bajaradi
---
# Not Responsible
DecisionService
✗ Decision Making
✗ Rule Validation
✗ Confidence Calculation
✗ Trade Execution
✗ Database Management
✗ Logging
---
# Input
DecisionService qabul qiladi.
• Decision Request
• Signal Package
• AI Package
• Session Metadata
---
# Output
DecisionService yaratadi.
• Decision Response
• Standard Response
• Decision Metadata
• Service Metadata
---
# Workflow
```text
Receive Request
↓
Validate Request
↓
DecisionEngine
↓
DecisionLogger
↓
Standardize Response
↓
Risk Layer
```
---
# Golden Rules
1. Decision Layer'ga barcha kirishlar DecisionService orqali amalga oshiriladi.
2. DecisionService Decision yaratmaydi.
3. Response yagona formatga o'tkaziladi.
4. Decision Layer tashqarisiga faqat DecisionService chiqadi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
DecisionService/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
DecisionService GoldBot Decision Layer uchun yagona Public Interface va Service Gateway hisoblanadi.
