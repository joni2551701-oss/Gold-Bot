# AI Service
Status: CANONICAL
---
# Purpose
AIService GoldBot AI Layer ichidagi Canonical Public AI Interface moduli hisoblanadi.
Uning asosiy vazifasi AI Layer uchun yagona kirish nuqtasi (Entry Point) bo'lish va boshqa Layer'larga AI xizmatlarini standart interfeys orqali taqdim etishdir.
AIService AI Analysis bajarmaydi.
AIService Decision qabul qilmaydi.
AIService Signal yaratmaydi.
AIService faqat AI Layer Service Gateway hisoblanadi.
---
# Objective
AIService quyidagi vazifalarni bajaradi.
• AI Request Management
• AI API Gateway
• AI Session Management
• Request Validation
• Response Standardization
• AI Layer Integration
---
# Layer Position
```text
Other Layers
↓
AIService
↓
AIEngine
↓
AICoordinator
```
---
# Responsibilities
AIService
✓ AI Request qabul qiladi
✓ Request formatini tekshiradi
✓ AIEngine'ga uzatadi
✓ AI javobini standartlashtiradi
✓ Session boshqaradi
✓ Public API vazifasini bajaradi
---
# Not Responsible
AIService
✗ AI Analysis
✗ Knowledge Management
✗ Learning
✗ Decision Making
✗ Signal Generation
✗ Trade Execution
---
# Input
AIService qabul qiladi.
• AI Request
• User Request
• Session Information
• Context Metadata
---
# Output
AIService yaratadi.
• AI Response
• Standard Response
• Service Metadata
---
# Workflow
```text
Receive Request
↓
Validate Request
↓
Forward To AIEngine
↓
Receive AI Package
↓
Standardize Response
↓
Return Response
```
---
# Golden Rules
1. AIService yagona AI Entry Point hisoblanadi.
2. AI Logic AIService ichida bajarilmaydi.
3. AI javoblari standart formatga o'tkaziladi.
4. AI Layer tashqarisiga faqat AIService chiqadi.
5. Circular Dependency qat'iyan taqiqlanadi.
---
# Related Documents
```text
AIService/
├── README.md
├── SequenceDiagram.md
├── ModuleMap.md
└── Contracts.md
```
---
# Summary
AIService GoldBot AI Layer uchun yagona Service Gateway va Public Interface hisoblanadi.
