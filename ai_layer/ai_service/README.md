# AI Service
Status: CANONICAL
---
# Purpose
AIService GoldBot AI Layer uchun Canonical Boundary Gateway hisoblanadi.
Uning asosiy vazifasi AI Layer'ning yagona Public Entry Point va Public Exit Point bo'lishidir — Signal Layer'dan kelgan so'rovlarni AIEngine'ga kiritish va AIEngine'dan qaytgan yakuniy AI Package'ni Decision Layer'ga chiqarish.
AIService AI Analysis bajarmaydi.
AIService AI Execution bilan shug'ullanmaydi.
AIService Confidence hisoblamaydi.
AIService Knowledge bilan ishlamaydi.
AIService faqat Entry/Exit Boundary, Validation, Serialization va API Boundary vazifalarini bajaradi.
---
# Objective
AIService quyidagi vazifalarni bajaradi.
• Public Entry Point
• Public Exit Point
• Request Validation
• Response Serialization
• Session Management
• API Boundary Enforcement
---
# Layer Position
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
# Responsibilities
AIService
✓ Signal Layer'dan Request qabul qiladi (Entry)
✓ Request formatini tekshiradi
✓ AIEngine'ga uzatadi
✓ AIEngine'dan AI Package qabul qiladi
✓ AI javobini standartlashtiradi
✓ Decision Layer'ga uzatadi (Exit)
✓ Session boshqaradi
---
# Not Responsible
AIService
✗ AI Analysis
✗ AI Execution
✗ Confidence Calculation
✗ Knowledge Management
✗ Learning
✗ Decision Making
✗ Signal Generation
✗ Trade Execution
---
# Input
AIService qabul qiladi.
• AI Request (Signal Layer'dan)
• AI Package (AIEngine'dan)
• Session Information
• Context Metadata
---
# Output
AIService yaratadi.
• Validated AI Request (AIEngine'ga)
• AI Response (Decision Layer'ga)
• Standard Response
• Service Metadata
---
# Workflow
```text
Receive Request (Signal Layer)
↓
Validate Request
↓
Forward To AIEngine
↓
Receive AI Package (AIEngine)
↓
Standardize Response
↓
Return Response (Decision Layer)
```
---
# Golden Rules
1. AIService AI Layer'ning yagona Entry Point va yagona Exit Point hisoblanadi.
2. AI Logic AIService ichida bajarilmaydi.
3. AI javoblari standart formatga o'tkaziladi.
4. AI Layer tashqarisiga faqat AIService orqali kiriladi va chiqiladi.
5. AIService AICoordinator yoki AI modullari bilan to'g'ridan-to'g'ri ishlamaydi — faqat AIEngine orqali.
6. Circular Dependency qat'iyan taqiqlanadi.
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
AIService GoldBot AI Layer uchun ikki tomonlama (bidirectional) Boundary Gateway hisoblanadi — Signal Layer'dan AI Layer'ga kirish va AI Layer'dan Decision Layer'ga chiqish uchun yagona nuqta.
